
'''
make pickle for thbgm and not thbgm
'''

import pickle
import numpy as np

def gather(directory,fileCount,dataName):
    feature = []
    for count in range(fileCount):
        def loadTfidf(path):
            return np.loadtxt(path,delimiter=",").tolist()
        degreeTfidf1gram = loadTfidf(directory+str(count)+"_degree_tfidf_1gram.txt")
        degreeTfidf2gram = loadTfidf(directory+str(count)+"_degree_tfidf_2gram.txt")
        degreeTfidf3gram = loadTfidf(directory+str(count)+"_degree_tfidf_3gram.txt")
        degreeTfidf4gram = loadTfidf(directory+str(count)+"_degree_tfidf_4gram.txt")
        chordTfidf1gram = loadTfidf(directory+str(count)+"_chord_tfidf_1gram.txt")
        chordTfidf2gram = loadTfidf(directory+str(count)+"_chord_tfidf_2gram.txt")
        chordTfidf3gram = loadTfidf(directory+str(count)+"_chord_tfidf_3gram.txt")
        chordTfidf4gram = loadTfidf(directory+str(count)+"_chord_tfidf_4gram.txt")
        tfidf = [degreeTfidf1gram,degreeTfidf2gram,degreeTfidf3gram,degreeTfidf4gram
                ,chordTfidf1gram,chordTfidf2gram,chordTfidf3gram,chordTfidf4gram]

        def loadRp(path):
            fin = open(path,"r")
            arr = [float(ele) for ele in fin.readline().split(",")[1:]]
            fin.close()
            return arr

        rp = loadRp(directory+str(count)+".rp")
        rh = loadRp(directory+str(count)+".rh")
        ssd = loadRp(directory+str(count)+".ssd")
        rps = [rp,rh,ssd]

        def loadMFCC(path):
            return np.loadtxt(path,delimiter=",").tolist()
        normal_mfcc = loadMFCC(directory+str(count)+"_normal_mfcc_stat.txt")
        harmonic_mfcc = loadMFCC(directory+str(count)+"_harmonic_mfcc_stat.txt")
        percussive_mfcc = loadMFCC(directory+str(count)+"_percussive_mfcc_stat.txt")
        mfccs = [normal_mfcc,harmonic_mfcc,percussive_mfcc]

        feature.append([mfccs,tfidf,rps]);
        print("{0}/{1} done".format(count+1,fileCount))
    fout = open("./feature/"+dataName+".pkl","wb")
    pickle.dump(feature,fout)
    fout.close()
