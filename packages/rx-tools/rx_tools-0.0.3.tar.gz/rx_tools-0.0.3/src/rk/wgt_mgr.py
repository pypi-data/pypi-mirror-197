import utils
import utils_noroot   as utnr
import os

from rk.weight_reader import weight_reader
#----------------------------------------
class wgt_mgr:
    '''
    '''
    log=utnr.getLogger(__name__)
    #-----------------------------------
    def __init__(self, d_set):
        self._l_kind      = ['gen', 'rec', 'raw', 'sel']
        self._s_wgt       = {'gen', 'rec', 'lzr', 'hlt', 'pid', 'qsq', 'trk', 'bts'}
        self._d_set       = d_set

        self._d_wgt       = {} 
        self._val_dir     = None

        self._initialized = False
    #-----------------------------------
    def __str__(self):
        self._initialize()

        line = f'\n**********\n{"Kind":<10}{"Version":<10}{"Systematic":<10}\n**********\n'
        for kind, (vers, syst) in self._d_wgt.items():
            line += f'{kind:<10}{vers:<10}{syst:<10}\n'

        return line
    #-----------------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._set_kin_dir()
        weight_reader.replica = utnr.get_from_dic(self._d_set, 'replica')
        val_dir               = utnr.get_from_dic(self._d_set, 'val_dir')

        self._val_dir = utnr.make_dir_path(val_dir)

        for wgt in self._s_wgt:
            try:
                ver = utnr.get_from_dic(self._d_set, f'{wgt}_ver', no_error=True)
                sys = utnr.get_from_dic(self._d_set, f'{wgt}_sys', no_error=True)
            except:
                continue

            self._d_wgt[wgt] = (ver, sys)

        #PID and q2 are always applied as cuts (weight = 0/1) or taken from maps
        if 'qsq' not in self._d_wgt:
            self._d_wgt['qsq'] = (None, '000')

        if 'pid' not in self._d_wgt:
            self._d_wgt['pid'] = (None, '000')

        self._initialized = True
    #-----------------------------------
    def _set_kin_dir(self):
        try:
            cal_dir = os.environ['CALDIR']
        except:
            self.log.error('Cannot extract CALDIR variable from environment')
            raise

        utnr.check_dir(cal_dir)

        weight_reader.kin_dir = cal_dir
    #-----------------------------------
    def get_reader(self, kind, df):
        '''
        '''
        self._initialize()

        if kind in ['raw', 'sel'] and not hasattr(df, 'trigger'):
            self.log.error(f'Dataframe has to trigger attribute for reader of kind {kind}')
            raise

        if kind not in self._l_kind:
            self.log.error(f'Kind {kind} not valid, use:')
            utnr.pretty_print(self._l_kind)
            raise
        #----------------
        rdr           = weight_reader(df, kind)
        rdr.valdir    = f'{self._val_dir}/{kind}'
        #----------------
        s_wgt = set(self._s_wgt)

        rdr['bts'] = self._d_wgt['bts'] 
        s_wgt.remove('bts')

        if 'gen' in self._d_wgt:
            rdr['gen'] = self._d_wgt['gen'] 
            s_wgt.remove('gen')

        if kind in ['gen', 'rec']:
            return rdr 
        #----------------
        if 'rec' in self._d_wgt:
            rdr['rec'] = self._d_wgt['rec'] 
            s_wgt.remove('rec')

        if kind == 'raw':
            return rdr 
        #----------------
        for wgt in s_wgt:
            if wgt in self._d_wgt:
                rdr[wgt] = self._d_wgt[wgt] 
        #----------------
        return rdr
#----------------------------------------

