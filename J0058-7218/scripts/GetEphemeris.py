import os
import numpy as np
import sys
import io

target = str(sys.argv[1])
year = str(sys.argv[2])
num_years = str(sys.argv[3])
     
os.system('lalapps_create_solar_system_ephemeris'
        f' --ephem-file /home/m206265/lalapps_work/J0058-7218/data/ephemeris/DE405.1950.2050'
        f' --output-file /home/m206265/lalapps_work/J0058-7218/data/ephemeris/'+target+'-'+year+'-'+num_years+'-DE405.dat'
        f' --year '+year+
        f' --interval 4'
        f' --num-years '+num_years+
        f' --overlap 10'
        f' --target '+target)