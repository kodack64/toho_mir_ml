import numpy as np
import xgboost as xgb
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report,roc_curve,roc_auc_score,confusion_matrix,f1_score
from sklearn.utils import shuffle,resample
import glob,pickle,os
import ml_learn_tune
from sklearn.feature_selection import RFE,RFECV
from sklearn.linear_model import Lasso
from sklearn.svm import SVC,LinearSVC
import ml_feature_name


def featureReductionTest(useFeature,trueSet,falseSet,dim=10,state=-1):
    if(state==-1):
        state = np.random.randint(10000)

    # load data and split
    X_true = []
    for dn in trueSet:
        fin = open("./learn/data/"+useFeature+"_"+dn+".pkl","rb")
        X_true.append(pickle.load(fin))
        fin.close()
    X_true = np.vstack(X_true)
#    print(X_true.shape)

    X_false = []
    for dn in falseSet:
        fin = open("./learn/data/"+useFeature+"_"+dn+".pkl","rb")
        X_false.append(pickle.load(fin))
        fin.close()
    X_false = np.vstack(X_false)
#    print(X_false.shape)

    test_size = 0.3
    X_true_train,X_true_test = train_test_split(X_true ,test_size=test_size,random_state=state)
    X_false_train, X_false_test = train_test_split(X_false ,train_size=len(X_true_train),test_size=len(X_true_test),random_state=state+1)

    X = np.vstack([X_true_train,X_false_train])
    X_ = np.vstack([X_true_test,X_false_test])
    Y = [1]*len(X_true_train)+[0]*len(X_false_train)
    Y_ = [1]*len(X_true_test)+[0]*len(X_false_test)
    X,Y = shuffle(X,Y)
    X_,Y_ = shuffle(X_,Y_)

    featNames = ml_feature_name.getFeatureName(useFeature)

    clf = LinearSVC(C=0.1)
    rfe = RFE(estimator =clf, n_features_to_select=dim,step=10)
    rfe.fit(X,Y)
    Xs = rfe.transform(X)
    Xs_ = rfe.transform(X_)
    clf.fit(Xs,Y)
    Yp = clf.predict(Xs)
    Yp_ = clf.predict(Xs_)

    supIndex = rfe.transform(list(range(len(X[0]))))[0]
    feats = [[abs(clf.coef_[0][i]),clf.coef_[0][i],v,featNames[v]] for i,v in enumerate(supIndex)]
    feats.sort()
    print("\n".join(list(map(str,feats))[::-1]))
    print(classification_report(Y,Yp))
    print(classification_report(Y_,Yp_))

    featNames = ml_feature_name.getFeatureName(useFeature)
    arr = Xs.T[0]
    reg = list(zip(arr,Y))
    reg.sort()
#    plt.plot(list(range(len(reg))),reg)
#    plt.ylim(0,2)
#    plt.show()


    if(useFeature=="rp"):
        fin = open("./feature/id_rhythm_barkband.txt","r")
        bark = [int(v) for v in fin.readline().split(",")]
        fin.close()

        barkName = []
        for ind in range(len(bark)):
            if(ind==0):
                barkName.append("0-"+str(bark[ind])+"Hz")
            else:
                barkName.append(str(bark[ind-1])+"-"+str(bark[ind])+"Hz")

        flucName = ["{0:.0f}bpm".format(((v)+1)*0.17*60) for v in range(60)]
        barkName.reverse()
        mat = np.zeros((60,24))
        for i,ind in enumerate(supIndex):
            val = clf.coef_[0][i]
            mat[ind//24,ind%24]=val
        mat =np.fliplr(mat)
        plt.yticks(range(24),barkName)
        plt.xticks(range(60),flucName,rotation="vertical")
        plt.imshow(mat.T,cmap="Greys_r")
        plt.savefig("./learn/feature/rp_rank"+str(dim)+".png")
        plt.show()
    return f1_score(Y,Yp),f1_score(Y_,Yp_)

if __name__ == "__main__":
    gram = ["tfidf_1gram","tfidf_2gram","tfidf_3gram","tfidf_4gram"]
    dims = list(range(1,200,10))
    st = np.random.randint(0,10000,len(dims)*5)
    gsc = []
    for g in gram:
        sc = []
        sct = []
        scv = []
        scvt = []
        for dim in dims:
            f1 = []
            f1t = []
            for i in range(5):
                t1,t2 = featureReductionTest(g,["thbgm"],["anison"],dim=dim,state=st[(dim-1)//10*5+i])
                f1.append(t1)
                f1t.append(t2)
#                print(t1,t2)
            f1=np.array(f1)
            f1t=np.array(f1t)
            sc.append(np.mean(f1))
            sct.append(np.mean(f1t))
            scv.append(np.var(f1))
            scvt.append(np.var(f1t))
            print("{0} dim={1}".format(g,dim))
#        plt.errorbar(list(range(1,30)),sc,yerr=scv,label=g)
        plt.errorbar(dims,sct,yerr=scvt,label=g+" test")
    plt.legend(loc=4)
    plt.show()

'''
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
'''
