import os
import json
import math
import array
import numpy

import utils_noroot as utnr
import utils

from atr_mgr import mgr

log=utnr.getLogger(__name__)
#------------------------------
class data:
    d_name_evt={}
    d_name_evt["ctrl_electron"]=12153001
    d_name_evt["psi2_electron"]=12153012
    d_name_evt["rare_electron"]=12123003
    d_name_evt["ctrl_ee"]      =12153001
    d_name_evt["psi2_ee"]      =12153012
    d_name_evt["rare_ee"]      =12123003

    d_name_evt["ctrl_muon"]    =12143001
    d_name_evt["psi2_muon"]    =12143020
    d_name_evt["rare_muon"]    =12113002
    d_name_evt["ctrl_mm"]      =12143001
    d_name_evt["psi2_mm"]      =12143020
    d_name_evt["rare_mm"]     =12113002
#------------------------------
def getProdID(evt, polarity, year):
    find_dir =os.environ['FINDIR']
    json_path=f'{find_dir}/json/prodID.json'
    d_key_id=utnr.load_json(json_path)

    key=f'{evt}_{polarity}_{year}'

    #Subtracting 1 due to merging step between Generator Statistics page and Dirac
    ID = utnr.get_from_dic(d_key_id, key) - 1

    return ID
#------------------------------
def calcGeomEff(name, polarity, year, perc=False):
    #This way can use either trigger or channel as key
    if True:
        name = name.replace('MTOS',     'muon')
        name = name.replace('ETOS', 'electron')
        name = name.replace('HTOS', 'electron')
        name = name.replace('GTIS', 'electron')

    evt=utnr.get_from_dic(data.d_name_evt, name)
    json_path = get_json_table(year, polarity, evt)
    utnr.check_file(json_path)

    obj=utnr.load_json(json_path)
    l_data=obj["Signal Counters"]

    d_part=l_data[0]
    d_anti=l_data[1]

    eff_part = 100 * d_part["value"] 
    err_part = 100 * d_part["error"] 

    eff_anti = 100 * d_anti["value"] 
    err_anti = 100 * d_anti["error"] 

    eff, err = utils.value_and_covariance('(p + a) / 2.', p = (eff_part, err_part), a = (eff_anti, err_anti) )

    if not perc:
        eff = eff / 100.
        err = err / 100.

    return (eff, err) 
#------------------------------
def get_json_table(year, polarity, evt):
    #wont break if year is int
    year=str(year)

    if   year == "2011":
        dirname=f'Sim09-Beam3500GeV-{year}-{polarity}-Nu2-Pythia8'
    elif year == "2012":
        dirname=f'Sim09-Beam4000GeV-{year}-{polarity}-Nu2.5-Pythia8'
    elif year in ["2015", "2016", "2017", "2018"]:
        dirname=f'Sim09-Beam6500GeV-{year}-{polarity}-Nu1.6-25ns-Pythia8'
    else:
        log.error(f'Year {year} is not supported')
        raise

    prodID=getProdID(evt, polarity, year)

    dbb_dir=os.environ['DBBDIR']
    json_path=f'{dbb_dir}/gen_info/{dirname}/Evt{evt}-P{prodID}.json'

    utnr.check_file(json_path)

    return json_path
#------------------------------
def getGeomEff(name, dset, perc=False):
    if dset in ['2011', '2012', '2015', '2016', '2017', '2018']:
        eff_1, err_1 = calcGeomEff(name,   "MagUp", dset, perc)
        eff_2, err_2 = calcGeomEff(name, "MagDown", dset, perc)
    elif dset == 'r1':
        eff_1, err_1 = getGeomEff(name, '2011', perc) 
        eff_2, err_2 = getGeomEff(name, '2012', perc) 
    elif dset == 'r2p1':
        eff_1, err_1 = getGeomEff(name, '2015', perc) 
        eff_2, err_2 = getGeomEff(name, '2016', perc) 
    elif dset == 'r2p2':
        eff_1, err_1 = getGeomEff(name, '2017', perc) 
        eff_2, err_2 = getGeomEff(name, '2018', perc) 
    else:
        log.error('Efficiencies not implemented yet for ' + dset)
        raise

    eff = (eff_1 + eff_2) / 2.
    err = 0.5 * math.sqrt(err_1 ** 2 + err_2 ** 2)

    return (eff, err)
#------------------------------
def get_binning(min_x, max_x):
    return numpy.linspace(min_x, max_x, 11)
#------------------------------
def getDiffHist(trigger='BOTH', l_ext=[]):
    import ROOT

    if trigger not in ['ETOS', 'HTOS', 'GTIS', 'MTOS', 'BOTH', 'test']:
        log.error(f'Using unsuported trigger: {trigger}')
        raise
    else:
        log.info(f'Using trigger: {trigger}')

    d_his={}
    if trigger == 'test':
        arr_B_ETA    = array.array('f', [1.9, 2.6, 2.9, 3.1, 3.2, 3.45, 3.65, 4, 5] )
        d_his["ETA"]      =ROOT.TH1D("h_B_ETA"    , "", len(arr_B_ETA)     - 1, arr_B_ETA)
        return d_his

    arr_B_ETA    = array.array('f', [1.9, 2.6, 2.9, 3.1, 3.2, 3.45, 3.65, 4, 5] )
    arr_B_PT     = array.array('f', [0, 4250, 5750, 7000, 8259, 9500, 11500, 14500, 18500 ] ) 
    arr_MinLPT   = array.array('f', [300, 750, 1100, 1400, 1750, 2200, 2800, 3700, 5000] )
    arr_MaxLPT   = array.array('f', [900, 2500, 3100, 3650, 4200, 4900, 5750, 7300, 10000] )

    arr_H_PT     = array.array('f', [400, 1100, 1600, 2100, 2700, 3400, 4400, 6000, 8500 ] ) 
    arr_H_calo_ET= array.array('f', [400, 1100, 1600, 2100, 2700, 3400, 4400, 6000, 8500, 12000 ] ) 
    arr_L_calo_ET= array.array('f', [400, 1100, 1600, 2100, 2700, 3400, 4400, 6000, 8500, 12000 ] ) 

    arr_MinLETA  = array.array('f', [1.5, 2.2, 2.4, 2.6, 2.7, 2.9, 3.1, 3.4, 5 ] ) 
    arr_MaxLETA  = array.array('f', [1.5, 2.7, 2.9, 3.1, 3.3, 3.5, 3.7, 3.9, 5.1] )
    arr_H_ETA    = array.array('f', [1.5, 2.4, 2.6, 2.9, 3.1, 3.3, 3.6, 3.9, 5.2] )
    arr_nSPDHits = array.array('f', [0, 168, 224, 272, 317, 366, 422, 491, 600] )
    arr_LogIPCHI2= array.array('f', [-5, -0.84, -0.05, 0.46, 0.88, 1.3, 1.7, 2.2, 3] )
    arr_vtxchi2  = array.array('f', [-3, -0.38, 0.21, 0.6, 0.92, 1.2, 1.5, 1.9, 3.3] )
    arr_llangle  = array.array('f', [0.0, 0.063, 0.086, 0.11, 0.13, 0.16, 0.2, 0.25, 0.5] )
    arr_klangle  = array.array('f', [0, 0.05, 0.07, 0.09, 0.12, 0.14, 0.18, 0.23, 0.5] )
    arr_cos_L    = array.array('f', [-1., -0.5, -0.3, -0.15, 0.0, 0.15, 0.3, 0.5, 1] )
    arr_et_reg   = array.array('f', [-0.001, 0.999, 1.999, 3])

    arr_fdchi2        = get_binning(+1.651e+00, 1.405e+01)
    arr_h_ipchi2      = get_binning(ROOT.TMath.Log(4), 1.2e+01)
    arr_max_lipchi2   = get_binning(+1.321e+00, 1.115e+01)
    arr_min_lipchi2   = get_binning(-8.080e+00, 1.000e+01)
    arr_cos_dira      = get_binning(+1.572e-05, 4.202e-02)
    arr_jpsi_pt       = get_binning(+1.296e+02, 3.639e+04)
    arr_jpsi_ip_chi2  = get_binning(-6.425e+00, 7.862e+00)

    arr_iso_cone = numpy.linspace(-1, +1, 20) 
    arr_vtx_onet = numpy.array([2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
    arr_vtx_twot = numpy.array([2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)

    d_his['B_T_L1_CONEPTASYM']             = ROOT.TH1D(    'h_B_T_L1_CONEPTASYM'        , '', len(arr_iso_cone) - 1, arr_iso_cone)
    d_his['log_B_VTXISODCHI2ONETRACK_p10'] = ROOT.TH1D('h_log_B_VTXISODCHI2ONETRACK_p10', '', len(arr_vtx_onet) - 1, arr_vtx_onet)
    d_his['log_B_VTXISODCHI2TWOTRACK_p10'] = ROOT.TH1D('h_log_B_VTXISODCHI2TWOTRACK_p10', '', len(arr_vtx_twot) - 1, arr_vtx_twot)

    d_his["PT"]       =ROOT.TH1D("h_B_PT"     , "", len(arr_B_PT)      - 1, arr_B_PT)
    d_his["ETA"]      =ROOT.TH1D("h_B_ETA"    , "", len(arr_B_ETA)     - 1, arr_B_ETA)
    d_his["MinLPT"]   =ROOT.TH1D("h_MinLPT"   , "", len(arr_MinLPT)    - 1, arr_MinLPT)
    d_his["MaxLPT"]   =ROOT.TH1D("h_MaxLPT"   , "", len(arr_MaxLPT)    - 1, arr_MaxLPT)
    d_his["MinLETA"]  =ROOT.TH1D("h_MinLETA"  , "", len(arr_MinLETA)   - 1, arr_MinLETA)
    d_his["MaxLETA"]  =ROOT.TH1D("h_MaxLETA"  , "", len(arr_MaxLETA)   - 1, arr_MaxLETA)
    d_his["H_PT"]     =ROOT.TH1D("h_H_PT"     , "", len(arr_H_PT)      - 1, arr_H_PT)
    d_his["H_ETA"]    =ROOT.TH1D("h_H_ETA"    , "", len(arr_H_ETA)     - 1, arr_H_ETA)
    d_his["nSPDHits"] =ROOT.TH1D("h_nSPDHits" , "", len(arr_nSPDHits)  - 1, arr_nSPDHits)
    d_his["LogIPCHI2"]=ROOT.TH1D("h_LogIPCHI2", "", len(arr_LogIPCHI2) - 1, arr_LogIPCHI2)
    d_his["vtxchi2"]  =ROOT.TH1D("h_vtxchi2"  , "", len(arr_vtxchi2)   - 1, arr_vtxchi2)
    d_his["llangle"]  =ROOT.TH1D("h_llangle"  , "", len(arr_llangle)   - 1, arr_llangle)
    d_his["klangle"]  =ROOT.TH1D("h_klangle"  , "", len(arr_klangle)   - 1, arr_klangle)
    d_his["cos_L"]    =ROOT.TH1D("h_cos_L"    , "", len(arr_cos_L)     - 1, arr_cos_L  )
    #-----------------
    #BDT variables
    #-----------------
    d_his["fdchi2"]       =ROOT.TH1D("h_fdchi2"      , "", len(arr_fdchi2)       - 1, arr_fdchi2)
    d_his["h_ipchi2"]     =ROOT.TH1D("h_h_ipchi2"    , "", len(arr_h_ipchi2)     - 1, arr_h_ipchi2)
    d_his["max_lipchi2"]  =ROOT.TH1D("h_max_lipchi2" , "", len(arr_max_lipchi2)  - 1, arr_max_lipchi2)
    d_his["min_lipchi2"]  =ROOT.TH1D("h_min_lipchi2" , "", len(arr_min_lipchi2)  - 1, arr_min_lipchi2)
    d_his["cos_dira"]     =ROOT.TH1D("h_cos_dira"    , "", len(arr_cos_dira)     - 1, arr_cos_dira)
    d_his["jpsi_pt"]      =ROOT.TH1D("h_jpsi_pt"     , "", len(arr_jpsi_pt)      - 1, arr_jpsi_pt)
    d_his["jpsi_ip_chi2"] =ROOT.TH1D("h_jpsi_ip_chi2", "", len(arr_jpsi_ip_chi2) - 1, arr_jpsi_ip_chi2)
    #-----------------
    #Check for reco mismodelling
    #-----------------
    d_his["L1_ETA"]    =ROOT.TH1D("h_L1_ETA"    , "", len(arr_H_ETA)     - 1, arr_H_ETA  )
    d_his["L2_ETA"]    =ROOT.TH1D("h_L2_ETA"    , "", len(arr_H_ETA)     - 1, arr_H_ETA  )

    d_his["L1_PT"]     =ROOT.TH1D("h_L1_PT"     , "", len(arr_H_PT)      - 1, arr_H_PT)
    d_his["L2_PT"]     =ROOT.TH1D("h_L2_PT"     , "", len(arr_H_PT)      - 1, arr_H_PT)


    if   trigger in ["ETOS", 'GTIS']:
        d_his["L1_L0Calo_ECAL_region"]=ROOT.TH1D("h_L1_L0Calo_ECAL_region", "", len(arr_et_reg) - 1, arr_et_reg)
        d_his["L2_L0Calo_ECAL_region"]=ROOT.TH1D("h_L2_L0Calo_ECAL_region", "", len(arr_et_reg) - 1, arr_et_reg)

        d_his["L1_L0Calo_ECAL_realET"]=ROOT.TH1D("h_L1_calo_ET", "", len(arr_L_calo_ET) - 1, arr_L_calo_ET)
    elif trigger in ['HTOS', 'GTIS']:
        d_his["H_L0Calo_HCAL_realET"] =ROOT.TH1D("h_H_calo_ET" , "", len(arr_H_calo_ET) - 1, arr_H_calo_ET)

    if 'bmass' in l_ext:
        log.info('Adding bmass')
        arr_B_const_mass_M = array.array('f', range(5070, 5700, 10))
        d_his["B_const_mass_M"]       =ROOT.TH1D("h_B_const_mass_M", "", len(arr_B_const_mass_M) - 1, arr_B_const_mass_M)

    if 'BDT_rdr'  in l_ext:
        log.info('Adding BDT')
        arr_BDT= numpy.linspace(0, 1.1, 31)
        d_his["BDT_rdr"]=ROOT.TH1D("h_BDT", "", arr_BDT.size - 1, arr_BDT)

    return d_his
#------------------------------
def addDiffVars(df):
    man = mgr(df)

    df=df.Define("PT"       , "B_PT")
    df=df.Define("ETA"      , "B_ETA" )
    df=df.Define("MinLPT"   , "TMath::Min(L1_PT , L2_PT)")
    df=df.Define("MaxLPT"   , "TMath::Max(L1_PT , L2_PT)")
    df=df.Define("MinLETA"  , "TMath::Min(L1_ETA, L2_ETA)")
    df=df.Define("MaxLETA"  , "TMath::Max(L1_ETA, L2_ETA)")
    df=df.Define("LogIPCHI2", "TMath::Log(B_IPCHI2_OWNPV)")
    df=df.Define("vtxchi2"  , "TMath::Log(B_ENDVERTEX_CHI2)")
    df=df.Define("llangle"  , "TVector3 v_l1(L1_PX, L1_PY, L1_PZ); TVector3 v_l2(L2_PX, L2_PY, L2_PZ); return v_l1.Angle(v_l2);")
    df=df.Define("klangle"  , "TVector3 v_k(H_PX, H_PY, H_PZ)    ; TVector3 v_l1(L1_PX, L1_PY, L1_PZ); return v_k.Angle(v_l1);")
    df=df.Define("cos_L"    , """TLorentzVector v_l1(L1_PX, L1_PY, L1_PZ, L1_PE); 
                                 TLorentzVector v_l2(L2_PX, L2_PY, L2_PZ, L2_PE);
                                 auto v_ll = v_l1 + v_l2; 
                                 auto v_boost = -1 * v_ll.BoostVector(); 
                                 v_l1.Boost(v_boost); 
                                 auto v1 = v_l1.Vect();
                                 auto v2 = v_ll.Vect();
                                 auto u1 = v1.Unit();
                                 auto u2 = v2.Unit();
                                 return u1.Dot(u2);""")

    df=df.Define('fdchi2'      , 'TMath::Log(B_FDCHI2_OWNPV)                                           ')
    df=df.Define('h_ipchi2'    , 'TMath::Log(H_IPCHI2_OWNPV)                                           ')
    df=df.Define('max_lipchi2' , 'TMath::Max(TMath::Log(L1_IPCHI2_OWNPV),TMath::Log(L2_IPCHI2_OWNPV))  ')
    df=df.Define('min_lipchi2' , 'TMath::Min(TMath::Log(L1_IPCHI2_OWNPV),TMath::Log(L2_IPCHI2_OWNPV))  ')
    df=df.Define('cos_dira'    , 'TMath::ACos(B_DIRA_OWNPV)                                            ')
    df=df.Define('jpsi_pt'     , 'Jpsi_PT                                                              ')
    df=df.Define('jpsi_ip_chi2', 'TMath::Log(Jpsi_IPCHI2_OWNPV)                                        ')
    df=df.Define('log_B_VTXISODCHI2ONETRACK_p10', 'TMath::Log(B_VTXISODCHI2ONETRACK + 10)')
    df=df.Define('log_B_VTXISODCHI2TWOTRACK_p10', 'TMath::Log(B_VTXISODCHI2TWOTRACK + 10)')

    return man.add_atr(df) 
#------------------------------


