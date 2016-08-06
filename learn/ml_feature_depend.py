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
import ml_feature_name


def featureDependency(useFeature,target,topn=30):
    cv = 4
    # load data and split
    fin = open("./learn/data/"+useFeature+"_thbgm.pkl","rb")
    X_th = pickle.load(fin)
    fin.close()
    fin = open("./learn/data/"+useFeature+"_"+target+".pkl","rb")
    X_nth = pickle.load(fin)
    fin.close()

    print(np.array(X_th).shape,np.array(X_nth).shape)

    test_size=0.0
    X_tr,X_ts = train_test_split(X_th ,test_size=test_size)
    X_ntr,X_nts = train_test_split(X_nth ,train_size=len(X_tr),test_size=len(X_ts))
    X = X_tr+X_ntr
    Y = [1]*len(X_tr)+[0]*len(X_ntr)
    X_ = X_ts+X_nts
    Y_ = [1]*len(X_ts)+[0]*len(X_nts)
    X,Y = shuffle(X,Y)
    X_,Y_ = shuffle(X_,Y_)
    featureCount = len(X_th[0])

    # retrieve feature name
    featNames = ml_feature_name.getFeatureName(useFeature)
    clf = xgb.XGBClassifier()
    param = ml_learn_tune.tune[useFeature]
    it = 1
    for v in param.values():
        it*=len(v)
    print("Start {0} iteration GridSearchCV @ {1} data with {2} features".format(it*cv,len(X),featureCount))
    grid = GridSearchCV(clf, param, n_jobs=1, cv=cv, scoring="f1")
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
