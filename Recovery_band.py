import os
import numpy as np
import glob
import sys
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

TimeStampsL1H1_O2_1 = np.concatenate((TimeStampsH1_O2_1, TimeStampsL1_O2_1))

Tstart = min(TimeStampsL1H1_O2_1)
Tend = max(TimeStampsL1H1_O2_1)
T_obs = (Tend - Tstart)+1800

Tref = 1171754150.0
sqrtSX = 0.00751

# ---------------------------------------
# F band
N = 50
dF = 1/T_obs
fBand = N*dF
f0st = dF/2 + f0_inj - fBand/2

cmd = 'lalapps_ComputeFstatistic_v2 -a '+str(Alpha)+' -d '+str(Delta)
cmd+=  ' -f {:.14f} --FreqBand {} --dFreq {:.15e}'.format(f0st, fBand, dF)
cmd+= ' --f1dot={:.15e}'.format(f1d_inj)
cmd+= ' --f2dot={:.15e}'.format(f2d_inj)
cmd+= ' -D "'+path_SFT+'*.sft" '
cmd+= ' --refTime={}'.format(Tref) 
cmd+= ' --FstatMethod=DemodBest'
cmd+= ' --outputFstat='+fname+'Fstat_noise_fband_shift.txt'
if noise == 0:
    cmd+= ' --assumeSqrtSX='+str(sqrtSX)
#print(cmd)
os.system(cmd)

# ---------------------------------------
# F1 band
N = 200
dF = 1/T_obs**2
fBand = N*dF # f band 
f1st = f1d_inj - fBand/2

cmd = 'lalapps_ComputeFstatistic_v2 -a '+str(Alpha)+' -d '+str(Delta)
cmd+=  ' -f {:.14f}'.format(f0_inj)
cmd+= ' --f1dot={:.15e} --f1dotBand {} --df1dot {:.15e}'.format(f1st, fBand, dF)
cmd+= ' --f2dot={:.15e}'.format(f2d_inj)
cmd+= ' -D "'+path_SFT+'*.sft" '
cmd+= ' --refTime={}'.format(Tref) 
cmd+= ' --FstatMethod=DemodBest'
cmd+= ' --outputFstat='+fname+'Fstat_noise_f1band.txt'
if noise == 0:
    cmd+= ' --assumeSqrtSX='+str(sqrtSX)
#print(cmd)
#os.system(cmd)

# ---------------------------------------
# F2 band
N = 500
dF = 1/T_obs**3
fBand = N*dF
f2st = f2d_inj - fBand/2

cmd = 'lalapps_ComputeFstatistic_v2 -a '+str(Alpha)+' -d '+str(Delta)
cmd+=  ' -f {:.14f}'.format(f0_inj)
cmd+= ' --f1dot={:.15e}'.format(f1d_inj)
cmd+= ' --f2dot={:.15e}  --f2dotBand {} --df2dot {:.15e}'.format(f2st, fBand, dF)
cmd+= ' -D "'+path_SFT+'*.sft" '
cmd+= ' --refTime={}'.format(Tref) 
cmd+= ' --FstatMethod=DemodBest'
cmd+= ' --outputFstat='+fname+'Fstat_noise_f2band.txt'
if noise == 0:
    cmd+= ' --assumeSqrtSX='+str(sqrtSX)
#print(cmd)
#os.system(cmd)
