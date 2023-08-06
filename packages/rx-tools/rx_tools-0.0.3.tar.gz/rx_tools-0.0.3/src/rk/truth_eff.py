import utils_noroot as utnr
import os

#---------------------------------------
def get_eff(sample, year, version, kind):
    mon_dir = os.environ['MONDIR']
    file_path = f'{mon_dir}/output/truth_eff/{version}/{kind}/{sample}_{year}.json'
    [pas, fal] = utnr.load_json(file_path)
    
    return pas / (pas + fal)
#---------------------------------------

