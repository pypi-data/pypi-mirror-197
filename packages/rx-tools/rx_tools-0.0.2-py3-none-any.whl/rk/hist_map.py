import ROOT
import numpy
import style

import utils
import utils_noroot as utnr
#---------------------------------------
class hist_map:
    log = utnr.getLogger(__name__)
    #------------------------
    def __init__(self, d_opt = {}):
        self.__d_opt          = d_opt

        self.__h_yld_fail_dat = None
        self.__h_yld_pass_dat = None
        self.__h_yld_fail_sim = None
        self.__h_yld_pass_sim = None

        self.__h_eff_dat      = None
        self.__h_eff_sim      = None

        self.__initialized = False
    #------------------------
    def __initialize(self):
        if self.__initialized:
            return

        utnr.check_none(self.__h_yld_fail_dat)
        utnr.check_none(self.__h_yld_pass_dat)
        utnr.check_none(self.__h_yld_fail_sim)
        utnr.check_none(self.__h_yld_pass_sim)

        self.__h_eff_dat = self.__get_eff_map(self.__h_yld_pass_dat, self.__h_yld_fail_dat)
        self.__h_eff_dat.SetTitle('Data')

        self.__h_eff_sim = self.__get_eff_map(self.__h_yld_pass_sim, self.__h_yld_fail_sim)
        self.__h_eff_sim.SetTitle('Simulation')

        self.__initialized = True
    #------------------------
    def __get_eff_map(self, h_yld_pass, h_yld_fail):
        name_pass = h_yld_pass.GetName()
        name_fail = h_yld_fail.GetName()

        name_eff = 'h_eff_{}_{}'.format(name_pass, name_fail)
        h_eff = h_yld_pass.Clone(name_eff) 

        nbins = h_eff.GetNumberOfBins()
        for i_bin in range(1, nbins + 1) :
            npass = h_yld_pass.GetBinContent(i_bin)
            nfail = h_yld_fail.GetBinContent(i_bin)

            epass = h_yld_pass.GetBinError(i_bin)
            efail = h_yld_fail.GetBinError(i_bin)

            eff, err = utils.value_and_covariance('p / (p + f)', p = (npass, epass), f = (nfail, efail))

            self.log.debug('{}+/-{}'.format(npass, epass))
            self.log.debug('{}+/-{}'.format(nfail, efail))

            h_eff.SetBinContent(i_bin, eff)
            h_eff.SetBinError(i_bin, err)

        return h_eff
    #------------------------
    def add_hist(self, h_pas, h_fal, data=None):
        if   data == True:
            self.__h_yld_pass_dat = h_pas 
            self.__h_yld_fail_dat = h_fal 
        elif data == False:
            self.__h_yld_pass_sim = h_pas 
            self.__h_yld_fail_sim = h_fal 
        else:
            self.log.error('Invalid data flag')
            raise
    #------------------------
    def __get_efficiency(self, arr_point, data=None):
        utnr.check_none(data)
    
        if data:
            h_eff = self.__h_eff_dat
        else:
            h_eff = self.__h_eff_sim
            
        arr_eff = utils.read_2Dpoly(arr_point, h_eff)
        
        return arr_eff
    #------------------------
    def get_yld_maps(self, data=None):
        if data:
            return self.__h_yld_pass_dat, self.__h_yld_fail_dat 
        else:
            return self.__h_yld_pass_sim, self.__h_yld_fail_sim
    #------------------------
    def get_efficiencies(self, arr_point, treename=None, replica=None, skip_direct=None):
        self.__initialize()

        #TODO: treename will be introduced always, but not used, might use it somehow.
        if replica not in [0, None]:
            self.log.error('Replica {} not supported'.format(replica))
            raise

        if skip_direct not in [True, None]:
            self.log.error('Skip direct {} not supported'.format(skip_direct))
            raise

        arr_eff_dat = self.__get_efficiency(arr_point, data=True)
        arr_eff_sim = self.__get_efficiency(arr_point, data=False)

        arr_eff = numpy.array([arr_eff_dat, arr_eff_sim]).T

        return arr_eff
    #------------------------
    def plot_maps(self, outdir, d_opt=None):
        self.__initialize()
        if d_opt is not None:
            self.__d_opt.update(d_opt)

        self.__do_plot_maps(self.__h_eff_sim     , self.__h_eff_dat     , 'eff', outdir)
        self.__do_plot_maps(self.__h_yld_pass_sim, self.__h_yld_pass_dat, 'pas', outdir)
        self.__do_plot_maps(self.__h_yld_fail_sim, self.__h_yld_fail_dat, 'fal', outdir)

        return (self.__h_eff_dat, self.__h_eff_sim)
    #------------------------
    def __do_plot_maps(self, h_sim, h_dat, kind, outdir):
        l_h_row_sim = utils.poly2D_to_1D(h_sim, kind + '_sim')
        l_h_row_dat = utils.poly2D_to_1D(h_dat, kind + '_dat')

        if   kind in ['pas', 'fal']:
            d_opt = {}
            d_opt['logy']   = True
            d_opt['yrange'] = (0.1, 1e6)
            d_opt['legend'] = -10
            d_opt['xgrid']  = True 
            d_opt['ygrid']  = True 
            d_opt['yname']  = 'Signal yield'

            if 'leg_head' in self.__d_opt:
                d_opt['leg_head'] = self.__d_opt['leg_head']
        elif kind == 'eff':
            d_opt = self.__d_opt
        else:
            self.log.error('Kind of plot {} not recognized'.format(kind))
            raise

        plot_id = utnr.get_from_dic(self.__d_opt, 'plot_id')
        counter = 1
        for h_row_sim, h_row_dat in zip(l_h_row_sim, l_h_row_dat):
            h_row_sim.SetTitle('Simulation')
            h_row_dat.SetTitle('Data')

            plotpath = f'{outdir}/{kind}_{plot_id}_{counter:02}.png'
            utils.plot_histograms([h_row_sim, h_row_dat], plotpath, d_opt=d_opt)
            counter+=1
#---------------------------------------

