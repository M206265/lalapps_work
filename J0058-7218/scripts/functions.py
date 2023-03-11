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
