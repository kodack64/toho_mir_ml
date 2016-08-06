import numpy as np
import xgboost as xgb
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report,roc_curve,roc_auc_score,confusion_matrix
from sklearn.utils import shuffle,resample
import glob,pickle,os
import ml_learn_tune
from sklearn.feature_selection import RFE,RFECV
from sklearn.linear_model import Lasso
from sklearn.svm import SVC,LinearSVC
import ml_feature_name


def featureRank(useFeature,trueSet,falseSet):

    # load data and split
    X_true = []
    for dn in trueSet:
        fin = open("./learn/data/"+useFeature+"_"+dn+".pkl","rb")
        X_true.append(pickle.load(fin))
        fin.close()
    X_true = np.vstack(X_true)
    print(X_true.shape)

    X_false = []
    for dn in falseSet:
        fin = open("./learn/data/"+useFeature+"_"+dn+".pkl","rb")
        X_false.append(pickle.load(fin))
        fin.close()
    X_false = np.vstack(X_false)
    print(X_false.shape)

    test_size = 0.3
    X_true_train,X_true_test = train_test_split(X_true ,test_size=test_size)
    X_false_train, X_false_test = train_test_split(X_false ,train_size=len(X_true_train),test_size=len(X_true_test))

    X = np.vstack([X_true_train,X_false_train])
    X_ = np.vstack([X_true_test,X_false_test])
    Y = [1]*len(X_true_train)+[0]*len(X_false_train)
    Y_ = [1]*len(X_true_test)+[0]*len(X_false_test)
    X,Y = shuffle(X,Y)
    X_,Y_ = shuffle(X_,Y_)

    featNames = ml_feature_name.getFeatureName(useFeature)

    clf = LinearSVC(C=0.1)
    rfe = RFE(estimator =clf, n_features_to_select=1,step=1)
    rfe.fit(X,Y)
    ranks = rfe.ranking_
    if(useFeature =="rp"):
        fout = open("./learn/feature/rp_feature_rank.txt","w")
        for i,r in enumerate(ranks):
            fout.write("{0} {1}\n".format(i,r))
        fout.close()

    rankFeat = list(zip(ranks,featNames))
    rankFeat.sort()
    for rf in rankFeat:
        if(useFeature in ["tfidf_1gram","tfidf_2gram","tfidf_3gram","tfidf_4gram"]):
            if(ml_feature_name.isDiatonic(rf[1])):
                print(rf)
        else:
            print(rf)
