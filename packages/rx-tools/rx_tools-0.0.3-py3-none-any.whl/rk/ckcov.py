import numpy
import logging

import pandas            as pnd 
import utils_noroot      as utnr
import matplotlib.pyplot as plt

from rk.eff_yld_loader import eff_yld_loader as eyl
from stats.covariance  import covariance

#------------------------------
class calculator:
    log=utnr.getLogger(__name__)
    #---------------
    def __init__(self, eff_version=None, yld_version=None, unc=None, proc='psi2', years=None):
        self._eff_version = eff_version 
        self._yld_version = yld_version 
        self._unc         = unc
        self._proc        = proc 
        self._l_year      = years

        self._tool_level  = logging.WARNING
        self._l_unc       = ['bts', 'sys', 'osc']
        self._l_good_year = ['2011', '2012', '2015', '2016', '2017', '2018', 'r1', 'r2p1']
        self._nboost      = 200 
        self._initialized = False

        self._d_kind_quant= None 
        self._l_trig_year = None 
        self._weights     = None 
        self._arr_mu_nom  = None
        self._arr_re_nom  = None
        self._arr_ce_nom  = None
        self._plot_dir    = None
        self._l_column    = None
        self._d_cov       = None
        self._d_yld       = {} 
        self._d_d_eff     = {} 

        self._df_ce_ee    = None
        self._df_re_ee    = None
        self._df_ce_mm    = None
        self._df_re_mm    = None

        self._df_cx       = None
        self._df_rx       = None

        self._df_mu       = None
    #---------------
    @property
    def plot_dir(self):
        return self._plot_dir

    @plot_dir.setter
    def plot_dir(self, plot_dir):
        self._plot_dir = utnr.make_dir_path(plot_dir)
    #---------------
    def _get_kind_quant(self):
        d_quant             = {}
        d_quant['r_jpsi']   = '$r_{J/\psi}$'
        d_quant['r_rare']   = '$r_{rare}$'
        d_quant['mu']       = '$R_{rare}$'

        d_quant['c_eff_ee'] = '$\\varepsilon(J/\psi \\to ee)$'
        d_quant['c_eff_mm'] = '$\\varepsilon(J/\psi \\to \mu\mu)$'
        d_quant['r_eff_ee'] = '$\\varepsilon(rare \\to ee)$'
        d_quant['r_eff_mm'] = '$\\varepsilon(rare \\to \mu\mu))$'

        return d_quant
    #---------------
    def _initialize(self):
        if self._initialized:
            return

        utnr.check_included(self._unc, self._l_unc)

        self._d_kind_quant = self._get_kind_quant()
        self._l_trig_year  = self._get_trig_year()

        if   self._unc == 'bts':
            self._weights = 'pnom_tnom_gnom_lnom_hnom_rnom_qnom_ball'
        elif self._unc == 'sys':
            self._weights = 'pall_tall_gall_lall_hall_rall_qall_bnom'
        else:
            self.log.error(f'Not supported uncertainty {self._unc}')
            raise

        eyl.log.setLevel(self._tool_level)

        self._l_column    = [ f'{trig} {year}' for trig, year in self._l_trig_year]

        self._df_ce_ee    = pnd.DataFrame(columns=self._l_column)
        self._df_re_ee    = pnd.DataFrame(columns=self._l_column)
        self._df_ce_mm    = pnd.DataFrame(columns=self._l_column)
        self._df_re_mm    = pnd.DataFrame(columns=self._l_column)

        self._df_cx       = pnd.DataFrame(columns=self._l_column)
        self._df_rx       = pnd.DataFrame(columns=self._l_column)
        self._df_mu       = pnd.DataFrame(columns=self._l_column)

        self._df_ce_ee.style.set_caption('Efficiency electron jpsi')
        self._df_re_ee.style.set_caption('Efficiency electron psi2')
        self._df_ce_mm.style.set_caption('Efficiency muon jpsi')
        self._df_re_mm.style.set_caption('Efficiency muon psi2')
                      
        self._df_cx.style.set_caption('r_jpsi')
        self._df_rx.style.set_caption('r_rare')
        self._df_mu.style.set_caption('Double ratio of corrected yields')

        self._fill_df('nom')

        self._arr_rx_nom  = self._df_rx.loc['nom'].to_numpy()
        self._arr_cx_nom  = self._df_cx.loc['nom'].to_numpy()
        self._arr_mu_nom  = self._df_mu.loc['nom'].to_numpy()

        self._initialized = True
    #---------------
    def _get_trig_year(self):
        l_trig_year = []
        utnr.check_none(self._l_year)
        for year in self._l_year:
            if year not in self._l_good_year:
                self.log.error(f'Invalid year introduced: {year}')
                raise

            l_trig_year += [('TOS', year), ('TIS', year)]

        return l_trig_year
    #---------------
    def _get_data(self, proc, trig, year, syst):
        key = f'{proc}_{trig}_{year}'

        if key not in self._d_yld:
            self.log.info(f'Loading {key}')

            obj        = eyl(proc, trig, year, self._weights)
            yld, d_eff = obj.get_values(eff_version = self._eff_version, yld_version=self._yld_version)

            self._d_yld[key]   = yld
            self._d_d_eff[key] = d_eff 

        d_eff = self._d_d_eff[key]
        yld   =   self._d_yld[key]

        #If systematic does not make sense (e.g. electron systematic applied to muon)
        #use nominal value
        if syst not in d_eff:
            eff = d_eff['nom']
        else:
            eff = d_eff[syst]

        return (yld, eff)
    #---------------
    def _get_syst(self, syst, trig, year):
        trig = 'ETOS' if trig == 'TOS' else 'GTIS'

        c_yld_ee, c_eff_ee = self._get_data(         'ctrl_ee',   trig, year, syst)
        c_yld_mm, c_eff_mm = self._get_data(         'ctrl_mm', 'MTOS', year, syst)

        r_yld_ee, r_eff_ee = self._get_data(f'{self._proc}_ee',   trig, year, syst)
        r_yld_mm, r_eff_mm = self._get_data(f'{self._proc}_mm', 'MTOS', year, syst)

        c_yld_ee_val, _ = c_yld_ee
        c_yld_mm_val, _ = c_yld_mm

        r_yld_ee_val, _ = r_yld_ee
        r_yld_mm_val, _ = r_yld_mm

        c_yld_rat = c_yld_mm_val / c_yld_ee_val
        r_yld_rat = r_yld_mm_val / r_yld_ee_val

        c_eff_rat = c_eff_mm     / c_eff_ee
        r_eff_rat = r_eff_mm     / r_eff_ee

        r_jpsi    = c_yld_rat    / c_eff_rat 
        r_rare    = r_yld_rat    / r_eff_rat 

        mu        = r_rare       / r_jpsi

        d_data             = {}
        d_data['c_eff_ee'] =  c_eff_ee.val[0]
        d_data['r_eff_ee'] =  r_eff_ee.val[0]
        d_data['c_eff_mm'] =  c_eff_mm.val[0]
        d_data['r_eff_mm'] =  r_eff_mm.val[0]

        d_data['r_jpsi'  ] =  r_jpsi
        d_data['r_rare'  ] =  r_rare 
        d_data['mu'      ] =  mu 

        return d_data 
    #---------------
    def _fill_df(self, syst):
        l_ce_ee = []
        l_re_ee = []
        l_ce_mm = []
        l_re_mm = []

        l_cx = []
        l_rx = []

        l_mu = []

        for trig, year in self._l_trig_year:
            d_data = self._get_syst(syst, trig, year)

            ce_ee = d_data['c_eff_ee']
            re_ee = d_data['r_eff_ee']
            ce_mm = d_data['c_eff_mm']
            re_mm = d_data['r_eff_mm']

            l_ce_ee.append(ce_ee)
            l_re_ee.append(re_ee)
            l_ce_mm.append(ce_mm)
            l_re_mm.append(re_mm)

            rx    = d_data['r_rare'  ]
            cx    = d_data['r_jpsi'  ]
            mu    = d_data['mu'      ]

            l_rx.append(rx)
            l_cx.append(cx)
            l_mu.append(mu)

        label       = syst.split('.')[0]
        self._df_ce_ee = utnr.add_row_to_df(self._df_ce_ee, l_ce_ee, index=label)
        self._df_re_ee = utnr.add_row_to_df(self._df_re_ee, l_re_ee, index=label)
        self._df_ce_mm = utnr.add_row_to_df(self._df_ce_mm, l_ce_mm, index=label)
        self._df_re_mm = utnr.add_row_to_df(self._df_re_mm, l_re_mm, index=label)

        self._df_cx = utnr.add_row_to_df(self._df_cx, l_cx, index=label)
        self._df_rx = utnr.add_row_to_df(self._df_rx, l_rx, index=label)

        self._df_mu = utnr.add_row_to_df(self._df_mu, l_mu, index=label)

        return label
    #---------------
    def _get_cov(self, label, l_syst):
        l_arr_mu_syst = []
        for syst in l_syst:
            index       = self._fill_df(syst)
            arr_mu_syst = self._df_cx.loc[index].to_numpy()
            l_arr_mu_syst.append(arr_mu_syst) 

        mat_mu_syst   = numpy.array(l_arr_mu_syst)
        obj = covariance(mat_mu_syst.T, self._arr_mu_nom)
        cov = obj.get_cov()

        return cov
    #---------------
    def _plot_df(self, df, column, kind):
        if self._plot_dir is None:
            return

        nom_val = df.iloc[0][column]
        nrm_col = f'{column} nrm'

        df[nrm_col]= 100 * (df[column] - nom_val) / nom_val
        df=df.drop('nom')

        fig, ax = plt.subplots(figsize=(10,4))
        ax.axhline(y=nom_val, color='red')

        arr_val = df[ column].values
        arr_nrm = df[nrm_col].values

        st = '-' if self._unc != 'bts' else '.'
        ax.plot(arr_val, linestyle=st)


        l_loc, l_lab = utnr.get_axis(df, 'index')
        if self._unc != 'bts':
            plt.xticks(l_loc, l_lab, rotation=80)

        ex=ax.twinx()
        ex.plot(arr_nrm, alpha=0, color='red')

        ax.legend(['Nominal', 'Systematic'])
        ax.grid()
        plt.title(column)

        quant = self._d_kind_quant[kind]
        ax.set_ylabel(quant)
        ex.set_ylabel('Bias [%]')

        fig.tight_layout()

        syst_dir = utnr.make_dir_path(f'{self._plot_dir}/syst_{kind}')
        plot_name= column.replace(' ', '_') + '.png'
        plot_path= f'{syst_dir}/{plot_name}'

        self.log.visible(f'Saving to: {plot_path}')
        fig.savefig(plot_path)
        plt.close('all')
    #---------------
    def _get_all_cov(self):
        d_cov = {}

        if   self._unc == 'bts':
            d_cov['bts']       = self._get_cov('bts'   , [f'bts_{num}' for num in range(1, self._nboost)] )
        elif self._unc == 'sys':
            d_cov['gen']       = self._get_cov('gen'   , ['gen_GTIS_mm', 'gen_npv', 'gen_nsp', 'gen_ntk'])

            d_cov['rec_to']    = self._get_cov('rec_to', ['rec_GTIS_ee'])
            d_cov['rec_ti']    = self._get_cov('rec_ti', ['rec_ETOS'])
            d_cov['rec_mu']    = self._get_cov('rec_mu', ['rec_GTIS_mm'])

            d_cov['lzr_mu']    = self._get_cov('lzr_mu', [    'lzr_L0MuonHAD',     'lzr_L0MuonMU1'])
            d_cov['lzr_el']    = self._get_cov('lzr_el', ['lzr_L0ElectronFAC', 'lzr_L0ElectronHAD'])
            d_cov['lzr_ts']    = self._get_cov('lzr_ts', ['lzr_L0TIS_MMMH.L0HadronElEL.L0ElectronTIS', 'lzr_L0TIS_EMBN.L0HadronElEL.L0ElectronTIS'])

            d_cov['pid_kp_el'] = self._get_cov('pid_kp', ['pid_kp_el_bin1', 'pid_kp_el_bin2', 'pid_kp_el_bin3', 'pid_kp_el_bin4', 'pid_kp_el_tis'])
            d_cov['pid_kp_mu'] = self._get_cov('pid_kp', ['pid_kp_mu_bin1', 'pid_kp_mu_bin2', 'pid_kp_mu_bin3', 'pid_kp_mu_bin4', 'pid_kp_mu_tis'])
            d_cov['pid_el'   ] = self._get_cov('pid_el', ['pid_el_bin1', 'pid_el_tis'])
            d_cov['pid_mu'   ] = self._get_cov('pid_mu', ['pid_mu_bin1', 'pid_mu_bin2', 'pid_mu_bin3', 'pid_mu_bin4', 'pid_mu_tis'])

            d_cov['qsq'   ]    = self._get_cov('qsq'   , ['qsq_lsh', 'qsq_mom', 'qsq_trg'])
        else:
            self.log.error(f'Invalid uncertainty type: {self._unc}')
            raise

        return d_cov
    #---------------
    def _plot_all_df(self):
        for column in self._l_column:
            self._plot_df(self._df_ce_ee, column, 'c_eff_ee')
            self._plot_df(self._df_re_ee, column, 'r_eff_ee')
            self._plot_df(self._df_ce_mm, column, 'c_eff_mm')
            self._plot_df(self._df_re_mm, column, 'r_eff_mm')

            self._plot_df(self._df_cx, column, 'r_jpsi')
            self._plot_df(self._df_rx, column, 'r_rare')
            self._plot_df(self._df_mu, column,     'mu')
    #---------------
    def _get_rel_cov(self, cv_ij):
        mu_ij = numpy.outer(self._arr_mu_nom, self._arr_mu_nom)
        un_ij = cv_ij / mu_ij

        return un_ij
    #---------------
    def _save_df(self):
        self._save_table(self._df_cx, 'r_jpsi')
        self._save_table(self._df_rx, 'r_rare')
        self._save_table(self._df_mu,     'mu')
    #---------------
    def _save_table(self, df, label):
        table_dir  = utnr.make_dir_path(f'{self._plot_dir}/tables')
        table_path = f'{table_dir}/{label}.tex'

        utnr.df_to_tex(df, table_path)
    #---------------
    def cov(self, relative=False):
        self._initialize()

        if self._d_cov is None:
            self._d_cov = self._get_all_cov()
            self._plot_all_df()
            self._save_df()

        if relative:
            d_cov = {syst : self._get_rel_cov(cov) for syst, cov in self._d_cov.items() }
        else:
            d_cov = self._d_cov

        return d_cov
#------------------------------

