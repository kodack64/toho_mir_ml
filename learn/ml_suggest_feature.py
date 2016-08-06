import numpy as np
import xgboost as xgb
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report,roc_curve,roc_auc_score,confusion_matrix
from sklearn.utils import shuffle
import glob,pickle,os
import ml_learn_tune


def featureDependency(useFeature,topn=30):
    cv = 4
    # load data and split
    fin = open("./learn/data/"+useFeature+"_true.pkl","rb")
    X_th = pickle.load(fin)
    fin.close()
    Y_th = [1]*len(X_th)
    fin = open("./learn/data/"+useFeature+"_false.pkl","rb")
    X_nth = pickle.load(fin)
    Y_nth = [0]*len(X_th)
    fin.close()
    featureCount = len(X_th[0])

    # retrieve feature name
    featNames = []
    if(useFeature in ["tfidf_1gram","tfidf_2gram","tfidf_3gram","tfidf_4gram"]):
        idname = "./feature/id_"+useFeature+".txt"
        featId = []
        fin = open(idname,"r")
        for line in fin:
            featId.append([int(val) for val in line.strip().split(",")[1].split("t") if val is not ""])
        fin.close()
        romanMaj = ["I","IIb","II","IIIb","III","IV","Vb","V","VIb","VI","VIIb","VII"]
        romanMin = ["IIIb","III","IV","Vb","V","VIb","VI","VIIb","VII","I","IIb","II"]
        nameMajMin = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
        minmaj = ["","m"]
        for f in featId:
            fmaj = "-".join([romanMaj[v%12]+minmaj[v//12] for v in f])
            fmin = "-".join([romanMin[v%12]+minmaj[v//12] for v in f])
            featNames.append("{0} ({1})".format(fmaj,fmin))

    if(useFeature in ["mfcc","hmfcc","pmfcc"]):
        fin = open("./feature/id_mfcc.txt")
        for line in fin:
            featNames.append(line.strip().split(",")[1])
        fin.close()

    if(useFeature in ["rp","rh","ssd"]):
        fin = open("./feature/id_rhythm_barkband.txt","r")
        bark = [int(v) for v in fin.readline().split(",")]
        fin.close()
        barkName = []
        for ind in range(len(bark)):
            if(ind==0):
                barkName.append("0-"+str(bark[ind])+"Hz")
            else:
                barkName.append(str(bark[ind-1])+"-"+str(bark[ind])+"Hz")
        ssdName = ["mean","var","skew","kurtosis","median","min","max"]
        if(useFeature is "rp"):
            for ind in range(featureCount):
                bands = barkName[ind%24]
                fluc = ((ind//24)+1)*0.17*60
                featNames.append("band={0} bpm={1:.1f}".format(bands,fluc))
        if(useFeature is "rh"):
            for ind in range(featureCount):
                fluc = ((ind+1)*0.17)*60
                featNames.append("bpm={0:.1f}".format(fluc))
        if(useFeature is "ssd"):
            for ind in range(featureCount):
                bands = barkName[ind%24]
                ssdn = ssdName[ind//24]
                featNames.append("band={0} stat={1}".format(bands,ssdn))

    X,Y = shuffle(X_th+X_nth,Y_th+Y_nth)
    clf = xgb.XGBClassifier()
    param = ml_learn_tune.tune[useFeature]
    it = 1
    for v in param.values():
        it*=len(v)
    print("Start {0} iteration GridSearchCV @ {1} data with {2} features".format(it*cv,len(X),featureCount))
    grid = GridSearchCV(clf, param, n_jobs=1, cv=cv, scoring="f1",iid=False)
    grid.fit(X,Y)
    for scores in grid.grid_scores_:
        print(scores)
    clf = grid.best_estimator_

    # make sorted important feature id
    featImp = [0]*featureCount
    sumImp = 0
    for fn,val in clf.booster().get_fscore().items():
        featImp[int(fn[1:])]=float(val)
        sumImp += val
    for ind in range(featureCount):
        featImp[ind] = [featImp[ind]/sumImp,ind]
    featImp.sort()
    featImp.reverse()


    fout = open("./learn/depend/"+useFeature+".txt","w")
    for feati in featImp:
        mes = "{0},{1:.5f},{2}\n".format(feati[1],feati[0],featNames[feati[1]])
        fout.write(mes)
    fout.close()

    def checkPositivity(featureIndex):
        Xr = np.array(X)
        fmin,fmax = min(Xr[:,featureIndex]),max(Xr[:,featureIndex])
        sl = 100
        dec = []
        for val in np.linspace(fmin,fmax,sl):
            Xr[:,featureIndex] = val
            pYr = np.log(clf.predict_proba(Xr))
            dec.append(sum(pYr[:,1]-pYr[:,0])/Xr.shape[0])
        return dec

    for rank in range(topn):
        featId = featImp[rank]
        dec = checkPositivity(featId[1])
        xr = np.linspace(0,1,len(dec))
        plt.plot(xr,dec)
        plt.xlabel("Feature strength")
        plt.ylabel("Dependency")
        plt.title(featNames[featId[1]])
        plt.savefig("./learn/depend/"+useFeature+"_"+"{0:0>3}".format(rank)+".png")
        plt.clf()
