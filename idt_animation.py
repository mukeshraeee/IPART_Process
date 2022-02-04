""" plot dust transport from IPART MERRA-2 Data"""
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
from matplotlib.offsetbox import AnchoredText
from pathlib import Path
import imageio
import xarray as xr
from IPython.display import HTML, display
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.mpl.ticker as cticker
import cartopy.feature as cfeat
import cartopy.feature as cfeature
import matplotlib.transforms as mtransforms
from mpl_toolkits.axes_grid1 import make_axes_locatable
import wrf
from wrf import (to_np, getvar,interplevel, smooth2d, get_basemap, latlon_coords, ALL_TIMES)
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)
from matplotlib._png import read_png
from matplotlib.cbook import get_sample_data
import matplotlib.image as mpimg
import matplotlib.image as image
from PIL import Image

""" Get data """
data  = Dataset("ivt_march_daymean1-THR-kernel-t360-s20.nc")
idt1  = data.variables['idt'][:,:,:]
idt = idt1*1000
lon = data.variables['lon'][:]
lat = data.variables['lat'][:]
time = data.variables['time'][:]
""" Create plots for each time """

for i in range(31):
		fig,ax = plt.subplots(figsize=(8,7))
		plt.style.use('dark_background')
		m = Basemap(projection='ortho',lon_0=80,lat_0=20)
		parallels = np.arange(-90.,90,30.)
		m.drawparallels(parallels,dashes=[2, 2], color='grey') # draw parallels
		meridians = np.arange(0.,360.,20.)
		m.drawmeridians(meridians,dashes=[2, 2], color='grey') # draw meridians
		lon1, lat1 = np.meshgrid(lon, lat)
		x, y = m(lon1, lat1)
		ax = m.contourf(x,y,idt[i,:,:],1000,cmap=cmaps.cmocean_curl)
		m.drawcountries(color='white',linewidth=0.3)
		m.drawcoastlines(color='white',linewidth=0.3)
		#=== Add colorbar ==========
		cbar = plt.colorbar(ax,orientation='vertical')
		cbar.set_label(r'IDT  [$10^{-3}$ $Kg  m^{-1} s^{-1}$]',fontsize=12,labelpad=10)
		plt.title("2021-March-"+str(i),fontsize=16,y=1.08)
		#=== Add twitter logos ==========================
		ax1 = plt.axes([0.05, 0.01, 0.08, 0.09]) ##left, bottom, width, height
		ax1.axis('off')
		tw = "twitter.png"
		twi = plt.imread(tw)
		plt.title("@mukeshraee")
		ax1.imshow(twi,zorder=10,origin='upper',alpha=0.9,aspect='auto')
		#==== Add Instagram logo =========================================
		ax2 = plt.axes([0.25, 0.01, 0.08, 0.09])
		ax2.axis('off')
		ins = "insta.png"
		insta = plt.imread(ins)
		plt.title("@mukesh_raee")
		ax2.imshow(insta,zorder=10,origin='upper',alpha=0.9,aspect='auto')
		#=== Add Linkdein logo ==============================================
		ax3 = plt.axes([0.45, 0.01, 0.08, 0.09])
		ax3.axis('off')
		lin = "Linkedin.png"
		link = plt.imread(lin)
		plt.title("@Mukesh Rai")
		ax3.imshow(link,zorder=10,origin='upper',alpha=0.9,aspect='auto')

		plt.savefig(f"/mnt/g/datas/Training/IPART/merra-2/2021_mar/figures/idt_{i:04}.png")
		plt.close()
#plt.show()
