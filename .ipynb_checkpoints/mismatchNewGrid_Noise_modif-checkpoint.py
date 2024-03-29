import os
import numpy as np
import glob
import sys
import io

noise = int(sys.argv[1]) # 0 - no noise, 1 - noise
iteration = int(sys.argv[2])

obj = 'Crab'
run = 'O2_1'

pathTimeStampsH1 = '/home/m206265/lalapps_work/data/'+run+'_H1_tslist.txt'
pathTimeStampsL1 = '/home/m206265/lalapps_work/data/'+run+'_L1_tslist.txt'


pathMetric = '/home/m206265/lalapps_work/FstatMetric_'+run+'.txt'

path_objData = '/home/m206265/lalapps_work/data/'+obj+'Data.dat'
pathRes = '/home/m206265/lalapps_work/mismatchNewGrid_Noise_modif'
if noise == 0:
    path_SFT = '/home/m206265/lalapps_work/SFTinj/'
    fname = '/home/m206265/lalapps_work/Fstat.txt'
else:
    path_SFT = '/home/m206265/lalapps_work/SFTinjnoise/'
    fname = '/home/m206265/lalapps_work/'


Alpha = np.genfromtxt(path_objData, delimiter = '=' )[0][1] # one array 
Delta = np.genfromtxt(path_objData, delimiter = '=' )[1][1]
f0_inj= np.genfromtxt(path_objData, delimiter = '=' )[2][1]
f1d_inj= np.genfromtxt(path_objData, delimiter = '=' )[3][1]
f2d_inj= np.genfromtxt(path_objData, delimiter = '=' )[4][1]

TimeStampsH1 = np.genfromtxt(pathTimeStampsH1)
TimeStampsL1 = np.genfromtxt(pathTimeStampsL1)

file = io.BytesIO(open(pathMetric, 'rb').read().replace(b';',b','))
gFav = np.genfromtxt(file, skip_header = 40, max_rows = 3, delimiter = ',', usecols = (0,1,2))

TimeStampsL1H1 = np.concatenate((TimeStampsH1, TimeStampsL1))

Tstart = min(TimeStampsL1H1)
Tend = max(TimeStampsL1H1)+1800
T_obs = (Tend - Tstart)

Tref = np.genfromtxt(path_objData, delimiter = '=')[9][1]
sqrtSX = 0.00751

# ---------------------------------------
# F bands with shift
K = 3.11
Mmetric = 0.06 # 6% theoretical mismatch
dF = K*2*np.sqrt(Mmetric/3/gFav[0,0])
d1F = K*2*np.sqrt(Mmetric/3/gFav[1,1])
d2F = K*2*np.sqrt(Mmetric/3/gFav[2,2])

fBand = 2*np.sqrt(1.2/gFav[0,0]) # SNR-reduction = 1 - mism; 
f1Band = 2*np.sqrt(1.2/gFav[1,1]) # taking 1.2 with a margin #we want 50-60% SNR-reduction => mism = 0.4 
f2Band = 2*np.sqrt(1.2/gFav[2,2]) # coef. 2 - we are looking not only on positive offsets

f0st = f0_inj + np.random.uniform(-0.5*dF, 0.5*dF) - fBand/2 # signal should not align with template => adding random value 
f1st = f1d_inj + np.random.uniform(-0.5*d1F, 0.5*d1F) - f1Band/2 
f2st = f2d_inj + np.random.uniform(-0.5*d2F, 0.5*d2F) - f2Band/2


os.system('python3 Injection.py 1') # Generating noise and injecting signal
# -------------------------------------------------------------
# Measuring 2F_0 (perf matched)

cmd = 'lalapps_ComputeFstatistic_v2 -a '+str(Alpha)+' -d '+str(Delta)
cmd+=  ' -f {:.14f} '.format(f0_inj)
cmd+= ' --f1dot={:.15e} '.format(f1d_inj)
cmd+= ' --f2dot={:.15e}  '.format(f2d_inj)
cmd+= ' -D "'+path_SFT+'*.sft" '
cmd+= ' --refTime={}'.format(Tref) 
cmd+= ' --FstatMethod=DemodBest'
cmd+= ' --outputFstat='+pathRes+'/mism'+str(int(Mmetric*100))+'/SNR_GridLoud_modif'+str(int(Mmetric*100))+'_'+str(iteration)+'_perfmatched.txt'
cmd+= ' --outputTiming='+pathRes+'/mism'+str(int(Mmetric*100))+'/Timing_SNR_GridLoud_modif'+str(int(Mmetric*100))+'_perfmatched.txt'
cmd+= ' --NumCandidatesToKeep=1'

os.system(cmd)
# ----------------------------------------------------------------

cmd = 'lalapps_ComputeFstatistic_v2 -a '+str(Alpha)+' -d '+str(Delta)
cmd+=  ' -f {:.14f} --FreqBand {} --dFreq {:.15e}'.format(f0st, fBand, dF)
cmd+= ' --f1dot={:.15e} --f1dotBand {} --df1dot {:.15e}'.format(f1st, f1Band, d1F)
cmd+= ' --f2dot={:.15e}  --f2dotBand {} --df2dot {:.15e}'.format(f2st, f2Band, d2F)
cmd+= ' -D "'+path_SFT+'*.sft" '
cmd+= ' --refTime={}'.format(Tref) 
cmd+= ' --FstatMethod=DemodBest'
cmd+= ' --outputFstat='+pathRes+'/mism'+str(int(Mmetric*100))+'/SNR_GridLoud_modif'+str(int(Mmetric*100))+'_'+str(iteration)+'.txt'
cmd+= ' --outputTiming='+pathRes+'/mism'+str(int(Mmetric*100))+'/Timing_SNR_GridLoud_modif'+str(int(Mmetric*100))+'.txt'
cmd+= ' --NumCandidatesToKeep=1'
if noise == 0:
    cmd+= ' --assumeSqrtSX='+str(sqrtSX)
#print(cmd)
os.system(cmd)

os.system('rm /home/m206265/lalapps_work/SFTinjnoise/*.sft')