# marine-extreme-event

The methodology to evaluate marine temperature extreme events physical importance within a predefined domain and predefined time range is provided in three steps: 
(i) detection of events, 
(ii) calculation of the activity metric for each year and for each grid point location of the domain, 
(iii) ranking according to the total activity (sum of activity of each grid point over the domain). 

It includes two python scripts. A script that loops over any domain the detection script of Hobday et al. (2016) (step (i), called mee_detect_step1.py) 
and a script that calculates the activity and ranks the year according to the total activity (step (ii) and step (iii) of the protocol of this study, called mee_activity_rank_step2-3.py). The whole chain uses as an input a daily SST time serie written as (time,lat,lon). The output is a pdf with the ranking according to activity, the total activity evolution and the spatial distribution of activity, number of events, duration, mean intensity of marine temperature extreme events within a predefined domain and time range. 

More information can be found in:
Simon A., Plecha S.M., Russo A., Teles-Machado A., Donat M., P-A Auger , Trigo R.M., 
“Hot and Cold Marine Extreme Events in the Mediterranean over the last four decades”, under review in Frontiers of Marine Science
