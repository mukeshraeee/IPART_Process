
import os
import numpy as np
from ipart.utils import funcs
from ipart import thr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from ipart.utils import plot


#=== Read data ============
ivt_file = os.path.join('.','ivt_bc_2017_hour_all.nc')
var      = 'ivt'

SHIFT_LON=10

KERNEL=[120,2,2]
OUTPUTDIR=os.path.abspath('.')
var=funcs.readNC(ivt_file, 'ivt')
lon=var.getLongitude()
var=var.shiftLon(SHIFT_LON)
print('var.shape=', var.shape)

ivt, ivtrec, ivtano=thr.THR(var, KERNEL)

#--------Save------------------------------------
if not os.path.exists(OUTPUTDIR):
    os.makedirs(OUTPUTDIR)

fname=os.path.split(ivt_file)[1]
file_out_name='%s-THR-kernel-year_hour-t%d-s%d.nc'\
        %(os.path.splitext(fname)[0], KERNEL[0], KERNEL[1])

abpath_out=os.path.join(OUTPUTDIR,file_out_name)
print('\n# Saving output to:\n',abpath_out)
funcs.saveNC(abpath_out, ivt, 'w')
funcs.saveNC(abpath_out, ivtrec, 'a')
funcs.saveNC(abpath_out, ivtano, 'a')

#======== Plot Figure ============================================
figure=plt.figure(figsize=(10,10),dpi=100)
idx=60  # select the 101th time step from the beginning
time_str=ivt.getTime()[idx]

plot_vars=[ivt.data[idx], ivtrec.data[idx], ivtano.data[idx]]
iso=plot.Isofill(plot_vars, 12, 1, 1, min_level=0, qr=0.001)
titles=['IVT (=IVT_rec + IVT_ano)', 'IVT_rec', 'IVT_ano']

for ii, vii in enumerate(plot_vars):
    axii=figure.add_subplot(3,1,ii+1,projection=ccrs.PlateCarree())
    
    plot.plot2(vii, iso, axii,
            title='%s, %s' %(str(time_str), titles[ii]),
               xarray=ivt.getLongitude(),
               yarray=ivt.getLatitude(),
            legend='local',
            fix_aspect=False)

plt.show()

