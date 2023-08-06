from collections import UserDict

from rk.differential_efficiency import defficiency
from rk.efficiency              import  efficiency
from ndict                      import       ndict

import utils_noroot as utnr
import pandas       as pnd
#-----------------------------------------
class cutflow(UserDict):
    log=utnr.getLogger('cutflow')
    #-------------------------------
    def __init__(self):
        self._tot_eff     = 1. 
        self._ful_eff     = None

        self._df_stat     = None
        self._df_cuts     = None

        self._initialized = False

        super().__init__()
    #-------------------------------
    def __setitem__(self, cut, obj):
        if not isinstance(obj, (efficiency, defficiency)):
            self.log.error(f'Value has to be efficiency or differential efficiency, found: {type(eff)}')
            raise

        self.data[cut] = obj

        if self._ful_eff is None:
            self._ful_eff  = obj.copy()
        else:
            self._ful_eff  = self._ful_eff * obj
    #-------------------------------
    def _initialize(self):
        if self._initialized:
            return

        d_cuts = {}
        d_stat = {}
        for label, obj in self.data.items():
            if isinstance(obj, defficiency):
                eff = obj.efficiency() 
            else:
                eff = obj

            eff_val, _, _ = eff.val
            self._tot_eff*= eff_val
            d_cuts[label] = eff.cut

            utnr.add_to_dic_lst(d_stat, 'Total'     , eff.fal + eff.pas)
            utnr.add_to_dic_lst(d_stat, 'Pased'     ,           eff.pas)
            utnr.add_to_dic_lst(d_stat, 'Efficiency',           eff_val)
            utnr.add_to_dic_lst(d_stat, 'Cumulative',     self._tot_eff)
            utnr.add_to_dic_lst(d_stat, 'Cut'       ,             label)

        self._df_stat=pnd.DataFrame(d_stat, columns=['Cut', 'Total', 'Pased', 'Efficiency', 'Cumulative'])
        self._df_stat=self._df_stat.set_index('Cut')

        self._df_cuts=pnd.DataFrame(d_cuts, index=['Cut'])
        self._df_cuts=self._df_cuts.T

        self._initialized = True
    #-------------------------------
    @property
    def df_eff(self):
        self._initialize()

        return self._df_stat
    #-------------------------------
    @property
    def df_cut(self):
        self._initialize()

        return self._df_cuts
    #-------------------------------
    @property
    def tot_eff(self):
        '''
        Returns numerical value of total efficiency
        '''
        self._initialize()

        return self._tot_eff
    #-------------------------------
    @property
    def efficiency(self):
        '''
        Returns efficiency object, product of all efficiencies
        '''
        self._initialize()

        return self._ful_eff
    #-------------------------------
    def __str__(self):
        self._initialize()

        msg= f'_____\n{"Kind":<20}{"Passed":>10} [{"Entries":>10}] / {"Total":>10} [{"Entries":>10}] = {"Eff":<9} | {"Cut":<40}{"Label":<20}\n \n'
        for kind, obj in self.items():
            if isinstance(obj, defficiency):
                eff = obj.efficiency()
            else:
                eff = obj

            eff_str = eff.__str__()

            msg += f'{kind:<20}{eff_str:<50}\n'

        msg += '-----\n'

        return msg
    #-------------------------------
    def __add__(self, other):
        self._initialize()

        if self.keys() != other.keys():
            self.log.error(f'Cannot add cutflows with different cuts:')
            print(self.df_eff)
            print(other.df_eff)
            raise

        res_cfl = cutflow()

        for key in other:
            other_eff = other[key]
            this_eff  =  self[key]

            eff = other_eff + this_eff

            res_cfl[key] = eff

        return res_cfl
#-----------------------------------------
class cutflow_manager():
    '''
    Class used to build cutflow objects. It takes care of switching between efficiencies, depending on the systematics
    '''
    log=utnr.getLogger('cutflow_manager')
    #----------------------------------
    def __init__(self):
        self._d_d_eff   = {}
        self._s_sys     = set()
        self._l_cut     = []
        self._has_dif   = False
        self._s_dif_var = None
    #----------------------------------
    def _check_nominal(self, d_eff, kind):
        '''
        Check if dictionary contains nominal efficiency
        '''
        if   isinstance(d_eff,  dict)                 and 'nom' not in d_eff:
            self.log.error(f'Nominal efficiency not found for: {kind}')
            print(d_eff.keys())
            raise
        elif isinstance(d_eff, ndict) and not d_eff.has_val('nom', axis='x'):
            self.log.error(f'Nominal efficiency not found for: {kind}')
            print(d_eff)
            raise
    #----------------------------------
    def __setitem__(self, cut, d_eff):
        self._check_nominal(d_eff, cut)
        self._check_sys_lab(d_eff, cut)

        if cut in self._l_cut:
            self.log.error(f'Kind {cut} already added')
            raise
        else:
            self._l_cut.append(cut)

        if   isinstance(d_eff, ndict) and not self._has_dif:
            self._has_dif   = True
            self._s_dif_var = d_eff.y_axis
            self._s_sys     = d_eff.x_axis.union(self._s_sys)
        elif isinstance(d_eff,  dict): 
            self._s_sys= set(d_eff.keys()).union(self._s_sys)
        elif isinstance(d_eff, ndict) and     self._has_dif:
            self.log.error(f'Cannot pass multiple differential efficiencies')
            raise
        else:
            self.log.error(f'Argument is neither dict nor ndict, but: {type(d_eff)}')
            raise

        self._d_d_eff[cut] = d_eff
    #----------------------------------
    def _pad_eff_int(self, d_eff):
        '''
        Takes {sys:eff}, pads with nominal missing sistematics
        '''
        eff_nom = d_eff['nom']

        for sys in self._s_sys:
            if sys in d_eff:
                continue

            d_eff[sys] = eff_nom.copy(label=sys)

        return d_eff
    #----------------------------------
    def _pad_eff_dif(self, d_eff):
        for var in d_eff.y_axis:
            nom_eff = d_eff['nom', var]
            for sys in self._s_sys:
                if (sys, var) not in d_eff:
                    d_eff[sys, var] = nom_eff.copy(label=sys, varname=var)

        return d_eff
    #----------------------------------
    def _pad_all(self):
        '''
        Will pad with nominal (cut, syst) locations for systematics that do not make sense for given cut.
        '''
        d_d_eff = {}
        for cut, d_eff in self._d_d_eff.items():
            if   isinstance(d_eff,  dict):
                d_d_eff[cut] = self._pad_eff_int(d_eff)
            elif isinstance(d_eff, ndict):
                d_d_eff[cut] = self._pad_eff_dif(d_eff)
            else:
                self.log.error(f'Object is not a dict or ndict, but: {type(d_eff)}')
                raise

        return d_d_eff
    #----------------------------------
    def _check_sys_lab(self, d_eff, cut):
        for key, eff in d_eff.items():
            try:
                sys, var = key
            except:
                sys      = key

            if sys != eff.label:
                self.log.error(f'For cut {cut} systematic and efficiency label dissagree: {sys}/{eff.label}')
                print(eff)
                raise
    #----------------------------------
    def _get_cf_int(self, sys, d_d_eff_pad):
        '''
        Takes sys string and {cut : {sys : eff...}...} and for given systematic returns cutflow object
        '''
        cf = cutflow()
        for cut in self._l_cut:
            d_eff   = d_d_eff_pad[cut]
            eff     = d_eff[sys]
            cf[cut] = eff

        return cf
    #----------------------------------
    def _get_cf_dif(self, sys, var, d_d_eff_pad):
        '''
        Takes sys, var strings and {cut : {sys[,var] : [d]eff...}...}, 
        i.e. inner dict (with sys -> eff) or ndict (with sys, var -> deff)

        Returns cutflow for given sys, var combination.
        '''
        cf = cutflow()
        for cut in self._l_cut:
            d_eff   = d_d_eff_pad[cut]
            if   isinstance(d_eff , dict):
                eff = d_eff[sys]
            elif isinstance(d_eff, ndict):
                eff = d_eff[sys, var]

            cf[cut] = eff

        return cf
    #----------------------------------
    def get_cf(self):
        '''
        Returns either {sys : cutflow} dict or {sys, var : cutflow} ndict

        Latter is returned if one of the efficiencies is differential
        '''
        d_d_eff_pad = self._pad_all()

        d_cf = ndict() if self._has_dif else {}

        self.log.info('Creating cutflows:')
        for sys in self._s_sys:
            self.log.info(sys)
            if not self._has_dif:
                d_cf[sys]          = self._get_cf_int(sys,      d_d_eff_pad)
            else:
                for var in self._s_dif_var:
                    d_cf[sys, var] = self._get_cf_dif(sys, var, d_d_eff_pad)

        return d_cf 
#----------------------------------

