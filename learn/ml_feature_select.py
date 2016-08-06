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


def featureSelect(useFeature,trueSet,falseSet):

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

    test_size = 0.5
    X_true_train,X_true_test = train_test_split(X_true ,test_size=test_size)
    X_false_train, X_false_test = train_test_split(X_false ,train_size=len(X_true_train),test_size=len(X_true_test))
    print(X_true_train.shape,X_true_test.shape)
    print(X_false_train.shape,X_false_test.shape)

    X = np.vstack([X_true_train,X_false_train])
    X_ = np.vstack([X_true_test,X_false_test])
    Y = [1]*len(X_true_train)+[0]*len(X_false_train)
    Y_ = [1]*len(X_true_test)+[0]*len(X_false_test)
    X,Y = shuffle(X,Y)
    X_,Y_ = shuffle(X_,Y_)

    featNames = ml_feature_name.getFeatureName(useFeature)

#    clf = Lasso(alpha=0.01)
    clf = LinearSVC(C=0.1)
    rfe = RFECV(estimator = clf , step = 1,cv = 3,verbose = 1)
    rfe.fit(X,Y)
    print("best is {0} features".format(rfe.n_features_))
#    ranking = rfe.ranking_;
#    fn = list(zip(ranking,featNames))
#    fn.sort()
#    print("\n".join([str(v) for v in fn][:20]))
    ss = rfe.grid_scores_
    plt.plot(range(len(ss)),ss)
    plt.savefig("./learn/feature/"+useFeature+"_fselect.png")
    plt.show()

    Xs = rfe.transform(X)
    Xs_ = rfe.transform(X_)
    clf.fit(Xs,Y)
    Yp = clf.predict(Xs)
    Yp_ = clf.predict(Xs_)
    print(classification_report(Y,Yp))
    print(classification_report(Y_,Yp_))
    clf.fit(X,Y)
    Yp = clf.predict(X)
    Yp_ = clf.predict(X_)
    print(classification_report(Y,Yp))
    print(classification_report(Y_,Yp_))
    print(X.shape,Xs.shape)
