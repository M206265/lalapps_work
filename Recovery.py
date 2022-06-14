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
    fname = '/home/m206265/lalapps_work/Fstat_noise.txt'


Alpha = np.genfromtxt(path_objData, delimiter = '=' )[0][1]
Delta = np.genfromtxt(path_objData, delimiter = '=' )[1][1]
f0_inj= np.genfromtxt(path_objData, delimiter = '=' )[2][1]
f1d_inj= np.genfromtxt(path_objData, delimiter = '=' )[3][1]
f2d_inj= np.genfromtxt(path_objData, delimiter = '=' )[4][1]

Tref = 1171754150.0
sqrtSX = 0.00751

cmd = 'lalapps_ComputeFstatistic_v2 -a '+str(Alpha)+' -d '+str(Delta)
cmd+= ' -f {:.14f}'.format(f0_inj)
cmd+= ' --f1dot={:.15e}'.format(f1d_inj)
cmd+= ' --f2dot={:.15e}'.format(f2d_inj)
cmd+= ' -D "'+path_SFT+'*.sft" '
cmd+= ' --refTime={}'.format(Tref) 
cmd+= ' --FstatMethod=DemodBest'
cmd+= ' --outputFstat='+fname
if noise == 0:
    cmd+= ' --assumeSqrtSX='+str(sqrtSX)
#print(cmd)
os.system(cmd)
