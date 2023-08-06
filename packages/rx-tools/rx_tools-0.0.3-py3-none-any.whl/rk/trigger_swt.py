import utils_noroot     as utnr

import read_calibration as rc

import numpy
import logging 
import trgwgt
import utils

#-------------------------------------------
class trigger_swt:
    log = utnr.getLogger(__name__)
    def __init__(self, tag, year, binning_dir, df_dat, df_sim, version=None):
        self.__tag         = tag
        self.__year        = year
        self.__binning_dir = binning_dir
        self.__df_dat      = df_dat
        self.__df_sim      = df_sim
        self.__version     = version

        self.__initialized = False
    #-------------------------------------------
    def __initialize(self):
        if self.__initialized:
            return

        self.__year = int(self.__year)

        utnr.check_none(self.__binning_dir)
        utnr.check_none(self.__version)

        utnr.check_dir(self.__binning_dir)

        self.__check_data(self.__df_dat)
        self.__check_data(self.__df_sim)

        self.__initialized = True
    #-------------------------------------------
    def __check_data(self, df):
        l_name = df.GetColumnNames()
        if 'weight' not in l_name:
            self.log.error('\'weight\' column not found in input data')
            raise

        if 'no_weight' in l_name:
            self.log.error('\'no_weight\' column found in input data')
            raise
    #-------------------------------------------
    def __print_stats(self, header, arr_val, arr_wgt, arr_evt):
        nval = len(arr_val)
        nwgt = len(arr_wgt)
        nevt = len(arr_evt)
        swgt = numpy.sum(arr_wgt)
    
        self.log.debug('_____________________')
        self.log.debug(header)
        self.log.debug('_____________________')
        self.log.debug('{0:20}{1:20}'.format('Values'         , nval))
        self.log.debug('{0:20}{1:20}'.format('Weights'        , nwgt))
        self.log.debug('{0:20}{1:20}'.format('Events'         , nevt))
        self.log.debug('{0:20}{1:20.0f}'.format('Sum of weights' , swgt))
        self.log.debug('_____________________')
    #-------------------------------------------
    def __split_by_probe(self, l_var, weight, flag, d_val):
        arr_wgt = d_val[weight]
        arr_flg = d_val[flag]
        arr_evt = d_val['eventNumber']
    
        self.log.debug('Flag sum/Flag length: {}/{}'.format(numpy.sum(arr_flg), len(arr_flg)))
    
        if   len(l_var) == 1:
            arr_val = d_val[l_var[0]]
        elif len(l_var)  > 1:
            l_arr = []
            for var in l_var:
                arr=d_val[var]
                l_arr.append(arr)
            tup_arr=tuple(l_arr)
            arr_val = numpy.vstack(tup_arr).T
        else:
            self.log.error('Wrong list of vars ' + str(l_var))
            raise
    
        l_evt_p = []
        l_val_p = []
        l_wgt_p = []
    
        l_evt_f = []
        l_val_f = []
        l_wgt_f = []
    
        for flg, wgt, evt, val in zip(arr_flg, arr_wgt, arr_evt, arr_val):
            if flg == 0:
                l_wgt_f.append(wgt)
                l_val_f.append(val)
                l_evt_f.append(evt)
            else:
                l_wgt_p.append(wgt)
                l_val_p.append(val)
                l_evt_p.append(evt)
    
        return ( numpy.array(l_val_p), numpy.array(l_val_f), numpy.array(l_wgt_p), numpy.array(l_wgt_f), numpy.array(l_evt_p), numpy.array(l_evt_f) )
    #-------------------------------------------
    def __get_weight_name(self, df, no_sweights=None):
        if   no_sweights == True:
            df = df.Define('no_weight', '1')
            weight = 'no_weight'
        elif no_sweights == False:
            weight   = 'weight'
            utils.df_has_col(df, weight, fail=True)
        else:
            self.log.error('Invalid no_sweights = ' + no_sweights)
            raise

        return (df, weight)
    #-------------------------------------------
    def __extract_info(self, df, tag, no_sweights=None):
        df, weight = self.__get_weight_name(df, no_sweights)

        if   tag == 'L0ElectronFAC':
            probe = rc.get('L0ElectronFAC', year=None)

            df = df.Define('flag', probe)
            df = df.Define('max_et', 'TMath::Max(L1_L0Calo_ECAL_realET, L2_L0Calo_ECAL_realET)')
            df = df.Define('r_calo', 'TVector3 e_1(L1_L0Calo_ECAL_xProjection, L1_L0Calo_ECAL_yProjection, 0); TVector3 e_2(L2_L0Calo_ECAL_xProjection, L2_L0Calo_ECAL_yProjection, 0); return (e_1 - e_2).Mag();')
    
            self.log.visible('{0:20}{1:40}'.format('Probe cut', probe))
    
            d_val = df.AsNumpy(['max_et', 'r_calo', 'eventNumber', weight, 'flag'])
            arr_val_p, arr_val_f, arr_wgt_p, arr_wgt_f, arr_evt_p, arr_evt_f = self.__split_by_probe(['max_et', 'r_calo'], weight, 'flag', d_val)
        elif tag in ['L0ElectronHAD', 'L0ElectronTIS']:
            probe_1 = rc.get('L0ElectronEL1', year=None)

            df = df.Define('fl1', probe_1)
            self.log.visible('{0:20}{1:40}'.format('Probe cut', probe_1))
    
            d_val_1 = df.AsNumpy(['L1_L0Calo_ECAL_realET', 'L1_L0Calo_ECAL_region', 'eventNumber', weight, 'fl1'])
            arr_val_p_1, arr_val_f_1, arr_wgt_p_1, arr_wgt_f_1, arr_evt_p_1, arr_evt_f_1 = self.__split_by_probe(['L1_L0Calo_ECAL_realET', 'L1_L0Calo_ECAL_region'], weight, 'fl1', d_val_1)
            #---------------
            probe_2 = rc.get('L0ElectronEL2', year=None)

            df = df.Define('fl2', probe_2)
            self.log.visible('{0:20}{1:40}'.format('Probe cut', probe_2))
    
            d_val_2 = df.AsNumpy(['L2_L0Calo_ECAL_realET', 'L2_L0Calo_ECAL_region', 'eventNumber', weight, 'fl2'])
            arr_val_p_2, arr_val_f_2, arr_wgt_p_2, arr_wgt_f_2, arr_evt_p_2, arr_evt_f_2 = self.__split_by_probe(['L2_L0Calo_ECAL_realET', 'L2_L0Calo_ECAL_region'], weight, 'fl2', d_val_2)
            #---------------
            arr_val_p = numpy.concatenate((arr_val_p_1, arr_val_p_2), axis = 0)
            arr_val_f = numpy.concatenate((arr_val_f_1, arr_val_f_2), axis = 0)
    
            arr_wgt_p = numpy.concatenate((arr_wgt_p_1, arr_wgt_p_2), axis = 0)
            arr_wgt_f = numpy.concatenate((arr_wgt_f_1, arr_wgt_f_2), axis = 0)
    
            arr_evt_p = numpy.concatenate((arr_evt_p_1, arr_evt_p_2), axis = 0)
            arr_evt_f = numpy.concatenate((arr_evt_f_1, arr_evt_f_2), axis = 0)
        elif tag in ['L0MuonHAD'    ,     'L0MuonTIS']:
            probe_1 = rc.get('L0MuonMU1', year=None)

            df = df.Define('fl1', probe_1)
            self.log.visible('{0:20}{1:40}'.format('Probe cut', probe_1))
    
            d_val_1 = df.AsNumpy(['L1_PT', 'L1_ETA', 'eventNumber', weight, 'fl1'])
            arr_val_p_1, arr_val_f_1, arr_wgt_p_1, arr_wgt_f_1, arr_evt_p_1, arr_evt_f_1 = self.__split_by_probe(['L1_PT', 'L1_ETA'], weight, 'fl1', d_val_1)
            #---------------
            probe_2 = rc.get('L0MuonMU2', year=None)

            df = df.Define('fl2', probe_2)
            self.log.visible('{0:20}{1:40}'.format('Probe cut', probe_2))
    
            d_val_2 = df.AsNumpy(['L2_PT', 'L2_ETA', 'eventNumber', weight, 'fl2'])
            arr_val_p_2, arr_val_f_2, arr_wgt_p_2, arr_wgt_f_2, arr_evt_p_2, arr_evt_f_2 = self.__split_by_probe(['L2_PT', 'L2_ETA'], weight, 'fl2', d_val_2)
            #---------------
            arr_val_p = numpy.concatenate((arr_val_p_1, arr_val_p_2), axis = 0)
            arr_val_f = numpy.concatenate((arr_val_f_1, arr_val_f_2), axis = 0)
    
            arr_wgt_p = numpy.concatenate((arr_wgt_p_1, arr_wgt_p_2), axis = 0)
            arr_wgt_f = numpy.concatenate((arr_wgt_f_1, arr_wgt_f_2), axis = 0)
    
            arr_evt_p = numpy.concatenate((arr_evt_p_1, arr_evt_p_2), axis = 0)
            arr_evt_f = numpy.concatenate((arr_evt_f_1, arr_evt_f_2), axis = 0)
        #TODO:Enable line below when branches missing be added to files.
        #elif tag in ['L0HadronElEL', 'L0HadronElTIS', 'L0HadronMuMU', 'L0HadronMuTIS']:
        elif tag in ['L0HadronElEL', 'L0HadronElTIS']:
            probe = rc.get('L0Hadron', year=None)

            df = df.Define('fl', probe)
            self.log.visible('{0:20}{1:40}'.format('Probe cut', probe))
    
            d_val = df.AsNumpy(['H_L0Calo_HCAL_realET', 'H_L0Calo_HCAL_region', 'eventNumber', weight, 'fl'])
            arr_val_p, arr_val_f, arr_wgt_p, arr_wgt_f, arr_evt_p, arr_evt_f = self.__split_by_probe(['H_L0Calo_HCAL_realET', 'H_L0Calo_HCAL_region'], weight, 'fl', d_val)
        elif tag in ['L0MuonALL1', 'L0MuonMU1']:
            probe = rc.get('L0MuonMU2', year=None)

            df = df.Define('fl', probe)
            self.log.visible('{0:20}{1:40}'.format('Probe cut', probe))
    
            d_val = df.AsNumpy(['L2_PT', 'L2_ETA', 'eventNumber', weight, 'fl'])
            arr_val_p, arr_val_f, arr_wgt_p, arr_wgt_f, arr_evt_p, arr_evt_f = self.__split_by_probe(['L2_PT', 'L2_ETA'], weight, 'fl', d_val)
        elif tag == 'L0TIS_MH':
            probe = rc.get('L0TIS_EM', year=None)

            xvar=   'TMath::Max(L1_PT, L2_PT)'
            yvar=   'L1_PT > L2_PT ? L1_ETA : L2_ETA'
    
            df = df.Define('fl', probe)
            df = df.Define('xv',  xvar)
            df = df.Define('yv',  yvar)
    
            self.log.visible('{0:20}{1:40}'.format('Probe cut', probe))
    
            d_val = df.AsNumpy(['xv', 'yv', 'eventNumber', weight, 'fl'])
            arr_val_p, arr_val_f, arr_wgt_p, arr_wgt_f, arr_evt_p, arr_evt_f = self.__split_by_probe(['xv', 'yv'], weight, 'fl', d_val)
        elif tag in ['L0TIS_EM', 'L0TIS_MM']:
            probe = rc.get('L0TIS_MH', year=None)

            df = df.Define('fl', probe)
            self.log.visible('{0:20}{1:40}'.format('Probe cut', probe))
    
            d_val = df.AsNumpy(['B_PT', 'B_ETA', 'eventNumber', weight, 'fl'])
            arr_val_p, arr_val_f, arr_wgt_p, arr_wgt_f, arr_evt_p, arr_evt_f = self.__split_by_probe(['B_PT', 'B_ETA'], weight, 'fl', d_val)
        elif tag.startswith('HLT_'):
            if   tag in ['HLT_ETOS', 'HLT_HTOS', 'HLT_GTIS']:
                probe = rc.get('HLTElectron', self.__year)

            elif tag == 'HLT_MTOS': 
                probe = rc.get('HLTMuon'    , self.__year)
            else:
                self.self.log.error('Invalid HLT tag ' + tag)
                raise

            df = df.Define('fl', probe)
            self.log.visible('{0:20}{1:40}'.format('Probe cut', probe))
    
            d_val = df.AsNumpy(['B_PT', 'B_ETA', 'eventNumber', weight, 'fl'])
            arr_val_p, arr_val_f, arr_wgt_p, arr_wgt_f, arr_evt_p, arr_evt_f = self.__split_by_probe(['B_PT', 'B_ETA'], weight, 'fl', d_val)
        else:
            self.log.error('Unrecognized tag ' +  tag)
            raise
    
        return ( (arr_val_p, arr_wgt_p, arr_evt_p), (arr_val_f, arr_wgt_f, arr_evt_f) ) 
    #-------------------------------------------
    def get_reweighter(self, tag, no_replicas=False):
        self.__initialize()

        tup_dat_p, tup_dat_f = self.__extract_info(self.__df_dat, tag, no_sweights = False)
        tup_sim_p, tup_sim_f = self.__extract_info(self.__df_sim, tag, no_sweights = False)
        tup_dir_p, tup_dir_f = self.__extract_info(self.__df_sim, tag, no_sweights = True )
        
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.__print_stats('Passed data'      , *tup_dat_p)
            self.__print_stats('Failed data'      , *tup_dat_f)
    
            self.__print_stats('Passed simulation', *tup_sim_p)
            self.__print_stats('Failed simulation', *tup_sim_f)
    
            self.__print_stats('Passed direct'    , *tup_dir_p)
            self.__print_stats('Failed direct'    , *tup_dir_f)
    
        rwt=trgwgt.rwt(tag, self.__year, self.__binning_dir, version=self.__version)
        rwt.set_array(tup_dat_p, 'data_passed')
        rwt.set_array(tup_dat_f, 'data_failed')
    
        rwt.set_array(tup_sim_p,  'sim_passed')
        rwt.set_array(tup_sim_f,  'sim_failed')
    
        rwt.set_array(tup_dir_p,  'dir_passed')
        rwt.set_array(tup_dir_f,  'dir_failed')
    
        rwt.fill_map(replica=0)
        if not no_replicas:
            rwt.fill_map(replica=10)
            rwt.fill_map(replica=100)
            rwt.fill_map(replica=1000)
    
        return rwt 
#-------------------------------------------

