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
import codecs

def test(useFeature,testSet):
    # load data and split
    fin = open("./learn/data/"+useFeature+"_"+testSet+".pkl","rb")
    X = pickle.load(fin)
    fin.close()

    fin = open("./learn/model/xgb_"+useFeature+".pkl","rb")
    clf = pickle.load(fin)
    fin.close()

    fin = codecs.open("./feature/"+testSet+".txt","r","utf-8")
    flist = []
    for line in fin:
        flist.append(line.strip().split("/")[-1])
    fin.close()

    probaY = clf.predict_proba(X)
    probaFile = [[probaY[i][1],v] for i,v in enumerate(flist)]
    probaFile.sort()
    probaFile.reverse()

    fout = codecs.open("./learn/test/"+testSet+"_"+useFeature+".txt","w","utf-8")
    for i,pf in enumerate(probaFile):
        fout.write("{0} {1:.5f} {2}\n".format(i,pf[0],pf[1]))
    fout.close()

def testForSoundTrack(useFeature,testSet):
    # load data and split
    fin = open("./learn/data/"+useFeature+"_"+testSet+".pkl","rb")
    X = pickle.load(fin)
    fin.close()

    fin = open("./learn/model/xgb_"+useFeature+".pkl","rb")
    clf = pickle.load(fin)
    fin.close()

    fin = codecs.open("./feature/"+testSet+".txt","r","utf-8")
    flist = []
    for line in fin:
        elem = line.strip().split("/")
        flist.append([elem[-2],elem[-1]])
    fin.close()

    probaY = clf.predict_proba(X)
    probaFile = [[v[0],probaY[i][1],v[1]] for i,v in enumerate(flist)]
    probaFile.sort()
    probaFile.reverse()

    fout = codecs.open("./learn/test/"+testSet+"_"+useFeature+".txt","w","utf-8")
    for i,pf in enumerate(probaFile):
        fout.write("{0} {1:.5f} {2} {3}\n".format(i,pf[1],pf[0],pf[2]))
    fout.close()
