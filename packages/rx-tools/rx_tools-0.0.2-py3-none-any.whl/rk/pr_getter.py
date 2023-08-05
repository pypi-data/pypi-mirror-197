import utils_noroot     as utnr
import read_calibration as rcal
import utils

from rk.cutflow      import cutflow
from rk.efficiency   import efficiency 
from rk.selection    import selection as rksl

import os
import re 
import ROOT

#-----------------------------------------------------------
class pr_getter:
    log = utnr.getLogger(__name__)
    def __init__(self, proc, dset, trig, vers, q2bin, selection):
        self._proc   = proc
        self._dset   = dset 
        self._trig   = trig 
        self._vers   = vers 
        self._sele   = selection
        self._q2bin  = q2bin
        self._wks    = ROOT.RooWorkspace('wks')
        self._tree   = None

        self._min_mass = None
        self._max_mass = None

        self._max_evt        = -1
        self._rho            = +1
        self._bkg_cat_cut    = None

        self._diagnostic_dir = None

        self._l_trig_sel = ['ETOS', 'GTIS']
        self._l_trig_cal = ['gtis_inclusive', 'L0TIS_EM', 'L0TIS_MH', 'L0ElectronTIS', 'L0ElectronHAD', 'L0HadronElEL']
        self._l_trig     = self._l_trig_sel + self._l_trig_cal

        self._l_proc = ['bpXcHs_ee', 'bdXcHs_ee']
        self._l_dset = ['r1', 'r2p1', '2016', '2017', '2018']
        self._l_vers = ['v10.11tf']
        self._l_sele = ['final_nobdt_gorder_wide']
        self._l_q2bin= ['jpsi', 'psi2']

        self._l_keep_in_mem = []
        self._d_q2bin_mass  = { 'jpsi' : 'B_const_mass_M[0]' , 'psi2' : 'B_const_mass_psi2S_M[0]' }
        self._evt_branch    = 'eventNumber'
        self._mass_branch   = None
        self._tree_name     = 'KEE'
        self._l_save_branch = ['mass', 'true_mass', 'L1_BremMultiplicity', 'L2_BremMultiplicity']

        self._initialized   = False
    #-----------------------------------------------------------
    @property
    def max_evt(self):
        return self._max_evt

    @max_evt.setter
    def max_evt(self, val):
        self._max_evt = val
    #-----------------------------------------------------------
    @property
    def rho(self):
        return self._rho

    @rho.setter
    def rho(self, val):
        self._rho = val
    #-----------------------------------------------------------
    @property
    def bkg_cat(self):
        return self._bkg_cat

    @bkg_cat.setter
    def bkg_cat(self, val):
        self._bkg_cat_cut = val
    #-----------------------------------------------------------
    def  _initialize(self):
        if self._initialized:
            return

        if self._trig == 'GTIS_ee':
            self._trig = 'gtis_inclusive'

        utnr.check_included(self._proc , self._l_proc )
        utnr.check_included(self._vers , self._l_vers )
        utnr.check_included(self._dset , self._l_dset )
        utnr.check_included(self._trig , self._l_trig )
        utnr.check_included(self._sele , self._l_sele )
        utnr.check_included(self._q2bin, self._l_q2bin)

        self._initialized = True
    #-----------------------------------------------------------
    def _get_df(self, l_year):
        dat_dir  = os.environ['DATDIR']
        file_dir = f'{dat_dir}/{self._proc}/{self._vers}'

        l_df = []
        for year in l_year:
            file_path = f'{file_dir}/{year}.root'
            self.log.visible(f'Using: {file_path}')
            df = ROOT.RDataFrame(self._tree_name, file_path)
            if self._max_evt > 0:
                df = df.Range(self._max_evt)
            df = self._filter(df, year)

            df = self._add_columns(df)

            l_df.append(df)

        return l_df
    #-----------------------------------------------------------
    def _add_columns(self, df):
        self._mass_branch = utnr.get_from_dic(self._d_q2bin_mass, self._q2bin)
        df = df.Define('mass', self._mass_branch)

        true_mass = '''
        ROOT::Math::LorentzVector<ROOT::Math::XYZTVector> v_h( H_TRUEP_X,  H_TRUEP_Y,  H_TRUEP_Z,  H_TRUEP_E);
        ROOT::Math::LorentzVector<ROOT::Math::XYZTVector> v_1(L1_TRUEP_X, L1_TRUEP_Y, L1_TRUEP_Z, L1_TRUEP_E);
        ROOT::Math::LorentzVector<ROOT::Math::XYZTVector> v_2(L2_TRUEP_X, L2_TRUEP_Y, L2_TRUEP_Z, L2_TRUEP_E);

        auto v_b = v_h + v_1 + v_2;

        return v_b.M();
        '''
        df = df.Define('true_mass', true_mass)

        return df
    #-----------------------------------------------------------
    def _get_years(self):
        if   self._proc in ['bpXcHs_ee', 'bdXcHs_ee']   and self._dset in [  'r1', '2011']:
            l_year = []
        elif self._proc == 'bpXcHs_ee'                  and self._dset in ['r2p1', '2015', '2016']:
            l_year = []
        #-----------------------------
        elif self._proc == 'psi2Kstr_ee'                and self._dset ==   'r1':
            l_year = ['2011', '2012']
        elif self._proc in ['psi2Kstr_ee', 'bdXcHs_ee'] and self._dset == 'r2p1':
            l_year = ['2015', '2016']
        #-----------------------------
        elif                               self._dset in ['2011', '2012', '2015', '2016', '2017', '2018']:
            l_year = [self._dset]
        else:
            self.log.error(f'Cannot find list of year for process "{self._proc}" and dataset "{self._dset}"')
            raise

        self.log.info(f'Using years "{l_year}" for process "{self._proc}" and dataset "{self._dset}"')

        return l_year
    #-----------------------------------------------------------
    def _get_mass(self, cut):
        regex='\(B_[\w_\[\]]+\s+>\s(\d+)\)\s+&&\s+\(B_[\w_\[\]]+\s+<\s(\d+)\)'

        try:
            min_mass = utnr.get_regex_group(cut, regex, i_group=1)
            max_mass = utnr.get_regex_group(cut, regex, i_group=2)

            self._min_mass = int(min_mass)
            self._max_mass = int(max_mass)
        except:
            self.log.error(f'Cannot extract mass window from "{cut}"')
            raise

        self.log.visible(f'Extracted mass window ({self._min_mass}, {self._max_mass})')
    #-----------------------------------------------------------
    def _add_bkg_cat(self, d_cut):
        if self._bkg_cat_cut is None:
            return d_cut

        self.log.visible(f'Using background categories: {self._bkg_cat_cut}')
        d_out = {'bkg_cat' : self._bkg_cat_cut} 

        d_out.update(d_cut)

        return d_out
    #-----------------------------------------------------------
    def _get_analysis_selection(self, year):
        self.log.visible('Applying cuts')
        if   self._trig in self._l_trig_cal:
            #Dummy trigger, will be replaced later
            trig = 'ETOS'
        elif self._trig in self._l_trig_sel:
            trig = self._trig
        else:
            self.log.error(f'Trigger {self._trig} not valid')
            raise

        d_cut = rksl(self._sele, trig, year, self._proc, q2bin=self._q2bin)

        return d_cut
    #-----------------------------------------------------------
    def _get_selection(self, year):
        d_cut = self._get_analysis_selection(year)
        d_cut = self._add_bkg_cat(d_cut)

        if self._trig in self._l_trig_sel:
            return d_cut

        cut = rcal.get(self._trig, year)
        d_cut_final = dict()
        for key, val in d_cut.items():
            if key != 'ETOS':
                d_cut_final[key]        = val
            else:
                d_cut_final[self._trig] = cut 

        return d_cut_final
    #-----------------------------------------------------------
    def _filter(self, df, year):
        d_cut = self._get_selection(year)

        l_cut = []
        for key, cut in d_cut.items():
            if key == 'mass':
                self._get_mass(cut)
            df = df.Filter(cut, key)
            l_cut.append(cut)

        cfl = self._get_cutflow(df, l_cut)
        self._save_cutflow(cfl, year)

        return df 
    #-----------------------------------------------------------
    def _get_cutflow(self, df, l_cut):
        cfl = cutflow()

        rep = df.Report()
        for cut_info, cut_str in zip(rep, l_cut):
            key  = cut_info.GetName()
            ival = cut_info.GetAll()
            fval = cut_info.GetPass()

            cfl[key] = efficiency(fval, arg_tot = ival, cut = cut_str)

        return cfl
    #-----------------------------------------------------------
    def _save_cutflow(self, cfl, year):
        if self.diagnostic_dir is None:
            return

        dir_path = utnr.make_dir_path(self.diagnostic_dir)

        cfl_path = f'{dir_path}/cutflow.tex'
        self.log.visible(f'Saving to: {cfl_path}')
        cfl.df_eff.to_latex(buf=open(cfl_path, 'w'), index=False)

        cut_path = f'{dir_path}/cuts.csv'
        self.log.visible(f'Saving to: {cut_path}')
        cfl.df_cut.to_csv(cut_path, index=False)
    #-----------------------------------------------------------
    def _save_events(self, l_df):
        d_evt_mas = {}
        for df in l_df:
            d_data = df.AsNumpy([self._evt_branch, 'mass'])

            arr_evt = d_data[self._evt_branch]
            arr_mas = d_data['mass']

            d_tmp = dict(zip(arr_evt.tolist(), arr_mas.tolist()))
            d_evt_mas.update(d_tmp)

        dir_path = utnr.make_dir_path(self.diagnostic_dir)
        evt_path = f'{dir_path}/events.json'
        self.log.visible(f'Saving to: {evt_path}')

        utnr.dump_json(d_evt_mas, evt_path)
    #-----------------------------------------------------------
    def _get_tree(self, l_df):
        self.log.visible('Getting trees')

        chain = ROOT.TChain('tree')
        for df in l_df:
            itree, ifile = utils.get_tree_from_df(df, tree_name='tree', file_path=None, l_col=self._l_save_branch)
            file_path = ifile.GetName()
            ifile.Close()

            chain.AddFile(file_path)

        return chain
    #-----------------------------------------------------------
    def _split_by_brem(self, tree):
        df   = ROOT.RDataFrame(tree)
        df   = df.Define('nbrem', 'L1_BremMultiplicity + L2_BremMultiplicity')

        df_z = df.Filter('nbrem == 0')
        df_o = df.Filter('nbrem == 1')
        df_m = df.Filter('nbrem >  1')

        tree_z, file_z = utils.get_tree_from_df(df_z, tree_name='tree', file_path=None, l_col=self._l_save_branch)
        tree_o, file_o = utils.get_tree_from_df(df_o, tree_name='tree', file_path=None, l_col=self._l_save_branch)
        tree_m, file_m = utils.get_tree_from_df(df_m, tree_name='tree', file_path=None, l_col=self._l_save_branch)

        self._l_keep_in_mem.append(file_z)
        self._l_keep_in_mem.append(file_o)
        self._l_keep_in_mem.append(file_m)

        return [tree_z, tree_o, tree_m]
    #-----------------------------------------------------------
    def _get_observable(self, kind):
        if   kind == 'reco':
            obs_name = 'mass'
        elif kind == 'true':
            obs_name = 'true_mass'
        else:
            log.error(f'Invalid kind {kind}')
            raise

        obs = ROOT.RooRealVar(obs_name, self._mass_branch, self._min_mass, self._max_mass)

        return obs
    #-----------------------------------------------------------
    def _fit(self, l_tp_tree, kind=None):
        self.log.visible('Fitting')

        obs = self._get_observable(kind)

        for dname, pname, tree in l_tp_tree:
            if kind == 'true':
                pname = f'{pname}_true'
                dname = f'{dname}_true'

            data = ROOT.RooDataSet(dname, '', ROOT.RooArgSet(obs), ROOT.RooFit.Import(tree))
            pdf  = ROOT.RooKeysPdf(pname, '', obs, data, ROOT.RooKeysPdf.MirrorBoth, self._rho)

            self._wks.Import(pdf)
            self._wks.Import(data)
    #-----------------------------------------------------------
    def _check_stats(self, tree, l_tree):
        ntot = tree.GetEntries()
        nsum = 0

        for stree in l_tree:
            nsum += stree.GetEntries()

        if nsum != ntot:
            self.log.error(f'Sum of partial trees does not equal full tree: {nsum} != {ntot}')
            raise
    #-----------------------------------------------------------
    def get_wks(self):
        self._initialize()

        l_year = self._get_years()

        if l_year == []:
            self.log.warning(f'Cannot get model for dataset "{self._dset}", no corresponding files found, skipping')
            raise

        l_df   = self._get_df(l_year)
        self._save_events(l_df)

        tree_a                 = self._get_tree(l_df)
        tree_z, tree_o, tree_m = self._split_by_brem(tree_a)

        self._check_stats(tree_a, [tree_z, tree_o, tree_m])

        l_tp_tree = []
        if True:
            l_tp_tree.append(('data'  , 'pdf'  , tree_a))
            l_tp_tree.append(('data_z', 'pdf_z', tree_z))
            l_tp_tree.append(('data_o', 'pdf_o', tree_o))
            l_tp_tree.append(('data_m', 'pdf_m', tree_m))

        self._fit(l_tp_tree, kind='true')
        self._fit(l_tp_tree, kind='reco')
        self._tree = tree_a

        return self._wks
    #-----------------------------------------------------------
    def get_tree(self):
        if self._tree is None:
            self.log.error(f'Tree not found, get_wks() needs to be run first')
            raise

        return self._tree
#-----------------------------------------------------------

