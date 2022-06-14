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

datapath = 'data/'
imgpath = 'images/'
object_Crab = 'J0534+2200'
run = 'O2_1'

pathTimeStampsH1 = '/home/m206265/lalapps_work/data/'+run+'_H1_tslist.txt'
pathTimeStampsL1 = '/home/m206265/lalapps_work/data/'+run+'_L1_tslist.txt'

#detector = input('Enter name of the detector (LL0, LH0, GEO600, TAMA300, VIRGO):') #LL0 - livingston, LH0 - hanford
#object_name = input('Enter name of the object (J####):') # in J#### format

objectData_Crab = getObject(object_Crab, datapath)

TimeStampsH1 = np.genfromtxt(pathTimeStampsH1)
TimeStampsL1 = np.genfromtxt(pathTimeStampsL1)
TimeStampsL1H1 = np.concatenate((TimeStampsH1, TimeStampsL1))

Tstart = min(TimeStampsL1H1)
Tend = max(TimeStampsL1H1)
T_obs = Tend - Tstart + 1800
refTimeCrab = 1171754150.0
myst = 7.408705e20
ds = 86400
iotaCrab = to_radian(60)
psiCrab = to_radian(100)
epsCrab = 1e-5
G = 6.674e-11
c = 2.998e+8
Izz = 1e+38
d_kpcCrab = 2
T0 = ds*120

H1 = "H1"
L1 = "L1"
sqrtSX = 0.00751
alphaCrab = objectData_Crab[0]
deltaCrab = objectData_Crab[1]
freqCrab = objectData_Crab[2]
f1dotCrab = objectData_Crab[3]
f2dotCrab = objectData_Crab[4]

ephemEarthPath = '/home/m206265/lalapps_work/data/earth00-19-DE405.dat'
ephemSunPath = '/home/m206265/lalapps_work/data/sun00-19-DE405.dat'
h0Crab = 4*np.pi**2*G*Izz*(freqCrab*2)**2*epsCrab/d_kpcCrab/3.09e+19/c**4*(myst/sqrtSX)
cosiCrab = cos(iotaCrab)
psiCrab = to_radian(100)
phi0Crab = 0

os.system('lalapps_FstatMetric_v2 '
          f'--IFOs="H1","L1"'
          f' --sqrtSX="{sqrtSX}"'
          f' --Alpha={alphaCrab[0]}'
          f' --Delta={deltaCrab[0]}'
          f' --Freq={freqCrab[0]}'
          f' --f1dot={f1dotCrab[0]}'
          f' --f2dot={f2dotCrab[0]}'
          f' --refTime={refTimeCrab}'
          f' --startTime={Tstart}'
          f' --duration={T_obs}'
          f' --ephemEarth={ephemEarthPath}'
          f' --ephemSun={ephemSunPath}'
          f' --h0={h0Crab[0]}'
          f' --cosi={cosiCrab}'
          f' --psi={psiCrab}'
          f' --phi0={phi0Crab} '
          '--metricType=1'
          ' --outputMetric="FstatMetric_'+run+'.txt"'
          f' --coords="freq","f1dot","f2dot"')
