import os
import numpy as np 
import glob
import sys

noise = int(sys.argv[1]) # 0 - no noise, 1 - noise
nameRun = str(sys.argv[2]) #'O2_1'
obj = str(sys.argv[3]) #'J0058-7218'

path = '/home/m206265/lalapps_work/J0058-7218/'
sys.path.insert(0, path+'scripts/')
from functions import getObject

# -----------------------------------------------------------------------
datapath = path+'data/'
fileInj = path+'data/'+obj+'Inj.dat'
path_ephemEarth = path+'data/ephemeris/earth00-19-DE405.dat'
path_ephemSun = path+'data/ephemeris/sun00-19-DE405.dat'
timestampsFiles_H1 = path+'data/timestamps/' +nameRun+ '_H1_tslist.txt'
#timestampsFiles_L1 = '/home/m206265/lalapps_work/data/'+nameRun+'_L1_tslist.txt'
#\path_SFT = '/home/m206265/lalapps_work/SFTnonoise/'
path_SFT = path+'result/SFTs/SFT_noise/'
if noise == 0:
    path_SFTinj = path+'result/SFTs/SFTinj_nonoise/'
else:
    path_SFTinj = path+'result/SFTs/SFTinj_noise/'

# -----------------------------------------------------------------------
objectData = getObject(obj, datapath)
freq = objectData[2][0]

finj= freq*4/3
fmin = finj - 0.014 - 0.05 - 0.03
fBand = 0.014 + 0.1 + 0.06
sqrtSh = 0.00751
print(fmin, finj)
TimeStampsH1 = np.genfromtxt(timestampsFiles_H1)
#TimeStampsL1 = np.genfromtxt(timestampsFiles_L1)
#TimeStampsL1H1 = np.concatenate((TimeStampsH1, TimeStampsL1))

#print(len(TimeStampsH1_O2_1), len(TimeStampsL1_O2_1), len(TimeStampsL1H1_O2_1))
Tstart = min(TimeStampsH1)
Tend = max(TimeStampsH1)
Tspan = (Tend - Tstart)+1800


# -----------------------------------------------------------------------
#hanford ---
#cmd = 'lalapps_Makefakedata_v5 --ephemEarth '+path_ephemEarth+' --ephemSun '+path_ephemSun
#cmd+= ' --Tsft 1800 --fmin %s --Band %s' % (fmin, fBand)
#cmd+= ' --outSingleSFT=0 --outSFTdir='+path_SFT+' --outLabel=noNOISE'
#  cmd+= ' --sqrtSX='+str(sqrtSX)
#cmd+= ' --timestampsFiles='+timestampsFiles_H1+' --IFOs=H1'
#os.system(cmd)


# -----------------------------------------------------------------------
# hanford 
cmd = 'lalapps_Makefakedata_v5 --ephemEarth '+path_ephemEarth+' --ephemSun '+path_ephemSun
cmd+= ' --Tsft 1800 --fmin %s --Band %s' % (fmin, fBand)
cmd+= ' --outSingleSFT=0'
cmd+= ' --outSFTdir='+path_SFT+' --outLabel=INJ_'+str(obj)[:5]
#cmd+= ' --startTime='+str(int(Tstart))+' --duration='+str(int(Tspan)) # tslist[3000]-tslist[0]
cmd+= ' --timestampsFiles='+timestampsFiles_H1+' --IFOs=H1'
if noise == 1: 
    cmd+= ' --sqrtSX='+str(sqrtSh)
#cmd+= ' --injectionSources='+fileInj+' \n'
os.system(cmd)

# livingston
#cmd = 'lalapps_Makefakedata_v5 --ephemEarth '+path_ephemEarth+' --ephemSun '+path_ephemSun
#cmd+= ' --Tsft 1800 --fmin %s --Band %s' % (fmin, fBand)
#cmd+= ' --outSingleSFT=0'
#cmd+= ' --outSFTdir='+path_SFTinj+' --outLabel=INJ_'+str(obj)
##cmd+= ' --startTime='+str(int(Tstart))+' --duration='+str(int(Tspan)) # tslist[3000]-tslist[0]
#cmd+= ' --timestampsFiles='+timestampsFiles_L1+' --IFOs=L1'
#if noise == 1:
#    cmd+= ' --sqrtSX='+str(sqrtSh)
#cmd+= ' --injectionSources='+fileInj+' \n'
#os.system(cmd)