import utils_noroot      as utnr
import matplotlib.pyplot as plt

import ROOT
import math
import utils 
import numpy
import os 
import logging 
import read_selection as rs
import rk.selection   as rksl
import pandas         as pnd

from rk.truth_eff          import get_eff           as get_truth_eff
from rk.calc_utility       import getGeomEff        as get_geo_eff
from atr_mgr               import mgr               as amgr
from rk.q2smear            import q2smear           as q2
from rk.mva                import mva_man

#-----------------------------------------
class InconsistentEff(Exception):
    log=utnr.getLogger('InconsistentEff')
    def __init__(self, eff_1, eff_2):
        self.message = 'Inconsistent efficiencies' 
        super().__init__(self.message)
        self.log.error(f'{eff_1._npas} != {eff_2._npas} + {eff_2._nfal}')
        print(eff_1)
        print(eff_2)
#-----------------------------------------
class DifferentLabel(Exception):
    log=utnr.getLogger('DifferentLabel')
    def __init__(self, eff_1, eff_2):
        self.message = 'Different labels' 
        super().__init__(self.message)
        self.log.error(f'{eff_1.label} != {eff_2.label}')
#-----------------------------------------
class efficiency:
    log=utnr.getLogger('efficiency')
    """
    Class meant to represent efficiencies
    """
    def __init__(self, arg_pas, arg_fal=None, arg_tot=None, err_pas=0, err_fal=0, cut='no-cut', lab='none'):
        '''
        arg_pas: int, tuple, ndarray
        arg_fal: int, tuple, ndarray
        arg_tot: int, tuple, ndarray

        tuple = (yield, frequency)
        '''
        pas, fal, npas, nfal = self._get_yields(arg_pas, arg_fal=arg_fal, arg_tot=arg_tot)

        self.log.debug(f'pas: {pas}')
        self.log.debug(f'fal: {fal}')

        if pas + fal == 0:
            self.log.error('Both passed and failed yields are zero')
            raise

        if pas == 0:
            self.log.debug('Passed yield is zero')

        self._pas  = pas
        self._fal  = fal
        self._npas = npas
        self._nfal = nfal

        self._cut = cut
        self._lab = lab
        self._lvl = 0.682689

        self._epsilon = 1e-7
        self._err_pas = err_pas
        self._err_fal = err_fal
    #------------------------------------
    def _get_yields(self, arg_pas, arg_fal=None, arg_tot=None):
        if   isinstance(arg_pas, int) and isinstance(arg_fal, int):
            self.log.debug('pas/fal args')

            pas  = arg_pas
            fal  = arg_fal

            npas = pas
            nfal = fal
        elif isinstance(arg_pas, int) and isinstance(arg_tot, int):
            self.log.debug('pas/tot args')
            pas  = arg_pas
            fal  = arg_tot - arg_pas

            npas = pas
            nfal = fal 
        elif isinstance(arg_pas,         tuple) and isinstance(arg_fal,         tuple):
            self.log.debug('tup_pas/tup_fal args')
            pas, npas = arg_pas
            fal, nfal = arg_fal
        elif isinstance(arg_pas,         tuple) and isinstance(arg_tot,         tuple):
            self.log.debug('tup_pas/tup_tot args')
            pas, npas = arg_pas
            tot, ntot = arg_tot

            fal       = tot  - pas
            nfal      = ntot - npas
        elif isinstance(arg_pas, numpy.ndarray) and isinstance(arg_fal, numpy.ndarray):
            self.log.debug('arr_pas/arr_fal args')
            pas  = numpy.sum(arg_pas) 
            fal  = numpy.sum(arg_fal)

            npas = len(arg_pas) 
            nfal = self._get_nfal(arg_fal) 
        elif isinstance(arg_pas, numpy.ndarray) and isinstance(arg_tot, numpy.ndarray):
            self.log.debug('arr_pas/arr_tot args')
            pas  = numpy.sum(arg_pas) 
            fal  = numpy.sum(arg_tot) - pas 

            npas = len(arg_pas) 
            nfal = len(arg_tot) - npas 
        else:
            self.log.error(f'Pass and fail arguments are neither integers nor arrays')
            print(arg_pas)
            print(arg_fal)
            raise

        return (pas, fal, npas, nfal)
    #------------------------------------
    def _get_nfal(self, arr_fal):
        nfal = len(arr_fal)
        if nfal == 0:
            return nfal

        #Needed if a cut has an above 1 efficiency, i.e.: 
        #negative failed yield == negative number of failed events
        if numpy.all(arr_fal == arr_fal[0]) and numpy.all(arr_fal < 0):
            nfal = -nfal

        return nfal
    #------------------------------------
    def __lt__(self, other):
        this_tot  = self._pas  + self._fal
        other_tot = other._pas + other._fal

        if this_tot == other_tot:
            return self._pas < other._pas

        return this_tot < other_tot
    #------------------------------------
    @property
    def npas(self):
        return self._npas
    #------------------------------------
    @property
    def nfal(self):
        return self._nfal
    #------------------------------------
    @property
    def pas(self):
        return self._pas
    #------------------------------------
    @property
    def fal(self):
        return self._fal
    #------------------------------------
    @property
    def cut(self):
        return self._cut
    #------------------------------------
    @property
    def label(self):
        return self._lab
    #------------------------------------
    @label.setter
    def label(self, label):
        self._lab = label
    #------------------------------------
    @property
    def val(self):
        '''
        Returns tuple (efficiency, error_up, error_down)
        '''

        if self._err_pas == 0 and self._err_fal == 0:
            val = self._get_val_noerror()
        else:
            self.log.error('Efficiency with error not implemented')
            raise

        return val
    #------------------------------------
    def copy(self, label=None, cut=None):
        label = self._lab if label is None else label
        cut   = self._cut if cut   is None else cut

        return efficiency((self._pas, self._npas), arg_fal = (self._fal, self._nfal), cut=cut, lab=label)
    #------------------------------------
    def _check_precision(self, eff, err_dn, err_up):
        prec_dn = 100 * err_dn/eff if eff > 0 else -1
        prec_up = 100 * err_up/eff if eff > 0 else -1

        if prec_dn > 10 or prec_dn < 0:
            self.log.debug(f'Precision for error down is {prec_dn:.3e}% of efficiency {eff:.3e}')
            self.log.debug(f'Eff central:{eff:.3e}   ')
            self.log.debug(f'Eff down:   {err_dn:.3e}')

        if prec_up > 10 or prec_dn < 0:
            self.log.debug(f'Precision for error down is {prec_up:.3e}% of efficiency {eff:.3e}')
            self.log.debug(f'Eff central:{eff:.3e}   ')
            self.log.debug(f'Eff up:     {err_up:.3e}')
    #------------------------------------
    def _get_val_noerror(self):
        pas = float(self._pas)
        fal = float(self._fal)

        total  = pas + fal
        eff_cn = pas / total 

        if eff_cn > 1:
            return (eff_cn, 0, 0)

        eff_up = ROOT.TEfficiency.ClopperPearson(total, pas, self._lvl,  True)
        eff_dn = ROOT.TEfficiency.ClopperPearson(total, pas, self._lvl, False)

        err_up = eff_up - eff_cn
        err_dn = eff_cn - eff_dn

        self._check_precision(eff_cn, err_dn, err_up)

        return (eff_cn, err_dn, err_up)
    #------------------------------------
    def show(self):
        eff_cn, err_dn, err_up = self.val

        self.log.info('------------------------------------------------')
        self.log.info('{0:<20}{1:<20}'.format('Cut'       , self.cut ))
        self.log.info('{0:<20}{1:<20}'.format('Pased'     , self._pas))
        self.log.info('{0:<20}{1:<20}'.format('Failed'    , self._fal))
        self.log.info('{0:<20}{1:<20}'.format('Total'     , self._pas + self._fal))
        self.log.info('------------------------------------------------')
        self.log.info('{0:<20}{1:<20}   '.format('Cut'       , self.cut))
        self.log.info('{0:<20}{1:<20.3e}'.format('Efficiency', eff_cn  ))
        self.log.info('{0:<20}{1:<20.3e}'.format('Error Up'  , err_up  ))
        self.log.info('{0:<20}{1:<20.3e}'.format('Error Down', err_dn  ))
        self.log.info('------------------------------------------------')
    #------------------------------------
    def __add__(self, other):
        """
        Takes efficiency object and returns efficiency object
        resulting from combining corresponding sample, with current
        object's sample
        """
        if not isinstance(other, efficiency):
            return NotImplemented


        if (other.cut != self.cut) or (other.label != self.label):
            self.log.error('Cannot add cuts/labels, cut strings differ:')
            self.log.error(f'This :  {self.cut}/{self.label}')
            self.log.error(f'Other: {other.cut}/{other.label}')
            raise
        else:
            cut = self.cut
            lab = self.label

        pas  = other._pas  + self._pas
        fal  = other._fal  + self._fal
        tot  =        pas  +       fal 

        npas = other._npas + self._npas
        nfal = other._nfal + self._nfal
        ntot =        npas +       nfal 

        err_pas   = math.sqrt(other._err_pas ** 2 + self._err_pas ** 2)
        err_fal   = math.sqrt(other._err_fal ** 2 + self._err_fal ** 2)

        tp_pas    = (pas, npas)
        tp_tot    = (tot, ntot)
        obj       = efficiency(tp_pas, arg_tot=tp_tot, err_pas=err_pas, err_fal=err_fal, cut=cut, lab=lab)

        return obj
    #------------------------------------
    def __mul__(self, other):
        """
        Returns product of efficiency objects, current object and argument object
        """
        if not isinstance(other, efficiency):
            return NotImplemented

        is_consistent = self._npas == other._npas + other._nfal
        same_label    = self.label == other.label

        if is_consistent == False:
            raise InconsistentEff(self, other)

        if same_label == False:
            raise DifferentLabel(self, other)

        err_fal   = math.sqrt(other._err_fal ** 2 + self._err_fal ** 2)
        cut       = f'({self.cut}) && ({other.cut})'
        lab       = self.label

        tp_pas    = (           other._pas,             other._npas)
        tp_tot    = (self._pas + self._fal, self._npas + self._nfal)
        obj       = efficiency(tp_pas, arg_tot = tp_tot, err_pas = other._err_pas, err_fal = err_fal, cut = cut, lab=lab) 

        return obj
    #------------------------------------
    def __truediv__(self, other):
        '''
        Takes numerical value of efficiency, returns ratio of this efficiency by other efficiency
        '''
        if not isinstance(other, float):
            return NotImplemented

        eff_this , _, _ =  self.val 
        eff_other, _, _ = other.val 

        if eff_other == 0:
            self.log.error(f'Denominator efficiency is zero')
            raise

        return eff_this / eff_other
    #------------------------------------
    def __eq__(self, other):
        if not isinstance(other, efficiency):
            return NotImplemented

        equal_yields = math.isclose(self._pas, other._pas, rel_tol=self._epsilon) and math.isclose(self._fal, other._fal, rel_tol=self._epsilon)
        equal_stats  = (self._npas == other._npas) and (self._nfal == other._nfal)
        equal_cuts   =  self.cut == other.cut

        return equal_yields and equal_cuts and equal_stats
    #------------------------------------
    def __str__(self):
        obj  = self 
        tot  = obj._pas  + obj._fal
        ntot = obj._npas + obj._nfal

        eff = obj._pas / tot
        line = f'{obj._pas:10.0f} [{obj._npas:>10}] / {tot:10.0f} [{ntot:>10}] = {eff:<.3e} | {obj._cut:<40}{obj._lab:<20}'

        return line
    #------------------------------------
    def scale(self, scl):
        if self._npas == 0:
            arr_pas = numpy.array([])
        else:
            pas = scl * self._pas / self._npas
            arr_pas = numpy.array([pas] * self._npas)

        if   self._nfal == 0:
            arr_fal = numpy.array([])

            return efficiency(arr_pas, arg_fal=arr_fal, cut=self._cut)
        elif self._nfal <  0:
            nfal    = - self._nfal
            fal     = scl * self._fal / nfal

            arr_fal = numpy.array([fal] * nfal)

            return efficiency(arr_pas, arg_fal=arr_fal, cut=self._cut)
        else:
            fal     = scl * self._fal / self._nfal
            arr_fal = numpy.array([fal] * self._nfal)

            return efficiency(arr_pas, arg_fal=arr_fal, cut=self._cut)
#-----------------------------------------
def transform_cflow(icflow):
    """  
    Transforms CutFlowReport object in c++ to cutflow object, python class.
    Useful to get pandas dataframe.
    """
    ocflow = cutflow()
    for cut in icflow:
        tot = cut.GetAll()
        pas = cut.GetPass()
        lab = cut.GetName()
        try:
            cut = cut.GetCut()
        except:
            cut = 'none'
            log.info('Converting ROOT cutflow object, cut == "none"')

        ocflow[lab] = efficiency(pas, tot, cut=cut)

    return ocflow
#-----------------------------------------

