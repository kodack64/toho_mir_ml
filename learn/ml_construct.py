
'''
convert all feature pickle to preprocessed feature pickle
'''

import pickle
import os

def construct(datasetNames):
    for dataName in datasetNames:
        fin = open("./feature/"+dataName+".pkl","rb")
        feature = pickle.load(fin)
        fin.close()
        print("{0} : {1} data".format(dataName,len(feature)))
        def save(name,arr):
            fout = open(name,"wb")
            pickle.dump(arr,fout)
            fout.close()
        ######################## MFCC
        save("./learn/data/mfcc_"+dataName+".pkl",[val[0][0] for val in feature])
        save("./learn/data/hmfcc_"+dataName+".pkl",[val[0][1] for val in feature])
        save("./learn/data/pmfcc_"+dataName+".pkl",[val[0][2] for val in feature])

        ######################## TFIDF
        save("./learn/data/tfidf_1gram_"+dataName+".pkl",[val[1][0] for val in feature])
        save("./learn/data/tfidf_2gram_"+dataName+".pkl",[val[1][1] for val in feature])
        save("./learn/data/tfidf_3gram_"+dataName+".pkl",[val[1][2] for val in feature])
        save("./learn/data/tfidf_4gram_"+dataName+".pkl",[val[1][3] for val in feature])
        save("./learn/data/tfidf_chord_1gram_"+dataName+".pkl",[val[1][4] for val in feature])
        save("./learn/data/tfidf_chord_2gram_"+dataName+".pkl",[val[1][5] for val in feature])
        save("./learn/data/tfidf_chord_3gram_"+dataName+".pkl",[val[1][6] for val in feature])
        save("./learn/data/tfidf_chord_4gram_"+dataName+".pkl",[val[1][7] for val in feature])

        ######################## Rhythm
        save("./learn/data/rp_"+dataName+".pkl",[val[2][0] for val in feature])
        save("./learn/data/rh_"+dataName+".pkl",[val[2][1] for val in feature])
        save("./learn/data/ssd_"+dataName+".pkl",[val[2][2] for val in feature])
