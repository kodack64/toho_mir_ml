
'''
make word vector from 4-bar degree name progression
'''

from sklearn.feature_extraction.text import TfidfVectorizer
import glob
import numpy as np

def makeTfidfFeature(targetDirectories,referenceDirectories,min_df=2,max_features=100):
    for isBeatGram in [True,False]:
        for useGram in [1,2,4]:
            if(isBeatGram):
                query = "*_degree_"+str(useGram)+"gram.txt"
                ext = str(useGram)+"gram"
            else:
                query = "*_degree_"+str(useGram)+"bar.txt"
                ext = str(useGram)+"bar"

            print(referenceDirectories)
            refDocs = []
            for directory in referenceDirectories:
                flist = glob.glob(directory+query)
                for fn in flist:
                    fin = open(fn,"r")
                    refDocs.append(fin.readline().strip())
                    fin.close()
            tarDocs = []
            tarOffset = [0]
            for directory in targetDirectories:
                flist = glob.glob(directory+query)
                tarOffset.append(tarOffset[-1]+len(flist));
                for fn in flist:
                    fin = open(fn,"r")
                    tarDocs.append(fin.readline().strip())
                    fin.close()
            print(len(refDocs),len(tarDocs))
            print(tarOffset)
            vec = TfidfVectorizer(min_df = min_df,max_features=max_features)
            vec.fit(refDocs);
            tfidf = vec.transform(tarDocs).todense()

            print("top 10 is {0}".format(vec.get_feature_names()[:10]))

            for i,directory in enumerate(targetDirectories):
                myTfidf = np.array(tfidf[tarOffset[i]:tarOffset[i+1]])
                np.savetxt(directory+str(i)+"_tfidf_"+ext+".txt",myTfidf,delimiter=",")
