import ROOT

import os
import json
import numpy
import numexpr

import utils
import utils_noroot as utnr

from rk.collector import collector
#-------------------------
class q2smear:
    log=utnr.getLogger(__name__)
    #-------------------------
    def __init__(self, df, q2dir):
        self._df          = df 
        self.q2dir        = q2dir
        self.storage      = collector() 
        self.jpsi_mass    = 'Jpsi_M'
        self.jpsi_pdg     = 3096.9
        self.arr_wgt      = None
        self.maxprint     = 0

        self._df_size     = None
        self._year        = None
        self._treename    = None
        self._initialized = False
        self._nprinted    = 0
    #-------------------------
    def __initialize(self):
        if self._initialized:
            return

        self._check_df()

        self._treename = utnr.get_attr(self._df, 'treename')

        utnr.check_dir(self.q2dir)

        for var_name in ['yearLabbel', self.jpsi_mass, 'L1_P', 'L2_P']:
            self.__check_var(var_name)

        if 'nbrem' not in self._df.GetColumnNames():
            self.__check_var('L1_BremMultiplicity')
            self.__check_var('L2_BremMultiplicity')
            self._df = self._df.Define('nbrem', 'L1_BremMultiplicity + L2_BremMultiplicity >= 2 ? 2 : int(L1_BremMultiplicity + L2_BremMultiplicity)')

        arr_year =self._df.AsNumpy(['yearLabbel'])['yearLabbel']
        self._year=int(arr_year[0])

        if self.storage is None:
            self._initialized = True
            return

        self.storage.add('q2smr_treename', self._treename)

        self.__load_pars()

        self._initialized = True
    #-------------------------
    def _check_df(self):
        try:
            df_size = self._df.Count().GetValue()
        except:
            self.log.error('Cannot get size from dataframe')
            print(self._df)
            raise

        if df_size <= 0:
            self.log.error(f'Invalid dataframe size: {df_size}')
            raise

        self._df_size = df_size
    #-------------------------
    def __check_keys(self):
        for var in ['mu_MC', 'delta_m', 's_sigma']:
            for gamma in [0, 1, 2]:
                key=f'{self._treename} {var} {gamma} gamma'
                if key not in self.__d_smear:
                    self.log.error(f'key {key} not found in {self._filepath}')
                    raise
    #-------------------------
    def _check_size(self, obj, kind):
        if   isinstance(obj, numpy.ndarray):
            obj_size = len(obj)
        elif isinstance(obj, utils.get_df_types() ):
            obj_size = obj.Count().GetValue()
        else:
            self.log.error(f'Invalid object type')
            print(obj)
            raise

        if obj_size != self._df_size:
            self.log.error(f'Dataframe size {self._df_size} and object size {obj_size}, differ for {kind}')
            raise
    #-------------------------
    def __check_var(self, var_name):
        l_var_name = self._df.GetColumnNames()
        if var_name not in l_var_name:
            self.log.error(f'Cannot retrieve {var_name} from dataframe')
            raise
    #-------------------------
    def __get_par(self, key, arr_ind):
        k0 = key.format(self._treename, 0)
        k1 = key.format(self._treename, 1)
        k2 = key.format(self._treename, 2)

        v0 = self.__d_smear[k0]
        v1 = self.__d_smear[k1]
        v2 = self.__d_smear[k2]

        arr_val = numpy.array([v0, v1, v2])

        arr_par = arr_val[arr_ind]

        if   arr_par.ndim == 1:
            return arr_par
        elif arr_par.ndim == 2:
            arr_val = arr_par[:,0:1]
            return arr_val.flatten()
        else:
            self.log.error(f'Array "{key}" has the wrong dimension:')
            print(arr_par)
            raise
    #-------------------------
    def _push_to_map(self, hist, val, axis):
        if val < 0:
            self.log.error(f'Found negative value of lepton momentum')
            raise

        if   axis == 'x':
            axe = hist.GetXaxis()
        elif axis == 'y': 
            axe = hist.GetYaxis()
        else:
            self.log.error(f'Invalid axis: {axis}')
            raise

        val_max = axe.GetXmax()
        
        if val < val_max:
            return val

        return val_max - 1
    #-------------------------
    def _get_sigma(self, arr_nbrem, arr_p1, arr_p2):
        if not self.q2dir.endswith('.mom'):
            arr_s_sigma = self.__get_par('{} s_sigma {} gamma', arr_nbrem)

            return arr_s_sigma

        root_path = f'{self.q2dir}/{self._year}_{self._treename}.root'

        self.log.info(f'Picking up momentum dependent ratio of resolutions from: {root_path}')

        ifile=ROOT.TFile(root_path)
        d_hist    = {}
        d_hist[0] = ifile.h_par_brem_0
        d_hist[1] = ifile.h_par_brem_1
        d_hist[2] = ifile.h_par_brem_2

        l_rat = []
        for nbrem, p1, p2 in zip(arr_nbrem, arr_p1, arr_p2):
            hist = d_hist[nbrem]

            p1   = self._push_to_map(hist, p1, 'x')
            p2   = self._push_to_map(hist, p2, 'y')

            ibin = hist.FindBin(p1, p2)
            rat  = hist.GetBinContent(ibin)

            l_rat.append(rat)

        ifile.Close()

        arr_rat = numpy.array(l_rat) 

        return arr_rat
    #-------------------------
    def __smear(self, arr_nbrem, arr_jpsi_m_reco, arr_p1, arr_p2):
        arr_s_sigma = self._get_sigma(arr_nbrem, arr_p1, arr_p2)
        arr_dmu     = self.__get_par('{} delta_m {} gamma', arr_nbrem)
        arr_mu_MC   = self.__get_par('{} mu_MC {} gamma'  , arr_nbrem)
        
        jpsi_m_true = self.jpsi_pdg

        arr_jpsi_smear = jpsi_m_true + arr_s_sigma * (arr_jpsi_m_reco - jpsi_m_true) + arr_dmu + (1 - arr_s_sigma) * (arr_mu_MC - self.jpsi_pdg)

        if self._nprinted < self.maxprint:
            self._nprinted += 1
            self.log.info('{} = {} + {} * ({} - {}) + {} + (1 - {}) * ({} - {})'.format(jpsi_smear, jpsi_m_true, s_sigma, jpsi_m_reco, jpsi_m_true, dmu, s_sigma, mu_MC, self.jpsi_pdg) )

        return arr_jpsi_smear
    #-------------------------
    def __load_pars(self):
        if self.q2dir.endswith('.mom'):
            q2dir = self.q2dir[:-3] + 'nom'
        else:
            q2dir = self.q2dir

        self._filepath=f'{q2dir}/{self._year}.json'

        self.storage.add_list('q2smr_path', self._filepath)

        utnr.check_file(self._filepath)
        self.__d_smear = utnr.load_json(self._filepath)

        self.__check_keys()

        self.log.info('----------------------------')
        self.log.info('{0:<20}{1:<20}'.format('q2 file'  , self._filepath))
        self.log.info('{0:<20}{1:<20}'.format('Tree name', self._treename))
        self.log.info('----------------------------')
    #-------------------------
    def get_q2_smear(self, replica=None):
        utnr.check_numeric(replica, [int])
        self.__initialize()

        d_data    = self._df.AsNumpy(['nbrem', self.jpsi_mass, 'L1_P', 'L2_P'])
        arr_nbrem = d_data['nbrem'].astype(int)
        arr_p1    = d_data['L1_P']
        arr_p2    = d_data['L2_P']
        arr_jpsim = d_data[self.jpsi_mass]

        self._check_size( self._df, 'DataFrame')
        self._check_size(arr_nbrem, 'Original J/psi mass')
        self._check_size(arr_nbrem, 'NBrem')

        arr_smear = self.__smear(arr_nbrem, arr_jpsim, arr_p1, arr_p2)

        self._check_size(arr_smear, 'Smeared J/Psi mass')

        return arr_smear 
    #-------------------------
    def get_weights(self, q2_sel, replica):
        self.__initialize()
        if self.arr_wgt is not None:
            return self.arr_wgt

        q2_sel  = q2_sel.replace('&&', '&')
        arr_smr = self.get_q2_smear(replica)

        self.arr_wgt = numexpr.evaluate(q2_sel, {'Jpsi_M' : arr_smr})

        return self.arr_wgt
#-------------------------

