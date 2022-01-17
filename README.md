To detect MHW:
     1.  Select region with ferret (SET REGION/X=48W:38E/Y=20N:60N)
     2.  Obtain time serie of 1 grid with cdo (cdo -O remapnn,lon=-40_lat=30 i.nc o.nc)
     3.  Detect MHW and properties, plot figures and save wit pdf with mhw_detect.sh


mhw_rank_season_domain_v2 with boundary with shapefile but too complicated;
mhw_rank_season_domain_v2.sh with boundary with basin.msk
