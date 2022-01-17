from datetime import date

## plot
import matplotlib.ticker as mticker
from netCDF4 import Dataset
from pylab import *

import cartopy.crs as ccrs
import cartopy.feature as cfeature


def compute(**kargs):
    print(kargs)
    pathdata = kargs["pathdata"]
    pathoutputfig = kargs["pathoutputfig"]
    pathoutputlatex = kargs["pathoutputlatex"]
    region = kargs["region"]
    target = kargs["target"]
    season = kargs["season"]
    yearbeg = kargs["yearbeg"]
    yearend = kargs["yearend"]
    dayendfilename = kargs["dayendfilename"]
    clim_type = kargs["clim_type"]
    yearbegclim = kargs["yearbegclim"]
    yearendclim = kargs["yearendclim"]
    criteria = kargs["criteria"]
    opeevents = kargs["opeevents"]
    npy = kargs["npy"]
    plot = kargs["plot"]
    rank = kargs["rank"]
    model = kargs["model"]
    subregion = kargs["subregion"]
    properties = kargs["properties"]
    modelfullname = kargs["modelfullname"]
    resolution = kargs["resolution"]
    lonmin = kargs["lonmin"]
    lonmax = kargs["lonmax"]
    latmin = kargs["latmin"]
    latmax = kargs["latmax"]
    subseas = kargs["subseas"]
    shrink = kargs["shrink"]
    ft_title = kargs["ft_title"]
    ft_label = kargs["ft_label"]
    ft_tick = kargs["ft_tick"]
    legend_orientation = kargs["legend_orientation"]
    region1 = kargs["region1"]
    region2 = kargs["region2"]
    index_lat = kargs["index_lat"]
    fileout = kargs["fileout"]
    nbyear = kargs["nbyear"]
    opeevents_name = str(np.nanmean)
    # for i in range(1, len(sys.argv)):
    #   print(sys.argv[i])
    print("ft_tick",ft_tick)
    print("type(ft_tick)",type(ft_tick))
    print("subseas",subseas)
    print("type(subseas)",type(subseas))

    # import lon,lat
    file_name = f'{pathdata}/{modelfullname}/{model}.sst.day.mean.1982-JAS.{resolution}.{region}.nc'
    # print(file_name)
    fh = Dataset(file_name, mode='r')
    lat = fh.variables['lat'][:]
    lon = fh.variables['lon'][:]
    fh.close()
    lat_half = lat[0:80]
    print("np.shape(lon.shape)", np.shape(lon))
    print("np.shape(lat.shape)", np.shape(lat))

    # import area
    file_name = f'{pathdata}/NOAA.OISST.V2.HIGHRES/gridarea.{resolution}.{region}.nc'

    # print(file_name)
    fh = Dataset(file_name, mode='r')
    cell_area = fh.variables['cell_area'][:]
    cell_area_copy = np.copy(cell_area)
    fh.close()
    print("np.shape(cell_area)", np.shape(cell_area))  # (lat,lon)

    # import mask
    if subregion == 'MedE2' or subregion == 'MedW2':
        mask_seas = np.load(f'{pathdata}/BOUNDARY/OceanMasks0.25x0.25_48W38E-20N60N_MedWMedE2.npy')
    else:
        mask_seas = np.load(f'{pathdata}/BOUNDARY/OceanMasks0.25x0.25_48W38E-20N60N.npy')

    print("mask_seas",np.shape(mask_seas))
    print("mask_seas",mask_seas)
    # initialization
    print("nbyear", nbyear)
    criteria_domain = np.zeros((nbyear))
    print("criteria_domain", np.shape(criteria_domain))
    longevents = np.zeros((nbyear))
    area_subseas_total = np.zeros((nbyear))

    print("step: begin loop year")
    mhw_r1 = np.load(
        f'{pathdata}/MHW/NPY.DETECT/{model}.{target}.{yearbeg}{yearend}{dayendfilename}.clim{clim_type}.{yearbegclim}{yearendclim}{dayendfilename}.{resolution}.{region1}.npy',
        allow_pickle=True).item()
    clim_r1 = np.load(
        f'{pathdata}/MHW/NPY.DETECT/{model}.clim-{target}.{yearbeg}{yearend}{dayendfilename}.clim{clim_type}.{yearbegclim}{yearendclim}{dayendfilename}.{resolution}.{region1}.npy',
        allow_pickle=True).item()

    mhw_r2 = np.load(
        f'{pathdata}/MHW/NPY.DETECT/{model}.{target}.{yearbeg}{yearend}{dayendfilename}.clim{clim_type}.{yearbegclim}{yearendclim}{dayendfilename}.{resolution}.{region2}.npy',
        allow_pickle=True).item()
    clim_r2 = np.load(
        f'{pathdata}/MHW/NPY.DETECT/{model}.clim-{target}.{yearbeg}{yearend}{dayendfilename}.clim{clim_type}.{yearbegclim}{yearendclim}{dayendfilename}.{resolution}.{region2}.npy',
        allow_pickle=True).item()

    # for year in range(yearbeg,yearend+1):
    for year in [2003]:
        if season == 'DJFM':
            print("HELLO DJFM")
            year1 = year - 1
            month_beg = 12
            day_beg = 1
            year2 = year
            month_end = 3
            day_end = 31
        elif season == 'JJAS':
            print("HELLO JJAS")
            year1 = year
            month_beg = 6
            day_beg = 1
            year2 = year
            month_end = 9
            day_end = 30
        elif season == 'Sept':
            year1 = year
            month_beg = 9
            day_beg = 1
            year2 = year
            month_end = 9
            day_end = 30
        print(year)
        t = np.arange(date(year1, month_beg, day_beg).toordinal(), date(year2, month_end, day_end).toordinal() + 1)
        # print(t)
        # print(t[-1]-t[0])
        # dates = [date.fromordinal(tt.astype(int)) for tt in t]
        # print(date.fromordinal(t[-1]))
        nevents = np.zeros((lat.shape[0], lon.shape[0]))
        duration = np.zeros((lat.shape[0], lon.shape[0]))
        frequency = np.zeros((lat.shape[0], lon.shape[0]))
        criteria = np.zeros((lat.shape[0], lon.shape[0]))
        criteria_witharea = np.zeros((lat.shape[0], lon.shape[0]))
        cell_area[:, :] = np.copy(cell_area_copy)

        for i in range(lon.shape[0]):
            for j in range(lat_half.shape[0]):
                if ((lonmin <= lon[i] <= lonmax) and (latmin <= lat[j] <= latmax)):
                    if ((mask_seas[j, i] == 17)):
                        area_subseas_total[year - yearbeg] = area_subseas_total[year - yearbeg] + cell_area[j, i]
                        pos_r1 = (i, j)
                        if pos_r1 in mhw_r1.keys():
                            nevents[j, i] = (mhw_r1[(i, j)]['n_events'])
                            if (nevents[j, i] > 0):
                                for nb in range(int(nevents[j, i])):
                                    if (mhw_r1[i, j]['date_start'][nb].toordinal() < t[0]) and (
                                            mhw_r1[i, j]['date_end'][nb].toordinal() > t[-1]):
                                        longevents[year - yearbeg] += 1
                                        criteria[j, i] += mhw_r1[(i, j)]['intensity_mean'][nb] * (t[-1] - t[0])
                                        criteria_witharea[j, i] += mhw_r1[(i, j)]['intensity_mean'][nb] * (
                                                t[-1] - t[0]) * \
                                                                   cell_area[j, i]
                                    for t_day in t:
                                        if (mhw_r1[i, j]['date_start'][nb].toordinal() == t_day) and (
                                                mhw_r1[i, j]['date_end'][nb].toordinal() <= t[-1]):
                                            criteria[j, i] += mhw_r1[(i, j)]['intensity_mean'][nb] * \
                                                              mhw_r1[(i, j)]['duration'][nb]
                                            criteria_witharea[j, i] += mhw_r1[(i, j)]['intensity_mean'][nb] * \
                                                                       mhw_r1[(i, j)]['duration'][nb] * cell_area[j, i]
                                        elif (mhw_r1[i, j]['date_start'][nb].toordinal() == t_day) and (
                                                mhw_r1[i, j]['date_end'][nb].toordinal() >= t[-1]):
                                            criteria[j, i] += mhw_r1[(i, j)]['intensity_mean'][nb] * (
                                                    t[-1] - mhw_r1[i, j]['date_start'][nb].toordinal())
                                            criteria_witharea[j, i] += mhw_r1[(i, j)]['intensity_mean'][nb] * (
                                                    t[-1] - mhw_r1[i, j]['date_start'][nb].toordinal()) * cell_area[
                                                                           j, i]
                                        elif (mhw_r1[i, j]['date_end'][nb].toordinal() == t_day) and (
                                                mhw_r1[i, j]['date_start'][nb].toordinal() <= t[0]):
                                            criteria[j, i] += mhw_r1[(i, j)]['intensity_mean'][nb] * (
                                                    mhw_r1[i, j]['date_end'][nb].toordinal() - t[0])
                                            criteria_witharea[j, i] += mhw_r1[(i, j)]['intensity_mean'][nb] * (
                                                    mhw_r1[i, j]['date_end'][nb].toordinal() - t[0]) * cell_area[j, i]
                if (lonmin <= lon[i] <= lonmax) and (latmin <= lat[j + index_lat] <= latmax):
                    if mask_seas[j + index_lat, i] == subseas:
                        area_subseas_total[year - yearbeg] = area_subseas_total[year - yearbeg] + cell_area[
                            j + index_lat, i]
                        pos_r2 = (i, j)
                        if pos_r2 in mhw_r2.keys():
                            nevents[j + index_lat, i] = (mhw_r2[(i, j)]['n_events'])
                            if nevents[j + index_lat, i] > 0:
                                for nb in range(int(nevents[j + index_lat, i])):
                                    if (mhw_r2[i, j]['date_start'][nb].toordinal() < t[0]) and (
                                            mhw_r2[i, j]['date_end'][nb].toordinal() > t[-1]):
                                        longevents[year - yearbeg] += 1
                                        criteria[j + index_lat, i] += mhw_r2[(i, j)]['intensity_mean'][nb] * (
                                                t[-1] - t[0])
                                        criteria_witharea[j + index_lat, i] += mhw_r2[(i, j)]['intensity_mean'][nb] * (
                                                t[-1] - t[0]) * cell_area[j + index_lat, i]
                                    for t_day in t:
                                        if (mhw_r2[i, j]['date_start'][nb].toordinal() == t_day) and (
                                                mhw_r2[i, j]['date_end'][nb].toordinal() <= t[-1]):
                                            criteria[j + index_lat, i] += mhw_r2[(i, j)]['intensity_mean'][nb] * \
                                                                          mhw_r2[(i, j)]['duration'][nb]
                                            criteria_witharea[j + index_lat, i] += mhw_r2[(i, j)]['intensity_mean'][
                                                                                       nb] * \
                                                                                   mhw_r2[(i, j)]['duration'][nb] * \
                                                                                   cell_area[j + index_lat, i]
                                        elif (mhw_r2[i, j]['date_start'][nb].toordinal() == t_day) and (
                                                mhw_r2[i, j]['date_end'][nb].toordinal() >= t[-1]):
                                            criteria[j + index_lat, i] += mhw_r2[(i, j)]['intensity_mean'][nb] * (
                                                    t[-1] - mhw_r2[i, j]['date_start'][nb].toordinal())
                                            criteria_witharea[j + index_lat, i] += mhw_r2[(i, j)]['intensity_mean'][
                                                                                       nb] * (
                                                                                           t[-1] -
                                                                                           mhw_r2[i, j]['date_start'][
                                                                                               nb].toordinal()) * \
                                                                                   cell_area[
                                                                                       j + index_lat, i]
                                        elif (mhw_r2[i, j]['date_end'][nb].toordinal() == t_day) and (
                                                mhw_r2[i, j]['date_start'][nb].toordinal() <= t[0]):
                                            criteria[j + index_lat, i] += mhw_r2[(i, j)]['intensity_mean'][nb] * (
                                                    mhw_r2[i, j]['date_end'][nb].toordinal() - t[0])
                                            criteria_witharea[j + index_lat, i] += mhw_r2[(i, j)]['intensity_mean'][
                                                                                       nb] * (
                                                                                           mhw_r2[i, j]['date_end'][
                                                                                               nb].toordinal() - t[0]) * \
                                                                                   cell_area[
                                                                                       j + index_lat, i]

        criteria_domain[year - yearbeg] = np.nansum(criteria_witharea[:, :])
        print("criteria_domain", criteria_domain)
        print("area_subseas_total", area_subseas_total)
        #   print(criteria_domain)
        # for i in range(lon.shape[0]):
        #   for j in range(lat.shape[0]):
        #      print(criteria_witharea[j,i])
        print("PLOT MAP AVANT")
        if npy in "y":
            np.save(
                f'{pathdata}/MHW/TXT.TS/ts.activity.{model}.{target}.{yearbeg}{yearend}{dayendfilename}.clim{clim_type}.{yearbegclim}{yearendclim}{dayendfilename}.{resolution}.{subregion}.npy',
                criteria_domain)

        if re.search(r'ts\b', plot):
            activity_Med = np.load(
                f'{pathdata}/MHW/TXT.TS/ts.activity.{model}.{target}.{yearbeg}{yearend}{dayendfilename}.clim{clim_type}.{yearbegclim}{yearendclim}{dayendfilename}.{resolution}.Med.npy')

            activity_MedW = np.load(
                f'{pathdata}/MHW/TXT.TS/ts.activity.{model}.{target}.{yearbeg}{yearend}{dayendfilename}.clim{clim_type}.{yearbegclim}{yearendclim}{dayendfilename}.{resolution}.MedW2.npy')

            activity_MedE = np.load(
                f'{pathdata}/MHW/TXT.TS/ts.activity.{model}.{target}.{yearbeg}{yearend}{dayendfilename}.clim{clim_type}.{yearbegclim}{yearendclim}{dayendfilename}.{resolution}.MedE2.npy')

            year_range = range(yearbeg, yearend + 1)
            model_Med = np.polyfit(year_range, activity_Med, 2)
            predict_Med = np.poly1d(model_Med)
            y_lin_reg_Med = predict_Med(year_range)

            model_MedW = np.polyfit(year_range, activity_MedW, 2)
            predict_MedW = np.poly1d(model_MedW)
            y_lin_reg_MedW = predict_MedW(year_range)

            model_MedE = np.polyfit(year_range, activity_MedE, 2)
            predict_MedE = np.poly1d(model_MedE)
            y_lin_reg_MedE = predict_MedE(year_range)

            fig = plt.figure(figsize=(8, 5))
            plt.plot(year_range, y_lin_reg_Med / 10 ** (12), c='darkmagenta', linestyle='--')
            plt.plot(year_range, activity_Med / 10 ** (12), c='darkmagenta')  # label="Med.",
            plt.plot(year_range, y_lin_reg_MedW / 10 ** (12), c='darkorange', linestyle='--')
            plt.plot(year_range, activity_MedW / 10 ** (12), c='darkorange')  # label="Western Med."
            plt.plot(year_range, y_lin_reg_MedE / 10 ** (12), c='darkgreen', linestyle='--')
            plt.plot(year_range, activity_MedE / 10 ** (12), c='darkgreen')  # label="Eastern Med."
            plt.plot(year_range, y_lin_reg_MedW / (10 ** (12) * 0.34), c='sandybrown', linestyle='--', )
            plt.plot(year_range, activity_MedW / (10 ** (12) * 0.34), c='sandybrown', label="Scaled Western Med.")
            plt.plot(year_range, y_lin_reg_MedE / (10 ** (12) * 0.66), c='seagreen', linestyle='--')
            plt.plot(year_range, activity_MedE / (10 ** (12) * 0.66), c='seagreen', label="Scaled Eastern Med.")
            plt.ylabel("Activity (ºC.days.10⁶km²) ", fontsize=14)
            # plt.xlabel("Year")
            plt.legend()
            plt.grid(True)
            plt.savefig(
                f'{pathoutputfig}/ts.activity.{model}.{target}.{yearbeg}{yearend}{dayendfilename}.clim{clim_type}.{yearbegclim}{yearendclim}{dayendfilename}.{resolution}.{subregion}.eps',
                format='eps')

        if re.search(rf'map\b', plot):
            print("PLOT MAP")
            fig = plt.figure(figsize=(8,5))
            ax = plt.axes(projection=ccrs.PlateCarree())
            ax.add_feature(cfeature.LAND)
            ax.coastlines()
            # aspect=1.
            # ax.set_aspect((abs(({lonmax}-{lonmin})/({latmax}-{latmin}))/aspect) )

            gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
            gl.ylocator = mticker.FixedLocator([25, 35, 45, 55])
            gl.top_labels = False
            gl.right_labels = False
            gl.xlabel_style = dict(fontsize=16)
            gl.ylabel_style = dict(fontsize=16)
            ax.set_xlabel('Longitude(°)')
            ax.set_label('Latitude(°)')
            plt.axis([lonmin, lonmax, latmin, latmax])

            if properties in "nevents":
                levels = np.linspace(0, 8, 9)
                if '{target}' == 'MCS':
                    cmap = plt.cm.Greys
                else:
                    cmap = plt.cm.Greys
                plt.contourf(lon, lat, nevents, levels=levels, cmap=cmap, extend='both')
                cb = plt.colorbar(ax=ax, orientation="vertical", shrink=shrink)
                cb.set_label("Nb of events (-)", fontsize=ft_label)
            if properties == "frequency":
                levels = np.linspace(0, 2, 9)
                if target == 'MCS':
                    cmap = plt.cm.Blues
                else:
                    cmap = plt.cm.Reds
                plt.contourf(lon, lat, frequency, levels=levels, cmap=cmap, extend='both')
                cb = plt.colorbar(ax=ax, orientation="vertical", shrink=shrink)
                cb.set_label("Frequency (Number events/months)", fontsize=ft_label)
            if properties == "duration":
                levels = np.linspace(0, 20, 8)
                if target == 'MCS':
                    cmap = plt.cm.Purples
                else:
                    cmap = plt.cm.Purples
                plt.contourf(lon, lat, duration, levels=levels, cmap=cmap, extend='both')
                cb = plt.colorbar(ax=ax, orientation="vertical", shrink=shrink)
                cb.set_label("Duration (days)", fontsize=ft_label)
            if properties == "intensity_mean":
                if target == 'MCS':
                    levels = np.linspace(-2, 0, 7)
                    cmap = plt.cm.Greens
                else:
                    levels = np.linspace(0, 2, 7)
                    cmap = plt.cm.Greens
                plt.contourf(lon, lat, intensity_mean, cmap=cmap, extend='both')
                cb = plt.colorbar(ax=ax, orientation="vertical", shrink=shrink)
                cb.set_label("Mean int. (°C)", fontsize=ft_label)
            if properties == "intensity_max":
                if 'target' == 'MCS':
                    levels = np.linspace(-4, 0, 9)
                    cmap = plt.cm.turbo
                else:
                    levels = np.linspace(0, 4, 9)
                    cmap = plt.cm.turbo
                plt.contourf(lon, lat, intensity_max, levels=levels, cmap=cmap, extend='both')
                cb = plt.colorbar(ax=ax, orientation="vertical", shrink=shrink)
                cb.set_label("Maximum Int. (degC)", fontsize=ft_label)
            if properties == "intensity_cumulative":
                criteria_witharea = np.ma.masked_where(criteria_witharea == 0, criteria_witharea)
                if target == 'MCS':
                    levels = np.linspace(-64, 0, 9)
                    cmap = plt.cm.Blues_r
                else:
                    levels = np.linspace(0, 128, 9)
                    cmap = plt.cm.Reds
                # np.set_printoptions(threshold=np.inf)
                # print(intensity_cumulative_witharea)
                plt.contourf(lon, lat, criteria_witharea / 10 ** (9), levels=levels, cmap=cmap,
                             extend='both')
                cmap.set_bad(color='white')
                cb = plt.colorbar(ax=ax, orientation="vertical", shrink=shrink)
                cb.set_label("Cum. Int. x area (degCxdaysx10³km²)", fontsize=ft_label)
            if properties == "intensity_var":
                levels = np.linspace(0, 1, 5)
                plt.contourf(lon, lat, intensity_var, levels=levels, cmap=cmap, extend='both')
                cb = plt.colorbar(ax=ax, orientation="vertical", shrink=shrink)
                cb.set_label("Intensity variability (degC)", fontsize=ft_label)

            cb.ax.tick_params(labelsize=16)
            # plt.title(f'{model} - {year}-{season} ', loc='center',fontsize=24)
            plt.title(f'{year}-{season} ', loc='center', fontsize=ft_title)
            plt.savefig(
                f'{pathoutputfig}/{target}_{opeevents}-{properties}-area_map_{model}_{year}-{season}_{subregion}.eps',
                format='eps')

    print("step: end loop")

    print("longevents:", longevents)

    if re.search(r'y\b', rank):
        print("step: find top years")

        if '{target}' == 'MHW':
            criteria_domain_rankyear = np.argsort(criteria_domain * -1) + yearbeg
        else:
            criteria_domain_rankyear = np.argsort(criteria_domain) + yearbeg
        print(criteria_domain_rankyear)

        np.savetxt(
            f'{pathdata}/MHW/TXT.RANK/rank.{model}.{target}.{season}.{resolution}.{subregion}.{opeevents}.{criteria}.area.txt',
            criteria_domain_rankyear, fmt='%d')

    del mhw_r1
    del mhw_r2
    del clim_r1
    del clim_r2
