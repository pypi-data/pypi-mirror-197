import utils_noroot      as utnr
import utils
import os
import re 
import ROOT

from hep_cl        import hist_reader as hr
from rk.fithst     import extractor

#----------------------------------------
class rwt(extractor):
    log=utnr.getLogger('rwt')
    #----------------------------------------
    @property
    def maxentries(self):
        return self._maxentries

    @maxentries.setter
    def maxentries(self, value):
        self._maxentries = value
    #----------------------------------------
    @property
    def dat_ver(self):
        return self._dat_ver

    @dat_ver.setter
    def dat_ver(self, value):
        self._dat_ver = value
    #----------------------------------------
    @property
    def cuts(self):
        return self._d_cut

    @cuts.setter
    def cuts(self, value):
        self._d_cut.update(value)
    #----------------------------------------
    @property
    def set_dir(self):
        return self._set_dir

    @set_dir.setter
    def set_dir(self, value):
        self._set_dir = value
    #----------------------------------------
    @property
    def wgt_dir(self):
        return self._wgt_dir

    @wgt_dir.setter
    def wgt_dir(self, value):
        self._wgt_dir = value
    #----------------------------------------
    @property
    def wgt_ver(self):
        return self._wgt_ver

    @wgt_ver.setter
    def wgt_ver(self, value):
        self._wgt_ver = value
    #----------------------------------------
    @property
    def syst(self):
        return self._syst

    @syst.setter
    def syst(self, value):
        self._syst = value
    #----------------------------------------
    def __init__(self, preffix, trigger, year):
        self._preffix     = preffix
        self._trigger     = trigger
        self._year        = year 

        self._pickle_path = None
        self._set_dir     = None
        self._wgt_dir     = None
        self._wgt_ver     = None
        self._syst        = None
        self._dat_ver     = None
        self._bin_ver     = None
        self._d_cut       = {}
        self._maxentries  = -1

        super().__init__()

        self._initialized = False
    #----------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        super()._initialize()

        self._pickle_path = self._get_pickle_path()

        utnr.check_dir(self._set_dir)
        utnr.check_none(self._wgt_ver)
        utnr.check_none(self._dat_ver)

        if self._wgt_dir is None:
            self._wgt_dir = os.environ['CALDIR']

        self._prepare_rdf()

        self._initialized=True
    #----------------------------------------
    def _prepare_rdf(self):
        rdf_mc = self._get_rdf('ctrl')
        rdf_dt = self._get_rdf('data')

        d_bin            = self._get_binning()
        rdf_mc, l_var_mc = self._add_vars(rdf_mc)
        rdf_dt, l_var_dt = self._add_vars(rdf_dt)

        if l_var_mc != l_var_dt:
            self.log.error(f'Variables added to data and MC differ:')
            self.log.error(l_var_mc)
            self.log.error(l_var_dt)
            raise
        else:
            self._l_var = l_var_mc

        self._d_bin  = { var : arr_bin for var, (_, arr_bin) in zip(l_var_mc, d_bin.items()) }

        self._rdf_mc = self._add_cuts(rdf_mc)
        self._rdf_dt = self._add_cuts(rdf_dt)
    #----------------------------------------
    def _get_rdf(self, kind):
        tree_name = 'KMM'        if self._trigger in ['MTOS', 'GTIS_mm'] else 'KEE'
        sample    = f'{kind}_mm' if self._trigger in ['MTOS', 'GTIS_mm'] else f'{kind}_ee'

        file_path = f'{os.environ["DATDIR"]}/{sample}/{self._dat_ver}/{self._year}.root'
        self.log.info(f'{kind}: {file_path}/{tree_name}')
        rdf = ROOT.RDataFrame(tree_name, file_path)

        return rdf
    #----------------------------------------
    def _add_vars(self, rdf):
        '''Takes RDF, ads expression columns and returns (rdf, list of variable names)'''
        l_col = rdf.GetColumnNames()
        if 'mass' not in l_col:
            rdf = rdf.Define('mass', self._mass_var)

        l_var = []
        for exp in self._l_exp:
            rdf, var = utils.add_column_df(rdf, exp)
            l_var.append(var)

        return rdf, l_var
    #----------------------------------------
    def _add_cuts(self, rdf):
        '''Takes RDF applies analysis cuts + boundary cuts and prints report'''
        for key, cut in self._d_cut.items():
            rdf = rdf.Filter(cut, key)

        self._bound_filter_rdf(rdf)

        rp = rdf.Report()
        rp.Print()

        return rdf
    #----------------------------------------
    def _get_pickle_path(self):
        '''Get path to output pickle file''' 
        if   self._preffix == 'toy':
             outdir=f'{self._wgt_dir}/TOY'
        elif self._preffix == 'gen':
            outdir=f'{self._wgt_dir}/GEN'
        elif self._preffix == 'rec':  
            outdir=f'{self._wgt_dir}/REC'
        else:
            self.log.error(f'Wrong prefix {self._prefix}')
            raise
        
        end_name = 'nom' if self._syst == 'trg' else self._syst
        
        pickle_dir = utnr.make_dir_path(f'{outdir}/{self._wgt_ver}')
        pickle_path= f'{pickle_dir}/{self._trigger}_{self._year}_{self._preffix}_{end_name}.pickle'
        
        return pickle_path 
    #----------------------------------------
    def _get_bin_vers(self):
        '''Get binning version from vX.(Y)'''
        regex = 'v\d+\.(\d+)'
        mtch  = re.match(regex, self._wgt_ver)

        if not mtch:
            self.log.error(f'Cannot extract binning version from: {self._wgt_ver} with {regex}')
            raise

        vers = mtch.group(1)

        return str(vers)
    #----------------------------------------
    def _get_binning(self):
        '''Get exp -> Array of boundaries dictionary by loading JSON and dropping entries'''
        set_path = f'{self._set_dir}/kinematics_trg.json'
        d_set    = utnr.load_json(set_path)
        key      = f'{self._preffix}_{self._trigger}_{self._year}'
        d_bin    = d_set[key]

        self._l_exp = d_bin['rwt_vars']

        l_to_delete = []
        bin_vers    = self._get_bin_vers()
        for key in d_bin:
            if not key.endswith(f'_{bin_vers}'):
                l_to_delete.append(key)

        for key in l_to_delete:
            del(d_bin[key])

        if len(d_bin) != len(self._l_exp):
            self.log.error(f'Inconsistent number of axes and expressions: {len(d_bin)}/{len(self._l_exp)}')
            raise

        self.log.debug(f'Using variables: {self._l_exp}')
        self.log.debug(f'Using binning:')
        for _, arr in d_bin.items():
            self.log.debug(f'   {arr}')

        return d_bin
    #----------------------------------------
    def save_reweighter(self, force_redo=False):
        self._initialize()

        if os.path.isfile(self._pickle_path) and force_redo == False:
            self.log.visible(f'Output already found in {self._pickle_path}, skipping')
            return

        h_mc, h_dt = self.get_histograms(force_redo = force_redo)

        obj  = hr(dt=h_dt, mc=h_mc)

        self.log.visible(f'Saving to: {self._pickle_path}')

        utnr.dump_pickle(obj, self._pickle_path)
#----------------------------------------

