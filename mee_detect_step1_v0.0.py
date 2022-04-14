from datetime import datetime
START = datetime.now()
from netCDF4 import Dataset
import numpy as np
from datetime import date

# Hobday et al., 2016
# https://github.com/ecjoliver/marineHeatWaves
import marineHeatWaves as mhw

###########     
# OPTIONS #
###########
print("OPTIONS") 

# BEGIN CHOICE
model='oisst'
resolution='1440x720'
region='7W37E-30N46N' 
target='MHW' #MHW (marine heatwaves) / MCS (coldspells)
yearbeg=1982
yearend=2021  
# END CHOICE

if target == 'MHW':
   target_boolean=False
elif taregt == 'MCS':
   target_boolean=True


################   
# IMPORT DATA  #
################
# It should be daily SST in (time,lat,lon)
print("IMPORT DATA")
   
pathdatainput="/media/ajsimon/Elements/DATA/NOAA.OISST.V2.HIGHRES"
pathdataoutput="/media/ajsimon/Elements/DATA/MEE/NPY.DETECT"

file_name= f'{pathdatainput}/{model}.sst.day.mean.{yearbeg}{yearend}.{resolution}.{region}.nc'
print(file_name)
fh = Dataset(file_name, mode='r')
sst= fh.variables['sst'][:] 
lat = fh.variables['lat'][:]
lon = fh.variables['lon'][:]
print("sst",np.shape(sst))
print("lon",np.shape(lon))
print("lat",np.shape(lat))
fh.close()

#############    
# DETECTION #
#############
print("DETECTION")

t = np.arange(date(yearbeg,1,1).toordinal(),date(yearend,12,31).toordinal()+1)
dates = [date.fromordinal(tt.astype(int)) for tt in t]

mhwnpy  = {}
climnpy = {}
for i in np.arange(lon.shape[0]): 
	for j in np.arange(lat.shape[0]):
		if sst[:,j,i].any() == True:
		   mhws, clim = mhw.detect(t, sst[:,j,i],coldSpells = target_boolean)
		   auxmhw = {(i, j):mhws}
		   mhwnpy.update(auxmhw)
		   auxclim = {(i, j):clim}
		   climnpy.update(auxclim)		   

########    
# SAVE #
########	
print("SAVE")
	
np.save(f'{pathdataoutput}/{model}.{target}.{yearbeg}{yearend}.{resolution}.{region}.npy', mhwnpy)
np.save(f'{pathdataoutput}/{model}.clim-{target}.{yearbeg}{yearend}.{resolution}.{region}.npy', climnpy)

del mhwnpy
del climnpy	

END = datetime.now()
DIFF = (END - START)
print(f'It took {int(DIFF.total_seconds() / 60)} minutes')

