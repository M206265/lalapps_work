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
path_Sh = path+'result/'
# -----------------------------------------------------------------------
objectData = getObject(obj, datapath)
freq = objectData[2][0]
finj= freq*4/3
fmin = finj - 0.014 - 0.05
fBand = 0.014 + 0.1

TimeStampsH1 = np.genfromtxt(timestampsFiles_H1)
Tstart = min(TimeStampsH1)
Tend = max(TimeStampsH1)
# -----------------------------------------------------------------------
cmd = 'lalapps_ComputePSD --inputData='+path_SFT+'*.sft'
cmd += ' --outputPSD='+path_Sh+'H1-SpectralDensity-'+obj[:5]+'-'+nameRun+'-gensft-nowings'
#cmd += f' --fStart={fmin} --fBand={fBand}'
cmd += f' --Freq={fmin} --FreqBand={fBand}'
cmd += f' --startTime={Tstart} --endTime={Tend}'
cmd += ' --timeStampsFile='+timestampsFiles_H1+' --IFO=H1'
cmd += ' -S 4' #For PSD, type of math. operation over SFTs, can be given by string names (preferred) or legacy numbers:arithsum (0), arithmean (1), arithmedian (2), harmsum (3), harmmean (4), powerminus2sum (5), powerminus2mean(6), min (7), max (8)
os.system(cmd)