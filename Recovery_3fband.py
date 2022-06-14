import os
import numpy as np
import glob
import sys
import time
import io
start_time = time.time()
noise = int(sys.argv[1]) # 0 - no noise, 1 - noise

obj = 'Crab'

path_objData = '/home/m206265/lalapps_work/data/'+obj+'Data.dat'
if noise == 0:
    path_SFT = '/home/m206265/lalapps_work/SFTinj/'
    fname = '/home/m206265/lalapps_work/Fstat.txt'
else:
    path_SFT = '/home/m206265/lalapps_work/SFTinjnoise/'
    fname = '/home/m206265/lalapps_work/'


Alpha = np.genfromtxt(path_objData, delimiter = '=' )[0][1]
Delta = np.genfromtxt(path_objData, delimiter = '=' )[1][1]
f0_inj= np.genfromtxt(path_objData, delimiter = '=' )[2][1]
f1d_inj= np.genfromtxt(path_objData, delimiter = '=' )[3][1]
f2d_inj= np.genfromtxt(path_objData, delimiter = '=' )[4][1]

pathTimeStampsH1_O2_1 = '/home/m206265/lalapps_work/data/O2_1_H1_tslist.txt'
TimeStampsH1_O2_1 = np.genfromtxt(pathTimeStampsH1_O2_1)

pathTimeStampsL1_O2_1 = '/home/m206265/lalapps_work/data/O2_1_L1_tslist.txt'
TimeStampsL1_O2_1 = np.genfromtxt(pathTimeStampsL1_O2_1)

path = '/home/m206265/lalapps_work/FstatMetric.txt'
file = io.BytesIO(open(path, 'rb').read().replace(b';',b','))
gFav = np.genfromtxt(file, skip_header = 40, max_rows = 3, delimiter = ',', usecols = (0,1,2))

TimeStampsL1H1_O2_1 = np.concatenate((TimeStampsH1_O2_1, TimeStampsL1_O2_1))

Tstart = min(TimeStampsL1H1_O2_1)
Tend = max(TimeStampsL1H1_O2_1)
T_obs = (Tend - Tstart)+1800

Tref = 1171754150.0
sqrtSX = 0.00751

# ---------------------------------------
# F bands with shift

Mmetric = 0.006
dF = 2*np.sqrt(Mmetric/3/gFav[0,0])
d1F = 2*np.sqrt(Mmetric/3/gFav[1,1])
d2F = 2*np.sqrt(Mmetric/3/gFav[2,2])

#offsets
dL = 0.5*dF
d1L = 0.5*d1F
d2L = 0.5*d2F

fBand = np.sqrt(1.2/gFav[0,0])
f1Band = np.sqrt(1.2/gFav[1,1])
f2Band = np.sqrt(1.2/gFav[2,2])

f0st = f0_inj
f1st = f1d_inj
f2st = f2d_inj

cmd = 'lalapps_ComputeFstatistic_v2 -a '+str(Alpha)+' -d '+str(Delta)
cmd+=  ' -f {:.14f} --FreqBand {} --dFreq {:.15e}'.format(f0st, fBand, dF)
cmd+= ' --f1dot={:.15e} --f1dotBand {} --df1dot {:.15e}'.format(f1st, f1Band, d1F)
cmd+= ' --f2dot={:.15e}  --f2dotBand {} --df2dot {:.15e}'.format(f2st, f2Band, d2F)
cmd+= ' -D "'+path_SFT+'*.sft" '
cmd+= ' --refTime={}'.format(Tref) 
cmd+= ' --FstatMethod=DemodBest'
cmd+= ' --outputFstat=SNR_offsets.txt'
cmd+= ' --outputTiming=Timing_SNR_offsets.txt'
if noise == 0:
    cmd+= ' --assumeSqrtSX='+str(sqrtSX)
#print(cmd)
os.system(cmd)
# ---------------------------------------
# perfectly matched


cmd = 'lalapps_ComputeFstatistic_v2 -a '+str(Alpha)+' -d '+str(Delta)
cmd+= ' -f {:.14f}'.format(f0_inj)
cmd+= ' --f1dot={:.15e}'.format(f1d_inj)

cmd+= ' --f2dot={:.15e}'.format(f2d_inj)
cmd+= ' -D "'+path_SFT+'*.sft" '
cmd+= ' --refTime={}'.format(Tref) 
cmd+= ' --FstatMethod=DemodBest'
cmd+= ' --outputFstat=Fstat_nonoise_perfmatched.txt'
if noise == 0:
    cmd+= ' --assumeSqrtSX='+str(sqrtSX)
#print(cmd)
#os.system(cmd)

end_time = time.time()

print(end_time - start_time)