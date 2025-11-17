#cmhw
# time series of mhw number of days.

import time
start_time_script = time.time()

import xarray as xr
import dask.array as da
import numpy as np

from netCDF4 import Dataset
from datetime import date, datetime

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import pandas as pd
import math  

###########     
# OPTIONS #
###########
print("OPTIONS") 

pathdata="/home/asimon/Documents/WORK/STUDY/MHW_202501/DATA"
pathoutputfig="/home/asimon/Documents/WORK/STUDY/MHW_202501/PLOT"

# input data
model='oisst' #oisst cmems 
yearbeg=1982 
yearend=2024  #2024
region='40W15W-5N125N' #'7W37E-30N46N' #'3E8E-39N44N' #'7W37E-30N46N' # '40W15W-5N125N'
choice_mask_region=0 #-1=no mask 4=Med
choice_date=0 #0=no, 1=yes (choose start_date and end_date)
start_mth=6 #3 #6 #3
start_day=1 #28 #1 #28
end_mth=9 #9 #4 #8 #4
end_day=30 #30 #14 #31 #14
print("choice_mask_region",choice_mask_region)

#import_data
import_data = 'y'

#Calculation
mhw_calculation = 'y'
detrend=0 #0/1
clim_start_year = 1982
clim_end_year   = 2024
percentile = 0.9
min_duration_mhw=5
min_gap_mhw=2 
dt_clim='time.dayofyear' #'time.dayofyear'  # 'time.month'
dt='day'

print("OPTIONS/PLOT")
plot = 'y'
size_fonte=14 
format_fig='png'
dpi_value=150   

#np.set_printoptions(threshold=np.inf)
   
################   
# IMPORT DATA  #
################
if import_data == 'y':
   print("TIME IMPORT DATA - START", (time.time() - start_time_script)/60)

   ds = xr.open_dataset(f'{pathdata}/{model}/{model}.sst.{dt}.mean.{yearbeg}{yearend}.{region}.nc', engine='netcdf4')  #0928
   #ds = xr.open_dataset(f'{pathdata}/{model}/{model}.sst.{dt}.mean.{yearbeg}{yearend}0928.{region}.nc', engine='netcdf4') 
   sst = ds.sst
   print("type(var)", type(sst))
   print("sst.shape",sst.shape)
   print("sst.dims",sst.dims)
   ds_grid=xr.open_dataset(f'{pathdata}/{model}/gridarea.{model}.{region}.nc', engine='netcdf4')
   print(ds_grid)
   cell_area = ds_grid.cell_area

   if choice_mask_region > 0:
      mask_region = np.load(f'{pathdata}/OceanMasks_oisst_{region}.npy')
      if model != 'oisst':
         mask_interp = xr.DataArray(mask_region,
                           dims=('lat', 'lon'),
                           coords={'lat': ds['lat'].values, 'lon': ds['lon'].values})
         mask_region = mask_interp.interp(lat=ds.lat, lon=ds.lon, method='nearest')
      print("mask_region",mask_region)
      print("np.shape(mask_region)",np.shape(mask_region))      
      sst = sst.where(mask_region == choice_mask_region)
   
   sst.isel(time=0).plot()
   plt.savefig(f'{pathoutputfig}/test.{model}.{region}.{format_fig}', format=f'{format_fig}')
   plt.close()
   
   mask_ocean = 1 * np.ones(sst.shape[1:]) * np.isfinite(sst.isel(time=0))
   mask_land = 0 * np.ones(sst.shape[1:]) * np.isnan(sst.isel(time=0))
   mask = mask_ocean + mask_land
   mask.plot()
   plt.savefig(f'{pathoutputfig}/mask_for_plot.{model}.{region}.{format_fig}', format=f'{format_fig}')
   plt.close()
   
   if choice_date == 1: # 
      print("choice_date") 
      if start_mth <= end_mth:
          # Case 1: Normal range (e.g., June 15 - September 30)
          mask_date = ((sst['time.month'] > start_mth) & (sst['time.month'] < end_mth)) | \
                   ((sst['time.month'] == start_mth) & (sst['time.day'] >= start_day)) | \
                   ((sst['time.month'] == end_mth) & (sst['time.day'] <= end_day))  
      else:
          # Case 2: Wrapping around the new year (e.g., December 10 - March 15)
          mask_date = ((sst['time.month'] > start_mth) | (sst['time.month'] < end_mth)) | \
                   ((sst['time.month'] == start_mth) & (sst['time.day'] >= start_day)) | \
                   ((sst['time.month'] == end_mth) & (sst['time.day'] <= end_day))
      filtered_values = sst[mask_date]
      # Select data using the mask
      sst = sst.sel(time=mask_date)   
   
###################   
# MHW CALCULATION #
###################
if mhw_calculation == 'y':
   print("TIME MHW_CALCULATION - START", (time.time() - start_time_script)/60)
   print("np.shape(sst)",np.shape(sst))
   ##############
   # Detrending
   if detrend == 1:
       time_axis = np.arange(len(sst['time']))
       print("time", time_axis)
       # Initialize an array to store the detrended SST data
       sst_detrended = np.zeros_like(sst)  # Same shape as sst

       # Reshape sst to a 2D array where each column is a time series for a (lat, lon) point
       sst_reshaped = sst.values.reshape(sst.sizes['time'], -1)
       # Perform regression on each time series
       trends = np.polyfit(time_axis, sst_reshaped, detrend)
       # Calculate the trend lines for each time series
       trend_lines = trends[0, :] * time_axis[:, np.newaxis] + trends[1, :]
       # Reshape trend_lines back to the original shape
       trend_lines_reshaped = trend_lines.reshape(sst.sizes['time'], sst.sizes['lat'], sst.sizes['lon'])

       # Subtract the trend from the original sst array
       sst_detrended = sst.values - trend_lines_reshaped
       sst = xr.DataArray(
       sst_detrended,
       dims=sst.dims,
       coords=sst.coords,
       attrs=sst.attrs,
       name=sst.name
       )
       
       #sst.rename("sst_detrended").to_netcdf(f"{pathdata}/OUTPUT/sst.detrend{detrend}_{model}.{yearbeg}{yearend}.{region}.start{start_day}-{start_mth}to{end_day}-{end_mth}.{region}.nc")  
       
   #sst.rename("sst").to_netcdf(f"{pathdata}/OUTPUT/sst.detrend{detrend}_{model}.{yearbeg}{yearend}.{region}.start{start_day}-{start_mth}to{end_day}-{end_mth}.{region}.nc") 
   ##############
   # Threshold
   sst_clim_period = sst.sel(time=slice(f"{clim_start_year}-01-01", f"{clim_end_year}-12-31"))
   climatology = sst_clim_period.groupby(dt_clim).mean().rolling(dayofyear=11, center=True, min_periods=1).mean()
   sstanomalyclim = sst.groupby(dt_clim) - climatology
   #sstanomalyclim.rename("sst_deseasonalized").to_netcdf(f"{pathdata}/OUTPUT/sst.detrend{detrend}.deseasonalized1_{model}.{yearbeg}{yearend}.{region}.start{start_day}-{start_mth}to{end_day}-{end_mth}.{region}.nc")  
   threshold = sst.groupby(dt_clim).quantile(percentile, dim='time', keep_attrs=True, skipna=True)
   mhw_meanintensity_all = sstanomalyclim.groupby(dt_clim).where(sst.groupby(dt_clim)>threshold)
   print("TIME MHW_CALCULATION - AFTER THRESHOLD", (time.time() - start_time_script)/60)
   del climatology, threshold
   
   ##############
   # min_duration & min_gap
   def filter_short_sequences(da, min_duration=min_duration_mhw-1, min_gap=min_gap_mhw):
       filtered_da = da.copy()
       # Iterate over each grid cell
       for i in range(da.sizes['lat']): #range(13,14): ##: 
           for j in range(da.sizes['lon']): #range(16,17): #range(da.sizes['lon']):  #range(da.sizes['lon']):
               # Extract the time series for the current grid cell
               ts = da.isel(lat=i, lon=j)   
               # Check if the time series is not empty
               if ts.sizes['time'] > 0:
                 # 1. FIND ALL WARM SEQUENCE
                ts_values = ts.notnull().values
                changes = np.diff(ts_values.astype(int))
                starts = np.where(changes == 1)[0] + 1
                ends = np.where(changes == -1)[0]
                # Handle edge cases
                if ts_values[0]:
                    starts = np.insert(starts, 0, 0)
                if ts_values[-1]:
                    ends = np.append(ends, len(ts_values) - 1)

                if starts.size > 0:                   
                    # 2. REMOVE EVENTS < min_duration_mhw
                    good_runs = []
                    for i_start, i_end in list(zip(starts, ends)):
                       if (i_end - i_start) >= min_duration:
                          good_runs.append((i_start, i_end))
                       else:
                          filtered_da.isel(lat=i, lon=j)[i_start:i_end+1] = np.nan
                        
                    if len(good_runs) == 0:
                        continue
                     
                    # 3. MERGED EVENTS < min_gap    
                    merged = []
                    current_start, current_end = good_runs[0]
                    for i_start, i_end in good_runs[1:]:
                       gap = i_start - current_end - 1  # number of cool days between two warm events                       
                       if gap <= min_gap:
                           # ---- fill gap with sst ----
                           filtered_da.isel(lat=i, lon=j)[current_end +1 : i_start] = sstanomalyclim.isel(lat=i, lon=j, time=slice(current_end+1,i_start))
                           # extend merged event
                           current_end = i_end
                       else:
                           merged.append((current_start, current_end))
                           current_start, current_end = i_start, i_end
                    merged.append((current_start, current_end))
       return filtered_da     

   mhw_meanintensity_filtered = filter_short_sequences(mhw_meanintensity_all)
   mhw_meanintensity_filtered.rename("mhw_meanintensity_filtered").to_netcdf(f"{pathdata}/OUTPUT/MHWmeanintensity.threshold-percentile{percentile}-clim{clim_start_year}-{clim_end_year}.minduration{min_duration_mhw}.min_gap{min_gap_mhw}.detrend{detrend}_{model}.{yearbeg}{yearend}.{region}.start{start_day}-{start_mth}to{end_day}-{end_mth}.{region}.nc")
   del mhw_meanintensity_filtered

#########
# PLOT #
########
if plot == 'y':
   print("TIME PLOT - START", (time.time() - start_time_script)/60)
   ds = xr.open_dataset(f"{pathdata}/OUTPUT/MHWmeanintensity.threshold-percentile{percentile}-clim{clim_start_year}-{clim_end_year}.minduration{min_duration_mhw}.min_gap{min_gap_mhw}.detrend{detrend}_{model}.{yearbeg}{yearend}.{region}.start{start_day}-{start_mth}to{end_day}-{end_mth}.{region}.nc")
   #print("ds",ds)
   mhw_meanintensity_filtered = ds["mhw_meanintensity_filtered"]
   print("mhw_meanintensity_filtered",mhw_meanintensity_filtered.shape)
   print("mhw_meanintensity_filtered",type(mhw_meanintensity_filtered))
   year_range=range(yearbeg,yearend+1)
  
   ###############
   # Intensity
   print("TIME PLOT - INTENSITY", (time.time() - start_time_script)/60)
   mhw_meanintensity_per_year = (
       mhw_meanintensity_filtered
       .where(mhw_meanintensity_filtered != 0)   # mask out zeros
       .groupby('time.year')
       .mean(dim='time', skipna=True)   # compute mean ignoring NaN (and zeros now masked)
       .mean(dim=('lon', 'lat'), skipna=True)
   )

   plt.figure(figsize=(7, 4))
   plt.plot(year_range, mhw_meanintensity_per_year,  c = 'red', marker='o')
   plt.ylabel("Mean intensity (°C) ", fontsize=size_fonte)
   plt.title(f"Region {region} - day {start_day} mth {start_mth} to day {end_day} mth {end_mth}", fontsize=size_fonte)
   plt.xticks(fontsize=size_fonte)
   plt.yticks(fontsize=size_fonte)
   plt.grid(True)
   plt.savefig(f'{pathoutputfig}/MHW.mean_intensity.{model}.{yearbeg}{yearend}.{region}.start{start_day}-{start_mth}to{end_day}-{end_mth}.{region}.detrend{detrend}.png')
   plt.close()
   
   
   ###################
   # MHW feaures
   events_count = xr.DataArray(
       np.zeros((len(mhw_meanintensity_filtered.time), len(mhw_meanintensity_filtered.lat), len(mhw_meanintensity_filtered.lon))),
       dims=('time', 'lat', 'lon'),
       coords={'time': mhw_meanintensity_filtered.time, 'lat': mhw_meanintensity_filtered.lat, 'lon': mhw_meanintensity_filtered.lon}
   )
   
   event_records  = []

   # Iterate over each grid cell
   for i in range(len(mhw_meanintensity_filtered.lat)):
       for j in range(len(mhw_meanintensity_filtered.lon)):
           # Extract the time series for the current grid cell
           intensity_series = mhw_meanintensity_filtered.isel(lat=i, lon=j)
           #print("intensity_series",intensity_series)
           # Identify where the intensity is greater than 0
           mhw_events = (intensity_series > 0).astype(int)
           #print("mhw_events",mhw_events)
           # Find the changes in the event status (start or end of an event)
           event_changes = np.diff(mhw_events, prepend=0)
           # Find the indices where events start and end          
           event_starts = np.where(event_changes == 1)[0]
           event_ends   = np.where(event_changes == -1)[0]                  
           #print("mhw_events",mhw_events)
           # Ensure that the number of starts and ends match
           if len(event_starts) > len(event_ends):
               event_ends = np.append(event_ends, len(mhw_events) - 1)
           # Count the number of events (each event start is marked by a positive change)
           events_count[:, i, j] = event_changes    
           for start, end in zip(event_starts, event_ends):
               start_time = mhw_meanintensity_filtered.time.isel(time=start).item()
               end_time = mhw_meanintensity_filtered.time.isel(time=end).item()
               duration = end - start
               area_cell = float(cell_area.isel(lat=i, lon=j).values)
               year      = pd.Timestamp(start_time).year
               event_records.append({
                   "year": year,
                   "duration": duration,
                   "start_time": start_time,
                   "end_time": end_time,
                   "area": area_cell,
                   "lat": mhw_meanintensity_filtered.lat.isel(lat=i).item(),
                   "lon": mhw_meanintensity_filtered.lon.isel(lon=j).item()
               })    
                
   event_df = pd.DataFrame(event_records)
   print(event_df.head())
   
   ### number of event
   print("TIME PLOT - NUMBER EVENTS", (time.time() - start_time_script)/60)
   total_events = (events_count == 1).sum(dim=('lat', 'lon'))
   events_per_year = (
       total_events
       .where(total_events != 0)   # mask out zeros
       .groupby('time.year')
       .mean(dim='time', skipna=True)   # compute mean ignoring NaN (and zeros now masked)
   )

   plt.figure(figsize=(7, 4))
   plt.plot(year_range, events_per_year,  c = 'red', marker='o')
   plt.ylabel("Mean number of events (-) ", fontsize=size_fonte) # over the area
   plt.title(f"Region {region} - day {start_day} mth {start_mth} to day {end_day} mth {end_mth}", fontsize=size_fonte)
   plt.xticks(fontsize=size_fonte)
   plt.yticks(fontsize=size_fonte)
   plt.grid(True)
   plt.savefig(f'{pathoutputfig}/MHW.nbevents.{model}.{yearbeg}{yearend}.start{start_day}-{start_mth}to{end_day}-{end_mth}.{region}.detrend{detrend}.png')
   plt.close()
   

   
   # map activity for all years
   min_value_leg=0
   max_value_leg=2e11
   n_years = yearend - yearbeg +1 
   years = range(yearbeg, yearend + 1)
   ncols = 6
   nrows = math.ceil(n_years / ncols)

   fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*3, nrows*2.5), constrained_layout=True)
   axes = axes.flatten()  # Flatten in case it's 2D array
   for i, year in enumerate(years):
       startdate = f'{year}-{start_mth}-{start_day}'
       if start_mth <= end_mth:
          enddate = f'{year}-{end_mth}-{end_day}'
       else:
          enddate = f'{year+1}-{end_mth}-{end_day}'       
       nb_events_plot =(mhw_meanintensity_filtered > 0).sel(time=slice(startdate, enddate)).sum(dim='time')
       ax = axes[i]
       nb_events_plot.plot(ax=ax, cmap='Reds', add_colorbar=False) #,vmin=min_value_leg, vmax=max_value_leg
       mask.where(mask == 0).plot.contourf(ax=ax, colors='k', add_colorbar=False)
       ax.set_title(f'{year}', fontsize=12)
       ax.set_xlabel('')
       ax.set_ylabel('')
   # Hide unused subplots if any
   for j in range(i + 1, len(axes)):
       axes[j].axis('off')
   # Add a global colorbar
   fig.subplots_adjust(bottom=0.15)
   cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.02])  # [left, bottom, width, height]
   nb_events_plot.plot(cmap='Reds', add_colorbar=True, cbar_ax=cbar_ax, cbar_kwargs={'orientation': 'horizontal'}) #vmin=min_value_leg,    vmax=max_value_leg
   cbar_ax.set_title('C.days.m²', fontsize=12)
   cbar_ax.set_xlabel('')
   cbar_ax.set_ylabel('')
   # Save figure
   fig.suptitle(f'MHW number of events ({start_mth}-{start_day} – {end_mth}-{end_day}) from {yearbeg} to {yearend}', fontsize=12)
   fig.savefig(f'{pathoutputfig}/MHW.map.nbevents.{model}.{region}.all_years.{start_mth}-{start_day}to{end_mth}-{end_day}.{format_fig}', format=format_fig, dpi=300)
   plt.close()

   """
      n_years = yearend - yearbeg + 1
   years = range(yearbeg, yearend + 1)
   ncols = 6
   nrows = math.ceil(n_years / ncols)
   fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*3, nrows*2.5), constrained_layout=True)
   axes = axes.flatten()
   
   for i, year in enumerate(years):
       ax = axes[i]
       # For event count, you can use the events_count array directly
       # (assuming you want the total number of events per grid cell for all years)
       # If you want per-year, you need to re-calculate or filter event_records by year
       # Here, we'll use the total events_count for simplicity
       da = events_count.sel(time=year).copy()
       da.plot(ax=ax, cmap='Reds', add_colorbar=False)
       mask.where(mask == 0).plot.contourf(ax=ax, colors='k', add_colorbar=False)
       ax.set_title(f'{year}', fontsize=12)
       ax.set_xlabel('')
       ax.set_ylabel('')

   # Hide unused subplots if any
   for j in range(i + 1, len(axes)):
       axes[j].axis('off')

   # Add a global colorbar
   fig.subplots_adjust(bottom=0.15)
   cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.02])
   events_count.plot(cmap='Reds', add_colorbar=True, cbar_ax=cbar_ax, cbar_kwargs={'orientation': 'horizontal'})
   cbar_ax.set_title('Number of events', fontsize=12)
   cbar_ax.set_xlabel('')
   cbar_ax.set_ylabel('')
   """


   
   ### duration
   print("TIME PLOT - DURATION", (time.time() - start_time_script)/60)
   durations_per_year_mean = (
       event_df.groupby("year")["duration"]
       .mean()
       .reindex(year_range, fill_value=np.nan)
   )
   durations_per_year_sum = (
       event_df.groupby("year")["duration"]
       .sum()
       .reindex(year_range, fill_value=np.nan)
   )
   
   ## time series duration
   plt.figure(figsize=(7, 4))
   plt.plot(durations_per_year_mean.index,durations_per_year_mean.values, c='red', marker='o') #durations_per_year.index, 
   plt.ylabel("Mean Duration (days)", fontsize=size_fonte) 
   plt.title(f"Region {region} - {start_day}/{start_mth} to {end_day}/{end_mth}", fontsize=size_fonte)
   plt.grid(True)
   plt.savefig(f"{pathoutputfig}/MHW.meanduration.{model}.{region}.{yearbeg}{yearend}.start{start_day}-{start_mth}to{end_day}-{end_mth}.{region}.detrend{detrend}.png", dpi=150)
   plt.close()

   
   """
   events_per_year_series = events_per_year.to_pandas()
   # Ensure index is year integers (matches durations_per_year_sum.index)
   events_per_year_series.index = events_per_year_series.index.astype(int)
   # Divide total duration by number of events
   number_days_per_year = durations_per_year_sum / total_events
   
   plt.figure(figsize=(7, 4))
   plt.plot(durations_per_year_sum.index,number_days_per_year.values, c='red', marker='o') #durations_per_year.index, 
   plt.ylabel("Sum Duration (days)", fontsize=size_fonte)
   plt.title(f"Region {region} - {start_day}/{start_mth} to {end_day}/{end_mth}", fontsize=size_fonte)
   plt.grid(True)
   plt.savefig(f"{pathoutputfig}/MHW.numbersdays.{model}.{region}.{yearbeg}{yearend}.start{start_day}-{start_mth}to{end_day}-{end_mth}.{region}.detrend{detrend}.png", dpi=150) 
   plt.close()
   """
   
   ## map duration for all years
   #min_value_leg=0
   #max_value_leg=2e11
   n_years = yearend - yearbeg +1 
   years = range(yearbeg, yearend + 1)
   ncols = 6
   nrows = math.ceil(n_years / ncols)

   fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*3, nrows*2.5), constrained_layout=True)
   axes = axes.flatten()  # Flatten in case it's 2D array
   for i, year in enumerate(years):
       startdate = f'{year}-{start_mth}-{start_day}'
       if start_mth <= end_mth:
          enddate = f'{year}-{end_mth}-{end_day}'
       else:
          enddate = f'{year+1}-{end_mth}-{end_day}'       
       ax = axes[i]
       duration_2d = (
           event_df[event_df["year"] == year]
           .groupby(["lat", "lon"])["duration"]
           .mean()
           .unstack(level="lon")
       )
       if duration_2d.empty or duration_2d.isna().all().all():
          ax.set_title(f'{year} (no data)', fontsize=12)
          ax.axis('off')
          continue
       # Convert to xarray DataArray
       da = xr.DataArray(
           duration_2d.values,
           dims=("lat", "lon"),
           coords={
               "lat": duration_2d.index,
               "lon": duration_2d.columns
           }
       )
       da.plot(ax=ax, cmap='Reds', add_colorbar=False)
       mask.where(mask == 0).plot.contourf(ax=ax, colors='k', add_colorbar=False)
       ax.set_title(f'{year}', fontsize=12)
       ax.set_xlabel('')
       ax.set_ylabel('')
   # Hide unused subplots if any
   for j in range(i + 1, len(axes)):
       axes[j].axis('off')
   # Add a global colorbar
   fig.subplots_adjust(bottom=0.15)
   cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.02])  # [left, bottom, width, height]
   da.plot(cmap='Reds', add_colorbar=True, cbar_ax=cbar_ax, cbar_kwargs={'orientation': 'horizontal'}) #, vmin=min_value_leg,    vmax=max_value_leg
   cbar_ax.set_title('m²', fontsize=12)
   cbar_ax.set_xlabel('')
   cbar_ax.set_ylabel('')

   # Save figure
   fig.suptitle(f'MHW area ({start_mth}-{start_day} – {end_mth}-{end_day}) from {yearbeg} to {yearend}', fontsize=12)
   fig.savefig(f'{pathoutputfig}/MHW.map.duration.area.{model}.{region}.all_years.{start_mth}-{start_day}to{end_mth}-{end_day}.{format_fig}', format=format_fig, dpi=300)
   plt.close()   
   
   
   ### area
   print("TIME PLOT - AREA", (time.time() - start_time_script)/60)
   area_per_year_mean = (
       event_df.groupby("year")["area"]
       .sum()
       .reindex(year_range, fill_value=0)
      ) 
   
   area_per_year_sum = (
       event_df.groupby("year")["area"]
       .sum()
       .reindex(year_range, fill_value=0)
      ) 
      
   ## time series area
   plt.figure(figsize=(7, 4))
   plt.plot(area_per_year_mean.index,area_per_year_mean.values/ 1e6, c='red', marker='o') #durations_per_year.index, 
   plt.ylabel("Mean area (km²)", fontsize=size_fonte) 
   plt.title(f"Region {region} - {start_day}/{start_mth} to {end_day}/{end_mth}", fontsize=size_fonte)
   plt.grid(True)
   plt.savefig(f"{pathoutputfig}/MHW.meanarea.{model}.{region}.{yearbeg}{yearend}.start{start_day}-{start_mth}to{end_day}-{end_mth}.{region}.detrend{detrend}.png", dpi=150)
   plt.close()

   plt.figure(figsize=(7, 4))
   plt.plot(area_per_year_sum.index,area_per_year_sum.values/ 1e6, c='red', marker='o') #durations_per_year.index, 
   plt.ylabel("Sum area (km2)", fontsize=size_fonte)
   plt.title(f"Region {region} - {start_day}/{start_mth} to {end_day}/{end_mth}", fontsize=size_fonte)
   plt.grid(True)
   plt.savefig(f"{pathoutputfig}/MHW.sumarea.{model}.{region}.{yearbeg}{yearend}.start{start_day}-{start_mth}to{end_day}-{end_mth}.{region}.detrend{detrend}.png", dpi=150) 
   plt.close()
   
   ## map area for all years
   #min_value_leg=0
   #max_value_leg=2e11

   fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*3, nrows*2.5), constrained_layout=True)
   axes = axes.flatten()  # Flatten in case it's 2D array
   for i, year in enumerate(years):
       startdate = f'{year}-{start_mth}-{start_day}'
       if start_mth <= end_mth:
          enddate = f'{year}-{end_mth}-{end_day}'
       else:
          enddate = f'{year+1}-{end_mth}-{end_day}'       
       ax = axes[i]
       area_2d = (
           event_df[event_df["year"] == year]
           .groupby(["lat", "lon"])["area"]
           .mean()
           .unstack(level="lon")
       )
       if area_2d.empty or area_2d.isna().all().all():
          ax.set_title(f'{year} (no data)', fontsize=12)
          ax.axis('off')
          continue
       # Convert to xarray DataArray
       da = xr.DataArray(
           area_2d.values,
           dims=("lat", "lon"),
           coords={
               "lat": area_2d.index,
               "lon": area_2d.columns
           }
       )
       da.plot(ax=ax, cmap='Reds', add_colorbar=False)
       mask.where(mask == 0).plot.contourf(ax=ax, colors='k', add_colorbar=False)
       ax.set_title(f'{year}', fontsize=12)
       ax.set_xlabel('')
       ax.set_ylabel('')
   # Hide unused subplots if any
   for j in range(i + 1, len(axes)):
       axes[j].axis('off')
   # Add a global colorbar
   fig.subplots_adjust(bottom=0.15)
   cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.02])  # [left, bottom, width, height]
   da.plot(cmap='Reds', add_colorbar=True, cbar_ax=cbar_ax, cbar_kwargs={'orientation': 'horizontal'}) # , vmin=min_value_leg,    vmax=max_value_leg
   cbar_ax.set_title('m²', fontsize=12)
   cbar_ax.set_xlabel('')
   cbar_ax.set_ylabel('')

   # Save figure
   fig.suptitle(f'MHW area ({start_mth}-{start_day} – {end_mth}-{end_day}) from {yearbeg} to {yearend}', fontsize=12)
   fig.savefig(f'{pathoutputfig}/MHW.map.area.{model}.{region}.all_years.{start_mth}-{start_day}to{end_mth}-{end_day}.{format_fig}', format=format_fig, dpi=300)
   plt.close()

   ### activity
   print("TIME PLOT - ACTIVITY", (time.time() - start_time_script)/60)
   mhw_meanintensity_weighted= mhw_meanintensity_filtered * cell_area
   activity_sum_per_year = mhw_meanintensity_weighted.groupby('time.year').sum(dim='time')
   # Then, sum over the 'lon' and 'lat' dimensions to get a single value per year
   total_activity = activity_sum_per_year.sum(dim=['lon', 'lat'])

   ## time series activity
   model_1=np.polyfit(year_range,total_activity,2)
   predict_1 = np.poly1d(model_1)
   y_lin_reg_1 = predict_1(year_range)

   plt.figure(figsize=(7, 4))
   plt.plot(year_range,y_lin_reg_1/10**(12), c = 'red', linestyle='--')
   plt.plot(year_range, total_activity/10**(12),  c = 'red', marker='o')
   plt.ylabel("MHWs Activity (°C.days.10⁶km²) ", fontsize=size_fonte)
   plt.title(f"Region {region} - day {start_day} mth {start_mth} to day {end_day} mth {end_mth}", fontsize=size_fonte)
   plt.xticks(fontsize=size_fonte)
   plt.yticks(fontsize=size_fonte)
   plt.grid(True)
   plt.savefig(f'{pathoutputfig}/MHW.total_activity.{model}.{yearbeg}{yearend}.{region}.start{start_day}-{start_mth}to{end_day}-{end_mth}.png')
   plt.close()

   ## map activity 
   #map activity for one specific year
   min_value_leg=0
   max_value_leg=10e10    
   plt.figure(figsize=(7, 4))
   startdate = f'2003-{start_mth}-{start_day}'
   enddate = f'2003-{end_mth}-{end_day}'  
   activity_a = mhw_meanintensity_filtered.sel(time=slice(startdate, enddate)).sum(dim='time') * cell_area
   activity_a.plot(cmap='Reds', add_colorbar=False,vmin=min_value_leg, vmax=max_value_leg)
   mask.where(mask == 0).plot.contourf(colors='k', add_colorbar=False)
   plt.savefig(f'{pathoutputfig}/MHW.activity.{model}.{region}.2003.{start_mth}-{start_day}to{end_mth}-{end_day}.{format_fig}',     
   format=format_fig, dpi=300)
   plt.close()
 
   # map activity for all years
   min_value_leg=0
   max_value_leg=2e11
   n_years = yearend - yearbeg +1 
   years = range(yearbeg, yearend + 1)
   ncols = 6
   nrows = math.ceil(n_years / ncols)

   fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*3, nrows*2.5), constrained_layout=True)
   axes = axes.flatten()  # Flatten in case it's 2D array
   for i, year in enumerate(years):
       startdate = f'{year}-{start_mth}-{start_day}'
       if start_mth <= end_mth:
          enddate = f'{year}-{end_mth}-{end_day}'
       else:
          enddate = f'{year+1}-{end_mth}-{end_day}'       
       activity_plot = mhw_meanintensity_filtered.sel(time=slice(startdate, enddate)).sum(dim='time') * cell_area
       ax = axes[i]
       activity_plot.plot(ax=ax, cmap='Reds', add_colorbar=False,vmin=min_value_leg, vmax=max_value_leg)
       mask.where(mask == 0).plot.contourf(ax=ax, colors='k', add_colorbar=False)
       ax.set_title(f'{year}', fontsize=12)
       ax.set_xlabel('')
       ax.set_ylabel('')
   # Hide unused subplots if any
   for j in range(i + 1, len(axes)):
       axes[j].axis('off')
   # Add a global colorbar
   fig.subplots_adjust(bottom=0.15)
   cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.02])  # [left, bottom, width, height]
   activity_plot.plot(cmap='Reds', add_colorbar=True, cbar_ax=cbar_ax, cbar_kwargs={'orientation': 'horizontal'}, vmin=min_value_leg,    vmax=max_value_leg) #
   cbar_ax.set_title('C.days.m²', fontsize=12)
   cbar_ax.set_xlabel('')
   cbar_ax.set_ylabel('')
   fig.suptitle(f'MHW Activity ({start_mth}-{start_day} – {end_mth}-{end_day}) from {yearbeg} to {yearend}', fontsize=12)
   fig.savefig(f'{pathoutputfig}/MHW.activity.{model}.{region}.all_years.{start_mth}-{start_day}to{end_mth}-{end_day}.{format_fig}', format=format_fig, dpi=300)
   plt.close()

#######
# END #
#######
duration_script = time.time() - start_time_script
print(f"Script executed in {int(duration_script / 60)} minutes or {int(duration_script / 3600)} hours.")
