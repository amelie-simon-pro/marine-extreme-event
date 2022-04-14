from datetime import datetime
START = datetime.now()

from netCDF4 import Dataset
from datetime import date
import numpy as np
import os

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

###########     
# OPTIONS #
###########
print("OPTIONS") 

# BEGIN CHOICE
# action y/n
python='y' 
load_nc='y'
loop='y'
plot_map='y'  
plot_ts='y'
rank='y'
latex='y'
# data
model='oisst'
resolution='1440x720'
region='7W37E-30N46N'
lonmin=-7
lonmax=37
latmin=30 
latmax=46 
target='MHW' #MHW (marine heatwaves) / MCS (coldspells)
season='JJAS' 
yearbeg=1982
yearend=2021
subseas=4
# plot
ft_title=16
shrink=0.65
ft_label=16
ft_tick=16
legend_orientation='horizontal'
leg_max_nevent=8
leg_max_duration=52
leg_min_duration=12
leg_max_int_mean=4.2
leg_min_int_mean=0.8
leg_max_activity=128
end='' # ''/'_test'
# END CHOICE

nevents_max=120 
nbyear=yearend-yearbeg+1

################   
# IMPORT DATA  #
################
print("IMPORT DATA")

pathdata="/media/ajsimon/Elements/DATA"
pathoutputfig="/home/ajsimon/Documents/WORK/POSTDOC_IDL/PROJETS/PLOT/MHW/FIGURE_RAW"
pathoutputlatex="/home/ajsimon/Documents/WORK/POSTDOC_IDL/PROJETS/PLOT/MHW/LATEX"
data=f'{model}.{target}.{yearbeg}{yearend}.{resolution}.{region}'

if load_nc == 'y':
   print("LOAD DATA")
   
   mhw_r1=np.load(f'{pathdata}/MEE/NPY.DETECT/{model}.{target}.{yearbeg}{yearend}.{resolution}.{region}.npy',allow_pickle=True).item()
   clim_r1=np.load(f'{pathdata}/MEE/NPY.DETECT/{model}.clim-{target}.{yearbeg}{yearend}.{resolution}.{region}.npy',allow_pickle=True).item()
   print(f'{pathdata}/MEE/NPY.DETECT/{model}.{target}.{yearbeg}{yearend}.{resolution}.{region}.npy')

   file_name=f'{pathdata}/GRID/gridarea.{resolution}.{region}.nc' 
   # example to create this file: cdo gridarea oisst.sst.day.mean.19822021.1440x720.7W11E-30N46N.nc gridarea.1440x720.7W11E-30N46N.nc
   fh = Dataset(file_name, mode='r')
   lat = fh.variables['lat'][:]
   lon = fh.variables['lon'][:]
   cell_area = fh.variables['cell_area'][:]
   fh.close()
   print(lat)
   print(lon)
   print("np.shape(lon.shape)",np.shape(lon))
   print("np.shape(lat.shape)",np.shape(lat))
   print("np.shape(cell_area)",np.shape(cell_area)) # (lat,lon)
   
   mask_seas=np.load(f'{pathdata}/MASK/OceanMasks0.25x0.25_{region}.npy')

if loop == 'y':
   print("BEGIN LOOP")
   activity_domain=np.zeros(nbyear)   
   for year in range(yearbeg,yearend+1):
   #for year in [2018]:
      print(year)
      if season == 'DJFM':
         year1=year-1
         month_beg=12
         day_beg=1
         year2=year
         month_end=3
         day_end=31
      elif season == 'JJAS':
         year1=year
         month_beg=6
         day_beg=1
         year2=year
         month_end=9
         day_end=30
      
      t = np.arange(date(year1,month_beg,day_beg).toordinal(),date(year2,month_end,day_end).toordinal()+1)
      dates = [date.fromordinal(tt.astype(int)) for tt in t]
      print(date.fromordinal(t[0]))
      print(date.fromordinal(t[-1]))
   
      nevents=np.zeros((lat.shape[0],lon.shape[0]))
      duration=np.zeros((lat.shape[0],lon.shape[0]))
      intensity_mean=np.zeros((lat.shape[0],lon.shape[0]))
      activity=np.zeros((lat.shape[0],lon.shape[0]))

      nevents_all=np.zeros((lat.shape[0],lon.shape[0]))
      intensity_mean_all=np.zeros((lat.shape[0],lon.shape[0],nevents_max))
      duration_all=np.zeros((lat.shape[0],lon.shape[0],nevents_max))
   
      for i in range(lon.shape[0]):
         for j in range(lat.shape[0]):
            if ((mask_seas[j,i]==subseas)):
               if ((lonmin <= lon[i] <= lonmax) and (latmin <= lat[j] <= latmax)):
                  cont_event=0
                  pos_r1=(i,j)
                  if pos_r1 in mhw_r1.keys():
                     nevents_all[j,i]=(mhw_r1[(i,j)]['n_events'])
                     if (nevents_all[j,i]>0):
                        for nb in range(int(nevents_all[j,i])):
                           if (mhw_r1[i,j]['date_start'][nb].toordinal() < t[0]) and (mhw_r1[i,j]['date_end'][nb].toordinal() > t[-1]):
                              activity[j,i] += mhw_r1[(i,j)]['intensity_mean'][nb]*(t[-1]-t[0])*cell_area[j,i]
                              intensity_mean_all[j,i,cont_event]=mhw_r1[(i,j)]['intensity_mean'][nb]
                              duration_all[j,i,cont_event]=mhw_r1[(i,j)]['duration'][nb]
                              nevents[j,i]=nevents[j,i]+1
                              cont_event=cont_event+1
                           for t_day in t:
                              if (mhw_r1[i,j]['date_start'][nb].toordinal() == t_day) and (mhw_r1[i,j]['date_end'][nb].toordinal() <= t[-1]):
                                 activity[j,i] += mhw_r1[(i,j)]['intensity_mean'][nb]*mhw_r1[(i,j)]['duration'][nb]*cell_area[j,i]
                                 intensity_mean_all[j,i,cont_event]=mhw_r1[(i,j)]['intensity_mean'][nb]
                                 duration_all[j,i,cont_event]=mhw_r1[(i,j)]['duration'][nb]
                                 nevents[j,i]=nevents[j,i]+1
                                 cont_event=cont_event+1
                              elif (mhw_r1[i,j]['date_start'][nb].toordinal() == t_day) and (mhw_r1[i,j]['date_end'][nb].toordinal() >= t[-1]):
                                 activity[j,i] += mhw_r1[(i,j)]['intensity_mean'][nb]*(t[-1] - mhw_r1[i,j]['date_start'][nb].toordinal() )*cell_area[j,i]
                                 intensity_mean_all[j,i,cont_event]=mhw_r1[(i,j)]['intensity_mean'][nb]
                                 duration_all[j,i,cont_event]=mhw_r1[(i,j)]['duration'][nb]
                                 nevents[j,i]=nevents[j,i]+1
                                 cont_event=cont_event+1
                              elif (mhw_r1[i,j]['date_end'][nb].toordinal() == t_day) and (mhw_r1[i,j]['date_start'][nb].toordinal() <= t[0]):
                                 activity[j,i] += mhw_r1[(i,j)]['intensity_mean'][nb]*(mhw_r1[i,j]['date_end'][nb].toordinal() - t[0])*cell_area[j,i]
                                 intensity_mean_all[j,i,cont_event]=mhw_r1[(i,j)]['intensity_mean'][nb]
                                 duration_all[j,i,cont_event]=mhw_r1[(i,j)]['duration'][nb]
                                 nevents[j,i]=nevents[j,i]+1
                                 cont_event=cont_event+1
                                 
      intensity_mean_all[intensity_mean_all==0]=np.nan
      duration_all[duration_all==0]=np.nan
      nevents[nevents==0]=np.nan
	
      for i in range(lon.shape[0]):
         for j in range(lat.shape[0]):
	         intensity_mean[j,i]=np.nanmean(intensity_mean_all[j,i,:])
	         duration[j,i]=np.nanmean(duration_all[j,i,:])
  
      activity_domain[year-yearbeg]=np.nansum(activity[:,:])
	
      if plot_map == 'y':
         list_map=["nevents", "duration", "intensity_mean", "activity"]
         for properties in list_map:
            print(properties)
            fig = plt.figure(figsize=(8,6))
            ax = plt.axes(projection=ccrs.PlateCarree())
            gl = ax.gridlines(draw_labels = True,linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
            gl.top_labels = False
            gl.right_labels = False
            gl.xlabel_style = dict(fontsize=16)
            gl.ylabel_style = dict(fontsize=16)
            ax.set_xlabel('Longitude(°)')
            ax.set_label('Latitude(°)')
            plt.axis([lonmin, lonmax, latmin, latmax])
      
            if properties == "nevents":
	            levels = np.linspace(0,leg_max_nevent,5)
	            cmap=plt.cm.Greys
	            plt.contourf(lon,lat,nevents,levels=levels,cmap=cmap,extend='both')
	            cb = plt.colorbar(ax=ax, orientation=legend_orientation, shrink=shrink)
	            cb.set_label("Nb of events (-)",fontsize=ft_label)
            if properties == "duration":
	            levels = np.linspace(leg_min_duration,leg_max_duration,5)
	            cmap=plt.cm.Greens
	            plt.contourf(lon,lat,duration,levels=levels,cmap=cmap,extend='both')
	            cb = plt.colorbar(ax=ax, orientation=legend_orientation, shrink=shrink)
	            cb.set_label("Duration (days)",fontsize=ft_label)
            if properties == "intensity_mean":
	            if target == 'MCS':
	               levels = np.linspace(-leg_max_int_mean,-leg_min_int_mean,5)
	               cmap=plt.cm.Purples_r
	            else:
	               levels = np.linspace(leg_min_int_mean,leg_max_int_mean,5)
	               cmap=plt.cm.Purples
	            plt.contourf(lon,lat,intensity_mean,levels=levels,cmap=cmap,extend='both')
	            cb = plt.colorbar(ax=ax, orientation=legend_orientation, shrink=shrink)
	            cb.set_label("Mean intensity (°C)",fontsize=ft_label)
            if properties == "activity":
               activity = np.ma.masked_where(activity == 0, activity)
               if 'target' == 'MCS':
                  levels = np.linspace(-leg_max_activity,0,5)
                  cmap=plt.cm.Blues_r
               else:
                  levels = np.linspace(0,leg_max_activity,5)
                  cmap=plt.cm.Reds
               plt.contourf(lon,lat, activity/10**(9), levels=levels,  cmap=cmap, extend='both')
               cmap.set_bad(color='white')
               cb = plt.colorbar(ax=ax, orientation=legend_orientation, shrink=shrink)
               cb.set_label("Activity (degCxdaysx10³km²)",fontsize=ft_label)
	         
            cb.ax.tick_params(labelsize=ft_tick)
            plt.title(f'{year}-{season} ', loc='center',fontsize=ft_title)
            ax.add_feature(cfeature.LAND)
            ax.coastlines()
            plt.savefig(f'{pathoutputfig}/map.{properties}.{data}.{season}.{year}{end}.eps', format='eps')
                   
   del mhw_r1
   del clim_r1
      
   print("END LOOP")
   print("activity_domain",activity_domain)
   np.save(f'{pathdata}/MEE/TXT.TS/ts.activity.{data}.{season}{end}.npy', activity_domain)

if rank == 'y':
   print("RANK")

   if target == "MHW":
      activity_domain_rankyear=np.argsort(activity_domain*-1)+yearbeg
   else:
      activity_domain_rankyear=np.argsort(activity_domain)+yearbeg   
   print(activity_domain_rankyear)

   np.savetxt(f'{pathdata}/MEE/TXT.RANK/rank.activity.{data}.{season}{end}.txt', activity_domain_rankyear, fmt='%d')		

if plot_ts == 'y':
   print("PLOT TS ACTIVITY")
   activity_r1=np.load(f'{pathdata}/MEE/TXT.TS/ts.activity.{data}.{season}{end}.npy')
      
   year_range=range(yearbeg,yearend+1)
   model_r1=np.polyfit(year_range,activity_r1,2)
   predict_r1 = np.poly1d(model_r1)
   y_lin_reg_r1 = predict_r1(year_range)
      
   fig = plt.figure(figsize=(8,6))
   plt.plot(year_range,y_lin_reg_r1/10**(12), c = 'darkmagenta', linestyle='--')
   plt.plot(year_range,activity_r1/10**(12),  c = 'darkmagenta') 
   plt.ylabel("Activity (°C.days.10⁶km²) ", fontsize=14)
   plt.title(f"{target} {season} {region} {model}")
   plt.grid(True)
   plt.savefig(f'{pathoutputfig}/ts.activity.{data}.{season}{end}.eps', format='eps')
   
##############        
# PLOT LATEX #
##############
if latex == "y":
   print('latex')

   fileout=f'{pathoutputlatex}/rank.all.{data}.{season}{end}.pdf'

   trim_ts="20 20 30 20"
   scale_ts="1."
   trim_map_a="25 40 55 30"
   trim_map_b="68 40 55 40"
   scale_map="0.24"

   with open("tmp_mee_rank.tex", "w") as file:
      file.write(r'''
\documentclass[12pt]{article}
\usepackage[dvips]{graphicx}
\usepackage[dvipsnames]{xcolor}
\usepackage{float}
\usepackage{fullpage}

\usepackage{fancyvrb}
% redefine \VerbatimInput
\RecustomVerbatimCommand{\VerbatimInput}{VerbatimInput}%
{fontsize=\footnotesize,
 %
 frame=lines,  % top and bottom rule only
 framesep=2em, % separation between frame and text
 rulecolor=\color{Gray},
 %
 label=\fbox{\color{Black} SUMMARY},
 labelposition=topline,
 %
 commandchars=\|\(\), % escape character and argument delimiters for
                      % commands within the verbatim
 commentchar=*        % comment character
}

%
\begin{document}
%
\title{
Rank for '''+ data + r''' \newline
 }
\author{WORK DOCUMENT - Amélie Simon}
\maketitle
\clearpage
%
\begin{figure}[p]
\begin{center}
\noindent\includegraphics[scale=''' + scale_ts + r''', trim=''' + trim_ts + r''', clip=true]{''' + pathoutputfig + r'''/ts.activity.''' + data + r'''.''' + season + r'''.eps}
\end{center}
\end{figure}

\VerbatimInput{''' + pathdata + r'''/MEE/TXT.RANK/rank.activity.''' + data + r'''.''' + season + r'''.txt}
\clearpage
'''
)

   with open(
            pathdata + r'''/MEE/TXT.RANK/rank.activity.''' + data + r'''.''' + season + r'''.txt''',"r") as f:
      for line in f:
         with open("tmp_mee_rank.tex", "a") as file:
            file.write(r''' 
\begin{figure}[p]
\begin{center}
\noindent\includegraphics[scale=''' + scale_map + r''', trim=''' + trim_map_a + r''', clip=true]{''' + pathoutputfig + r'''/map.activity.''' + data + r'''.''' + season + r'''.''' + str(line.strip()) + r'''.eps}
\noindent\includegraphics[scale=''' + scale_map + r''', trim=''' + trim_map_b + r''', clip=true]{''' + pathoutputfig + r'''/map.nevents.''' + data + r'''.''' + season + r'''.''' + str(line.strip()) + r'''.eps}
\noindent\includegraphics[scale=''' + scale_map + r''', trim=''' + trim_map_b + r''', clip=true]{''' + pathoutputfig + r'''/map.duration.''' + data + r'''.''' + season + r'''.''' + str(line.strip()) + r'''.eps}
\noindent\includegraphics[scale=''' + scale_map + r''', trim=''' + trim_map_b + r''', clip=true]{''' + pathoutputfig + r'''/map.intensity_mean.''' + data + r'''.''' + season + r'''.''' + str(line.strip()) + r'''.eps}
\end{center}
\end{figure}
'''
)

   with open("tmp_mee_rank.tex", "a") as file:
      file.write(r''' 
%
\end{document}
'''
)

   os.system("latex tmp_mee_rank.tex")
   os.system("dvipdf -R0 tmp_mee_rank.dvi " + fileout)
   print(f'{fileout}')

END = datetime.now()
DIFF = (END - START)
print(f'It took {int(DIFF.total_seconds() / 60)} minutes')
