
'''
make word vector from 4-bar degree name progression
'''

from sklearn.feature_extraction.text import TfidfVectorizer
import glob
import numpy as np

# calculate IDF from referenceDirectories and output TF-IDF vector of targetDirectories and referenceDirectories
def makeTfidfFeature(targetDirectories,referenceDirectories,min_df=2,max_features=200,modeDegree=True):
    for useGram in [1,2,3,4]:
        print("start {0}-gram".format(useGram))
        if(modeDegree):
            query = "*_degree_"+str(useGram)+"gram.txt"
        else:
            query = "*_chord_"+str(useGram)+"gram.txt"
        ext = str(useGram)+"gram"

        # load reference Directories
        refDocs = []
        refOffset = [0]
        for directory in referenceDirectories:
            flist = glob.glob(directory+query)
            fileCount = len(flist)
            flist = []
            for ind in range(fileCount):
                if(modeDegree):
                    flist.append(directory+str(ind)+"_degree_"+str(useGram)+"gram.txt")
                else:
                    flist.append(directory+str(ind)+"_chord_"+str(useGram)+"gram.txt")
            refOffset.append(refOffset[-1]+len(flist));
            for fn in flist:
                fin = open(fn,"r")
                s = fin.readline().strip().replace("-","t")
                if(useGram==1):
                    s = " ".join([v+"t" for v in s.split(" ")])
                refDocs.append(s)
                fin.close()
        vec = TfidfVectorizer(min_df = min_df,max_features=max_features,use_idf=True,lowercase=False)
        vec.fit(refDocs);

        print("feature count is :{0}".format(len(vec.get_feature_names())))

        idfs = vec.idf_
        names = vec.get_feature_names()
        idn = list(zip(idfs,names))
        idn.sort()
        print("top 10 popular words is :{0}".format(" ".join([v[1].replace("t","-") for v in idn[:10]])))

        refTfidf = vec.transform(refDocs).todense()
        for di,directory in enumerate(referenceDirectories):
#            print("output to "+directory)
            myTfidf = np.array(refTfidf[refOffset[di]:refOffset[di+1]])
            for i,tfidf in enumerate(myTfidf):
                if(modeDegree):
                    np.savetxt(directory+str(i)+"_degree_tfidf_"+ext+".txt",np.transpose(tfidf),delimiter=",")
                else:
                    np.savetxt(directory+str(i)+"_chord_tfidf_"+ext+".txt",np.transpose(tfidf),delimiter=",")

        tarDocs = []
        tarOffset = [0]
        for directory in targetDirectories:
            flist = glob.glob(directory+query)
            fileCount = len(flist)
            flist = []
            for ind in range(fileCount):
                if(modeDegree):
                    flist.append(directory+str(ind)+"_degree_"+str(useGram)+"gram.txt")
                else:
                    flist.append(directory+str(ind)+"_chord_"+str(useGram)+"gram.txt")
#            print(len(flist))
            tarOffset.append(tarOffset[-1]+len(flist));
            for fn in flist:
                fin = open(fn,"r")
                s = fin.readline().strip().replace("-","t")
                if(useGram==1):
                    sl = [ele+"t" for ele in s.split(" ")]
                    s = " ".join(sl)
                tarDocs.append(s)
                fin.close()
#        print("transform")
        tarTfidf = vec.transform(tarDocs).todense()
        for i,directory in enumerate(targetDirectories):
#            print("output to "+directory)
            myTfidf = np.array(tarTfidf[tarOffset[i]:tarOffset[i+1]])
            for i,tfidf in enumerate(myTfidf):
                if(modeDegree):
                    np.savetxt(directory+str(i)+"_degree_tfidf_"+ext+".txt",np.transpose(tfidf),delimiter=",")
                else:
                    np.savetxt(directory+str(i)+"_chord_tfidf_"+ext+".txt",np.transpose(tfidf),delimiter=",")

#        print("feature count is :{0}".format(len(vec.get_feature_names())))
#        print("top 40 is :{0}".format(vec.get_feature_names()[:40]))
        if(modeDegree):
            fout = open("./feature/id_degree_tfidf_{0}gram.txt".format(useGram),"w")
        else:
            fout = open("./feature/id_chord_tfidf_{0}gram.txt".format(useGram),"w")
        for ind,name in enumerate(vec.get_feature_names()):
            fout.write("{0},{1}\n".format(ind,name))
        fout.close()
