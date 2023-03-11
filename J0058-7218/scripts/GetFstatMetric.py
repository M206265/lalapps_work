import numpy as np
import pandas as pd
from math import cos as cos
import math
import os

def to_radian(degrees):
    result = degrees * math.pi / 180
    return(result)

def getObject(object_name, datapath):
    objectData = pd.read_csv(datapath + 'objects_data.csv', delimiter=',')
    alpha = objectData[objectData.object == object_name]['right ascension']
    delta = objectData[objectData.object == object_name]['declination']
    F0 = objectData[objectData.object == object_name]['F0']
    F1 = objectData[objectData.object == object_name]['F1']
    F2 = objectData[objectData.object == object_name]['F2']

    alpha = to_radian(alpha.values)
    delta = to_radian(delta.values)
    F0 = F0.values
    F1 = F1.values
    F2 = F2.values

    objectData = np.array([alpha, delta, F0, F1, F2], dtype = float)
    return (objectData)

datapath = '/home/m206265/lalapps_work/J0058-7218/data/'
imgpath = '/home/m206265/lalapps_work/J0058-7218/images/'
resultpath = '/home/m206265/lalapps_work/J0058-7218/result/'

object_name = 'J0058-7218'
run = 'O2_1'

pathTimeStampsH1 = datapath+'timestamps/'+run+'_H1_tslist.txt'
pathTimeStampsL1 = datapath+'timestamps/'+run+'_L1_tslist.txt'

#detector = input('Enter name of the detector (LL0, LH0, GEO600, TAMA300, VIRGO):') #LL0 - livingston, LH0 - hanford
#object_name = input('Enter name of the object (J####):') # in J#### format

objectData = getObject(object_name, datapath)

TimeStampsH1 = np.genfromtxt(pathTimeStampsH1)
TimeStampsL1 = np.genfromtxt(pathTimeStampsL1)
TimeStampsL1H1 = np.concatenate((TimeStampsH1, TimeStampsL1))

Tstart = min(TimeStampsL1H1)
Tend = max(TimeStampsL1H1)
T_obs = Tend - Tstart + 1800
refTime = Tstart + (Tend - Tstart)/2
myst = 7.408705e20
ds = 86400
iota = to_radian(90) # !!!!!!
cosi = 0 #cos(iota)
psi = to_radian(0) # !!!!!!!!!
phi0 = 0 # !!!!!!
eps = 1e-5
G = 6.674e-11
c = 2.998e+8
Izz = 1e+38
d_kpc = 62 # !!!!! Graczyk, D., Pietrzy ́ nski, G., Thompson, I. B., et al. 2020, ApJ, 904, 13
T0 = ds*120 #!!!!!!!!!!!!!!!!!!!!!!!! run
n = 4/3 # wave mode, 2 - gw mass-quadrupole, 4/3 - r-modes
H1 = "H1"
L1 = "L1"
sqrtSX = 0.00751
alpha = objectData[0]
delta = objectData[1]
freq = objectData[2]*n #frequency of GW
f1dot = objectData[3]
f2dot = objectData[4]

ephemEarthPath = datapath + 'ephemeris/EARTH-2000-30-DE405.dat'
ephemSunPath = datapath + 'ephemeris/SUN-2000-30-DE405.dat'
h0 = 4*np.pi**2*G*Izz*(freq*2)**2*eps/d_kpc/3.09e+19/c**4*(myst/sqrtSX)

os.system('lalapps_FstatMetric_v2 '
          f'--IFOs="H1","L1"'
          f' --sqrtSX="{sqrtSX}"'
          f' --Alpha={alpha[0]}'
          f' --Delta={delta[0]}'
          f' --Freq={freq[0]}'
          f' --f1dot={f1dot[0]}'
          f' --f2dot={f2dot[0]}'
          f' --refTime={refTime}'
          f' --startTime={Tstart}'
          f' --duration={T_obs}'
          f' --ephemEarth={ephemEarthPath}'
          f' --ephemSun={ephemSunPath}'
          f' --h0={h0[0]}'
          f' --cosi={cosi}'
          f' --psi={psi}'
          f' --phi0={phi0} '
          '--metricType=1'
          ' --outputMetric='+resultpath+'"FstatMetric_'+run+'.txt"'
          f' --coords="freq","f1dot","f2dot"')
