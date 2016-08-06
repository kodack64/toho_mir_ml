
def isDiatonic(cps):
    diatonic = ["Am","C","Dm","Em","F","G"]
    clist = cps.split("-")
    flag=True
    for c in clist:
        flag = flag & (c in diatonic)
    return flag

def getFeatureName(useFeature):
    featNames = []
    if(useFeature in ["tfidf_1gram","tfidf_2gram","tfidf_3gram","tfidf_4gram"]):
        idname = "./feature/id_degree_"+useFeature+".txt"
        fin = open(idname,"r")
        for line in fin:
            chordStr = line.strip().split(",")[1].replace("t","-")
            if(chordStr.endswith("-")):
                chordStr = chordStr[:-1]
            featNames.append(chordStr)
        fin.close()
        chordToDegreeMapMajor = {
            "C":"I","Cm":"Im",
            "Db":"IIb","Dbm":"IIbm",
            "D":"II","Dm":"IIm",
            "Eb":"IIIb","Ebm":"IIIbm",
            "E":"III","Em":"IIIm",
            "F":"IV","Fm":"IVm",
            "Gb":"Vb","Gbm":"Vbm",
            "G":"V","Gm":"Vm",
            "Ab":"VIb","Abm":"VIbm",
            "A":"VI","Am":"VIm",
            "Bb":"VIIb","Bbm":"VIIbm",
            "B":"VII","Bm":"VIIm",
        }
        chordToDegreeMapMinor = {
            "C":"IIIb","Cm":"IIIbm",
            "Db":"III","Dbm":"IIIm",
            "D":"IV","Dm":"IVm",
            "Eb":"Vb","Ebm":"Vbm",
            "E":"V","Em":"Vm",
            "F":"VIb","Fm":"VIbm",
            "Gb":"VI","Gbm":"VIm",
            "G":"VIIb","Gm":"VIIbm",
            "Ab":"VII","Abm":"VIIm",
            "A":"I","Am":"Im",
            "Bb":"IIb","Bbm":"IIbm",
            "B":"II","Bm":"IIm",
        }
#        romanMaj = ["I","IIb","II","IIIb","III","IV","Vb","V","VIb","VI","VIIb","VII"]
#        romanMin = ["IIIb","III","IV","Vb","V","VIb","VI","VIIb","VII","I","IIb","II"]
#        nameMajMin = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
#        minmaj = ["","m"]
# #       for f in featId:
#            fmaj = "-".join([romanMaj[v%12]+minmaj[v//12] for v in f])
#            fmin = "-".join([romanMin[v%12]+minmaj[v//12] for v in f])
#            featNames.append("{0} ({1})".format(fmaj,fmin))

    if(useFeature in ["mfcc","hmfcc","pmfcc"]):
        fin = open("./feature/id_mfcc.txt")
        for line in fin:
            featNames.append(line.strip().split(",")[1])
        fin.close()

    if(useFeature in ["rp","rh","ssd"]):
        fin = open("./feature/id_rhythm_barkband.txt","r")
        bark = [int(v) for v in fin.readline().split(",")]
        fin.close()
        barkName = []
        for ind in range(len(bark)):
            if(ind==0):
                barkName.append("0-"+str(bark[ind])+"Hz")
            else:
                barkName.append(str(bark[ind-1])+"-"+str(bark[ind])+"Hz")
        ssdName = ["mean","var","skew","kurtosis","median","min","max"]
        if(useFeature is "rp"):
            featureCount = 1440
            for ind in range(featureCount):
                bands = barkName[ind%24]
                fluc = ((ind//24)+1)*0.17*60
                featNames.append("band={0} bpm={1:.1f}".format(bands,fluc))
        if(useFeature is "rh"):
            featureCount=60
            for ind in range(featureCount):
                fluc = ((ind+1)*0.17)*60
                featNames.append("bpm={0:.1f}".format(fluc))
        if(useFeature is "ssd"):
            featureCount = 168
            for ind in range(featureCount):
                bands = barkName[ind%24]
                ssdn = ssdName[ind//24]
                featNames.append("band={0} stat={1}".format(bands,ssdn))
    return featNames
