import os, sys
import numpy as np
import pandas as pd
from ipart.utils import funcs
from ipart.AR_detector import findARs
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from ipart.utils import plot


YEAR=2017
TIME_START = '%d-01-16 00:00:00' %YEAR
TIME_END   = '%d-02-16 00:00:00' %YEAR
#==== Import data => contains aerosols data from MERRA-2 =================
data = os.path.join('.', 'merra2_jan.nc')
#==== ivt reconstruction and anomalies ===================
ivt_file = os.path.join('.', 'ivt_bc_2017_jan-THR-kernel-hourmean-t10-s2.nc') #save nc file in given name
#------------------Output folder------------------
output_dir = os.path.join('.', str(YEAR))




PLOT=True          # create maps of found ARs or not
SHIFT_LON=10          # degree, shift left bound to longitude. Should match
                      # that used in compute_thr_singlefile.py


PARAM_DICT={
    # kg/m/s, define AR candidates as regions >= than this anomalous ivt.
    'thres_low' : 1,
    # km^2, drop AR candidates smaller than this area.
    'min_area': 50*1e4,
    # km^2, drop AR candidates larger than this area.
    'max_area': 1800*1e4,
    # float, minimal length/width ratio.
    'min_LW': 2,
    # degree, exclude systems whose centroids are lower than this latitude.
    'min_lat': 20,
    # degree, exclude systems whose centroids are higher than this latitude.
    'max_lat': 80,
    # km, ARs shorter than this length is treated as relaxed.
    'min_length': 2000,
    # km, ARs shorter than this length is discarded.
    'min_length_hard': 1500,
    # degree lat/lon, error when simplifying axis using rdp algorithm.
    'rdp_thres': 2,
    # grids. Remove small holes in AR contour.
    'fill_radius': None,
    # do peak partition or not, used to separate systems that are merged
    # together with an outer contour.
    'single_dome': False,
    # max prominence/height ratio of a local peak. Only used when single_dome=True
    'max_ph_ratio': 0.6,
    # minimal proportion of flux component in a direction to total flux to
    # allow edge building in that direction
    'edge_eps': 0.4
    }


#==== Read in data ===============
uflux=funcs.readNC(data, 'BCFLUXU')
vflux=funcs.readNC(data, 'BCFLUXV')


#-------------------Read in ivt-------------------
print('\n# Read in file:\n',ivt_file)
ivt=funcs.readNC(ivt_file, 'ivt')
ivtrec=funcs.readNC(ivt_file, 'ivt_rec')
ivtano=funcs.readNC(ivt_file, 'ivt_ano')
#-----------------Shift longitude-----------------
qu=uflux.shiftLon(SHIFT_LON)
qv=vflux.shiftLon(SHIFT_LON)
ivt=ivt.shiftLon(SHIFT_LON)
ivtrec=ivtrec.shiftLon(SHIFT_LON)
ivtano=ivtano.shiftLon(SHIFT_LON)
#--------------------Slice data--------------------
qu=qu.sliceData(TIME_START,TIME_END,axis=0).squeeze()
qv=qv.sliceData(TIME_START,TIME_END,axis=0).squeeze()
ivt=ivt.sliceData(TIME_START,TIME_END,axis=0).squeeze()
ivtrec=ivtrec.sliceData(TIME_START,TIME_END,axis=0).squeeze()
ivtano=ivtano.sliceData(TIME_START,TIME_END,axis=0).squeeze()
#-----------------Get coordinates-----------------
latax=qu.getLatitude()
lonax=qu.getLongitude()
timeax=ivt.getTime()
timeax=['%d-%02d-%02d %02d:00' %(timett.year, timett.month, timett.day, timett.hour) for timett in timeax]

time_idx, labels, angles, crossfluxes, result_df = findARs(ivt.data, ivtrec.data,
            ivtano.data, qu.data, qv.data, latax, lonax, times=timeax, **PARAM_DICT)

