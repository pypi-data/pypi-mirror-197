import ROOT
import tqdm
import logging 
import sys

import utils
import utils_noroot as utnr

#----------------------------------------
class mcstudy:
    log=utnr.getLogger('mcstudy')
    #----------------------------------------
    def __init__(self, wks, obs_name=None, d_opt={}):
        self._wks      = wks
        self._obs_name = obs_name
        self._mod_name = 'model' 
        self._ful_mod  = None
        self._gen_mod  = None
        self._fit_mod  = None
        self._d_opt    = d_opt
        self._l_result = []
        self._ran      = ROOT.TRandom3(0)

        self._obs             = None
        self._mod             = None
        self._bin_thr         = None
        self._nbins           = None
        self._spread_scale    = 1
        self._max_smear_count = 100
        self._binned          = None

        self._initialized = False
    #----------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        utnr.check_type(self._wks     , ROOT.RooWorkspace)
        utnr.check_type(self._obs_name,               str) 
        utnr.check_type(self._d_opt   ,              dict) 

        self._obs = utils.check_wks_obj(self._wks, self._obs_name, 'var', retrieve=True)

        self._ful_mod = utils.check_wks_obj(self._wks, self._mod_name, 'pdf', retrieve=True)
        self._set_models()

        ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)

        #-------------------------------------------------------------------
        self._spread_scale = utnr.get_from_dic(self._d_opt, 'initial_spread_factor') 
        self._bin_thr      = utnr.get_from_dic(self._d_opt, 'binning_threshold') 
        self._nbins        = utnr.get_from_dic(self._d_opt, 'nbins') 

        self._initialzed = True
    #----------------------------------------
    def _set_models(self):
        if   self._ful_mod.InheritsFrom('RooProdPdf'):
            l_pdf = self._ful_mod.pdfList()

            self._gen_mod = l_pdf.at(0)
            self._fit_mod = self._ful_mod
        elif self._ful_mod.InheritsFrom('RooAddPdf'):
            self._gen_mod = self._ful_mod
            self._fit_mod = self._ful_mod
        else:
            self.log.error(f'Full model is not a RooAddPdf or RooProdPdf')
            raise

        self.log.info('-----------------')
        self.log.info('Generating model:')
        self._gen_mod.Print()
        self.log.info('')
        self.log.info('Fitting model:')
        self._fit_mod.Print()
        self.log.info('-----------------')
    #----------------------------------------
    def run(self, ndatasets=None):
        self._initialize()

        utnr.check_type(ndatasets, int)

        iterator = tqdm.trange(ndatasets, file=sys.stdout, ascii=' -') if self.log.level > logging.DEBUG else range(ndatasets)
        for i_dataset in iterator:
            res = self._run_dataset()

            name = f'res_{i_dataset:05d}'
            res.SetName(name)

            self._l_result.append(res)

        if self._binned:
            self.log.visible(f'Done toy study with {ndatasets} binned datasets')
        else:
            self.log.visible(f'Done toy study with {ndatasets} unbinned datasets')
    #----------------------------------------
    def _get_data(self):
        self._obs.setBins(self._nbins)
        data = self._gen_mod.generate(ROOT.RooArgSet(self._obs), ROOT.RooFit.Extended())

        nentries = data.numEntries()

        if nentries < self._bin_thr:
            self.log.debug(f'Using unbinned dataset with {nentries} entries')
            self._binned = False
            return data

        self.log.debug(f'Using binned dataset with {nentries} entries and {self._nbins} bins')
        self._binned = True 

        hdata = data.binnedClone('hdata', '')

        return hdata
    #----------------------------------------
    def _run_dataset(self):
        self._load_snapshot('prefit')
        data = self._get_data()

        er = ROOT.RooFit.SumW2Error(False)
        sv = ROOT.RooFit.Save(True)
        mn = ROOT.RooFit.Minimizer('Minuit2', 'migrad')
        of = ROOT.RooFit.Offset(True)
        op = ROOT.RooFit.Optimize(True)
        st = ROOT.RooFit.Strategy(2)   
        pl = ROOT.RooFit.PrintLevel(-1)

        self._smear_init_pars()
        res = self._fit_mod.fitTo(data, er, mn, of, op, st, sv, pl)

        return res
    #----------------------------------------
    def _load_snapshot(self, name):
        success = self._wks.loadSnapshot(name)
        if success == False:
            self.log.error(f'Cannot load snapshot: {name} in:')
            self._wks.Print()
            raise
    #----------------------------------------
    def _smear_init_pars(self):
        s_var = self._wks.allVars()
        self._load_snapshot('prefit')
        self.log.debug('-----------------------------------------------------')
        self.log.debug(f'{"Parameter":<20}{"Prefit":<20}{"Initial":<20}')
        self.log.debug('-----------------------------------------------------')

        s_smr = ROOT.RooArgSet()
        for var in s_var:
            if var.isConstant():
                continue

            var_name = var.GetName()
            if var_name == self._obs_name:
                continue

            self._smear_par(var)
            s_smr.add(var)

        return s_smr
    #----------------------------------------
    def _smear_par(self, par):
        org_val = par.getVal()
        min_val = par.getMin()
        max_val = par.getMax()
        err_val = par.getError()
        par_nam = par.GetName()

        counter = 1
        while True:
            ini_val = self._ran.Gaus(org_val, err_val * self._spread_scale)

            if min_val < ini_val < max_val:
                break

            counter+=1

            self._check_smear_counter(counter, par)

        self.log.debug(f'{par_nam:<20}{org_val:<20.3e}{ini_val:<20.3e}')
        par.setVal(ini_val)
    #----------------------------------------
    def _check_smear_counter(self, counter, par):
        if counter > self._max_smear_count:
            self.log.error(f'Smear counter {counter} went above max {self._max_smear_count} for:')
            par.Print()
            raise
    #----------------------------------------
    def results(self):
        return self._l_result
#----------------------------------------

