import os
import ROOT
import math
import re
import utils 
import logging

import utils_noroot   as utnr
import read_selection as rs
import rk.selection   as rksl

from atr_mgr               import mgr         as amgr
from rk.mva                import mva_man
from rk.cutflow            import cutflow
from rk.efficiency         import efficiency

#-----------------------------------------
class ds_getter:
    log=utnr.getLogger('ds_getter')
    #------------------------------------
    def __init__(self, q2bin, trig, year, version, partition, kind, sel):
        self._q2bin     = q2bin 
        self._year_file = year
        self._vers      = version
        self._trig      = trig
        self._sel       = sel
        self._kind      = kind
        self._part      = partition

        self._l_year    = ['2011', '2012', '2015', '2016', '2017', '2018']
        self._l_version = ['v10.11tf', 'v10.12', 'v10.13', 'v10.14', 'v10.15']
        self._l_kind    = ['sign', 'data', 'cmb', 'bp_x', 'bd_x']

        self._bdt_dir   = f'{os.environ["MVADIR"]}/electron/bdt_v10.11tf.a0v2ss'
        self._h_ipchi2  = 'H_IPCHI2_OWNPV > 4'

        #Fake trigger needed to get nspd hits cut, tool needs a trigger
        #but cut does not depend on trigger
        self._dummy_trigger = 'ETOS'

        self._initialized   = False
    #------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        amgr.log.setLevel(logging.WARNING)
        mva_man.log.setLevel(logging.WARNING)
        cutflow.log.setLevel(logging.WARNING)
        efficiency.log.setLevel(logging.WARNING)

        #To find files xxxx_test will work, for everything else, only xxxx works
        self._year   = self._year_file.replace('_test', '')
        self._sample = self._get_sample()

        utnr.check_included(self._year, self._l_year   )
        utnr.check_included(self._vers, self._l_version)
        utnr.check_included(self._kind, self._l_kind)

        try:
            if self._part is not None:
                i_part, n_part = self._part
        except:
            self.log.error(f'Could not extract partitioning scheme from: {self._part}')
            raise

        self._initialized = True
    #------------------------------------
    def _get_sample(self):
        chan = 'mm' if self._trig == 'MTOS' else 'ee'

        if    self._kind == 'data':
            proc = 'data'
        elif  self._kind == 'cmb':
            proc = 'cmb'
        elif self._kind == 'sign' and self._q2bin == 'jpsi':
            proc = 'ctrl'
        elif self._kind == 'sign' and self._q2bin == 'psi2':
            proc = 'psi2'
        elif self._kind == 'bp_x' and self._trig !=  'MTOS': 
            proc = 'bpXcHs'
        elif self._kind == 'bd_x' and self._trig !=  'MTOS': 
            proc = 'bdXcHs'
        else:
            self.log.error(f'Cannot determine process for:')
            self.log.error(f'{"Kind ":<10}{self._kind:<20}')
            self.log.error(f'{"q2bin":<10}{self._q2bin:<20}')
            self.log.error(f'{"Trig ":<10}{self._trig:<20}')
            raise

        return f'{proc}_{chan}'
    #------------------------------------
    def _add_reco_cuts(self, d_cut):
        d_cut_extra = {}
        for key, cut in d_cut.items():
            if key != 'truth':
                d_cut_extra[key] = cut
                continue

            d_cut_extra[key]        = cut
            d_cut_extra['K_IPChi2'] = self._h_ipchi2

        return d_cut_extra
    #------------------------------------
    def _filter_bdt(self, df, cut):
        man=mva_man(df, self._bdt_dir, self._trig)
        df =man.add_scores('BDT')
        df = df.Filter(cut, 'bdt')

        return df
    #------------------------------------
    def _skim_df(self, df):
        if self._part is None:
            return df

        islice, nslice = self._part

        df = utils.get_df_range(df, islice, nslice)

        return df
    #------------------------------------
    def _get_df_raw(self):
        dat_dir   = os.environ['DATDIR']
        file_path = f'{dat_dir}/{self._sample}/{self._vers}/{self._year_file}.root'

        if   self._kind == 'cmb':
            tree_path = 'KSS'
        elif self._trig == 'MTOS':
            tree_path = 'KMM'
        elif self._trig in ['ETOS', 'GTIS']:
            tree_path = 'KEE'
        else:
            log.error(f'Cannot pick tree path, invalid kind/trigger: {self._kind}/{self._trig}')
            raise

        utnr.check_file(file_path)

        self.log.visible('------------------------------------')
        self.log.visible(f'Retrieving dataframe for:')
        self.log.visible(f'{"File path  ":<20}{file_path:<100}')
        self.log.visible(f'{"Tree path  ":<20}{tree_path:<100}')
        self.log.visible('------------------------------------')

        df = ROOT.RDataFrame(tree_path, file_path)
        df = self._skim_df(df)

        df.filepath = file_path
        df.treename = tree_path
        df.year     = self._year

        return df
    #------------------------------------
    def _redefine(self, d_cut, d_redefine):
        for key, new_cut in d_redefine.items():
            if key not in d_cut:
                self.log.error(f'Cannot redefine {key}, not a valid cut')
                raise ValueError

            old_cut = d_cut[key]
            d_cut[key] = new_cut

            self.log.info(f'{key:<20}{old_cut:<40}{"--->":10}{new_cut:<40}')

        return d_cut
    #------------------------------------
    def get_df(self, remove_cuts=[], d_redefine=None):
        self._initialize()

        self._remove_cuts = remove_cuts

        df    = self._get_df_raw()
        dfmgr = amgr(df)

        cf    = cutflow()
        tot   = df.Count().GetValue()
        d_cut = rksl.selection(self._sel, self._trig, self._year, self._sample, q2bin=self._q2bin)
        if self._kind in ['data', 'cmb']:
            d_cut = dict( [('truth', '(1)')] + list(d_cut.items()) )

        d_cut = self._add_reco_cuts(d_cut)

        if d_redefine is not None:
            d_cut = self._redefine(d_cut, d_redefine)

        self.log.info(f'Applying selection: {self._sel}')
        for key, cut in d_cut.items():
            if key in self._remove_cuts:
                self.log.info(f'{"skip":<10}{key:>20}')
                continue
            else:
                self.log.info(f'{"":<10}{key:>20}')

            if key == 'bdt':
                df = self._filter_bdt(df, cut)
            else:
                df = df.Filter(cut, key)

            pas=df.Count().GetValue()

            cf[key] = efficiency(pas, tot - pas, cut=cut)
            tot=pas

        df          = dfmgr.add_atr(df)
        df.treename = self._trig 
        df.cf       = cf

        return df
#-----------------------------------------

