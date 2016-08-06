
import pickle
import numpy as np
from sklearn.cross_validation import train_test_split,StratifiedKFold
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

def stacking(featureNames,dataNames):

    rs = np.random.randint(100000)

    # check data set info
    print("*** data load ***")
    print(featureNames,dataNames)
    Xs = []
    ratio = 0.7
    for dataName in dataNames:
        fin = open("./learn/data/"+featureNames[0]+"_"+dataName+".pkl","rb")
        Xs.append(pickle.load(fin))
        fin.close()
    minDataSize = min([len(X) for X in Xs])
    trainSize = int(minDataSize * ratio)
    testSize = minDataSize-trainSize
    clfs = [RandomForestClassifier(),XGBClassifier(),SVC(probability=True,C=1),
        ExtraTreesClassifier(),LogisticRegression()]

    featureCount = [0]
    for featureName in featureNames:
        fin = open("./learn/data/"+featureName+"_"+dataNames[0]+".pkl","rb")
        X = pickle.load(fin)
        fin.close()
        featureCount.append(featureCount[-1]+len(X[0]))

    print("train,test = {0},{1}".format(trainSize,testSize))
    print("featureCount boundary = {0}".format(featureCount))
    print("models = {0}".format(clfs))

    # generate 1st layer feature vector
    print("\n*** 1st layer ***")
    X1_tr = []
    X1_te = []
    Y1_tr = []
    Y1_te = []
    featCount = [0]
    for i,dataName in enumerate(dataNames):
        Xf = []
        for featureName in featureNames:
            fin = open("./learn/data/"+featureName+"_"+dataName+".pkl","rb")
            X = np.array(pickle.load(fin))
            fin.close()
            print("first layer from {0}-{1} : {2}".format(dataName,featureName,X.shape))
            Xf.append(X)
        Xf = np.hstack(Xf)
        X_tr,X_te = train_test_split(Xf ,train_size=trainSize, test_size=testSize,random_state=rs)
#        print(X_tr.shape,X_te.shape)
        X1_tr.append(X_tr)
        X1_te.append(X_te)
        Y1_tr += [i]*trainSize
        Y1_te += [i]*testSize
    X1_tr = np.vstack(X1_tr)
    X1_te = np.vstack(X1_te)
    Y1_tr = np.array(Y1_tr)
    Y1_te = np.array(Y1_te)

    print("train vector : {0} label {1}".format(X1_tr.shape,Y1_tr.shape))
    print("test vector : {0} label {1}".format(X1_te.shape,Y1_te.shape))

    # generate 2nd layer feature vector
    print("\n*** 2nd layer ***")
    featureLength = len(featureNames)*len(dataNames)*len(clfs)
    featurePerModel = len(featureCount)*len(dataNames)
    X2_tr = np.zeros((trainSize*len(dataNames),featureLength))
    X2_te = np.zeros((testSize*len(dataNames),featureLength))
    Y2_tr = Y1_tr
    Y2_te = Y1_te
    nfold = 5

    print("{0}-class * {1}-models * {2}-features -> length = {3}".format(len(dataNames),len(clfs),len(featureNames),featureLength))
    print("{0}-fold * {1}-models * {2}-features -> #train = {3}".format(nfold,len(clfs),len(featureNames),nfold*len(clfs)*len(featureNames)))

    totacc = [0]*len(featureNames)
    skf = StratifiedKFold(Y1_tr,n_folds =nfold,shuffle=True,random_state=rs)
    i=0
    for trind,valind in skf:
        Xtrall = X1_tr[trind]
        Xvalall = X1_tr[valind]
        Ytr = Y1_tr[trind]
        Yval = Y1_tr[valind]
        for fi in range(len(featureCount)-1):
            Xtr = Xtrall[:,featureCount[fi]:featureCount[fi+1]]
            Xval = Xvalall[:,featureCount[fi]:featureCount[fi+1]]

            for ci,clf in enumerate(clfs):
                clf.fit(Xtr,Ytr)
                proba = clf.predict_proba(Xval)

#                           print(X2_tr.shape)
#               print(X2_tr[valind].shape)
                for pi,ind in enumerate(valind):
                    pos = fi*len(dataNames)*len(clfs)+len(dataNames)*ci
                    posend = pos+len(dataNames)
                    X2_tr[ind,pos:posend] = proba[pi]
#               (X2_tr[valind])[:,len(dataNames)*fi:len(dataNames)*(fi+1)] = proba

                Yvalp = clf.predict(Xval)
                acc = accuracy_score(Yval,Yvalp)
                print("{0}th fold : {1}th feature : {2}th model : validation acc = {3}".format(i,fi,ci,acc))
                totacc[fi] += acc
        i+=1
    for fi,acc in enumerate(totacc):
        print("{0} th feature {1} : ave acc = {2}".format(fi,featureNames[fi],acc/nfold/len(clfs)))

    fout = open("./learn/stack/result.txt","a")

    for fi in range(len(featureCount)-1):
        Xtr = X1_tr[:,featureCount[fi]:featureCount[fi+1]]
        Xte = X1_te[:,featureCount[fi]:featureCount[fi+1]]
        Ytr = Y1_tr
        Yte = Y1_te
        for ci,clf in enumerate(clfs):
            clf.fit(Xtr,Ytr)
            proba = clf.predict_proba(Xte)
            pos = fi*len(dataNames)*len(clfs)+len(dataNames)*ci
            posend = pos+len(dataNames)
            X2_te[:,pos:posend] = proba

            Ypr = clf.predict(Xte)
            acc = accuracy_score(Yte,Ypr)
            print("{0}th feature : {1}th model : test acc = {2}".format(fi,ci,acc))
            fout.write("{0} ".format(acc))
    Xtr = X1_tr
    Xte = X1_te
    Ytr = Y1_tr
    Yte = Y1_te
    for ci,clf in enumerate(clfs):
        clf.fit(Xtr,Ytr)
        Ypr = clf.predict(Xte)
        acc = accuracy_score(Yte,Ypr)
        print("all feature : {0}th model : test acc = {1}".format(ci,acc))
        fout.write("{0} ".format(acc))

    print("train vector {0}".format(X2_tr.shape))
    print("test vector {0}".format(X2_te.shape))

    # 3rd layer
    print("\n*** 3rd layer ***")
    clf = XGBClassifier()
    clf.fit(X2_tr,Y2_tr)
    Y2_tr_pr = clf.predict(X2_tr)
    Y2_te_pr = clf.predict(X2_te)
    train_acc = accuracy_score(Y2_tr,Y2_tr_pr)
    test_acc = accuracy_score(Y2_te,Y2_te_pr)
    print("final acc (train,test) = {0},{1}".format(train_acc,test_acc))
    fout.write("{0} ".format(test_acc))
    fout.write("\n")
    fout.close()
