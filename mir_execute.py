
'''
execute extracting all features
'''

import glob
import os,sys
import threading

import dataset

sys.path.append("./convert")
import mir_convert
import mir_make_mfcc_sample
import mir_make_degree
import mir_make_wordvector
import mir_gather_pickle

# read argument
argv = sys.argv
chord=False
key=False
rp=False
mfcc=False
core = 1
debug=False
if("-chord" in argv):
    chord=True
if("-key" in argv):
    key=True
if("-rp" in argv):
    rp=True
if("-mfcc" in argv):
    mfcc=True
if("-allfeature" in argv):
    key=True
    chord=True
    rp=True
    mfcc=True
if("-core" in argv):
    core = int(argv[argv.index("-core")+1])
if("-debug" in argv):
    debug=True


dataList = dataset.dataList
trainDataTrue = dataset.trainDataTrue
trainDataFalse = dataset.trainDataFalse
testData = dataset.testData

featureDir = "./feature/"
maxMusicSize = 20000000 # ignore music (larger than 20MByte & not .wav)

def getMIDfile(name):
    return featureDir+name+".txt"

# make stat file
# write valid filelist to MIDFile in feature folder
# # of line is music ID
def makeStat():
    for dataName in (trainDataTrue+trainDataFalse+testData):
        fileList = glob.glob(dataList[dataName]["directory"])
        fileList = [fp for fp in fileList if (os.stat(fp).st_size < maxMusicSize) | fp.endswith(".wav") ]
        fileList = [fp for fp in fileList if ("downsampled" not in fp) ]
        fileList.sort()
        fout = open(getMIDfile(dataList[dataName]["name"]),"w")
        for path in fileList:
            fout.write("{0}\n".format(path))
        fout.close()

# one thread task
# read taskFileList (array of [musicId and filePath])
# process and save feature to ./feature/[dataName]/[musicId]_[featureExt]
def threadTask(taskFileList,cid,dataName):
    if(len(taskFileList)==0):
        print("********** thread{0} no file assigned **********".format(cid))
        return
    print("********** thread{0} process ({1}-{2}) **********".format(cid,taskFileList[0][0],taskFileList[-1][0]))
    for count,fileInfo in enumerate(taskFileList):
        musicId, fileName = fileInfo
        print("********** thread{0} process {1} ({2}/{3}) **********".format(cid,fileName,count+1,len(taskFileList)))
        mir_convert.process(fileName,str(musicId),"./feature/"+dataName+"/",mfcc=mfcc,chord=chord,key=key,rp=rp,debug=debug)

def getFileList(dataName):
    fin = open(getMIDfile(dataList[dataName]["name"]),"r")
    fileList = []
    lc = 0
    for line in fin:
        fileList.append([lc,line.strip().replace("\\","/")])
        lc+=1;
    fin.close()
    return fileList

def checkMusicFeature(dataName,musicId):
    reqs = [".rp",".rh",".ssd","_chord.txt","_key.csv","_percussive_mfcc.csv","_harmonic_mfcc.csv","_normal_mfcc.csv"]
    res = True
    for req in reqs:
        p = "./feature/"+dataName+"/"+str(musicId)+req
        if(not os.path.exists(p)):
            res = False
        elif(os.stat(p).st_size == 0):
            res = False
    return res

# check whther there is all required feature
def checkDataSet():
    undoneFileList = []
    for dataName in (trainDataTrue+trainDataFalse+testData):
        fileList = getFileList(dataName)
        for felem in fileList:
            res = checkMusicFeature(dataName,felem[0])
            if(not res):
                undoneFileList.append(feleme)
    if(len(undoneFileList)==0):
        print("all features extracted")
    else:
        print(undoneFileList)

def checkDataSetPost():
    required = [".rp",".ssd",".rh"
    ,"_chord_tfidf_1gram.txt","_chord_tfidf_2gram.txt","_chord_tfidf_3gram.txt","_chord_tfidf_4gram.txt"
    ,"_degree_tfidf_1gram.txt","_degree_tfidf_2gram.txt","_degree_tfidf_3gram.txt","_degree_tfidf_4gram.txt"
    , "_normal_mfcc_stat.txt", "_harmonic_mfcc_stat.txt", "_percussive_mfcc_stat.txt"]
    fout = open("./feature/undonePost.txt","w")
    fout.close()
    for dataName in (trainDataTrue+trainDataFalse+testData):
        undone = []
        directory = dataList[dataName]["directory"]
        fileList = getFileList(dataName)

        fout = open("./feature/undonePost.txt","a")
        for i,p in fileList:
            for req in required:
                if(not os.path.exists("./feature/"+dataName+"/"+str(i)+req)):
                    undone.append("{0},{1},{2}\n".format(i,dataName,req))
        if(len(undone)>0):
            print(undone)
        else:
            print("{0}: all feature extracted".format(dataName))

# make threads
# read all file list in MIDFile and make set with [musicId, filePath]
# split files to thread number task and execute them
def process(dataName,chord=False,key=False,mfcc=False,rp=False,core=1):

    undoneFileList = []
    fileList = getFileList(dataName)
    for felem in fileList:
        res = checkMusicFeature(dataName,felem[0])
        if(not res):
            undoneFileList.append(felem)
    fileList = undoneFileList
    fileCount = len(fileList)

    if(fileCount==0):
        print("feature extraction completed")
        return
    print("{0} unextracted files in {1}".format(fileCount,dataName))

    block = fileCount//core
    res = fileCount%core

    taskList = []
    offset=0
    for cid in range(core):
        if(cid<res):
            taskFileList = fileList[(block+1)*cid:(block+1)*(cid+1)]
        else:
            taskFileList = fileList[block*cid+res:block*(cid+1)+res]
        task = threading.Thread(target=threadTask,name="thread"+str(cid),args=(taskFileList,cid,dataName))
        taskList.append(task)

    for task in taskList:
        task.start()
    for task in taskList:
        task.join()

# post processing for MFCC and ChordProgression
# first, reduce all MFCC to MFCC-statistics for each dataSet
# second, convert chordname+key to degreename for each dataSet
# third, calculate TfIdf feature vector of trainData with trainData
# fourth, calculate TfIdf feature vector of testData with trainData
def postProcessMFCC():
    for dataName in (trainDataTrue+trainDataFalse+testData):
        print("start {0}".format(dataName))
        fin = open(getMIDfile(dataList[dataName]["name"]),"r")
        fileList = getFileList(dataName)
        fileCount = len(fileList)
        mir_make_mfcc_sample.mfccPostProcess("./feature/"+dataName+"/",fileCount)
def postProcessChord():
    for dataName in (trainDataTrue+trainDataFalse+testData):
#    for dataName in (trainDataTrue):
        print("start {0}".format(dataName))
        fin = open(getMIDfile(dataList[dataName]["name"]),"r")
        fileList = getFileList(dataName)
        fileCount = len(fileList)
        mir_make_degree.makeDegreeFromChord("./feature/"+dataName+"/",fileCount,False)
        mir_make_degree.makeDegreeFromChord("./feature/"+dataName+"/",fileCount,True)

def postProcessTFIDF():
    trainDataDirectory = []
    testDataDirectory = []
    for dataName in trainDataTrue+trainDataFalse+testData:
        name = dataList[dataName]["name"]
        trainDataDirectory.append(featureDir+name+"/")
    for dataName in testData:
        name = dataList[dataName]["name"]
        testDataDirectory.append(featureDir+name+"/")
    mir_make_wordvector.makeTfidfFeature(testDataDirectory,trainDataDirectory,modeDegree=True)
    mir_make_wordvector.makeTfidfFeature(testDataDirectory,trainDataDirectory,modeDegree=False)

def update():
    for dataName in (trainDataTrue+trainDataFalse+testData):
        fileList = getFileList(dataName)
        fileCount = len(fileList)
        mir_gather_pickle.gather(featureDir+dataName+"/",fileCount,dataName)

if("-init" in argv):
    makeStat()
if("-extract" in argv):
    dataName = argv[argv.index("-extract")+1]
    process(dataName,chord,key,mfcc,rp,core)
if("-check" in argv):
    checkDataSet()
if("-postMFCC" in argv):
    postProcessMFCC()
if("-postChord" in argv):
    postProcessChord()
if("-postTFIDF" in argv):
    postProcessTFIDF()
if("-postCheck" in argv):
    checkDataSetPost()
if("-update" in argv):
    update()

if(len(argv)==1):
    print('''
    *arguments*

        -init : initialize file list for all dataset

        -chord : enable feature extraction of chordProgressionBar (this requires harmtrace and sonic-annotator)
        -key : enable feature extraction of keydetection (this requires sonic-annotator)
        -rp : enable feature extraction of rhythm pattern (this requires rp_extract folder in ./convert/, python2.7 only)
        -mfcc : enable feature extraction of MFCC (this requires librosa)
        -allfeature : enable all feature extraction

        -extract [dataset] : extract features from train data set
        -core [N] : set # of working thread in feature extraction to N (default : N = 1)

        -check : checking all extractions are done
        -postMFCC : execute heuristic dimensionality reduction to raw features
        -postChord : convert chord progression and key progression to shifted chord progression
        -postDegree : convert shifted chord progression to TFIDF-n-gram-wordvec
        -postCheck : checking all post processings are done

        -update : gather all features and send data to learning folder

        -debug : output all debug messages

    *How to add data set*
        1. locate your data set to ./data/[dataset name]/[SoundTrack Name]/*.*
        2. add [dataName] and [directory] to dataList in dataset.py
        3. add [dataName] to the list of trainDataTrue, trainDataFalse or testData

    *feature extraction steps*
        0. Install python, harmtrace, sonic-annotator, rp_extract, librosa and ffmpeg
            "Linux 64bit + Python2.7" is strongly recommended
        1. "python mir_execute.py -init"
        2. "python mir_execute.py -extract [dataset] -allfeature -core [N]"
        3. "python mir_execute.py -check"
        4. If extraction is completed, go to 5. If not, back to 2. You can see error message with -debug.
        5. "python mir_execute.py -postMFCC"
        6. "python mir_execute.py -postChord"
        7. "python mir_execute.py -postTFIDF"
        8. "python mir_execute.py -update"
        9. Move to ml_execute.py
    ''')
