import ROOT

import re
import os
import pickle
import numpy
import logging 

import hep_gb
import hep_cl

import pandas       as pnd
import utils_noroot as utnr
import utils

from rk.weight_reader import weight_reader
#----------------------------------------
class rwt:
    log = utnr.getLogger(__name__)
    #-------------------------------
    def __init__(self, preffix, trigger, year):
        self._preffix     = preffix
        self._trigger     = trigger
        self._year        = year
        #Public
        self.swt_ver      = None
        self.wgt_ver      = None
        self.set_dir      = 'share'
        self.maxentries   = -1 
        #From JSON 
        self._d_settings  = None
        self._version     = None
        self._binning     = None
        self._l_var       = None
        self._arr_x       = None
        self._arr_y       = None
        self._arr_z       = None
        #Built from args
        self._syst        = None
        self._sigpath     = None
        self._simpath     = None
        self._treename    = None
        self._weight      = None
        self._chan        = None
        #Used for checks
        self._l_preffix   = ['toy' ,  'gen', 'rec']
        self._l_ee_trigger= ['ETOS', 'GTIS_ee', 'GTIS']
        self._l_mm_trigger= ['MTOS', 'GTIS_mm']
        self._l_trigger   = ['TRG'] + self._l_ee_trigger + self._l_mm_trigger
        self._l_year      = ['0'   , '2011', '2012', '2015', '2016', '2017', '2018']
        self._l_syst      = ['trg' , 'npv' , 'nsp' , 'ntk' ]

        self._dat_ver     = None
        self._wgt_dir     = None
        self._val_dir     = None
        self._df_info     = None

        self._initialized = False
    #-------------------------------
    @property
    def syst(self):
        return self._syst

    @syst.setter
    def syst(self, value):
        self._syst = value 
    #-------------------------------
    @property
    def dat_ver(self):
        return self._dat_ver

    @dat_ver.setter
    def dat_ver(self, value):
        self._dat_ver = value 
    #-------------------------------
    @property
    def dat_path(self):
        return self._sigpath

    @dat_path.setter
    def dat_path(self, value):
        self._sigpath = value
    #-------------------------------
    @property
    def wgt_dir(self):
        return self._wgt_dir

    @wgt_dir.setter
    def wgt_dir(self, value):
        self._wgt_dir = utnr.make_dir_path(value)
    #-------------------------------
    def _set_binning(self):
        regex = 'v(\d+)\.(\d)'
        mtch = re.match(regex, self.wgt_ver)
        if not mtch:
            self.log.error(f'Cannot extract binning from: {self.wgt_ver}')
            self.log.error(f'Need version that matches regex: {regex}')
            raise

        version = mtch.group(1)
        binning = mtch.group(2)

        x_key = f'arr_x_{binning}'
        y_key = f'arr_y_{binning}'
        z_key = f'arr_z_{binning}'
        try:
            l_x        =self._d_settings[x_key]
            l_y        =self._d_settings[y_key]
            l_z        =self._d_settings[z_key]

            self._arr_x=numpy.array(l_x).astype(float)
            self._arr_y=numpy.array(l_y).astype(float)
            self._arr_z=numpy.array(l_z).astype(float)
        except:
            self.log.error(f'Cannot read array of boundaries {x_key}/{y_key}/{z_key}')
            raise

        self.log.info(f'Using binning: {binning}')
        self.log.info(f'X bounds: {l_x}')
        self.log.info(f'Y bounds: {l_y}')
        self.log.info(f'Z bounds: {l_z}')

        self._version = version
        self._binning = binning
    #-------------------------------
    def _check_setting(self, setting, l_setting):
        if setting not in l_setting:
            self.log.error('Unsupported setting {}, use:'.format(setting))
            print(l_setting)
            raise
    #-------------------------------
    def _initialize(self):
        if self._initialized:
            return

        utnr.check_included(self._syst, self._l_syst)
        #-----
        if self._wgt_dir is None:
            self._wgt_dir = os.environ['CALDIR']
        #-----
        self._check_setting(self._preffix, self._l_preffix)
        self._check_setting(self._trigger, self._l_trigger)
        self._check_setting(self._year   , self._l_year   )
        #-----
        json_path = f'{self.set_dir}/kinematics_{self._syst}.json'
        sett_key  = f'{self._preffix}_{self._trigger}_{self._year}'
        self.log.info(f'Reading {sett_key} settings from: {json_path}')

        d_data           = utnr.load_json(json_path)
        self._d_settings = utnr.get_from_dic(d_data, sett_key)
        #-----
        if self._wgt_dir is None:
            self.log.error('Calibration directory not specified')
            raise

        utnr.check_dir(self._wgt_dir)
        #-----
        if self.wgt_ver is None:
            self.log.error('No weights version specified')
            raise

        if self.swt_ver is None:
            self.log.error('No sweights version specified')
            raise

        self._set_binning()
        #-----
        self._l_var   = self._d_settings["rwt_vars"]
        #-----
        self._chan    = self._get_channel()
        self._sigpath = self._get_sigpath()
        self._simpath = self._sigpath.replace("dt", "mc").replace("data_", "ctrl_")

        utnr.check_file(self._sigpath)
        utnr.check_file(self._simpath)

        self._treename = self._get_treename()
        #-----
        self._weight = f'pid_eff * sw_{self._trigger}' 

        self._df_info = self._get_info_df()
        #-----
        self._val_dir = self._get_val_dir()

        self._initialized = True
    #-------------------------------
    def _get_val_dir(self):
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

        val_dir = utnr.make_dir_path(f'{outdir}/{self.wgt_ver}/{self._trigger}_{self._year}_{self._preffix}_{end_name}')

        return val_dir
    #-------------------------------
    def _get_channel(self):
        if   self._trigger in self._l_ee_trigger:
            return 'ee'
        elif self._trigger in self._l_mm_trigger:
            return 'mm'
        elif self._trigger == 'TRG':
            return None
        else:
            self.log.error(f'Unrecognized trigger {self._trigger}')
            raise
    #-------------------------------
    def _get_sigpath(self):
        if self._sigpath is not None: 
            return self._sigpath

        dat_dir  = os.environ['DATDIR']
        inputdir = f'{dat_dir}/data_{self._chan}/{self._dat_ver}' 
        sigpath  = f'{inputdir}/sweights_{self.swt_ver}/{self._year}_dt_trigger_weights_sweighted.root'

        return sigpath
    #-------------------------------
    def _get_treename(self):
        if   self._trigger == 'TRG':
            return 'TRG'
        elif self._trigger in ['MTOS', 'GTIS_mm']:
            return 'KMM'
        elif self._trigger in ['ETOS', 'GTIS_ee', 'GTIS']:
            return 'KEE'
        else:
            self.log.error(f'Invalid trigger: {self._trigger}')
            raise
    #-------------------------------
    def _get_info_df(self):
        df = pnd.DataFrame(columns=['Setting', 'Value'])

        utnr.add_row_to_df(df, ["Data"      ,  self._sigpath])
        utnr.add_row_to_df(df, ["Simulation",  self._simpath])
        utnr.add_row_to_df(df, ["Weight"    ,   self._weight])
        utnr.add_row_to_df(df, ["Tree"      , self._treename])
        utnr.add_row_to_df(df, ["xVar "     , self._l_var[0]])
        utnr.add_row_to_df(df, ["yVar "     , self._l_var[1]])
        utnr.add_row_to_df(df, ["zVar "     , self._l_var[2]])

        return df
    #-------------------------------
    def _save_reweighter(self, reweighter):
        pickle_path = f'{self._val_dir}.pickle'
        self.log.visible(f'Saving {pickle_path}')
        utnr.dump_pickle(reweighter, pickle_path)

        info_path  = f'{self._val_dir}/info.csv'
        self.log.visible(f'Saving {info_path}')
        self._df_info.to_csv(info_path, index=False)
    #-------------------------------
    def _get_df(self):
        df_sig=ROOT.RDataFrame(self._treename, self._sigpath)
        df_sim=ROOT.RDataFrame(self._treename, self._simpath)

        if self.maxentries > 0:
            df_sig = df_sig.Range(self.maxentries)
            df_sim = df_sim.Range(self.maxentries)

            self.log.info(f'Limiting datasets sizes to: {self.maxentries}')
        #-----------------
        df_sig=df_sig.Define('weight', self._weight)
        df_sim=df_sim.Define('wgt_01', self._weight)

        if self._preffix == 'rec':
            self.log.info(f'Adding calibration weights before calculating {self._preffix} maps')
            df_sim=self._add_calib(df_sim)
        else:
            self.log.info(f'Not using calibration weights for {self._preffix} maps')
            df_sim=df_sim.Define('weight', 'wgt_01')

        return (df_sig, df_sim)
    #-------------------------------
    def _add_calib(self, df):
        df.filepath = self._simpath
        df.treename = self._treename
        df.year     = self._year

        arr_gen_wgt = self._get_gen_wgt(df)

        arr_wgt_01  = df.AsNumpy(['wgt_01'])['wgt_01']

        arr_wgt = arr_wgt_01 * arr_gen_wgt

        df = utils.add_df_column(df, arr_wgt, 'weight')

        return df
    #-------------------------------
    def _get_gen_wgt(self, df):
        weight_reader.replica = 0
        weight_reader.log.setLevel(logging.WARNING)

        wrd        = weight_reader(df, 'rec')
        wrd.valdir = self._val_dir
        wrd['bts'] = ('001'              , 'nom')
        wrd['gen'] = (f'v{self._version}', 'nom')
        d_wgt      = wrd.get_weights()
        arr_wgt    = d_wgt['nom']

        return arr_wgt
    #-------------------------------
    def save_reweighter(self, nreplica=0):
        self._initialize()
        #-----------------
        df_sig, df_sim = self._get_df()

        self.log.info('Extracting data')
        arr_sig_val=utils.getMatrix(df_sig, self._l_var)
        arr_sig_wgt=df_sig.AsNumpy(["weight"])['weight']
        nentries = len(arr_sig_val)
        self.log.info(f'Found {nentries} entries')

        self.log.info('Extracting simulation')
        arr_sim_val=utils.getMatrix(df_sim, self._l_var)
        arr_sim_wgt=df_sim.AsNumpy(["weight"])['weight']
        nentries   =len(arr_sim_val)
        self.log.info(f'Found {nentries} entries')
        #-------------------------

        utnr.add_row_to_df(self._df_info, ['X binning'       , self._arr_x])
        utnr.add_row_to_df(self._df_info, ['Y binning'       , self._arr_y])
        utnr.add_row_to_df(self._df_info, ['Z binning'       , self._arr_z])

        utnr.add_row_to_df(self._df_info, ['Num weight (Sim)', arr_sim_val.size ])
        utnr.add_row_to_df(self._df_info, ['Sum weight (Sim)', arr_sim_val.sum()])
        utnr.add_row_to_df(self._df_info, ['Num weight (Dat)', arr_sig_val.size ])
        utnr.add_row_to_df(self._df_info, ['Sum weight (Dat)', arr_sig_val.sum()])
        #-------------------------
        self.log.info("Reweighting")

        #reweighter = hep_gb.BDT(arr_sim_val, arr_sig_val, arr_sim_wgt=arr_sim_wgt, arr_dat_wgt=arr_sig_wgt)
        #reweighter.fit()

        reweighter = hep_cl.HIS(arr_sim_val, arr_sig_val, arr_original_weight=arr_sim_wgt, arr_target_weight=arr_sig_wgt)
        reweighter.arr_bin_x   = self._arr_x
        reweighter.arr_bin_y   = self._arr_y
        reweighter.arr_bin_z   = self._arr_z

        self._save_reweighter(reweighter)
#----------------------------------------

