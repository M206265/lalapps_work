import os
import numpy as np

nameRun = 'O2_1'
obj = 'Crab'

path_objData = '/home/m206265/lalapps_work/data/'+obj+'Data.dat'
path_ephemEarth = '/home/m206265/lalapps_work/data/earth00-19-DE405.dat'
path_ephemSun = '/home/m206265/lalapps_work/data/sun00-19-DE405.dat'
timestampsFiles_H1 = '/home/m206265/lalapps_work/data/' +nameRun+ '_H1_tslist.txt'
timestampsFiles_L1 = '/home/m206265/lalapps_work/data/'+nameRun+'_L1_tslist.txt'

alpha = np.genfromtxt(path_objData, delimiter = '=' )[0][1]
delta = np.genfromtxt(path_objData, delimiter = '=' )[1][1]

cmd = 'lalapps_ComputeAntennaPattern'
cmd += ' -a '+str(alpha)+' -d '+str(delta)
cmd += ' --ephemSun='+path_ephemSun+' --ephemEarth='+path_ephemEarth
cmd += ' -I "H1" -T '+timestampsFiles_H1
cmd += ' --Tsft=1800 --noiseSqrtShX=0.00751 -o AntPatt_H1.txt -O ABCD_H1.txt' 
os.system(cmd)

cmd = 'lalapps_ComputeAntennaPattern '
cmd += ' -a '+str(alpha)+' -d '+str(delta)
cmd += ' --ephemSun='+path_ephemSun+' --ephemEarth='+path_ephemEarth
cmd += ' -I "L1" -T '+timestampsFiles_L1
cmd += ' --Tsft=1800 --noiseSqrtShX=0.00751 -o AntPatt_L1.txt -O ABCD_L1.txt ' 
os.system(cmd)