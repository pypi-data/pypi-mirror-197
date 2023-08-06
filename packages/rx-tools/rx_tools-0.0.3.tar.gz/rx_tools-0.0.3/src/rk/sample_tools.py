import utils_noroot as utnr

#------------------------------
def get_evt_dec():
    d_evt_dec = {}

    d_evt_dec['15876430'] = '\Lambda_b \\to (\Lambda_c^+ \\to 2h + X) \pi^+ \pi^- \mu^- \\bar{\\nu}_{\mu})' 
    d_evt_dec['17876650'] = 'B_s^{2*0} \\to K^- (B^+ \\to D^0 X \mu^+ \\nu_{\mu}' 
    d_evt_dec['12155110'] = 'B^+\\to \psi(\\to ee)K^{*+}'
    d_evt_dec['12103025'] = 'B^+\\to \pi^+\pi^-K^+'
    d_evt_dec['12153012'] = 'B^+\\to \psi(\\to ee)K^+'
    d_evt_dec['15454101'] = '\Lambda_b\\to J/\psi(\\to ee)X'
    d_evt_dec['12143001'] = 'B^+\\to J/\psi(\\to \mu\mu)K^+'
    d_evt_dec['12425000'] = 'B^+\\to K_1^+(\\to K^+\pi^+\pi^-)ee'
    d_evt_dec['12153001'] = 'B^+\\to J/\psi(\\to ee)K^+'
    d_evt_dec['12143020'] = 'B^+\\to \psi(\\to \mu\mu)K^+'
    d_evt_dec['13454001'] = 'B_s\\to J/\psi(\\to ee)X'
    d_evt_dec['12425011'] = 'B^+\\to K_2^+(\\to X \\to K^+\pi^+\pi^-)ee'
    d_evt_dec['12123445'] = 'B^+\\to K^{*+}ee'
    d_evt_dec['12153020'] = 'B^+\\to J/\psi(\\to ee)\pi^+'
    d_evt_dec['12952000'] = 'B^+\\to J/\psi(\\to ee)X'
    d_evt_dec['11453001'] = 'B^0\\to J\psi(\\to ee)X'
    d_evt_dec['12143010'] = 'B^+\\to J/\psi(\\to \mu\mu)\pi^+'
    d_evt_dec['11154001'] = 'B^0\\to J/\psi(\\to ee) K^{*0}'
    d_evt_dec['12155100'] = 'B^+\\to J/\psi(\\to ee) K^{*+}'
    d_evt_dec['11154011'] = 'B^0\\to \psi(\\to ee) K^{*0}'
    d_evt_dec['12183004'] = 'B^+\\to D^0(K^+e\\nu)\pi^0'
    d_evt_dec['12583013'] = 'B^+\\to D^0(K^+\pi^-)e\\nu'
    d_evt_dec['12113002'] = 'B^+\\to K^+\mu\mu'
    d_evt_dec['12583021'] = 'B^+\\to D^0(K^+e\\nu)e\\nu'
    d_evt_dec['11124002'] = 'B^0\\to K^{*0}ee'
    d_evt_dec['12123003'] = 'B^+\\to K^+e^+e^-'
    d_evt_dec['12123445'] = 'B^+\\to K^{*+}e^+e^-'
    d_evt_dec['12103025'] = 'B^+\\to K^+\pi^+\pi^-'
    d_evt_dec['12155110'] = 'B^+\\to K^{*+}\psi(2S)(\\to e^+e^-)'
    d_evt_dec['12123444'] = 'B^+\\to K^{*+}ee'
    d_evt_dec['12123005'] = 'B^+\\to K^+e^+e^-'
    d_evt_dec['12123002'] = 'B^+\\to K^+e^+e^-'
    d_evt_dec['12113001'] = 'B^+\\to K^+\mu\mu'
    d_evt_dec['11124001'] = 'B^0\\to K^{*0}ee'
    d_evt_dec['11102211'] = 'B^0\\to K^{*0} (\\to K^+ pi^-) pi^0 \gamma'
    d_evt_dec['11453012'] = 'B^0\\to \psi(2S) (\\to e+ e-) X'
    d_evt_dec['12103019'] = 'B^+\\to K^+K^+K^-'

    d_evt_dec['12103021'] = 'B^+\\to \pi^+\pi^- K^+'
    d_evt_dec['12103022'] = 'B^+\\to \pi^+\pi^- K^+'
    d_evt_dec['12103023'] = 'B^+\\to \pi^+\pi^- K^+'
    d_evt_dec['12103028'] = 'B^+\\to \pi^+\pi^- K^+'
    d_evt_dec['12103029'] = 'B^+\\to \pi^+\pi^- K^+'
    d_evt_dec['12203020'] = 'B^+\\to \pi^+\pi^- K^+'
    d_evt_dec['12203021'] = 'B^+\\to \pi^+\pi^- K^+'

    d_evt_dec['12103038'] = 'B^+\\to \pi^+  K^- K^+'
    d_evt_dec['12155020'] = 'B^+\\to (K_1(1270)^+ \\to K^+ pi^+ pi^-) (J/\psi \\to e^+ e^-)'
    d_evt_dec['12155021'] = 'B^+\\to (K_1(1270)^+ \\to K^+ pi^+ pi^-) (J/\psi \\to e^+ e^-)'
    d_evt_dec['12155030'] = 'B^+\\to K^+ (\psi(2S)\\to (J/\psi \\to e^+ e^-) \pi^+ \pi^-)'
    d_evt_dec['12155030'] = 'B^+\\to (J/\psi \\to e^+ e^-) (\phi \\to K^+ K^-) K^+'
    d_evt_dec['12155040'] = 'B^+\\to (J/\psi \\to e^+ e^-) (\phi \\to K^+ K^-) K^+'

    return d_evt_dec
#------------------------------
class data:
    d_evt_dec = get_evt_dec()
#------------------------------
def get_decay_from_evt(evt):
    evt = str(evt)
    return utnr.get_from_dic(data.d_evt_dec, evt)
#------------------------------

