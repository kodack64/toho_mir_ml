

'''
make sampled mfcc from mfcc files
'''

import os
from scipy import stats
import librosa
import numpy as np

mfccList = ["_normal_mfcc","_harmonic_mfcc","_percussive_mfcc"]

def mfccPostProcess(directory,fileCount):
    for count in range(fileCount):
        print("{0}/{1}".format(count+1,fileCount))
        for mfccext in mfccList:
            mfcc = np.loadtxt(directory+str(count)+mfccext+".csv",delimiter=",")
            dmfcc = librosa.feature.delta(mfcc)
            result = np.zeros((mfcc.shape[1],14))

            result[:,0] = np.mean(mfcc, axis=0)
            result[:,1] = np.var(mfcc, axis=0, dtype=np.float64)
            result[:,2] = stats.skew(mfcc, axis=0)
            result[:,3] = stats.kurtosis(mfcc, axis=0, fisher=False)
            result[:,4] = np.median(mfcc, axis=0)
            result[:,5] = np.min(mfcc, axis=0)
            result[:,6] = np.max(mfcc, axis=0)
            result[:,7] = np.mean(dmfcc, axis=0)
            result[:,8] = np.var(dmfcc, axis=0, dtype=np.float64)
            result[:,9] = stats.skew(dmfcc, axis=0)
            result[:,10] = stats.kurtosis(dmfcc, axis=0, fisher=False)
            result[:,11] = np.median(dmfcc, axis=0)
            result[:,12] = np.min(dmfcc, axis=0)
            result[:,13] = np.max(dmfcc, axis=0)
            result[np.where(np.isnan(result))] = 0
            np.savetxt(directory+str(count)+mfccext+"_stat.txt",result.flatten("F"),delimiter=",")
