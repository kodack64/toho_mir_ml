
'''
execute extracting all features
'''

import glob
import os,sys
import threading

import dataset

sys.path.append("./learn")
import ml_learn
import ml_construct
import ml_visualize
import ml_suggest_TN
import ml_suggest_test
import ml_feature_depend
import ml_feature_select
import ml_feature_rank
import ml_feature_select_report
import ml_stacking

dataList = dataset.dataList
trainDataTrue = dataset.trainDataTrue
trainDataFalse = dataset.trainDataFalse
testData = dataset.testData
allDataSet = trainDataTrue+trainDataFalse+testData

#useFeatures = ["mfcc","hmfcc","pmfcc","tfidf_1gram","tfidf_2gram","tfidf_3gram","tfidf_4gram","rp","rh","ssd"]
useFeatures = ["mfcc","tfidf_1gram","tfidf_2gram","tfidf_3gram","tfidf_4gram","ssd"]

# read argument
argv = sys.argv
useFeature = ""
state = -1
trial = 300
if("-rp" in argv):
    useFeature = "rp"
if("-rh" in argv):
    useFeature = "rh"
if("-ssd" in argv):
    useFeature = "ssd"
if("-mfcc" in argv):
    useFeature = "mfcc"
if("-hmfcc" in argv):
    useFeature = "hmfcc"
if("-pmfcc" in argv):
    useFeature = "pmfcc"
if("-tfidf_1gram" in argv):
    useFeature = "tfidf_1gram"
if("-tfidf_2gram" in argv):
    useFeature = "tfidf_2gram"
if("-tfidf_3gram" in argv):
    useFeature = "tfidf_3gram"
if("-tfidf_4gram" in argv):
    useFeature = "tfidf_4gram"
if("-random" in argv):
    state = int(argv[argv.index("-random")+1])
if("-trial" in argv):
    trial = int(argv[argv.index("-trial")+1])

featureDir = "./feature/"

if("-construct" in argv):
    ml_construct.construct(allDataSet)
if("-visualize" in argv):
    ref = argv[argv.index("-visualize")+1]
    for f in useFeatures:
        ml_visualize.visualize(f,"thbgm",ref)
if("-frank" in argv):
    ml_feature_rank.featureRank(useFeature,["thbgm"],["gtzan"])
#    ml_feature_rank.featureRank(useFeature,["anison"],["gtzan"])
if("-fselect" in argv):
    ml_feature_select.featureSelect(useFeature,["thbgm"],["gtzan"])
if("-train" in argv):
    target = argv[argv.index("-train")+1]
    if(useFeature is not ""):
        ml_learn.train(useFeature,target)
if("-fdepend" in argv):
    ml_feature_depend.featureDependency(useFeature,"gtzan")
if("-fdependrfe" in argv):
    ml_feature_depend.featureDependencyWithRFE(useFeature,"gtzan")

if("-suggestTN" in argv):
    ml_suggest_TN.suggest(useFeature,trial)
if("-reduct" in argv):
    dim = int(argv[argv.index("-reduct")+1])
    ml_feature_select_report.featureReductionTest(useFeature,["thbgm"],["anison"],dim)

if("-stacking" in argv):
    ml_stacking.stacking(["mfcc","tfidf_3gram","ssd"],["thbgm","gtzan","anison"])

if("-test" in argv):
    testSet = argv[argv.index("-test")+1]
    ml_suggest_test.test(useFeature,testSet)
if("-testst" in argv):
    testSet = argv[argv.index("-testst")+1]
    ml_suggest_test.testForSoundTrack(useFeature,testSet)

if(len(argv)==1):
    print('''
    *arguments*
        -construct : construct data pickle from ./feature/
        -visualize [target] : execute dimensionality reduction to 2d by LDA and compare "thbgm" and [target] dataset
        -frank : analyse feature rank by recursive feature ellmination with LinearSVM
        -fselect : analysis best feature number by RFE cross validation with LinearSVM
        -train [target] : train classification wiht "thbgm" and [target] dataset
        -fdepend : analyse feature denependency of the most important 30 features with XGBoost
        -suggestTN : averaging predict probability and suggest the most "False Positive" and "False Negative" samples

        -random [s] : specify random state
        -trial [N] : specify trial number in -suggestTN

        above analysis must specify one of below features
            -rp, -rh, -ssd : feature about rhythm patterns
            -mfcc, -hmfcc, -pmfcc : feature about MFCC
            -tfidf_1gram, -tfidf_2gram, -tfidf_3gram, -tfidf_4gram : feature about Chord Progression

    ''')
