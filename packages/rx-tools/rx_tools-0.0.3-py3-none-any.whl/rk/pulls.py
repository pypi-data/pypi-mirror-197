import ROOT

import utils
import numpy
import math
import os
import re
import tqdm

from itertools  import combinations
from rk.mcstudy import mcstudy

import utils_noroot      as utnr
import matplotlib.pyplot as plt

import style

#-----------------------------------------------------------------
class pulls:
    log = utnr.getLogger('pulls')
    #--------------------------
    def __init__(self, wks, d_set):
        self._wks         = wks
        self._d_set       = d_set

        self._l_var_name  = []
        self._extended    = True
        self._ncpu        = 4
        self._model_name  = 'model'
        self._obs_pref    = 'mass'
        self._fits_file   = 'fits.root'

        self._obs_name    = None
        self._nbins       = None
        self._bin_thr     = None
        self._spread      = None
        self._ntoy        = None
        self._out_dir     = None

        self._res_path    = None
        self._jsn_path    = None
        self._toy_path    = None
        self._ran_seed    = 0

        self._initialized = False
    #--------------------------
    def _initialize(self):
        if self._initialized:
            return

        ROOT.RooRandom.randomGenerator().SetSeed(self._ran_seed);

        self._check_pull_opts()
        self._check_wks()

        self._obs_name = self._get_obs_name()
        self._nbins    = self._d_set['nbins']
        self._bin_thr  = self._d_set['bin_thr']
        self._spread   = self._d_set['spread']
        self._ntoy     = self._d_set['ntoy']

        self._out_dir  = utnr.make_dir_path(self._d_set['out_dir'])
        self._res_path = f'{self._out_dir}/{self._fits_file}'
        self._jsn_path = self._res_path.replace('.root', '.json')
        self._toy_path = f'{self._out_dir}/data_%02d.dat'

        self._initialized = True
    #--------------------------
    @property
    def random_seed(self):
        return self._ran_seed

    @random_seed.setter
    def random_seed(self, value):
        self._ran_seed = value 
    #--------------------------
    def _check_wks(self):
        utils.check_wks_obj(self._wks, self._model_name, 'pdf')
    #-----------------------------------------------------------------
    def _check_pull_opts(self):
        if 'ntoy'     not in self._d_set:
            self.log.error('Missing "ntoy" from pull options')
            raise

        if 'out_dir'  not in self._d_set:
            self.log.error('Missing "out_dir" from pull options')
            raise

        if 'bin_thr'  not in self._d_set:
            self.log.error('Missing "bin_thr" from pull options')
            raise

        if 'nbins'    not in self._d_set:
            self.log.error('Missing "nbins" from pull options')
            raise

        if 'spread'   not in self._d_set:
            self._d_set['spread']   = 1 
    #--------------------------
    def run(self):
        self._initialize()

        if self._is_cached():
            return


        success = self._wks.loadSnapshot('prefit')
        if success == False:
            self.log.error(f'Could not load prefit snapshot from:')
            self._wks.Print()
            raise

        pdf = self._wks.pdf(self._model_name)

        self._save_model()

        d_opt = self._get_mcst_settings()

        self._mcst = mcstudy(self._wks, obs_name=self._obs_name, d_opt = d_opt) 
        self._mcst.run(ndatasets = self._ntoy)
    #--------------------------
    def _get_mcst_settings(self):
        d_set = {}
        d_set['nbins']                 = self._nbins
        d_set['binning_threshold']     = self._bin_thr
        d_set['initial_spread_factor'] = self._spread

        return d_set
    #--------------------------
    def save(self, d_opt={}):
        self._initialize()

        self._save_resu(d_opt)

        d_data = self._get_data()
        self._save_pull_stat(d_data)
    #--------------------------
    def _save_model(self):
        ofile=ROOT.TFile(self._res_path, 'recreate')
        self._wks.Write()
        ofile.Close()
    #--------------------------
    def _save_resu(self, d_opt):
        if self._is_cached():
            return

        self.log.visible(f'Saving to: {self._res_path}')
        ofile = ROOT.TFile(self._res_path, 'update')
        for fit_res in self._mcst.results(): 
            fit_res.Write()

        ofile.Close()
    #-----------------------------------------------------------
    def _get_data(self):
        d_data = {}

        if self._is_cached(): 
            d_data = utnr.load_json(self._jsn_path)
            self._read_vars(d_data)

            return d_data

        self.log.info(f'Reading data from {self._res_path}')

        rob   = result_reader([self._res_path])
        d_data= rob.get_data()
    
        self.log.info(f'Dumping data to {self._jsn_path}')
        utnr.dump_json(d_data, self._jsn_path)
        self._read_vars(d_data)
    
        return d_data
    #-----------------------------------------------------------
    def _save_pull_stat(self, d_data):
        d_stat = {}
        for var_name in self._l_var_name:
            val_gen  = utnr.get_from_dic(d_data, f'{var_name}_gen')
            l_val    = utnr.get_from_dic(d_data, f'{var_name}_val')
            l_erc    = utnr.get_from_dic(d_data, f'{var_name}_erc')
    
            arr_val  = numpy.array(l_val)
            arr_erc  = numpy.array(l_erc)
    
            arr_dev  = arr_val - val_gen
            arr_pul  = arr_dev / arr_erc

            arr_fil  = (-5 < arr_pul) & (arr_pul < +5)
            arr_pul  = arr_pul[arr_fil]
    
            mu = numpy.mean(arr_pul)
            sg = numpy.std(arr_pul)

            d_stat[var_name] = [mu, sg]

        pull_stat_path = f'{self._out_dir}/stat.json'
        self.log.info(f'Saving pulls statistics to: {pull_stat_path}')
        utnr.dump_json(d_stat, pull_stat_path) 
    #-----------------------------------------------------------
    def _is_cached(self):
        is_cached = os.path.isfile(self._jsn_path)

        if is_cached:
            self.log.info(f'Using cached data from: {self._jsn_path}')
            return True

        return False
    #-----------------------------------------------------------
    def _read_vars(self, d_data):
        for key in d_data:
            if not key.endswith('_ini') and not key.endswith('_val'): 
                continue

            var_name = key.replace('_ini', '').replace('_val', '')
            self._l_var_name.append(var_name)
    #-----------------------------------------------------------------
    def _get_fit_opts(self):
        er = ROOT.RooFit.SumW2Error(True)
        mn = ROOT.RooFit.Minimizer('Minuit2', 'migrad')
        of = ROOT.RooFit.Offset(True)
        op = ROOT.RooFit.Optimize(True)
        pf = ROOT.RooFit.PrefitDataFraction(0.1)
        st = ROOT.RooFit.Strategy(2)
        sv = ROOT.RooFit.Save(True)
    
        fit_opt = ROOT.RooFit.FitOptions(er, mn, of, op, st, sv)
    
        return fit_opt
    #-----------------------------------------------------------------
    def _get_obs_name(self):
        s_all = self._wks.allVars()
        l_obs_name = []
        for var in s_all:
            var_name = var.GetName()
            is_obs   = var_name.startswith(self._obs_pref)
            if is_obs:
                l_obs_name.append(var_name)

        if len(l_obs_name) != 1:
            self.log.error(f'Not found one observable, found:')
            print(l_obs_name)
            raise
    
        return l_obs_name[0] 
#-----------------------------------------------------------------
class plot_pulls:
    log = utnr.getLogger('plot_pulls')
    #--------------------------
    def __init__(self, pull_dir):
        self._pull_dir  = pull_dir
        self._plot_dir  = None

        self._result_wc_path= f'{self._pull_dir}/fits.root'
        self._d_data        = None
        self._l_var_name    = None
        self._empty_data    = None

        self._initialized   = False
    #--------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._d_data     = self._get_data()
        if self._empty_data:
            self._initialized = True
            return

        self._l_var_name = utnr.get_from_dic(self._d_data, 'variables')

        utnr.make_dir_path(self._plot_dir)

        self._initialized = True
    #--------------------------
    def _get_data(self):
        l_json_path = utnr.glob_wc(self._result_wc_path, allow_empty=True)

        if len(l_json_path) == 0:
            self.log.warning(f'No result files found in: {self._result_wc_path}')
            self._empty_data = True
            return {}

        rob    = result_reader(l_json_path)
        d_data = rob.get_data()

        if bool(d_data) == False:
            self.log.warning('No data could be extracted by the result_reader')
            self._empty_data = True
        else:
            self._empty_data = False

        return d_data
    #--------------------------
    @property
    def plot_dir(self):
        return self._plot_dir

    @plot_dir.setter
    def plot_dir(self, value):
        self._plot_dir = value
    #--------------------------
    def _no_input(self):
        l_input = utnr.glob_wc(self._pull_dir, allow_empty=True)

        if self._empty_data or len(l_input) == 0:
            return True

        return False
    #--------------------------
    def save_plots(self):
        self._initialize()

        if self._no_input():
            self.log.warning(f'No input found, skipping: {self._pull_dir}')
            return

        self._plot_data()
        self._plot_correlations()
        self._plot_status      ()
        self._plot_error       ()
        self._plot_pull        ()
        self._plot_dist        (kind='val')
        self._plot_dist        (kind='ini')
    #-----------------------------------------------------------
    def _plot_data(self):
        toy_path_wc = f'{self._pull_dir}/data_*.dat'
        l_toy_path  = utnr.glob_wc(toy_path_wc, allow_empty=True)
        for toy_path in l_toy_path:
            toy_name = os.path.basename(toy_path)
            plot_path= f'{self._plot_dir}/{toy_name}.png' 

            arr_mass = numpy.loadtxt(toy_path, unpack=False)

            plt.hist(arr_mass, 100, alpha=0.75)
            plt.savefig(plot_path)
            plt.close('all')
    #-----------------------------------------------------------
    def _plot_correlations(self):
        l_cov = self._d_data['covariance']
        l_var = self._d_data['variables']
    
        mat   = numpy.array(l_cov)

        plot_path = f'{self._plot_dir}/correlation.png'
        utnr.plot_matrix(plot_path, l_var, l_var, mat, title='correlations', upper=False, form=None)
    #-----------------------------------------------------------
    def _plot_status(self):
        self.log.info('Plotting status')
        l_status = self._d_data['status']
    
        plot_path = f'{self._plot_dir}/status.png'
        self.log.visible(f'Saving to: {plot_path}')

        plt.hist(l_status)
        plt.savefig(plot_path)
        plt.close('all')
    #-----------------------------------------------------------
    def _plot_error(self):
        self.log.info('Plotting errors')
        for var_name in self._l_var_name:
            self.log.debug(f'Plotting: {var_name}')

            l_var_err = self._d_data[f'{var_name}_erc']
            l_var_err = utnr.remove_outliers(l_var_err)
    
            plt.hist(l_var_err, 100, alpha=0.75) 
            plt.xlabel(f'{var_name} error')
            plt.ylabel('Entries')
   
            plot_path = f'{self._plot_dir}/err_cen_{var_name}.png'
            self.log.visible(f'Saving to: {plot_path}')
            plt.savefig(plot_path)
            plt.close('all')
    #-----------------------------------------------------------
    def _plot_dist(self, kind = None):
        utnr.check_none(kind)
        self.log.info('Plotting distributions')
        for var_name in self._l_var_name:
            l_val_ini = self._d_data[f'{var_name}_ini']
            l_val_fit = self._d_data[f'{var_name}_val']
            gen_val   = self._d_data[f'{var_name}_gen']

            self.log.debug(f'{var_name:<20}{"=":<10}{gen_val:<20}')

            l_val_fit = utnr.remove_outliers(l_val_fit)
    
            plt.hist(l_val_fit, 100, label = 'Fitted'   , alpha=0.75, fill=True ) 
            plt.hist(l_val_ini, 100, label = 'Initial'  , alpha=0.75, fill=False, histtype='step') 
            plt.axvline(gen_val,     label = 'Generated', color='red')

            plt.title(var_name)
            plt.xticks(rotation=30)
            plt.ylabel('Entries')
            plt.legend()

            plot_path = f'{self._plot_dir}/dist_{var_name}.png'
            self.log.visible(f'Saving to: {plot_path}')

            plt.savefig(plot_path)
            plt.close('all')
    #-----------------------------------------------------------
    def _plot_ratio(self, sig_1, sig_2):
        l_sig_1 = self._d_data[f'{sig_1}_val']
        l_sig_2 = self._d_data[f'{sig_2}_val']

        arr_1   = numpy.array(l_sig_1)
        arr_2   = numpy.array(l_sig_2)
        arr_r   = arr_1 / arr_2

        gen_1   = self._d_data[f'{sig_1}_gen']
        gen_2   = self._d_data[f'{sig_2}_gen']
        gen_r   = gen_1 / gen_2

        max_x   = 2 * max(gen_1, gen_2)
        min_x   = 0
        rng     = (min_x, max_x)

        fig, l_ax = plt.subplots(2, 1, figsize=(5, 7))
        #-------------
        arr_1=utnr.remove_outliers(arr_1)
        arr_2=utnr.remove_outliers(arr_2)

        l_ax[0].hist(arr_1, 100, label=sig_1, alpha=0.75)
        l_ax[0].axvline(gen_1, color='blue')

        l_ax[0].hist(arr_2, 100, label=sig_2, alpha=0.75)
        l_ax[0].axvline(gen_2, color='orange')
        
        l_ax[0].set_xlabel('$\sigma$')
        l_ax[0].set_ylabel('Entries')
        l_ax[0].legend()
        #-------------
        arr_r   = utnr.remove_outliers(arr_r)

        l_ax[1].hist(arr_r, 100, color='black', label='Fit', alpha=0.50)
        l_ax[1].axvline(gen_r, color='black', label='Generated')
        l_ax[1].legend()

        l_ax[1].set_xlabel(f'{sig_1}/{sig_2}')
        l_ax[1].set_ylabel('Entries')
        #-------------

        plot_path = f'{self._plot_dir}/sig_ratio_{sig_1}_{sig_2}.png'
        self.log.visible(f'Saving to: {plot_path}')
        plt.savefig(plot_path)
        plt.close('all')
    #-----------------------------------------------------------
    def _plot_pull(self):
        for var_name in self._l_var_name:
            val_gen  = utnr.get_from_dic(self._d_data, f'{var_name}_gen')
            l_val    = utnr.get_from_dic(self._d_data, f'{var_name}_val')
            l_erc    = utnr.get_from_dic(self._d_data, f'{var_name}_erc')
    
            arr_val  = numpy.array(l_val)
            arr_erc  = numpy.array(l_erc)
    
            arr_dev  = arr_val - val_gen
            arr_pul  = arr_dev / arr_erc

            arr_fil  = (-5 < arr_pul) & (arr_pul < +5)
            arr_pul  = arr_pul[arr_fil]

            mu = numpy.mean(arr_pul)
            sg = numpy.std(arr_pul)

            stats_text = f'$\mu$={mu:.3e}\n$\sigma$={sg:.3e}'

            plt.hist(arr_pul, 100, alpha=0.75)

            plt.xlabel(f'{var_name} pull')
            plt.ylabel('Entries')
            plt.text(0.75, 0.85, stats_text, fontsize=12, transform=plt.gca().transAxes)
            plt.axvline(x=mu+ 0, ls = '-' , color='red', alpha=0.5)
            plt.axvline(x=mu-sg, ls = '-.', color='red', alpha=0.5)
            plt.axvline(x=mu+sg, ls = '-.', color='red', alpha=0.5)

            plot_path = f'{self._plot_dir}/pull_{var_name}.png'
            self.log.visible(f'Saving to: {plot_path}')

            plt.savefig(plot_path)
            plt.close('all')
#-----------------------------------------------------------
class result_reader:
    log = utnr.getLogger('result_reader')
    #-----------------------------------------------------------
    def __init__(self, l_res_path):
        self._l_res_path = l_res_path
        self._d_data     = {}

        self._initialized = False
    #-----------------------------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        if len(self._l_res_path) == 0:
            self.log.error('No result file passed')
            raise

        for res_path in self._l_res_path:
            utnr.check_file(res_path)

        self._initialized = True
    #-----------------------------------------------------------
    def _read_fit_files(self):
        l_result = []
        wks      = None
    
        for res_path in self._l_res_path:
            ifile  = ROOT.TFile(res_path)
            l_key  = ifile.GetListOfKeys()
    
            for key in l_key:
                obj = key.ReadObj()
                if wks is None and obj.InheritsFrom('RooWorkspace'):
                    wks = obj
                    continue
    
                if not obj.InheritsFrom('RooFitResult'):
                    continue
        
                if obj.status() not in [0, 1]:
                    continue
    
                l_result.append(obj)
    
        return (l_result, wks)
    #-----------------------------------------------------------
    def _add_result(self, obj):
        l_par_fin = obj.floatParsFinal()
        l_par_ini = obj.floatParsInit()
    
        l_par_name = []
        for par in l_par_fin:
            par_name = par.GetName()
            l_par_name.append(par_name)
    
            par_val = par.getVal()
            par_erp = par.getErrorHi()
            par_erc = par.getError()
            par_erm = par.getErrorLo()
    
            utnr.add_to_dic_lst(self._d_data, f'{par_name}_val', par_val)
            utnr.add_to_dic_lst(self._d_data, f'{par_name}_erp', par_erp)
            utnr.add_to_dic_lst(self._d_data, f'{par_name}_erc', par_erc)
            utnr.add_to_dic_lst(self._d_data, f'{par_name}_erm', par_erm)
    
        for par in l_par_ini:
            par_val  = par.getVal()
            par_name = par.GetName()
    
            utnr.add_to_dic_lst(self._d_data, f'{par_name}_ini', par_val)
    
        self._add_covariance(obj, l_par_name)
        self._add_par_name(l_par_name)
    
        status = obj.status()
        minNll = obj.minNll()
        covQty = obj.covQual()
    
        utnr.add_to_dic_lst(self._d_data, 'status', status)
        utnr.add_to_dic_lst(self._d_data, 'minNll', minNll)
        utnr.add_to_dic_lst(self._d_data, 'covQty', covQty)
    
        if 'nsample' not in self._d_data:
            self._d_data['nsample'] = 1
        else:
            self._d_data['nsample']+= 1
    #-----------------------------------------------------------
    def _add_par_name(self, l_par_name):
        if 'variables' in self._d_data:
            l_var_in = self._d_data['variables']
            if l_var_in != l_par_name:
                self.log.error('Array of parameter names differ:')
                self.log.into(l_var_in)
                self.log.into(l_par_name)
        else:
            self._d_data['variables']  = l_par_name
    #-----------------------------------------------------------
    def _add_covariance(self, obj, l_par_name):
        nvar     = len(l_par_name)
        mat      = numpy.zeros((nvar, nvar), dtype=float)
        mat_fail = numpy.zeros((nvar, nvar), dtype=float)
    
        for i_par_x, par_x in enumerate(l_par_name):
            for i_par_y, par_y in enumerate(l_par_name):
                corr = obj.correlation(par_x, par_y)
                if math.isnan(corr) or math.isinf(corr):
                    mat_fail[i_par_x][i_par_y] += 1
                else:
                    mat     [i_par_x][i_par_y]  = corr
    
        if 'covariance' in self._d_data:
            self._d_data['covariance'] += mat
        else:
            self._d_data['covariance']  = mat
    
        if 'cov_fail' not in self._d_data:
            self._d_data['cov_fail']    = mat_fail
        else:
            self._d_data['cov_fail']   += mat_fail
    #-----------------------------------------------------------
    def _add_gen_par(self, wks):
        d_gen_par = {}

        success = wks.loadSnapshot('prefit')
        if success == False:
            self.log.error('Could not find a prefit snapshot in:')
            wks.Print()
            raise

        l_par = wks.allVars()
        self.log.info('-----------------------------------')
        self.log.info('Extracting generation parameter values')
        self.log.info('-----------------------------------')
        for par in l_par:
            if par.isConstant():
                continue

            par_name = par.GetName()
            par_val  = par.getVal()
            utnr.add_to_dic(d_gen_par, f'{par_name}_gen', par_val)
    
            self.log.info(f'{par_name:<40}{par_val:<20.3f}')
        self.log.info('-----------------------------------')
    
        self._d_data.update(d_gen_par)
    #-----------------------------------------------------------
    def _post_process_data(self):
        nsample = utnr.get_from_dic(self._d_data, 'nsample')
    
        mat        = utnr.get_from_dic(self._d_data, 'covariance')
        mat        = mat / nsample
        covariance = mat.tolist()
    
        mat_fail   = utnr.get_from_dic(self._d_data, 'cov_fail')
        mat_fail   = mat_fail / nsample
        cov_fail   = mat_fail.tolist()

        self._d_data['covariance'] = covariance
        self._d_data['cov_fail'  ] = cov_fail 
    #-----------------------------------------------------------
    def get_data(self):
        self._initialize()

        l_result, wks = self._read_fit_files()
        self._add_gen_par(wks)

        if len(l_result) == 0:
            return {}

        for result in tqdm.tqdm(l_result, ascii=' -'):
            self._add_result(result)

        self._post_process_data()
    
        return self._d_data
#-----------------------------------------------------------

