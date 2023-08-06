from rk.weight_reader import weight_reader

import os
import utils
import utils_noroot     as utnr
import read_selection   as rs

from atr_mgr import mgr as amgr

#-------------------------------
class data_filter:
    log=utnr.getLogger('data_filter')
    #-------------------------------
    def __init__(self, df):
        self._am            = amgr(df)
        self._df            = df
        self._val_dir       = None
        self._d_dilepton_id = {'jpsi' : '443', 'psi2' : '100443'}

        weight_reader.replica = 0
        weight_reader.kin_dir = os.environ['CALDIR'] 

        self._initialized   = False
    #-------------------------------
    def _get_df_attr(self, name):
        try:
            attr = getattr(self._df, name)
        except:
            self.log.error(f'Cannot find {name} attached to dataframe')
            raise

        return attr
    #-------------------------------
    def _initialize(self):
        if self._initialized:
            return

        trig = self._get_df_attr('treename')
        proc = self._get_df_attr('proc')
        year = self._get_df_attr('year')

        q2_sel = rs.get('q2', trig, q2bin=proc, year = year)

        dilepton_id = utnr.get_from_dic(self._d_dilepton_id, proc)

        df = self._df
        df = self._define_df(df, 'B_TRUEP_X', 'B_PX')
        df = self._define_df(df, 'B_TRUEP_Y', 'B_PY')
        df = self._define_df(df, 'B_TRUEP_Z', 'B_PZ')
        df = self._define_df(df, 'B_TRUEPT' , 'B_PT')
        df = self._define_df(df, 'B_TRUEID' , '521' )
        df = self._define_df(df, 'Jpsi_TRUEID', dilepton_id)

        df = df.Filter(q2_sel)

        self._df = self._am.add_atr(df)

        self._initialized = True
    #----------------------------
    def _define_df(self, df, org, trg):
        #In case we run over MC and therefore the variable already exists
        l_column = df.GetColumnNames()
        if org in l_column:
            return df

        df = df.Define(org, trg)

        return df
    #----------------------------
    @property
    def val_dir(self):
        return self._val_dir

    @val_dir.setter
    def val_dir(self, value):
        try:
            self._val_dir = utnr.make_dir_path(value)
        except:
            self.log.error(f'Cannot make directory: {value}')
            raise

        self.log.info(f'Sending plots to: {value}')
    #----------------------------
    def _get_ver_dc(self):
        d_ver               = {}
        d_ver['GVER']       ='v9'
        d_ver['EVER']       ='v1'
        d_ver['RVER']       ='v9'
        d_ver['TVER']       ='v11'
        d_ver['PVER']       ='v1'
        d_ver['QVER']       ='v1'
    
        return d_ver
    #----------------------------
    def _get_flags(self):
        d_ver = self._get_ver_dc()
        gver  = d_ver['GVER'] 
        rver  = d_ver['RVER'] 
        tver  = d_ver['TVER'] 
        tver  = d_ver['TVER'] 
        pver  = d_ver['PVER'] 
        qver  = d_ver['QVER'] 
        ever  = d_ver['EVER'] 
    
        wgt          = weight_reader(self._df)
        wgt.valdir   = self._val_dir 
        wgt['gen']   = (gver, '1')
        wgt['rec']   = (rver, '1')
        wgt['lzr']   = (tver, '1')
        wgt['hlt']   = (tver, '1')
        wgt['pid']   = (pver, '1')
        wgt['trk']   = (ever, '1')
        wgt['qsq']   = (None, '0')
    
        arr_flg = wgt.get_weights(return_type='product')
    
        return arr_flg
    #----------------------------
    def filter(self):
        self._initialize()
    
        arr_wgt = self._get_flags() 
        size_df = self._df.Count().GetValue()
        size_ar = arr_wgt.size
    
        if size_df != size_ar:
            self.log.error(f'Dataframe and array of weights sizes differ: {size_df}/{size_ar}')
            raise
    
        self._df = utils.add_df_column(self._df, arr_wgt, 'wgt_filt')
    
        self._df = self._df.Filter('wgt_filt > 0', 'Map filter')
    
        rp = self._df.Report()
        rp.Print()
    
        return self._df
#----------------------------
def filter_zeros(df, val_dir):
    obj = data_filter(df)
    obj.val_dir = val_dir
    df  = obj.filter()

    return df
#----------------------------

