"""This code is inspired from IPART
   => xugzhi1987@gmail.com """

#==== import libraries ==================
import os
import numpy as np
from ipart.utils import funcs
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from ipart.utils import plot
#==== Import data => contains aerosols data from MERRA-2 =================
data = os.path.join('.', 'merra2_hourly.nc') 

#==== Read in data ===============
uflux=funcs.readNC(data, 'BCFLUXU')
vflux=funcs.readNC(data, 'BCFLUXV')
output=os.path.join('.', 'ivt_bc_2017_hour_all.nc') #save nc file in given name
#=== Get data info ==============
#print(uflux.info())
#print(vflux.info())
#print(uflux.getLatitude())
#print(uflux.getLongitude())
#print(uflux.getTime())

#=== compute Aerosol IVT ==================
ivt=np.ma.sqrt(uflux.data*uflux.data+vflux.data*vflux.data)
ivt=funcs.NCVAR(ivt, 'ivt', uflux.axislist, {'name': 'ivt', 'long_name': 'integrated vapor transport (IVT)',
                                            'standard_name': 'integrated_vapor_transport',
                                            'title': 'integrated vapor transport (IVT)',
                                            'units': getattr(uflux, 'units', '')})
funcs.saveNC(output, ivt)

figure=plt.figure(figsize=(7,10),dpi=100)
idx=120  # select the 101th time step from the beginning
time_str=uflux.getTime()[idx]

plot_vars=[uflux.data[idx], vflux.data[idx], ivt.data[idx]]
titles=['U', 'V', 'IVT']

for ii, vii in enumerate(plot_vars):
    axii=figure.add_subplot(3,1,ii+1,projection=ccrs.PlateCarree())
    iso=plot.Isofill(vii, 10, 1, 2)
    plot.plot2(vii, iso, axii,
            title='%s, %s' %(str(time_str), titles[ii]),
            xarray=uflux.getLongitude(),
               yarray=uflux.getLatitude(),
            legend='local',
            fix_aspect=False)

plt.show()
