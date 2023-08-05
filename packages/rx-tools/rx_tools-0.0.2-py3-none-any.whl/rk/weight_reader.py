import os
import numpy
import numexpr
import random
import collections

import ROOT

import matplotlib.pyplot as plt
import pandas            as pnd
import utils_noroot      as utnr
import read_selection    as rs

import utils

from hep_cl           import hist_reader as hr
from rk.oscillator    import oscillator  as osc
from rk.collector     import collector
from rk.hist_map      import hist_map

from rk.bootstrapping import reader  as btsrd
from rk.trackreader   import reader  as trard
from rk.trgreader     import reader  as trgrd
from rk.pidreader     import reader  as pidrd 
from rk.q2smear       import q2smear

from atr_mgr        import mgr

#------------------------------
class weight_reader:
    turn_on  =True
    normalize=False
    replica  =None

    log=utnr.getLogger(__name__)
    #------------------------------
    def __init__(self, df, kind):
        self._man_df                  = mgr(df)
        self._df                      = df
        self._kind                    = kind
        self._d_wgt_ver               = {}
        self._d_wgt_pat               = {}
        self._d_d_arr_wgt             = {} 
        self._l_supported_weight      = ['pid', 'trk', 'gen', 'lzr', 'hlt', 'rec', 'qsq', 'bts']
        self._l_supported_kind        = ['gen', 'rec', 'raw', 'sel']

        self._l_ee_trigger            = ['ETOS', 'GTIS']
        self._l_mm_trigger            = ['MTOS']
        self._l_trigger               = self._l_ee_trigger + self._l_mm_trigger 

        self._l_occ                   = ['npv', 'nsp', 'ntk']
        self._l_gen_treename          = ['truth', 'gen'] 
        self._l_ee_treename           = ['KEE', 'ETOS', 'GTIS']
        self._l_mm_treename           = ['KMM', 'MTOS']
        self._l_treename              = self._l_gen_treename + self._l_ee_treename + self._l_mm_treename

        self._l_year                  = ['2011', '2012', '2015', '2016', '2017', '2018']
        self._min_plt_wgt             = 0
        self._max_plt_wgt             = 3
        self._initialized             = False
        self._l_supported_return_type = ['product', 'dict']
        self._d_sys_occ               = {} 
         
        self._nboots         = None
        self._nosc           = None
        self._d_arr_wgt_nom  = None
        self._df_stat        = None
        self._kin_dir        = None

        self._size           = None

        self._mode           = None

        self._arr_wgt_cur    = None
        self._filepath       = None
        self._treename       = None
        self._trigger        = None
        self._year           = None
        self._after_sel      = None
        self._pick_attr()

        self.valdir          = None
        self.file            = None
        self.tree            = None
        self.noweights       = False
        self.storage         = collector()
        self.d_storage       = {'weight_reader' : self.storage }
        #-------------------------
        self._d_syst = {}

        self._add_gen_syst()
        self._add_rec_syst()
        self._add_pid_syst()
        self._add_lzr_syst()
        self._add_hlt_syst()
        self._add_qsq_syst()
        self._add_trk_syst()
        self._add_bts_syst()
    #------------------------------
    @property
    def df(self):
        return self._df
    #------------------------------
    def _initialize(self):
        if self._initialized:
            return

        utnr.check_included(self._kind, self._l_supported_kind)
        #-------------------------
        self._set_sys_occ()
        self._add_df_cols()
        #-------------------------
        if len(self._d_wgt_ver) == 0:
            self.noweights    = True
            self.identifier   = 'nokeys'
        else:
            l_key=list(self._d_wgt_ver.keys())
            l_key.sort()
            self.identifier = '_'.join(l_key)
        #-------------------------
        self._get_kin_dir()
        self._check_valdir()
        #-------------------------
        self._size=self._df.Count().GetValue()

        l_col = ['Weight',      'Sum', 'Cummulative', 'Zeros[\%]', 'NaNs[\%]', 'Infs[\%]']
        l_val = [  'none', self._size,    self._size,          0 ,         0 ,         0 ]

        self._df_stat        = pnd.DataFrame(columns=l_col)
        self._df_stat.loc[0] = l_val 
        #-------------------------
        if self.replica is None:
            self.log.error('Replica not specified')
            raise
        #-------------------------
        self._check_qsq()
        self._check_sel_quant('pid')

        if self._after_sel:
            self.log.info(f'Extracting mode for trigger "{self._treename}"')
            self._find_mode()
        else:
            self.log.info(f'Not extracting mode for trigger "{self._treename}"')

        self._check_corrections()

        #Version of bootstrapping "maps" is used to pass number of bootstrapping replicas
        if 'bts' in self._d_wgt_ver:
            ver, _ = self._d_wgt_ver['bts']
            self._nboots = int(ver)

        self._trigger     = self._get_trigger()
        self._initialized = True
    #----------------------------------------------
    def _get_trigger(self):
        if self._kind not in ['raw', 'sel']:
            return

        if not hasattr(self._df, 'trigger'):
            self.log.error(f'Dataframe has no trigger attribute for kind {kind}')
            raise

        trigger = self._df.trigger
        if trigger not in self._l_trigger:
            self.log.error(f'Invalid trigger {trigger} for kind {kind}')
            raise

        return trigger
    #----------------------------------------------
    def _set_sys_occ(self):
        self._d_sys_occ['MTOS'   ] = 'nTracks'
        self._d_sys_occ['ETOS'   ] = 'nTracks'
        self._d_sys_occ['GTIS'   ] = 'nTracks'
        self._d_sys_occ['GTIS_ee'] = 'nTracks'
        self._d_sys_occ['GTIS_mm'] = 'nTracks'

        self._d_sys_occ['npv'    ] = 'nPVs'
        self._d_sys_occ['ntk'    ] = 'nTracks'
        self._d_sys_occ['nsp'    ] = 'nSPDHits'
    #----------------------------------------------
    def _check_corrections(self):
        weights = self._d_wgt_ver.keys()
        l_wgt   = list(weights)
        l_wgt   = sorted(l_wgt)
        l_sup   = sorted(self._l_supported_weight)

        if   self._kind == 'gen' and l_wgt == ['bts', 'gen']:
            return
        elif self._kind == 'rec' and l_wgt == ['bts', 'gen']:
            return
        elif self._kind == 'raw' and l_wgt == ['bts', 'gen', 'rec']:
            return
        elif self._kind == 'sel' and l_wgt == l_sup:
            return
        else:
            self.log.warning(f'For kind {self._kind} found weights:')
            self.log.warning(l_wgt)
    #----------------------------------------------
    def _pick_attr(self):
        self._filepath = utnr.get_attr(self._df, 'filepath')
        self._treename = utnr.get_attr(self._df, 'treename')
        self._year     = utnr.get_attr(self._df, 'year')

        if self._treename not in self._l_treename: 
            self.log.error(f'Unrecognized trigger: {self._df.treename}')
            raise

        self._after_sel = self._treename in self._l_trigger
    #------------------------------
    def _add_gen_syst(self):
        d_gen_syst = {}

        for treename in self._l_treename:
            d_gen_syst[ ('gen', treename, '000') ] = None
            d_gen_syst[ ('gen', treename, 'all') ] = None
            d_gen_syst[ ('gen', treename, 'nom') ] = None

        self._d_syst.update(d_gen_syst)
    #------------------------------
    def _add_rec_syst(self):
        d_rec_syst = {}

        for treename in self._l_treename:
            d_rec_syst[ ('rec', treename, '000') ] = None
            d_rec_syst[ ('rec', treename, 'all') ] = None
            d_rec_syst[ ('rec', treename, 'nom') ] = None

        self._d_syst.update(d_rec_syst)
    #------------------------------
    def _add_pid_syst(self):
        d_pid_syst = {}

        for trg in ['MTOS', 'ETOS', 'GTIS']:
            d_pid_syst[ ('pid', trg, '000') ] = None
            d_pid_syst[ ('pid', trg, 'all') ] = None
            d_pid_syst[ ('pid', trg, 'nom') ] = None 

        self._d_syst.update(d_pid_syst)
    #------------------------------
    def _add_lzr_syst(self):
        d_lzr_syst = {}

        for trg in self._l_trigger: 
            d_lzr_syst[('lzr', trg, '000')] = None 
            d_lzr_syst[('lzr', trg, 'all')] = None 
            d_lzr_syst[('lzr', trg, 'nom')] = None 

        self._d_syst.update(d_lzr_syst)
    #------------------------------
    def _add_hlt_syst(self):
        d_hlt_syst = {}

        for trg in self._l_trigger: 
            d_hlt_syst[('hlt', trg, '000')] = None
            d_hlt_syst[('hlt', trg, 'all')] = None
            d_hlt_syst[('hlt', trg, 'nom')] = None

        self._d_syst.update(d_hlt_syst)
    #------------------------------
    def _add_qsq_syst(self):
        d_qsq_syst = {}

        for trg in ['MTOS', 'ETOS', 'GTIS']:
            for sys in ['000', 'nom', 'all']:
                d_qsq_syst[('qsq',  trg,  sys)] = None

        self._d_syst.update(d_qsq_syst)
    #------------------------------
    def _add_trk_syst(self):
        d_trk_syst = {}

        for trg in ['MTOS', 'ETOS', 'GTIS']:
            d_trk_syst[ ('trk', trg, '000') ] = None
            d_trk_syst[ ('trk', trg, 'all') ] = None
            d_trk_syst[ ('trk', trg, 'nom') ] = None

        self._d_syst.update(d_trk_syst)
    #------------------------------
    def _add_bts_syst(self):
        d_bts_syst = {}

        for trg in ['gen', 'KEE', 'KMM', 'MTOS', 'ETOS', 'GTIS']:
            d_bts_syst[ ('bts', trg, 'nom') ] = None
            d_bts_syst[ ('bts', trg, 'all') ] = None

        self._d_syst.update(d_bts_syst)
    #------------------------------
    def __setitem__(self, sys, value):
        if sys not in self._l_supported_weight:
            self.log.error(f'Weight {sys} is not supported')
            self.log.info(self._l_supported_weight)
            raise

        try:
            _, sys_set = value
        except:
            self.log.error(f'Value for key {key} is {value}, expected tuple (version, systematic)')
            raise

        self._check_sys(sys, sys_set)
        self._d_wgt_ver[sys] = value
    #------------------------------
    def _check_sys(self, sys, sys_set):
        tp_sys = (sys, self._treename, sys_set)

        if tp_sys not in self._d_syst:
            self.log.error(f'{tp_sys} setting not allowed by:')
            for wgt, trg, sys in self._d_syst:
                if trg != self._treename:
                    continue
                self.log.info(f'{wgt:<10}{trg:<10}{sys:<10}')
            raise
    #----------------------------------------------
    def _add_df_cols(self):
        l_col = self._df.GetColumnNames()
        if 'B_TRUEETA' not in l_col:
            df       = self._df.Define('B_TRUEETA', 'TVector3 b(B_TRUEP_X, B_TRUEP_Y, B_TRUEP_Z); return b.Eta();')
            self._df = self._man_df.add_atr(df)
    #----------------------------------------------
    def _get_kin_dir(self):
        try:
            self._kin_dir = os.environ['CALDIR']
            self.log.info(f'Using calibration path: {self._kin_dir}')
        except:
            self.log.error(f'Cannot find directory with calibration maps in {CALDIR}')
            raise
    #----------------------------------------------
    def _check_valdir(self):
        if self.valdir is not None and not os.path.isdir(self.valdir):
            try:
                self.log.info('Making validation directory: ' + self.valdir)
                utnr.make_dir_path(self.valdir)
            except:
                self.log.info('Could not make validation directory: ' + self.valdir)
                raise
    #----------------------------------------------
    def _check_qsq(self):
        self._check_sel_quant('qsq')

        if not self._after_sel: 
            return

        _, sys_set = self._d_wgt_ver['qsq']

        if sys_set != '000' and self._treename == 'MTOS':
            self.log.error(f'Using setting {sys_set} for q2 weights and trigger {self._treename}, only setting "0" can be used.')
            raise
    #----------------------------------------------
    def _check_sel_quant(self, quant):
        if  not self._after_sel and quant in self._d_wgt_ver:
            self.log.error(f'Selection weight, {quant}, specified for trigger {self._treename} (before selection)')
            raise

        if self._after_sel and quant not in self._d_wgt_ver:
            self.log.error(f'Selection weight, {quant}, not specified for trigger {self._treename}')
            utnr.pretty_print(self._d_wgt_ver)
            raise
    #----------------------------------------------
    def _find_mode(self):
        try:
            arr_jpsi_id = self._df.AsNumpy(['Jpsi_TRUEID'])['Jpsi_TRUEID']
        except:
            self.log.error('Cannot read "Jpsi_TRUEID" from')
            self.log.error('{0:<20}{1:<100}'.format('Filepath', self._filepath))
            self.log.error('{0:<20}{1:<100}'.format('Tree'    , self._treename))
            raise

        if   numpy.all(arr_jpsi_id ==    443):
            self._mode = 'jpsi'
        elif numpy.all(arr_jpsi_id == 100443):
            self._mode = 'psi2'
        else:
            #Rare mode needs to be implemented
            self.log.error('Unsuppored channel for dilepton ID:')
            print(arr_jpsi_id)
            raise
    #----------------------------------------------
    def _get_gen_path(self, kind, ver, sys_set):
        binning = '3'     if sys_set in self._l_occ else '1'
        end_nam = sys_set if sys_set in self._l_occ else 'nom'
        trigger = 'MTOS'  if sys_set in self._l_occ else sys_set

        return f'{self._kin_dir}/{kind}/{ver}.{binning}/{trigger}_{self._year}_{kind}_{end_nam}.root'
    #----------------------------------------------
    def _get_wgt_args(self, kind, ver, sys_set):
        if   kind == 'gen':
            wgt_path = self._get_gen_path(kind, ver, sys_set)
        elif kind == 'rec':
            wgt_path = f'{self._kin_dir}/{kind}/{ver}.1/{sys_set}_{self._year}_{kind}_nom.root'
        elif kind == 'qsq':
            wgt_path = f'{self._kin_dir}/{kind}/{ver}.{sys_set}'
        elif kind in ['lzr', 'hlt']:
            wgt_path = f'{self._kin_dir}/trg/{ver}.1'
            tp_tag   = tuple(sys_set.split('.'))
        elif kind == 'pid':
            wgt_path = f'{self._kin_dir}/{kind}/{ver}.{sys_set}'
        elif kind == 'trk':
            wgt_path = f'{self._kin_dir}/{kind}/{ver}.{sys_set}'
        else:
            self.log.error(f'Unsupported weight kind/sys: {kind}/{sys_set}')
            raise

        wgt_path = wgt_path.replace(' ', '')
        self._d_wgt_pat[kind] = wgt_path

        if kind == 'lzr':
            return (tp_tag, wgt_path)
        else:
            return wgt_path
    #------------------------------
    def _is_data_hist(self, hist):
        name = hist.GetName() 

        if   name == 'h_data' or name.startswith('h_num'):
            return True
        elif name == 'h_ctrl' or name.startswith('h_den'):
            return False 
        else:
            self.log.error('Histogram is neither data nor MC:')
            hist.Print()
            raise
    #------------------------------
    def _get_kin_hist(self, path, kind):
        '''Get numerator and denominator histograms from ROOT file in path'''
        utnr.check_file(path)

        ifile = ROOT.TFile(path)
        l_key = ifile.GetListOfKeys()
        h_1, h_2 = [ key.ReadObj() for key in l_key]

        h_num = h_1 if self._is_data_hist(h_1) else h_2
        h_den = h_2 if self._is_data_hist(h_1) else h_1

        h_num.SetDirectory(0)
        h_den.SetDirectory(0)

        ifile.Close()

        return [h_num, h_den]
    #------------------------------
    def _get_kin_weights(self, kind, ver, sys_set):
        self.log.info(f'Calculating {kind} weights for systematic {sys_set}')
        wgt_path=self._get_wgt_args(kind, ver, sys_set)
        h_num, h_den = self._get_kin_hist(wgt_path, kind)

        obj   = osc()
        h_num = obj.get_oscillated_map('num', h_num)
        h_den = obj.get_oscillated_map('den', h_den)

        rwt = hr(dt=h_num, mc=h_den)

        occ_var=utnr.get_from_dic(self._d_sys_occ, sys_set)
        if   kind == 'gen':
            arr_val=utils.getMatrix(self._df, ['B_TRUEPT', 'B_TRUEETA', occ_var])
        elif kind == 'rec':
            arr_val=utils.getMatrix(self._df, ['log(B_ENDVERTEX_CHI2)', 'log(B_IPCHI2_OWNPV)', 'TMath::ACos(B_DIRA_OWNPV)'])
        else:
            self.log.error(f'Invalid kind: {kind}')
            raise

        arr_wgt = rwt.predict_weights(arr_val)

        return arr_wgt
    #------------------------------
    def _get_pid_sim(self):
        self.log.info(f'Calculating PID weights from simulation')

        l_col_name = self._df.GetColumnNames()
        if 'pid_sim' not in l_col_name:
            pid_sel  = rs.get('pid', self._treename, q2bin=self._mode, year = self._year)
            self.log.info(f'Defining pid_sim as: {pid_sel} == 1')
            df = self._df.Define('pid_sim', f'{pid_sel} == 1')
        else:
            self.log.info(f'pid_sim found')
            df = self._df

        arr_wgt = df.AsNumpy(['pid_sim'])['pid_sim']
        arr_wgt = arr_wgt.astype(int)

        wgt_sum = numpy.sum(arr_wgt)
        wgt_len = len(arr_wgt)

        if wgt_sum >= wgt_len:
            self.log.error(f'Weight sum is larger or equal than number of weights: {wgt_sum} >= {wgt_len}')
            self.log.error(f'Filename: {self._filepath}[{self._treename}]')
            raise

        return arr_wgt
    #------------------------------
    def _get_pid_weights(self, ver, sys_set):
        self.log.info(f'Calculating PID weights for systematic {sys_set}')

        dirpath = self._get_wgt_args('pid', ver, sys_set)

        reweighter=pidrd()
        reweighter.setMapPath(dirpath)
        arr_pid_l1, arr_pid_l2, arr_pid_hd=reweighter.predict_weights(self._df, replica=self.replica)

        self._plot_wgt(f'pid_lp1_{sys_set}', {sys_set : arr_pid_l1             })
        self._plot_wgt(f'pid_lp2_{sys_set}', {sys_set : arr_pid_l2             })
        self._plot_wgt(f'pid_lep_{sys_set}', {sys_set : arr_pid_l1 * arr_pid_l2})
        self._plot_wgt(f'pid_had_{sys_set}', {sys_set : arr_pid_hd             })

        self.d_storage['pid'] = reweighter.storage
        arr_wgt = arr_pid_l1 * arr_pid_l2 * arr_pid_hd

        return arr_wgt
    #------------------------------
    def _get_lzr_weights(self, ver, sys_set):
        self.log.info(f'Calculating L0 weights for systematic {sys_set}')

        tp_tag, wgt_dir = self._get_wgt_args('lzr', ver, sys_set)

        reweighter=trgrd(self._year, wgt_dir)
        arr_wgt = reweighter.predict_weights(tp_tag, self._df, replica=self.replica) 

        return arr_wgt
    #------------------------------
    def _get_hlt_rwt(self, mappath):
        ifile = ROOT.TFile(mappath)
        h_pas_dat = ifile.h_data_pass
        h_fal_dat = ifile.h_data_fail
        h_pas_sim = ifile.h_sim_pass
        h_fal_sim = ifile.h_sim_fail

        h_pas_dat.SetDirectory(0)
        h_fal_dat.SetDirectory(0)
        h_pas_sim.SetDirectory(0)
        h_fal_sim.SetDirectory(0)

        ifile.Close()

        obj       = osc()
        h_pas_dat = obj.get_oscillated_map('h_pas_dat', h_pas_dat)
        h_fal_dat = obj.get_oscillated_map('h_fal_dat', h_fal_dat)
        h_pas_sim = obj.get_oscillated_map('h_pas_sim', h_pas_sim)
        h_fal_sim = obj.get_oscillated_map('h_fal_sim', h_fal_sim)

        rwt = hist_map()
        rwt.add_hist(h_pas_dat, h_fal_dat, data=True)
        rwt.add_hist(h_pas_sim, h_fal_sim, data=False)

        return rwt
    #----------------------------------------------
    def _get_hlt_weights(self, ver, sys_set):
        self.log.info(f'Calculating HLT weights for systematic {sys_set}')

        d_data    = self._df.AsNumpy(['B_PT', 'B_ETA'])
        arr_pt    = d_data['B_PT']
        arr_et    = d_data['B_ETA']
        arr_point = numpy.array([arr_pt, arr_et]).T

        dirpath     = self._get_wgt_args('hlt', ver, sys_set)
        mappath     = f'{dirpath}/HLT_{self._treename}_{self._year}.root'
        rwt         = self._get_hlt_rwt(mappath)
        arr_eff     = rwt.get_efficiencies(arr_point) 

        arr_eff_dat = arr_eff.T[0]
        arr_eff_sim = arr_eff.T[1]

        arr_wgt = arr_eff_dat / arr_eff_sim

        return arr_wgt
    #----------------------------------------------
    def _get_qsq_weights(self, ver, sys_set, smear=True):
        self.log.info(f'Calculating Q2 weights for systematic {sys_set}')

        treename=self._df.treename
        #-------------------------
        if smear:
            q2dir=self._get_wgt_args('qsq', ver, sys_set)
            smr=q2smear(self._df, q2dir)
            self.log.visible(f'Applying q2 smearing for trigger/systematic: {treename}/{sys_set}')
            storage=smr.storage

            arr_smr=smr.get_q2_smear(self.replica)
        else:
            arr_smr = self._df.AsNumpy(['Jpsi_M'])['Jpsi_M']
            storage=collector()
        #-------------------------

        q2_sel  = rs.get('q2', self._treename, q2bin=self._mode, year = self._year)
        q2_sel  = q2_sel.replace('&&', '&')

        arr_wgt = numexpr.evaluate(q2_sel, {'Jpsi_M' : arr_smr})

        arr_wgt = arr_wgt.astype(float)

        self._check_eff(arr_wgt, q2_sel, max_eff=0.999, min_eff=0.900)
        #-------------------------
        storage.add('qsq_jpsi_mass_smr', arr_smr)
        storage.add('qsq_jpsi_mass_wgt', arr_wgt)

        self.d_storage['qsq'] = storage
        #-------------------------

        return arr_wgt
    #------------------------------
    def _get_trk_weights(self, ver, sys_set):
        self.log.info(f'Calculating TRK weights for systematic {sys_set}')

        rdr = trard()
        dirpath = self._get_wgt_args('trk', ver, sys_set)
        rdr.setMapPath(dirpath)
        wgt_l1, wgt_l2         = rdr.getWeight(self._df)
        self._d_wgt_pat['trk'] = rdr.maps

        arr_wgt = numpy.multiply(wgt_l1, wgt_l2) 

        return arr_wgt
    #------------------------------
    def _get_bts_weights(self, version, syst):
        rdr = btsrd()
        rdr.setYear(self._year)
        arr_wgt = rdr.getWeight(self._df, syst)

        return arr_wgt
    #------------------------------
    def _get_weights(self, kind, ver, sys_set):
        self.log.visible(f'Getting {kind} weights')

        l_syst = self._get_syst(kind, sys_set)

        if   kind not in ['pid', 'qsq'] and sys_set == '000':
            d_arr_wgt = {'0'   : numpy.ones(self._size)}
        elif kind == 'pid'              and sys_set == '000': 
            d_arr_wgt = {'0'   : self._get_pid_sim() }
        elif kind == 'qsq'              and sys_set == '000':
            d_arr_wgt = {'0'   : self._get_qsq_weights(ver, sys_set, smear=False)}
        #----------------------------
        elif kind in ['gen', 'rec']:
            d_arr_wgt = { syst : self._get_kin_weights(kind, ver, syst) for syst in l_syst}
        elif kind == 'lzr':
            d_arr_wgt = { syst : self._get_lzr_weights(      ver, syst) for syst in l_syst}
        elif kind == 'hlt':
            d_arr_wgt = { syst : self._get_hlt_weights(      ver, syst) for syst in l_syst}
        elif kind == 'pid': 
            d_arr_wgt = { syst : self._get_pid_weights(      ver, syst) for syst in l_syst}
        elif kind == 'qsq':
            d_arr_wgt = { syst : self._get_qsq_weights(      ver, syst) for syst in l_syst}
        elif kind == 'trk':
            d_arr_wgt = { syst : self._get_trk_weights(      ver, syst) for syst in l_syst}
        elif kind == 'bts':
            d_arr_wgt = { syst : self._get_bts_weights(      ver, syst) for syst in l_syst} 
        #----------------------------
        else:
            self.log.error(f'Wrong kind or setting: {kind}/{sys_set}')
            raise

        for syst, arr_wgt in d_arr_wgt.items():
            self._check_weights(arr_wgt, kind, syst)

        self._plot_wgt(kind, d_arr_wgt)
        #self._add_stat(kind, d_arr_wgt)

        return d_arr_wgt 
    #------------------------------
    def _add_stat(self, kind, d_arr_wgt):
        keys    = d_arr_wgt.keys()
        nom_key = list(keys)[0]
        arr_wgt = d_arr_wgt[nom_key]
        if self._arr_wgt_cur is None:
            self._arr_wgt_cur  = arr_wgt
        else:
            self._arr_wgt_cur *= arr_wgt 

        try:
            nwgt = arr_wgt.size
            nz   = 100. * numpy.count_nonzero(arr_wgt       < 1e-5) / nwgt 
            nn   = 100. * numpy.count_nonzero(numpy.isnan(arr_wgt)) / nwgt 
            ni   = 100. * numpy.count_nonzero(numpy.isinf(arr_wgt)) / nwgt 
        except:
            self.log.error(f'Could not extract information from kind: {kind}')
            print(arr_wgt)
            raise

        sum_wgt = numpy.sum(arr_wgt)
        cum_wgt = numpy.sum(self._arr_wgt_cur)

        l_val = [kind, f'{sum_wgt:.0f}', f'{cum_wgt:.0f}', f'{nz:.3f}', f'{nn:.3f}', f'{ni:.3f}'] 

        self._df_stat = utnr.add_row_to_df(self._df_stat, l_val)
    #------------------------------
    def _calculate_weights(self):
        d_d_arr_wgt = {}
        for kind, (ver, sys) in self._d_wgt_ver.items():
            d_d_arr_wgt[kind] = self._get_weights(kind, ver, sys)

        self._d_d_arr_wgt= {kind : d_d_arr_wgt[kind] for kind in self._l_supported_weight if kind in d_d_arr_wgt}
    #----------------------------------------------
    def _check_eff(self, arr_wgt, sel, min_eff = 0.10, max_eff = 0.99):
        eff = numpy.sum(arr_wgt) / float(arr_wgt.size)

        if  (eff > 0.00 and eff < min_eff) or (eff > max_eff and eff < 1.00):
            self.log.warning('{0:<20}{1:40.3e}'.format('Efficiency', eff))
            self.log.warning('{0:<20}{1:40}'.format('Selection' , sel))
            self.log.warning(self._filepath)
        elif eff <= 0.00 or eff >  1.00:
            self.log.error('{0:<20}{1:40.3e}'.format('Efficiency', eff))
            self.log.error('{0:<20}{1:40}'.format('Selection' , sel))
            self.log.error(self._filepath)

            d_freq = collections.Counter(arr_wgt)
            nzero  = d_freq[0.]
            nones  = d_freq[1.]

            self.log.error('{0:<20}{1:40}'.format('Fail freq' , nzero))
            self.log.error('{0:<20}{1:40}'.format('Pass freq' , nones))

            raise
        else:
            self.log.debug('{0:<20}{1:40.3e}'.format('Efficiency', eff))
            self.log.debug('{0:<20}{1:40}'.format('Selection' , sel))
    #------------------------------
    def _get_syst(self, kind, sys_set):
        if   kind == 'gen':
            l_sys = ['MTOS', 'GTIS_mm', 'npv', 'nsp', 'ntk']
        #---------------------
        elif kind == 'rec' and self._trigger == 'MTOS':
            l_sys = ['MTOS', 'GTIS_mm']
        elif kind == 'rec' and self._trigger == 'ETOS':
            l_sys = ['ETOS', 'GTIS_ee']
        elif kind == 'rec' and self._trigger == 'GTIS':
            l_sys = ['GTIS', 'ETOS']
        #---------------------
        elif kind == 'pid' and self._treename in ['ETOS', 'GTIS']:
            l_sys = ['nom', 'kp_el_bin1', 'kp_el_bin2', 'kp_el_bin3', 'kp_el_bin4', 'kp_el_tis', 'el_bin1', 'el_tis']
        elif kind == 'pid' and self._treename == 'MTOS':
            l_sys = ['nom', 'kp_mu_bin1', 'kp_mu_bin2', 'kp_mu_bin3', 'kp_mu_bin4', 'kp_mu_tis', 'mu_bin1', 'mu_bin2', 'mu_bin3', 'mu_bin4', 'mu_tis']
        #---------------------
        elif kind == 'lzr' and self._treename == 'MTOS':
            l_sys = ['L0MuonTIS', 'L0MuonHAD', 'L0MuonMU1']
        elif kind == 'lzr' and self._treename == 'ETOS':
            l_sys = ['L0ElectronTIS', 'L0ElectronHAD', 'L0ElectronFAC']
        elif kind == 'lzr' and self._treename == 'GTIS':
            l_tag_1 = ['L0TIS_EMMH.L0HadronElEL.L0ElectronTIS', 'L0TIS_MMMH.L0HadronElEL.L0ElectronTIS', 'L0TIS_EMBN.L0HadronElEL.L0ElectronTIS']
            l_tag_2 = ['L0TIS_EMMH.L0HadronElEL.L0ElectronHAD', 'L0TIS_EMMH.L0HadronElEL.L0ElectronFAC']

            l_sys = l_tag_1 + l_tag_2
        #---------------------
        elif kind == 'hlt':
            l_sys = [self._treename]
        #---------------------
        elif kind == 'trk':
            l_sys = ['nom']
        #---------------------
        elif kind == 'qsq':
            l_sys = ['nom', 'lsh', 'mom', 'trg']
        #---------------------
        elif kind == 'bts':
            l_sys = list(range(self._nboots)) 
        #---------------------
        else:
            self.log.error(f'Invalid kind: {kind}')
            raise

        # Due to not knowing if KEE will be paired with ETOS or GTIS, cannot drop rec weights
        if sys_set == 'nom' and kind != 'rec':
            l_sys = l_sys[:1]

        return l_sys
    #------------------------------
    def _plot_wgt(self, kind, d_arr_wgt):
        if   self.valdir is None: 
            return 

        plot_path=f'{self.valdir}/{kind}_{self._treename}.png'

        if   kind.startswith('pid'):
            yrange = (0, 1)
            nbins  = 100
        elif kind.startswith('bts'):
            yrange = (0, 10)
            nbins  = 10
        else:
            yrange = (0, 2)
            nbins  = 100

        if kind == 'bts' and len(d_arr_wgt) > 5:
            l_key = random.sample(d_arr_wgt.keys(), 5)
            d_tmp = {key : d_arr_wgt[key] for key in l_key}
            d_arr_wgt = d_tmp

        for sys, arr_wgt in d_arr_wgt.items():
            plt.hist(arr_wgt, range=yrange, bins=nbins, alpha=0.75, label=sys)

        plt.xlabel('Weight')
        plt.ylabel('Entries')
        plt.title(kind)
        plt.legend()
        plt.savefig(plot_path)
        plt.close('all')
    #------------------------------
    def _check_weights(self, arr_wgt, kind, sys):
        self._check_wgt_size(arr_wgt, kind, sys)

        arr_unique_wgt = numpy.unique(arr_wgt)
        if kind != 'bts' and len(arr_unique_wgt) == 1 and sys != '0':
            self.log.warning(f'For {kind} correction, systematic {sys} found only one weight: {arr_wgt[0]}')
    #------------------------------
    def _print_settings(self):
        l_str_sys = list(self._d_wgt_ver.keys())
        l_str_val = list(self._d_wgt_ver.values())

        self.log.visible('-------------------')
        self.log.visible(f'Getting {self._kind} weights for')
        self.log.visible('-------------------')
        self.log.visible(f'{"Mode":<15}{str(self._mode):<50}') 
        self.log.visible(f'{"Tree":<15}{self._treename :<50}') 
        self.log.visible(f'{"Year":<15}{self._year     :<50}') 

        for sys, val in zip(l_str_sys, l_str_val):
            sys = str(sys)
            val = str(val)
            self.log.visible(f'{sys:<15}{val:<50}')
    #------------------------------
    def _check_wgt_size(self, arr_wgt, kind, syst):
        size_arr = numpy.size(arr_wgt, axis=0)
        if size_arr != self._size:
            self.log.error(f'Weights of kind/syst {kind}/{syst} are not compatible with input data')
            self.log.error(f'{"Weight size":<20}{size_arr:<20}')
            self.log.error(f'{"Data size  ":<20}{self._size:<20}')
            raise
    #------------------------------
    def _save(self):
        self.storage.add('weight_flow', self._df_stat)
        self._save_wf()
        self._save_paths()
    #------------------------------
    def _save_wf(self):
        if self.valdir is None:
            return

        table_path = f'{self.valdir}/stats_{self.identifier}_{self._treename}.tex'
        self._df_stat.style.to_latex(table_path)
    #------------------------------
    def _save_paths(self):
        if self.valdir is None:
            return

        pathspath=f'{self.valdir}/paths_{self.identifier}_{self._treename}.txt'
        ofile=open(pathspath, 'w')

        for key, (ver, sys) in sorted(self._d_wgt_ver.items()):
            ofile.write(f'{key:<20}{ver:<10}{sys:<10}\n')
        ofile.write('---------------------------\n')

        for key, value      in sorted(self._d_wgt_pat.items()):
            ofile.write(f'{key:<20}{value:<20}\n')
        ofile.write('---------------------------\n')

        ofile.write(f'{"filepath":<20}{self._filepath:<80}\n')

        ofile.close()
    #------------------------------
    def _get_ext_columns(self, l_ext_col):
        if len(l_ext_col) == 0:
            d_data = {}
        else:
            self.log.info('Adding extra columns')
            utils.check_df_has_columns(self._df, l_ext_col)
            d_data = self._df.AsNumpy(l_ext_col)

        return d_data
    #------------------------------
    def _multiply_weights(self):
        d_arr_wgt_nom = {} 
        for wgt, d_arr_wgt in self._d_d_arr_wgt.items():
            l_arr_wgt = list(d_arr_wgt.values())
            try:
                arr_wgt_nom = l_arr_wgt[0]
            except:
                self.log.error(f'For {wgt} correction, cannot extract any weights')
                utnr.pretty_print(self._d_d_arr_wgt)
                raise

            d_arr_wgt_nom[wgt] = arr_wgt_nom

        d_arr_wgt_sys_all = {}
        for wgt, d_arr_wgt in self._d_d_arr_wgt.items():
            d_arr_wgt_sys = self._multiply_syst(wgt, d_arr_wgt_nom, d_arr_wgt)
            d_arr_wgt_sys_all.update(d_arr_wgt_sys)

        l_arr_wgt_nom = list(d_arr_wgt_nom.values())

        d_arr_wgt_sys_all['nom'] = numpy.multiply.reduce(l_arr_wgt_nom) 

        self._d_arr_wgt_nom = d_arr_wgt_nom

        return d_arr_wgt_sys_all 
    #------------------------------
    def _multiply_syst(self, wgt, d_arr_wgt_nom, d_arr_wgt):
        d_arr_wgt_sys = {}
        first         = True

        self.log.info(f'For {wgt}, systematics calculated:')
        for sys, arr_wgt_sys in d_arr_wgt.items():
            if first:
                first=False
                continue

            l_sys = [sys]
            arr_wgt_tot = numpy.copy(arr_wgt_sys)
            for key, arr_wgt_nom in d_arr_wgt_nom.items():
                if key == wgt:
                    continue

                l_sys.append(key)
                arr_wgt_tot = utnr.numpy_multiply(arr_wgt_tot, arr_wgt_nom, same_size=True)

            self._print_list(l_sys, col_width = 20)
            d_arr_wgt_sys[f'{wgt}_{sys}'] = arr_wgt_tot

        return d_arr_wgt_sys
    #------------------------------
    def _print_list(self, l_data, col_width = 20):
        line = f''
        for data in l_data:
            line += f'{data:<{col_width}}'
        self.log.info(line)
    #------------------------------
    def get_weights(self, l_ext_col=None):
        self._initialize()
        self._print_settings()
        self._calculate_weights()
        self._save()

        d_wgt=self._multiply_weights()

        return d_wgt
    #------------------------------
    def get_wgt_fac(self):
        if self._d_arr_wgt_nom is None:
            self.get_weights()

        d_fac = self._d_arr_wgt_nom
        if 'bts' not in d_fac:
            self.log.error(f'Not found bts entry in nominal weight dictionary:')
            print(d_fac.keys())
            raise

        del(d_fac['bts'])

        return d_fac
#------------------------------

