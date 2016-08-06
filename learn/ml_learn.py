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


def train(useFeature,target,state=-1):
    test_size = 0.25
    cv = 3
    plot = False
    useXGBCV = False
    if(state==-1):
        state = np.random.randint(10000)

    # load data and split
    fin = open("./learn/data/"+useFeature+"_thbgm.pkl","rb")
    X_th = pickle.load(fin)
    fin.close()
    fin = open("./learn/data/"+useFeature+"_"+target+".pkl","rb")
    X_nth = pickle.load(fin)
    fin.close()

    print(np.array(X_th).shape,np.array(X_nth).shape)

    X_tr,X_ts = train_test_split(X_th ,test_size=test_size,random_state=state)
    X_ntr,X_nts = train_test_split(X_nth ,train_size=len(X_tr),test_size=len(X_ts),random_state=state+1)
    X = X_tr+X_ntr
    Y = [1]*len(X_tr)+[0]*len(X_ntr)
    X_ = X_ts+X_nts
    Y_ = [1]*len(X_ts)+[0]*len(X_nts)
    X,Y = shuffle(X,Y,random_state=state)
    X_,Y_ = shuffle(X_,Y_,random_state=state)
    featureCount = len(X_th[0])

    # grid search and find best estimator
    clf = xgb.XGBClassifier()
    param = ml_learn_tune.tune[useFeature]
    it = 1
    for v in param.values():
        it*=len(v)
    print("Start {0} iteration GridSearchCV @ {1} data with {2} features".format(it*cv,len(X),featureCount))

    #grid = GridSearchCV(clf, param, n_jobs=1, cv=cv, scoring="roc_auc")
    grid = GridSearchCV(clf, param, n_jobs=1, cv=cv, scoring="f1",iid=False)
    grid.fit(X,Y)
    for scores in grid.grid_scores_:
        print(scores)
    clf = grid.best_estimator_

    # optmize n_estimator
    if(useXGBCV):
        xgb_param = clf.get_xgb_params()
        num_boost_round = clf.get_params()['n_estimators']
        early_stopping_rounds = 50
        xgtrain = xgb.DMatrix(X, label=Y)
        xgtest = xgb.DMatrix(X_)
        cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=num_boost_round, nfold=cv,
            metrics=['error'], early_stopping_rounds=early_stopping_rounds, show_progress=False)
        clf.set_params(n_estimators=cvresult.shape[0])
        print(cvresult.shape[0])
        clf.fit(X,Y,eval_metric=['auc'])

    # predict test set
    predY_ = clf.predict(X_)
    predProbY_ = clf.predict_proba(X_)[:,1]
    auc = roc_auc_score(Y_, predProbY_)
    fpr,tpr,_ = roc_curve(Y_,predProbY_)

    # reports
    print("Best Params : {0}".format(grid.best_params_))
    print(classification_report(Y_,predY_,target_names=["not toho","toho"]).replace("\n\n","\n"),end="")
    cf = confusion_matrix(Y_,predY_)
    print(cf)
    prec = cf[1][1]/(cf[1][0]+cf[1][1])
    print("Precision : {0}".format(prec))
    print("Recall    : {0}".format(cf[1][1]/(cf[0][1]+cf[1][1])))
    acc = (cf[1][1]+cf[0][0])/(cf[0][0]+cf[1][0]+cf[0][1]+cf[1][1])
    print("Accur : {0}".format(acc))
    print("AUC   : {0}".format(auc))

    score = prec

    # update best estimator
    scorepath = "./learn/model/"+target+"score.txt"
    modelpath = "./learn/model/"+target+"xgb_"+useFeature+".pkl"
    scores = {}
    if(os.path.exists(scorepath)):
        fin = open(scorepath,"r")
        for line in fin:
            elem = line.split(",")
            scores[elem[0]]=float(elem[1])
        fin.close()
    isBest = useFeature not in scores
    lastBest=0.0
    if(not isBest):
        isBest = scores[useFeature] < score
        lastBest = scores[useFeature]
    if(isBest):
        print("Update {0} precision {1}->{2}".format(useFeature,lastBest,score))
        scores[useFeature]=score
        fout=open(modelpath,"wb")
        pickle.dump(clf,fout)
        fout.close()
        fout=open(scorepath,"w")
        for k,v in scores.items():
            fout.write(k+","+str(v)+"\n")
        fout.close()


    # retrieve feature name
    featNames = ml_feature_name.getFeatureName(useFeature)

    # get important feature id
    featImp = [0]*featureCount
    sumImp = 0
    for fn,val in clf.booster().get_fscore().items():
        featImp[int(fn[1:])]=float(val)
        sumImp += val
    for ind in range(featureCount):
        featImp[ind] = [featImp[ind]/sumImp,ind]
    featImp.sort()
    featImp.reverse()

    for i,featId in enumerate(featImp[0:20]):
        print("{0}:s={1:.3f} {2}".format(i,featId[0],featNames[featId[1]]))
    if(isBest):
        fout = open("./learn/feature/"+target+"_"+useFeature+".txt","w")
        for i,featId in enumerate(featImp):
            fout.write("{0} {1} {2:.5f} {3}\n".format(i,featId[1],featId[0],featNames[featId[1]]))
        fout.close()
