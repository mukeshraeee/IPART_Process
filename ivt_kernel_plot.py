"""plot integrated dust transport data """

from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import numpy as np
from matplotlib.cm import get_cmap
import matplotlib.pyplot as plt
import cmaps
from pylab import *
import scipy as sp
import scipy.ndimage
import matplotlib.gridspec as gridspec
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
from matplotlib.patches import FancyArrowPatch
from matplotlib.legend_handler import HandlerLine2D
from ipart.utils import funcs
import pandas as pd 
import numpy.ma as ma
from scipy.interpolate import interp1d
from scipy.interpolate import griddata

data  = Dataset("ivt_march_daymean1-THR-kernel-t360-s20.nc")

idt1  = data.variables['idt'][16,:,:]
idt = idt1*1000
#=== Take time average===========
#idt = np.mean(idt1[:,:,:],axis=0)
#== interpolation ======

#idt2  = np.mean(idt1[:,:,:], axis = 0)
#idt   = idt2*100000

#==== Mask out =================
#idt = ma.masked_where(np.isnan(idt1),idt1)
#idt = ma.masked_invalid(idt1)
#idt   = idt2.dropna()

lon = data.variables['lon'][:]
lat = data.variables['lat'][:]

#lon = np.clip(lon, -180, 180)
#===interpolation===
#idt = griddata(3, idt, (lon, lat), method='nearest')

fig,ax = plt.subplots(figsize=(8,7))
#=== ortho gonal ======================================
m = Basemap(projection='ortho',lon_0=80,lat_0=20)
parallels = np.arange(-90.,90,30.)
m.drawparallels(parallels,dashes=[2, 2], color='grey') # draw parallels 畫緯度線
meridians = np.arange(0.,360.,20.)
m.drawmeridians(meridians,dashes=[2, 2], color='grey') # draw meridians 畫經度線

#==== Robinson projection ========
#m = Basemap(projection='robin',lon_0=0,resolution='c')
#m.drawparallels(np.arange(-90.,120.,30.))
#m.drawmeridians(np.arange(0.,360.,60.))

lon1, lat1 = np.meshgrid(lon, lat)
x, y = m(lon1, lat1)
#ax = m.pcolormesh(x,y,np.squeeze(idt),cmap=cmaps.cmocean_curl)
ax = m.contourf(x,y,np.squeeze(idt),1000,cmap=cmaps.cmocean_curl) #CBR_coldhot)
#m.drawparallels(np.arange(10, 60, 15), linewidth=0.5, dashes=[4, 1], labels=[1,0,0,0], fontsize=10, color='black')
#m.drawmeridians(np.arange(45, 125,15),linewidth=0.5, dashes=[4, 1],  color='black')
m.drawcountries()
m.drawcoastlines(linewidth=0.3)
#plt.clim(10, 1200)
plt.title('2021-March-16',y=1.1,fontsize=20)
cbar = plt.colorbar(ax,orientation='vertical')
cbar.set_label(r'IDT  [$10^{-3}$ $Kg  m^{-1} s^{-1}$]',fontsize=12,labelpad=10)

#cax = fig.add_axes([0.885,0.04,0.023,0.915])   # left, bottom, width, and height
#cbar= fig.colorbar(ax, cax=cax,ticks=[10, 100,200,300,400,500,600,700,800,900,1000,1100,1200]) #,7,8,9,10])
#cbar.set_label(r'IDT  [$Kg  m^{-1} m^{-1}$]',fontsize=8,labelpad=0)
#cbar.ax.tick_params(labelsize=7)


plt.show()
