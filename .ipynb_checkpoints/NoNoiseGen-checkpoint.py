import os
import numpy as np 

nameRun = 'O2_1'
obj = 'Crab'

fileInj = '/home/m206265/lalapps_work/data/'+obj+'Inj.dat'
path_ephemEarth = '/home/m206265/lalapps_work/data/earth00-19-DE405.dat'
path_ephemSun = '/home/m206265/lalapps_work/data/sun00-19-DE405.dat'
timestampsFiles_H1 = '/home/m206265/lalapps_work/data/' +nameRun+ '_H1_tslist.txt'
timestampsFiles_L1 = '/home/m206265/lalapps_work/data/'+nameRun+'_L1_tslist.txt'
#path_SFT = '/home/m206265/lalapps_work/SFTnonoise/'
path_SFT = 'SFTnonoise/'
path_objData = '/home/m206265/lalapps_work/data/'+obj+'Data.dat'

#fmin = 60 # ?
#fBand = 0.01 # ?
#finj = 60.001
#finj = 85.987
finj= np.genfromtxt(path_objData, delimiter = '=' )[2][1]
fmin = finj - 0.014 - 0.05
fBand = 0.014 + 0.1


TimeStampsH1 = np.genfromtxt(timestampsFiles_H1)
TimeStampsL1 = np.genfromtxt(timestampsFiles_L1)
TimeStampsL1H1 = np.concatenate((TimeStampsH1, TimeStampsL1))

#print(len(TimeStampsH1_O2_1), len(TimeStampsL1_O2_1), len(TimeStampsL1H1_O2_1))
Tstart = min(TimeStampsL1H1)
Tend = max(TimeStampsL1H1)
Tspan = (Tend - Tstart)+1800


#hanford ---
cmd = 'lalapps_Makefakedata_v5 --ephemEarth '+path_ephemEarth+' --ephemSun '+path_ephemSun
cmd+= ' --Tsft 1800 --fmin %s --Band %s' % (fmin, fBand)
cmd+= ' --outSingleSFT=0 --outSFTdir='+path_SFT+' --outLabel=noNOISE'
#  cmd+= ' --sqrtSX='+str(sqrtSX)
cmd+= ' --timestampsFiles='+timestampsFiles_H1+' --IFOs=H1'
os.system(cmd)

#livingston ---
cmd = 'lalapps_Makefakedata_v5 --ephemEarth '+path_ephemEarth+' --ephemSun '+path_ephemSun
cmd+= ' --Tsft 1800 --fmin %s --Band %s' % (fmin, fBand)
cmd+= ' --outSingleSFT=0 --outSFTdir='+path_SFT+' --outLabel=noNOISE'
#  cmd+= ' --sqrtSX='+str(sqrtSX)
cmd+= ' --timestampsFiles='+timestampsFiles_L1+' --IFOs=L1'
os.system(cmd)

