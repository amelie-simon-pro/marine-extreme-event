from datetime import datetime
import os
from mhw_rank_season_domain_compute import compute

START = datetime.now()

# ccart
# PATH
# path
pathdata = "/home/ajsimon/Documents/DATA"
pathoutputfig = "/home/ajsimon/Documents/POSTDOC_IDL/PROJETS/PLOT/MHW/FIGURE_RAW"
pathoutputlatex = "/home/ajsimon/Documents/POSTDOC_IDL/PROJETS/PLOT/MHW/LATEX"

# BEGIN CHOICE
region = "48W38E-20N60N"  # for file input
# subregion=NA #48W0E-40N60N #NA #48W0E-40N60N # 48W38E-20N60N / 48W0E-20N40N / 48W0E-40N60N / 0W38E-20N60N
# model=era5-sst  #era5-sst oisst ostia
target = "MHW"  # MHW (heatwaves) / MCW (coldspells)
season = "JJAS"  # DJFM #JJAS
yearbeg = 1982
yearend = 2021
dayendfilename = "1123"
clim_type = "day.mean"  # ydaymean=climato, ts=day.mean
yearbegclim = "1982"
yearendclim = "2021"  # for 2020 ends 30 of June
nmonths = "4"  # for frequency
criteria = "intensity_cumulative"  # intensity_mean intensity_max intensity_cumulative intensity_var duration (frequency, nevents not coded for ranking)
opeevents = "sum"  # MARCHE PAS VERSION 9# max=rank event; sum=rank period
python = "y"  # y/n
npy = "n"  # ts activity
plot = "map"  # /n/map/ts
rank = "n"
latex = "n"  # top4-9year-1region #top3year-1region #top3year-1region #top4-9year-1region # #top3year-1region #top3year-1region
# top3year-3regions # top5years-3products #topyear #allyear # y/n
# lonmin_plot=-40
# lonmax_plot=10
# latmin_plot=20
# latmax_plot=60
# END CHOICE

if region == "48W38E-20N60N":
    region1 = "48W38E-20N40N"
    region2 = "48W38E-40N60N"
    index_lat = 80

for model in ["oisst"]:  # oisst era5-sst ostia
    # cont_subregion=0 # for plot ts
    if model == "oisst":
        modelfullname = "NOAA.OISST.V2.HIGHRES"
        var = "sst"
        resolution = "1440x720"
    elif model == "ostia":
        modelfullname = "METOFFICE.OSTIA"
        var = "analysed_sst"
        resolution = "1440x720"
    elif model == "era5-sst":
        modelfullname = "CDS.ERA5"
        resolution = "1440x720"
        model = "era5"

    for subregion in ["MedW2"]:  # MedE MedW Med NA 30W0W-30N50N
        if subregion == "30W0W-30N50N":
            lonmin = -30
            lonmax = 0
            latmin = 30
            latmax = 50
            subseas = 1
        elif subregion == "Med":
            lonmin = -7
            lonmax = 37
            latmin = 30
            latmax = 46
            subseas = 4
            figsize = "8,5"
            shrink = 1
            ft_title = 24
            ft_label = 16
            ft_tick = 16
            scale = 0.34
            legend_orientation = "horizontal"
        elif subregion == "MedW2":
            lonmin = -7
            lonmax = 17
            latmin = 34
            latmax = 46
            subseas = 17
            figsize = "8,5"
            ft_title = 16
            shrink = 0.65
            ft_label = 16
            ft_tick = 16
            scale = 0.34
            legend_orientation = "horizontal"
        elif subregion == "MedE2":
            lonmin = 9
            lonmax = 37
            latmin = 29
            latmax = 47
            subseas = 16
            figsize = "8,5"
            shrink = 0.65
            ft_title = 16
            ft_label = 16
            ft_tick = 16
            scale = 0.34
            legend_orientation = "horizontal"
            area = "1.60374412e+12"

        for properties in ["intensity_cumulative"]:  # for plot map nevents  duration intensity_mean
            trim = "40 110 70 120"
            trim1a = '20 162 147 140'
            trim1b = '20 162 147 140'
            trim1c = '20 110 147 140'
            trim2a = '70 162 147 140'
            trim2b = '70 162 147 140'
            trim2c = '70 110 147 140'
            if target == "MHW":
                trim3a = '70 162 75 140'
                trim3b = '70 162 75 140'
                trim3c = '70 110 75 140'
            elif target == "MCS":
                trim3a = '70 162 70 140'
                trim3b = '70 162 70 140'
                trim3c = '70 110 70 140'

            print(f'{model}')
            print(f'{region}')
            print(f'{subregion}')
            print(f'{criteria}')
            print(f'{season}')
            fileout = pathoutputlatex + "/rank_" + model + "_" + target + "_" + season + "_" + subregion + "_" + opeevents + "_" + criteria + "_area_" + yearbegclim + yearendclim + dayendfilename + "_v8.pdf"
            nbyear = yearend - yearbeg + 1
            print(f'nbyear {nbyear}')

            if python == "y":
                compute(
                    pathdata=pathdata, pathoutputfig=pathoutputfig, pathoutputlatex=pathoutputlatex,
                    region=region,
                    target=target,
                    season=season,
                    yearbeg=yearbeg, yearend=yearend,
                    dayendfilename=dayendfilename,
                    clim_type=clim_type,
                    yearbegclim=yearbegclim, yearendclim=yearendclim,
                    nmonths=nmonths,
                    criteria=criteria,
                    opeevents=opeevents,
                    python=python,
                    npy=npy,
                    plot=plot,
                    rank=rank,
                    latex=latex,
                    model=model,
                    subregion=subregion,
                    properties=properties,
                    modelfullname=modelfullname,
                    resolution=resolution,
                    lonmin=lonmin, lonmax=lonmax, latmin=latmin, latmax=latmax,
                    subseas=subseas,
                    shrink=shrink,
                    ft_title=ft_title, ft_label=ft_label, ft_tick=ft_tick,
                    legend_orientation=legend_orientation,
                    region1=region1, region2=region2,
                    index_lat=index_lat,
                    fileout=fileout,
                    nbyear=nbyear)

#######
if latex == "allyear":
    scale = "0.26"
    with open("tmp_rank_v8.tex", "w") as file:
        file.write(r'''
\documentclass[12pt]{article}
\usepackage[dvips]{graphicx}
\usepackage[dvipsnames]{xcolor}
 \usepackage[utf8]{inputenc}
 \usepackage{color}
 \usepackage{fullpage}
  \usepackage{float}
 \pagestyle{empty}
\usepackage{hyperref}
\hypersetup{
    colorlinks,
    citecolor=black,
    filecolor=black,
    linkcolor=black,
    urlcolor=black
}
%
\usepackage{fullpage}
\pagestyle{empty}

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
Rank based on the SST of ''' + model + r''' for ''' + target + r''' in ''' + season + r''' over ''' + subregion + r''' \newline
 }
\vspace{5cm}
\author{WORK DOCUMENT}
\maketitle
%\tableofcontents
%
\clearpage
\thispagestyle{empty}
\pagestyle{empty}
eod
'''
                   )

    with open(
            pathdata + "/MHW/TXT.RANK/rank." + model + "." + target + "." + season + "." + resolution + "." + subregion + "." + opeevents + "." + criteria + ".area.txt") as f:
        for year in f:
            with open("tmp_rank_v8.tex", "w") as file:
                file.write(r'''
\newpage 
\begin{figure}[p]
 \begin{center}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim + r''', clip=true]{''' + pathoutputfig + "/" + target + "_" + opeevents + "-" + criteria + "-area_map_" + model + "_" + year + "-" + season + "_" + subregion + r'''.eps} 
 \end{center}
\end{figure}

eod''')
    with open("tmp_rank_v8.tex", "w") as file:
        file.write(r'''
%
\end{document}
eod''')

    os.system("latex tmp_rank_v8.tex")
    os.system("dvipdf -R0 tmp_rank_v8.dvi " + fileout)
    print(f'{fileout}')

    # done #model
    # done #subregion
    # done #criteria

    if latex == "top5year-3products":
        fileout = pathoutputlatex + "/rank_top5year_3products_" + target + "_" + season + "_" + subregion + "_" + opeevents + "_" + criteria + "_area_" + yearbegclim + yearendclim + dayendfilename + "_v8.pdf"
        era5_year = []
        with open(
                pathdata + "/MHW/TXT.RANK/rank.era5." + target + "." + season + "." + resolution + "." + subregion + "." + opeevents + "." + criteria + "." + ".area.txt") as f:
            for line in f:
                print(f'', line.strip())
                era5_year.append(line.strip())

        oisst_year = []

        with open(
                pathdata + "/MHW/TXT.RANK/rank.oisst." + target + "." + season + "." + resolution + "." + subregion + "." + opeevents + "." + criteria + ".area.txt") as f:
            for line in f:
                print(f'', line.strip())
                oisst_year.append(line.strip())

        ostia_year = []
        with open(
                pathdata + "/MHW/TXT.RANK/rank.ostia." + target + "." + season + "." + resolution + "." + subregion + "." + opeevents + "." + criteria + ".area.txt") as f:
            for line in f:
                print(f'', line.strip())
                ostia_year.append(line.strip())

        with open("tmp_rank_v8.tex", "w") as file:
            file.write(r'''
\documentclass[12pt]{article}
\usepackage[dvips]{graphicx}
\usepackage[dvipsnames]{xcolor}
 \usepackage[utf8]{inputenc}
 \usepackage{color}
 \usepackage{fullpage}
  \usepackage{float}
 \pagestyle{empty}
\usepackage{hyperref}
\hypersetup{
    colorlinks,
    citecolor=black,
    filecolor=black,
    linkcolor=black,
    urlcolor=black
}
%
\usepackage{fullpage}
\pagestyle{empty}

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
%\title{ Rank based on the SST of ''' + model + r''' for ''' + target + r''' in ''' + season + r''' over ''' + subregion + r''' \newline  }
%\vspace{5cm}
%\author{WORK DOCUMENT}
%\maketitle
%\tableofcontents
%
\clearpage
\thispagestyle{empty}
\pagestyle{empty}
eod



\newpage 
\begin{figure}[p]
 \begin{center}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_oisst_''' +
                       oisst_year[0] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_ostia_''' +
                       ostia_year[0] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_era5_''' +
                       era5_year[0] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
%
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_oisst_''' +
                       oisst_year[1] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_ostia_''' +
                       ostia_year[1] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_era5_''' +
                       era5_year[1] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
%
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_oisst_''' +
                       oisst_year[2] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_ostia_''' +
                       ostia_year[2] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_era5_''' +
                       era5_year[2] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
%
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_oisst_''' +
                       oisst_year[3] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_ostia_''' +
                       ostia_year[3] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_era5_''' +
                       era5_year[3] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
%
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1c + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_oisst_''' +
                       oisst_year[4] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2c + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_ostia_''' +
                       ostia_year[4] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3c + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_era5_''' +
                       era5_year[4] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
 \end{center}
\end{figure}
eod'''
                       )

    with open("tmp_rank_v8.tex", "w") as file:
        file.write(r'''
%
\end{document}
eod'''
                   )

    os.system("latex tmp_rank_v8.tex")
    os.system("dvipdf -R0 tmp_rank_v8.dvi " + fileout)
    print(f'{fileout}')

    if latex == "top5year-3regions":
        fileout = pathoutputlatex + "/rank_top5year_" + model + "_" + target + "_" + season + "_" + subregion + "_" + opeevents + "_" + criteria + "_area_" + yearbegclim + yearendclim + dayendfilename + "_v8.pdf"

        if subregion == "Med":
            subregion1 = "Med"
            subregion2 = "MedW"
            subregion3 = "MedE"

        region1_year = []
        with open(
                pathdata + "/MHW/TXT.RANK/rank." + model + "." + target + "." + season + "." + resolution + "." + subregion1 + "." + opeevents + "." + criteria + ".area.txt") as f:
            for line in f:
                print(f'', line.strip())
                region1_year.append(line.strip())

        region2_year = []
        with open(
                pathdata + "/MHW/TXT.RANK/rank." + model + "." + target + "." + season + "." + resolution + "." + subregion2 + "." + opeevents + "." + criteria + ".area.txt") as f:
            for line in f:
                print(f'', line.strip())
                region2_year.append(line.strip())

        region3_year = []
        with open(
                pathdata + "/MHW/TXT.RANK/rank." + model + "." + target + "." + season + "." + resolution + "." + subregion3 + "." + opeevents + "." + criteria + ".area.txt") as f:
            for line in f:
                print(f'', line.strip())
                region3_year.append(line.strip())

        with open("tmp_rank_v8.tex", "w") as file:
            file.write(r'''
\documentclass[12pt]{article}
\usepackage[dvips]{graphicx}
\usepackage[dvipsnames]{xcolor}
 \usepackage[utf8]{inputenc}
 \usepackage{color}
 \usepackage{fullpage}
  \usepackage{float}
 \pagestyle{empty}
\usepackage{hyperref}
\hypersetup{
    colorlinks,
    citecolor=black,
    filecolor=black,
    linkcolor=black,
    urlcolor=black
}
%
\usepackage{fullpage}
\pagestyle{empty}

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

\clearpage
\thispagestyle{empty}
\pagestyle{empty}
eod'''
                       )

        with open("tmp_rank_v8.tex", "w") as file:
            file.write(r'''

\newpage 
\begin{figure}[p]
 \begin{center}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region1_year[0] + r'''-''' + season + r'''_''' + subregion1 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region2_year[0] + r'''-''' + season + r'''_''' + subregion2 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region3_year[0] + r'''-''' + season + r'''_''' + subregion3 + r'''.eps} 
%
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region1_year[1] + r'''-''' + season + r'''_''' + subregion1 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region2_year[1] + r'''-''' + season + r'''_''' + subregion2 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region3_year[1] + r'''-''' + season + r'''_''' + subregion3 + r'''.eps} 
%
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region1_year[2] + r'''-''' + season + r'''_''' + subregion1 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region2_year[2] + r'''-''' + season + r'''_''' + subregion2 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region3_year[2] + r'''-''' + season + r'''_''' + subregion3 + r'''.eps} 
%
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region1_year[3] + r'''-''' + season + r'''_''' + subregion1 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region2_year[3] + r'''-''' + season + r'''_''' + subregion2 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region3_year[3] + r'''-''' + season + r'''_''' + subregion3 + r'''.eps} 
%
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1c + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region1_year[4] + r'''-''' + season + r'''_''' + subregion1 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2c + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region2_year[4] + r'''-''' + season + r'''_''' + subregion2 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3c + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region3_year[4] + r'''-''' + season + r'''_''' + subregion3 + r'''.eps} 
 \end{center}
\end{figure}
eod

eod
%
\end{document}
eod''')

        os.system("latex tmp_rank_v8.tex")
        os.system("dvipdf -R0 tmp_rank_v8.dvi " + fileout)
        print(f'{fileout}')

    if latex == "top3year-3regions":

        fileout = pathoutputlatex + "/rank_top5year_3products_" + model \
                  + "_" + target + "_" \
                  + season + "_" \
                  + subregion + "- 3_" \
                  + opeevents \
                  + "_" + criteria \
                  + "_area_" + yearbegclim + yearendclim + dayendfilename \
                  + "_v8.pdf"

        if subregion == "Med":
            subregion1 = "Med"
            subregion2 = "MedW"
            subregion3 = "MedE"

        region1_year = []
        with open(
                pathdata + "/MHW/TXT.RANK/rank.rank." + model + "." + target + "." + season + "." + resolution + "." + subregion1 + "." + opeevents + "." + criteria + ".area.txt") as f:
            for line in f:
                print(f'', line.strip())
                region1_year.append(line.strip())

        region2_year = []
        with open(
                pathdata + "/MHW/TXT.RANK/rank.rank." + model + "." + target + "." + season + "." + resolution + "." + subregion2 + "." + opeevents + "." + criteria + ".area.txt") as f:
            for line in f:
                print(f'', line.strip())
                region2_year.append(line.strip())

        region3_year = []
        with open(
                pathdata + "/MHW/TXT.RANK/rank.rank." + model + "." + target + "." + season + "." + resolution + "." + subregion3 + "." + opeevents + "." + criteria + ".area.txt") as f:
            for line in f:
                print(f'', line.strip())
                region3_year.append(line.strip())

        with open("tmp_rank_v8.tex", "w") as file:
            file.write(r'''
\documentclass[12pt]{article}
\usepackage[dvips]{graphicx}
\usepackage[dvipsnames]{xcolor}
 \usepackage[utf8]{inputenc}
 \usepackage{color}
 \usepackage{fullpage}
  \usepackage{float}
 \pagestyle{empty}
\usepackage{hyperref}
\hypersetup{
    colorlinks,
    citecolor=black,
    filecolor=black,
    linkcolor=black,
    urlcolor=black
}
%
\usepackage{fullpage}
\pagestyle{empty}

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

\clearpage
\thispagestyle{empty}
\pagestyle{empty}
eod



\newpage 
\begin{figure}[p]
 \begin{center}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region1_year[0] + r'''-''' + season + r'''_''' + subregion1 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region2_year[0] + r'''-''' + season + r'''_''' + subregion2 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region3_year[0] + r'''-''' + season + r'''_''' + subregion3 + r'''.eps} 
%
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region1_year[1] + r'''-''' + season + r'''_''' + subregion1 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region2_year[1] + r'''-''' + season + r'''_''' + subregion2 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region3_year[1] + r'''-''' + season + r'''_''' + subregion3 + r'''.eps} 
%
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1c + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region1_year[2] + r'''-''' + season + r'''_''' + subregion1 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2c + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region2_year[2] + r'''-''' + season + r'''_''' + subregion2 + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3c + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region3_year[2] + r'''-''' + season + r'''_''' + subregion3 + r'''.eps} 
 \end{center}
\end{figure}
eod

eod
%
\end{document}
eod'''
                       )

    os.system("latex tmp_rank_v8.tex")
    os.system("dvipdf -R0 tmp_rank_v8.dvi " + fileout)
    print(f'{fileout}')

    #

    if latex == "top3year-1region":

        model = "oisst"
        subregion = "MedE2"

        fileout = pathoutputlatex + "/rank_top3year_" + model + "_" + target + "_" + season + "_" + subregion + "_" + opeevents + "_" + criteria + "_area_" + yearbegclim + yearendclim + dayendfilename + "_v8.pdf"
        region_year = []
        with open(
                pathdata + "/MHW/TXT.RANK/rank." + model + target + "." + season + "." + resolution + subregion + opeevents + criteria + ".area.txt") as f:
            for line in f:
                print(f'', line.strip())
                region_year.append(line.strip())

        if subregion == "Med":
            scale = 0.45
            trim1 = '20 38 50 50'
            trim2 = '70 38 50 50'
        if target == "MHW":
            trim3 = '70 38 50 50'
        elif target == "MCS":
            trim3 = '70 38 50 50'

        if subregion == "MedW":
            scale = 0.45
            trim1 = '105 41 130 19'
            trim2 = '147 41 130 19'
        if target == "MHW":
            trim3 = '147 41 130 19'
        elif target == "MCS":
            trim3 = '147 41 130 19'

        if subregion == "MedE":
            scale = 0.45
            trim1 = '105 41 130 19'
            trim2 = '147 41 130 19'
        if target == "MHW":
            trim3 = '147 41 130 19'
        elif target == "MCS":
            trim3 = '147 41 130 19'

        if subregion == "MedW2":
            scale = 0.35
            trim1 = '50 42 82 25'
            trim2 = '100 42 82 25'
        if target == "MHW":
            trim3 = '100 42 82 25'
        elif target == "MCS":
            trim3 = '100 42 82 25'

        if subregion == "MedE2":
            scale = 0.35
            trim1 = '85 42 130 25'
            trim2 = '139 42 130 25'
        if target == "MHW":
            trim3 = '139 42 130 25'
        elif target == "MCS":
            trim3 = '139 42 130 25'

        with open("tmp_rank_v8.tex", "w") as file:
            file.write(r'''
\documentclass[12pt]{article}
\usepackage[dvips]{graphicx}
\usepackage[dvipsnames]{xcolor}
 \usepackage[utf8]{inputenc}
 \usepackage{color}
 \usepackage{fullpage}
  \usepackage{float}
 \pagestyle{empty}
\usepackage{hyperref}
\hypersetup{
    colorlinks,
    citecolor=black,
    filecolor=black,
    linkcolor=black,
    urlcolor=black
}
%
\usepackage{fullpage}
\pagestyle{empty}

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

\clearpage
\thispagestyle{empty}
\pagestyle{empty}
eod


\newpage 
\begin{figure}[p]
 \begin{center}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1 + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region_year[0] + r'''-''' + season + r'''_''' + subregion + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2 + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region_year[1] + r'''-''' + season + r'''_''' + subregion + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3 + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region_year[2] + r'''-''' + season + r'''_''' + subregion + r'''.eps} 
 \end{center}
\end{figure}
eod

eod
%
\end{document}
eod'''
                       )

        os.system("latex tmp_rank_v8.tex")
        os.system("dvipdf -R0 tmp_rank_v8.dvi " + fileout)
        print(f'{fileout}')

    if latex == "top4-9year-1region":

        model = "oisst"
        subregion = "MedE2"
        fileout = pathoutputlatex + "/rank_top4-9year_" + target + "_" + season + "_" + subregion + "_" + opeevents + "_" + criteria + "_area_" + yearbegclim + yearendclim + dayendfilename + "_v8.pdf"
        print(
            f'{pathdata + "/MHW/TXT.RANK/rank." + model + "." + target + "." + season + "." + resolution + "." + subregion + "." + opeevents + "." + criteria + ".area.txt"}')

        region_year = []
        with open(
                pathdata + "/MHW/TXT.RANK/rank" + model + "." + target + "." + season + "." + resolution + "." + subregion + "." + opeevents + "." + criteria + "." + ".area.txt") as f:
            for line in f:
                print(f'', line.strip())
                region_year.append(line.strip())

        if subregion == "Med":
            scale = 0.32
            trim1a = '20 118 50 50'
            trim1b = '20 38 50 50'
            trim2a = '70 118 50 50'
            trim2b = '70 38 50 50'
            trim3a = '70 118 50 50'
            trim3b = '70 38 50 50'

        if subregion == "MedW":
            scale = 0.45
            trim1a = '105 121 130 19'
            trim1b = '105 41 130 19'
            trim2a = '147 121 130 19'
            trim2b = '147 41 130 19'
            trim3a = '147 121 130 19'
            trim3b = '147 41 130 19'

        if subregion == "MedE":
            scale = 0.45
            trim1a = '105 121 130 19'
            trim1b = '105 41 130 19'
            trim2a = '147 121 130 19'
            trim2b = '147 41 130 19'
            trim3a = '147 121 130 19'
            trim3b = '147 41 130 19'

        if subregion == "MedW2":
            scale = 0.32
            trim1a = '50 121 82 25'
            trim1b = '50 41 82 25'
            trim2a = '100 121 82 25'
            trim2b = '100 41 82 25'
            trim3a = '100 121 82 25'
            trim3b = '100 41 82 25'

        if subregion == "MedE2":
            scale = 0.35
            trim1a = '85 121 130 25'
            trim1b = '85 41 130 25'
            trim2a = '139 121 130 25'
            trim2b = '139 41 130 25'
            trim3a = '139 121 130 25'
            trim3b = '139 41 130 25'

        with open("tmp_rank_v8.tex", "w") as file:
            file.write(r'''
\documentclass[12pt]{article}
\usepackage[dvips]{graphicx}
\usepackage[dvipsnames]{xcolor}
 \usepackage[utf8]{inputenc}
 \usepackage{color}
 \usepackage{fullpage}
  \usepackage{float}
 \pagestyle{empty}
\usepackage{hyperref}
\hypersetup{
    colorlinks,
    citecolor=black,
    filecolor=black,
    linkcolor=black,
    urlcolor=black
}
%
\usepackage{fullpage}
\pagestyle{empty}

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

\clearpage
\thispagestyle{empty}
\pagestyle{empty}
eod


\newpage 
\begin{figure}[p]
 \begin{center}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region_year[3] + r'''-''' + season + r'''_''' + subregion + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region_year[4] + r'''-''' + season + r'''_''' + subregion + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region_year[5] + r'''-''' + season + r'''_''' + subregion + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region_year[6] + r'''-''' + season + r'''_''' + subregion + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region_year[7] + r'''-''' + season + r'''_''' + subregion + r'''.eps} 
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + criteria + r'''-area_map_''' + model + r'''_''' +
                       region_year[8] + r'''-''' + season + r'''_''' + subregion + r'''.eps} 
 \end{center}
\end{figure}
eod

%
\end{document}
eod'''
                       )

        os.system("latex tmp_rank_v8.tex")
        os.system("dvipdf -R0 tmp_rank_v8.dvi " + fileout)
        print(f'{fileout}')

    if latex == "top3year-3criteria":

        fileout = pathoutputlatex + "/rank_top3year_" + model \
                  + "_" + target \
                  + "_" + season \
                  + "_" + subregion \
                  + "_" + opeevents \
                  + "_NbeventDurationIntensity_area_" + yearbegclim + yearendclim + dayendfilename \
                  + "_v8.pdf"

        properties1 = "nevents"
        properties2 = "duration"
        properties3 = "intensity_mean"
        rank_year = []
        with open(
                pathdata + "/MHW/TXT.RANK/rank." + model + "." + target + "." + season + "." + resolution + "." + subregion + "." + opeevents + "." + criteria + "." + ".area.txt") as f:
            for line in f:
                print(f'', line.strip())
                rank_year.append(line.strip())

        with open("tmp_rank_v8.tex", "w") as file:
            file.write(r'''
\documentclass[12pt]{article}
\usepackage[dvips]{graphicx}
\usepackage[dvipsnames]{xcolor}
 \usepackage[utf8]{inputenc}
 \usepackage{color}
 \usepackage{fullpage}
  \usepackage{float}
 \pagestyle{empty}
\usepackage{hyperref}
\hypersetup{
    colorlinks,
    citecolor=black,
    filecolor=black,
    linkcolor=black,
    urlcolor=black
}
%
\usepackage{fullpage}
\pagestyle{empty}

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

\clearpage
\thispagestyle{empty}
\pagestyle{empty}
eod


\newpage
\begin{figure}[p]
 \begin{center}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + properties1 + r'''-area_map_''' + model + r'''_''' +
                       rank_year[0] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + properties2 + r'''-area_map_''' + model + r'''_''' +
                       rank_year[0] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3a + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + properties3 + r'''-area_map_''' + model + r'''_''' +
                       rank_year[0] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
%
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + properties1 + r'''-area_map_''' + model + r'''_''' +
                       rank_year[1] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + properties2 + r'''-area_map_''' + model + r'''_''' +
                       rank_year[1] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3b + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + properties3 + r'''-area_map_''' + model + r'''_''' +
                       rank_year[1] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
%
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim1c + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + properties1 + r'''-area_map_''' + model + r'''_''' +
                       rank_year[2] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim2c + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + properties2 + r'''-area_map_''' + model + r'''_''' +
                       rank_year[2] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
\noindent\includegraphics[scale=''' + scale + r''', trim=''' + trim3c + r''', clip=true]{''' + pathoutputfig + r'''/''' + target + r'''_''' + opeevents + r'''-''' + properties3 + r'''-area_map_''' + model + r'''_''' +
                       rank_year[2] + r'''-''' + season + r'''_''' + subregion + r'''.eps}
 \end{center}
\end{figure}
eod

%
\end{document}
eod'''
                       )

    os.system("latex tmp_rank_v8.tex")
    os.system("dvipdf -R0 tmp_rank_v8.dvi " + fileout)
    print(f'{fileout}')

END = datetime.now()
DIFF = (END - START)
print(f'It took {DIFF.total_seconds() / 60} minutes')
