import os
import numpy as np 
import glob
import sys
noise = int(sys.argv[1]) # 0 - no noise, 1 - noise
nameRun = 'O2_1'
obj = 'Crab'

fileInj = '/home/m206265/lalapps_work/data/'+obj+'Inj.dat'
path_ephemEarth = '/home/m206265/lalapps_work/data/earth00-19-DE405.dat'
path_ephemSun = '/home/m206265/lalapps_work/data/sun00-19-DE405.dat'
timestampsFiles_H1 = '/home/m206265/lalapps_work/data/' +nameRun+ '_H1_tslist.txt'
timestampsFiles_L1 = '/home/m206265/lalapps_work/data/'+nameRun+'_L1_tslist.txt'
#path_SFT = '/home/m206265/lalapps_work/SFTnonoise/'
path_SFT = 'SFTnonoise/'
if noise == 0:
    path_SFTinj = '/home/m206265/lalapps_work/SFTinj/'
else:
    path_SFTinj = '/home/m206265/lalapps_work/SFTinjnoise/'
path_objData = '/home/m206265/lalapps_work/data/'+obj+'Data.dat'


    
#fmin = 60 # ?
#fBand = 0.01 # ?
#finj = 60.001
#finj = 85.987
finj= np.genfromtxt(path_objData, delimiter = '=' )[2][1]
fmin = finj - 0.014 - 0.05
fBand = 0.014 + 0.1
sqrtSh = 0.00751

TimeStampsH1 = np.genfromtxt(timestampsFiles_H1)
TimeStampsL1 = np.genfromtxt(timestampsFiles_L1)
TimeStampsL1H1 = np.concatenate((TimeStampsH1, TimeStampsL1))

#print(len(TimeStampsH1_O2_1), len(TimeStampsL1_O2_1), len(TimeStampsL1H1_O2_1))
Tstart = min(TimeStampsL1H1)
Tend = max(TimeStampsL1H1)
Tspan = (Tend - Tstart)+1800

#signal injection


cmd = 'lalapps_Makefakedata_v5 --ephemEarth '+path_ephemEarth+' --ephemSun '+path_ephemSun
cmd+= ' --Tsft 1800 --fmin %s --Band %s' % (fmin, fBand)
cmd+= ' --outSingleSFT=0'
cmd+= ' --noiseSFTs='+path_SFT+'*.sft --outSFTdir='+path_SFTinj+' --outLabel=INJ_'+str(obj)
cmd+= ' --startTime='+str(int(Tstart))+' --duration='+str(int(Tspan)) # tslist[3000]-tslist[0]
if noise == 1:
    cmd+= ' --sqrtSX='+str(sqrtSh)
cmd+= ' --injectionSources='+fileInj+' \n'

# hanford 
cmd = 'lalapps_Makefakedata_v5 --ephemEarth '+path_ephemEarth+' --ephemSun '+path_ephemSun
cmd+= ' --Tsft 1800 --fmin %s --Band %s' % (fmin, fBand)
cmd+= ' --outSingleSFT=0'
cmd+= ' --outSFTdir='+path_SFTinj+' --outLabel=INJ_'+str(obj)
#cmd+= ' --startTime='+str(int(Tstart))+' --duration='+str(int(Tspan)) # tslist[3000]-tslist[0]
cmd+= ' --timestampsFiles='+timestampsFiles_H1+' --IFOs=H1'
if noise == 1: 
    cmd+= ' --sqrtSX='+str(sqrtSh)
cmd+= ' --injectionSources='+fileInj+' \n'
os.system(cmd)

# livingston
cmd = 'lalapps_Makefakedata_v5 --ephemEarth '+path_ephemEarth+' --ephemSun '+path_ephemSun
cmd+= ' --Tsft 1800 --fmin %s --Band %s' % (fmin, fBand)
cmd+= ' --outSingleSFT=0'
cmd+= ' --outSFTdir='+path_SFTinj+' --outLabel=INJ_'+str(obj)
#cmd+= ' --startTime='+str(int(Tstart))+' --duration='+str(int(Tspan)) # tslist[3000]-tslist[0]
cmd+= ' --timestampsFiles='+timestampsFiles_L1+' --IFOs=L1'
if noise == 1:
    cmd+= ' --sqrtSX='+str(sqrtSh)
cmd+= ' --injectionSources='+fileInj+' \n'
os.system(cmd)