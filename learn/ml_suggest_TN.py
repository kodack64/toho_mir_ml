

import os
import numpy as np
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn import svm
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split
from sklearn.utils import shuffle
import xgboost as xgb
import glob
import random
import pickle
import ml_learn_tune
import matplotlib.pyplot as plt
import codecs


def suggest(useFeature,trial = 1000):
    test_size = 0.25

    # load data and split
    fin = open("./learn/data/"+useFeature+"_thbgm.pkl","rb")
    X_th = pickle.load(fin)
    fin.close()
    Y_th = [1]*len(X_th)
    thnum = len(X_th)
    fin = open("./learn/data/"+useFeature+"_anison.pkl","rb")
    X_nth = pickle.load(fin)
    Y_nth = [0]*len(X_th)
    fin.close()
    nthnum = len(X_nth)
    X_tot = X_th+X_nth


    def update():
        X_tr,X_ts = train_test_split(X_th ,test_size=test_size)
        X_ntr,X_nts = train_test_split(X_nth  ,train_size=len(X_tr),test_size=len(X_ts))
        X = X_tr+X_ntr
        Y = [1]*len(X_tr)+[0]*len(X_ntr)
        X_ = X_ts+X_nts
        Y_ = [1]*len(X_ts)+[0]*len(X_nts)
        X,Y = shuffle(X,Y)
        X_,Y_ = shuffle(X_,Y_)

        # predict
        clf = xgb.XGBClassifier()
        tune = ml_learn_tune.tune[useFeature]
        grid = GridSearchCV(clf,tune,cv=3,n_jobs=1)
        grid.fit(X,Y)
        clf = grid.best_estimator_
        predProbaY_ = clf.predict_proba(X_)[:,1]

        # if there is no stat file, generete it
        statText = "./learn/stat/stat_"+useFeature+".txt"
        if(not os.path.exists(statText)):
            fout = open(statText,"w")
            fout.write("0,0\n"*len(X_tot))
            fout.close()

        # read stat
        freq = []
        fin = open(statText,"r")
        for line in fin:
            freq.append([float(val) for val in line.split(",")])
        fin.close()

        # update stat
        for ind in range(len(predProbaY_)):
            curs = [i for i,v in enumerate(X_tot) if v==X_[ind]]
            for cur in curs:
                freq[cur][0]+=1.0/len(curs)
                freq[cur][1]+=predProbaY_[ind]/len(curs)
        fout = open(statText,"w")
        for ind in range(len(freq)):
            fout.write("{0},{1}\n".format(freq[ind][0],freq[ind][1]))
        fout.close()

    # loop [trial] update
    for i in range(trial):
        update()
        print("{0}/{1}".format(i+1,trial))

    # read original file and songname
    fin = open("./feature/thbgm.txt")
    mlist = []
    for line in fin:
    	mlist.append(line.split("/")[-1].strip())
    fin.close()
    fin = open("./feature/thbgm_music.txt")
    mnlist = []
    for line in fin:
    	mnlist.append(line.strip())
    fin.close()
    fin = codecs.open("./feature/"+"anison"+".txt","r","utf-8")
    mlist_nth = []
    for line in fin:
    	mlist_nth.append(line.split("/")[-1].strip())
    fin.close()

    # read stat and calculate mean robability
    fin = open("./learn/stat/stat_"+useFeature+".txt","r")
    freq = []
    count = 0
    for line in fin:
        elem = [float(val) for val in line.split(",")]
        freq.append([elem[1]/elem[0],count])
        count += 1
    fin.close()

    # divide data and sort
    freq_th = freq[:thnum]
    freq_nth = [[1-fr[0],fr[1]] for fr in freq[thnum:]]
    freq_th.sort()
    freq_nth.sort()

    # plot sample-accuracy curve
    xth = np.linspace(0,1,thnum)
    xnth = np.linspace(0,1,nthnum)
    plt.xlim(0,1)
    plt.plot([0,1],[0.5,0.5],label="random classifier")
    plt.plot(xth,[e[0] for e in freq_th],label=useFeature+" toho")
    plt.plot(xnth,[e[0] for e in freq_nth],label=useFeature+" not toho")
    plt.legend()
    plt.savefig("./learn/stat/stat_"+useFeature+".png")

    # write music-name in ranking order
    fout = open("./learn/stat/stat_"+useFeature+"_th_rank.txt","w")
    for rank in range(len(freq_th)):
        idt = freq_th[rank][1]
        fout.write("{0},{1},{2:.5f},{3} {4}\n".format(rank+1,idt,freq_th[rank][0],mlist[idt],mnlist[idt]))
    fout.close()

    fout = codecs.open("./learn/stat/stat_"+useFeature+"_nth_rank.txt","w","utf-8")
    for rank in range(len(freq_nth)):
        idt = freq_nth[rank][1]-thnum
        fout.write("{0},{1},{2:.5f},{3}\n".format(rank+1,idt,freq_nth[rank][0],mlist_nth[idt]))
    fout.close()

    topn = worn = 10
    for rank in range(topn):
        idt = freq_th[rank][1]
        print("{0}:p={1:.5f}:{2}->{3}".format(rank+1,freq_th[rank][0],mlist[idt],mnlist[idt]))
    for rank in range(len(freq_th)-worn,len(freq_th)):
        idt = freq_th[rank][1]
        print("{0}:p={1:.5f}:{2}->{3}".format(rank+1,freq_th[rank][0],mlist[idt],mnlist[idt]))
