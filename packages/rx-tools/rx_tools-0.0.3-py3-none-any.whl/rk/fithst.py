import utils_noroot      as utnr
import matplotlib.pyplot as plt
import zutils.utils      as zut

import ROOT
import zfit
import math 
import tqdm
import numpy 
import logging 
import os 
import utils

from zutils.plot   import plot     as zfplot 
from data_splitter import splitter as dsplit
from fitter        import zfitter

#----------------------------------------
class extractor:
    log=utnr.getLogger('extractor')
    #----------------------------------------
    @property
    def data(self):
        return self._rdf_mc, self._rdf_dt

    @data.setter
    def data(self, value):
        self._rdf_mc, self._rdf_dt = value
    #----------------------------------------
    @property
    def model(self):
        return self._l_pdf

    @model.setter
    def model(self, value):
        self._l_pdf = value 
    #----------------------------------------
    @property
    def res_dir(self):
        return self._res_dir

    @res_dir.setter
    def res_dir(self, value):
        self._res_dir = value
    #----------------------------------------
    @property
    def binning(self):
        return self._d_bin

    @binning.setter
    def binning(self, value):
        self._d_bin = value
    #----------------------------------------
    def __init__(self):
        self._rdf_mc      = None 
        self._rdf_dt      = None 
        self._res_dir     = None
        self._d_bin       = None
        self._l_exp       = None
        self._l_var       = None
        self._l_pdf       = None
        self._d_res       = {}
        self._l_float     = ['mu', 'sg']
        self._mass_var    = 'B_const_mass_M[0]'

        self._initialized = False
    #----------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        if len(self._l_pdf) < 2:
            self.log.error(f'Found fewer than 2 PDFs:')
            print(self._l_pdf)
            raise

        zfitter.log.setLevel(logging.WARNING)
        dsplit.log.setLevel(logging.WARNING)

        ROOT.lhcbStyle()

        self._initialized = True
    #----------------------------------------
    def _bound_filter_rdf(self, rdf):
        if self._maxentries > 0:
            rdf = rdf.Range(self._maxentries)

        axis=0
        for var, arr in self._d_bin.items():
            min_var = min(arr)
            max_var = max(arr)

            cut = f'{min_var} < {var} && {var} < {max_var}'

            rdf = rdf.Filter(cut, f'{axis} bound')
            axis+=1

        return rdf
    #----------------------------------------
    def _get_pdf(self, kind):
        if kind == 'ctrl':
            pdf = self._l_pdf[0]
        elif kind == 'data':
            pdf = zfit.pdf.SumPDF(self._l_pdf)
        else:
            self.log.error(f'Invalid PDF kind: {kind}')
            raise

        return pdf
    #----------------------------------------
    def _is_yield(self, pdf, par_name):
        l_yld_nam = []

        par = pdf.get_yield()
        if   isinstance(par, zfit.Parameter):
            l_yld_nam = [par.name]
        elif isinstance(par, zfit.ComposedParameter):
            l_yld_nam = [par.name for _, par in par.params.items()]
        else:
            self.log.error(f'PDF parameter is invalid:')
            print(par)
            raise

        if len(l_yld_nam) == 0:
            self.log.error(f'No yields found in PDF:')
            print(pdf)
            raise

        is_yield = par_name in l_yld_nam

        self.log.debug(f'{is_yield} = {par_name} in {l_yld_nam}')

        return is_yield
    #----------------------------------------
    def _fix_pars(self, pdf, i_df):
        if i_df not in self._d_res:
            self.log.warning(f'Dataset {i_df:03} does not have simulation parameters to fix data fit')
            return pdf

        res = self._d_res[i_df]

        l_par = list(pdf.get_params(floating=True)) + list(pdf.get_params(floating=False))

        self.log.debug(f'Fixing parameeters')
        for par in l_par:
            if par.name not in res.params or par.name in self._l_float or self._is_yield(pdf, par.name):
                continue

            val = res.params[par.name]['value']
            par.assign(val)
            par.floating = False

            self.log.debug(f'{par.name:<20}{"->" :20}{val:>.3f}')

        return pdf
    #----------------------------------------
    def _get_bin_info(self, df, kind, i_df):
        arr = df['mass'].to_numpy()
        if len(arr) == 0:
            return None

        try:
            l_mean = [ df[var].mean() for var in self._l_var]
        except:
            self.log.error('Cannot extract mean list')
            print(df)
            print(self._l_var)
            raise

        self.log.debug(f'Fitting {i_df:03} dataset: {arr.shape}')

        pdf = self._get_pdf(kind)

        if kind == 'data':
            pdf = self._fix_pars(pdf, i_df)

        ftr = zfitter(pdf, arr)

        try:
            res = ftr.fit()
        except:
            self.log.warning(f'Fit failed, will assign yield as dataset size: {arr.size}')
            return [arr.size, 0] + l_mean + [None]

        with zfit.run.set_graph_mode(False):
            res.hesse(name='hesse_np')

        yld = res.params['nsg']['value']
        try:
            err = res.params['nsg']['hesse_np']['error']
        except:
            self.log.warning(f'Setting error 2 * sqrt(S), cannot recover hesse error:')
            err = 2 * math.sqrt(yld)

        self._plot_fit(pdf, arr, i_df, res, kind)
        self._save_res(pdf, i_df, res, kind)

        pdf.reset_cache_self()

        if kind != 'data': 
            return [arr.size, 0] + l_mean + [res]
        else:
            return [yld,    err] + l_mean + [res]
    #----------------------------------------
    def _save_res(self, pdf, i_df, res, kind):
        pkl_dir  = utnr.make_dir_path(f'{self._res_dir}/pickle/{kind}')
        pkl_path = f'{pkl_dir}/result_{i_df:03}.pkl'

        res.freeze()
        utnr.dump_pickle(res, pkl_path)

        tex_dir  = utnr.make_dir_path(f'{self._res_dir}/latex/{kind}')
        tex_path = f'{tex_dir}/result_{i_df:03}.tex'

        zut.pdf_to_latex(pdf, tex_path)
    #----------------------------------------
    def _plot_his(self, his, kind):
        if self._res_dir is None:
            return

        his_dir = utnr.make_dir_path(f'{self._res_dir}/plots/hist')
        his     = his.Project3D('yx')

        can = ROOT.TCanvas(f'c_{kind}', '', 600, 400)
        his.Draw('colz')
        utils.Reformat2D(can)
        can.SaveAs(f'{his_dir}/his_{kind}.png')
    #----------------------------------------
    def _plot_fit(self, pdf, arr, index, res, kind):
        if self._res_dir is None:
            return

        fit_dir = utnr.make_dir_path(f'{self._res_dir}/plots/fits/{kind}')

        obj=zfplot(model=pdf, data=arr, result=res, suffix=f'{index}')
        plot_path = f'{fit_dir}/fit_{index:03}.png'
        try:
            obj.plot()
            plt.savefig(plot_path)
            plt.close('all')
        except:
            self.log.warning(f'Could not save {plot_path}')
    #----------------------------------------
    def _get_datasets(self, kind):
        rdf  = self._rdf_mc if kind == 'ctrl' else self._rdf_dt
        self.log.info(f'Splitting {rdf.Count().GetValue()} entries')

        obj  = dsplit(rdf, self._d_bin, spectators=['mass'])
        obj.plot_dir = 'tests/fitwgt/simple/splitting/' 
        l_df = obj.get_datasets()

        return l_df
    #----------------------------------------
    def _get_fit_info(self, kind):
        l_df   = self._get_datasets(kind) 
        l_info = [ self._get_bin_info(df, kind, i_df) for i_df, df in enumerate(tqdm.tqdm(l_df, ascii=' -')) ]

        return l_info
    #----------------------------------------
    def _get_hist(self, kind):
        arr_x = numpy.array( list(self._d_bin.values())[0] ).astype(float)
        arr_y = numpy.array( list(self._d_bin.values())[1] ).astype(float)
        arr_z = numpy.array( list(self._d_bin.values())[2] ).astype(float)

        hist = ROOT.TH3F(f'h_{kind}', kind, arr_x.size - 1, arr_x, arr_y.size - 1, arr_y, arr_z.size - 1, arr_z)

        self.log.info(f'Bin contents for {kind}')
        l_info = self._get_fit_info(kind)
        for i_df, info in enumerate(l_info):
            if info is None:
                continue

            [yld, err, xm, ym, zm, res] = info
            if kind == 'ctrl' and res is not None:
                self._d_res[i_df] = res

            i_bin = hist.FindBin(xm, ym, zm)
            hist.SetBinContent(i_bin, yld)
            hist.SetBinError  (i_bin, err)
            self.log.debug(f'{i_bin:<10}{yld:<20.0f}')

        self._plot_his(hist, kind)

        return hist
    #----------------------------------------
    def get_histograms(self, force_redo=False):
        self._initialize()

        h_mc = self._get_hist('ctrl')
        h_dt = self._get_hist('data')

        return h_mc, h_dt
#----------------------------------------

