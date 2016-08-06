
'''
make degree name list from  chord name list and key
'''

import os

chordToIdMap = {
    "N":-1
    ,"C":0
    ,"C#":1
    ,"Db":1
    ,"D":2
    ,"D#":3
    ,"Eb":3
    ,"E":4
    ,"F":5
    ,"F#":6
    ,"Gb":6
    ,"G":7
    ,"G#":8
    ,"Ab":8
    ,"A":9
    ,"A#":10
    ,"Bb":10
    ,"B":11
    }
idToChordMap = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B",
                "Cm","Dbm","Dm","Ebm","Em","Fm","Gbm","Gm","Abm","Am","Bbm","Bm"]

idToDegreeMap = {
    -1:"NC"
    ,0:"I"
    ,1:"IIb"
    ,2:"II"
    ,3:"IIIb"
    ,4:"III"
    ,5:"IV"
    ,6:"Vb"
    ,7:"V"
    ,8:"VIb"
    ,9:"VI"
    ,10:"VIIb"
    ,11:"VII"
    ,12:"Im"
    ,13:"IIbm"
    ,14:"IIm"
    ,15:"IIIbm"
    ,16:"IIIm"
    ,17:"IVm"
    ,18:"Vbm"
    ,19:"Vm"
    ,20:"VIbm"
    ,21:"VIm"
    ,22:"VIIbm"
    ,23:"VIIm"
    }
# when major
# given [G-A-Bm in D] -> [F-G-Am in C] -> [5-7-9m in 0(maj)]
# [a-b in k(maj)] -> [(a-k)-(b-k) in 0(maj)] = [(a+12-k)-(b+12-k) in 0(maj)]
# when minor
# given [G-A-Bm in Bm] -> [F-G-Am in Am] -> [5-7-9m in 9(min)] -> [5-7-9m in 0(maj)]
# [a-b in k(min)] -> [(a-(k-9))-(b-(k-9)) in 9(min)] -> [(a-k+21)-(b-k+21) in 9(min)] -> [(a-k+21)-(b-k+21) in 0(maj)]

majMinMap = {"maj":0,"min":1}
chordNameCount = 12

def makeDegreeFromChord(directory,fileCount,modeDegree=True):

    hist = [0]*24

    for count in range(fileCount):

        # read chord names
        # format
        # if chord == NC : [beatCount];["N":0.0];[startTime];[endTime]
        # else : [beatCount];[ChordRoot:min|maj:length];[startTime];[endTime]
        # make array of ["beat","ChordId","StartTime"]
        # ignore NC
        chordProgression = []
        fin = open(directory+str(count)+"_chord.txt","r")
        for line in fin:
            (beat,chord,start,end) = line.split(";")
            chordElem = chord.split(":")
            if(chordElem[0] is "N"):
                continue

            beat = int(beat)
            chordRoot = chordToIdMap[chordElem[0]]
            minmaj = majMinMap[chordElem[1]]
            start = float(start)
            chordId = chordRoot + chordNameCount*minmaj
            chordProgression.append([beat,chordId,start])
        fin.close()
#        print(chordProgression)

        # packing in each bar
        # make chordProgressionBar, array of [ bar start time , [chordIds in bar]]
        chordProgressionBar = []
        barChord = []
        barStart = 0.0
        for chordInfo in chordProgression:
            beat, chordId, start = chordInfo
            if(beat==1):
                if(len(barChord)>0):
                    chordProgressionBar.append([barStart,barChord])
                barChord = [chordId]
                barStart = start
            else:
                barChord.append(chordId)
        if(len(barChord)>0):
            chordProgressionBar.append([barStart,barChord])
#        print(chordProgressionBar)

        # read key progression
        # format [filename or null],[time],[key Id],[key Id string]
        # keyId is NC = 0 , 1-12:major , 13:24:minor, 25:unknown
        # output keyProgression, array of [startTime, key(0-11), minmaj ]
        keyProgression = []
        fin = open(directory+str(count)+"_key.csv","r")
        for line in fin:
            _,t,keyId,_ = line.split(",")
            t = float(t)
            keyId = int(keyId)
            if(keyId>=25):
                continue
            key = (keyId-1)%12
            minmaj = (keyId-1)//12
            keyProgression.append([t,key,minmaj])
        fin.close()
        if(len(keyProgression)==0):
            keyProgression.append([0.0,0,0])
#        print(keyProgression)

        # fix key change timing to the nearest beggining of bar
        # keyProgression becomes array of [startTime, key(0-11), minmaj, startBar]
        for keyProg in keyProgression:
            difTime = [abs(bar[0]-keyProg[0]) for bar in chordProgressionBar]
            keyProg.append(difTime.index(min(difTime)))
#        print(keyProgression)

        # calculate degree from chord progression and current key
        # make chordProgressionBar, array of [ bar start time, [chordIds in bar], [key, minmaj]]
        keyId = keyProgression[0][1]
        keyMajMin = keyProgression[0][2]
        keyCount = 1
        for barCount,bar in enumerate(chordProgressionBar):
            if(keyCount < len(keyProgression)):
                if(keyProgression[keyCount][3] <= barCount):
                    keyId = keyProgression[keyCount][1]
                    keyMajMin = keyProgression[keyCount][2]
                    keyCount += 1
            bar.append([keyId,keyMajMin])

        fout = open(directory+str(count)+"_chord_name.txt","w")
        for i,cp in enumerate(chordProgressionBar):
            barIndex = i+1
            startTime = cp[0]
            chords = [idToChordMap[c] for c in cp[1]]
            if(cp[2][0]+chordNameCount*cp[2][1]<0 or cp[2][0]+chordNameCount*cp[2][1]>=24):
                print(cp[2])
            key = idToChordMap[cp[2][0]+chordNameCount*cp[2][1]]
            fout.write("{0}:{1} (key {2}) from t={3}\n".format(barIndex," ".join(chords),key,startTime))
        fout.close()


        # degree-minmaj to id
        # -1:NC 0-11 = C-B , 12-23 = Cm-Bm
        # degreeProgression : len = #bar
        # degreeProgression[i][0] = list of degree id at i-th bar
        # [value of degree] is distance from C in major key,
        #                       distance from A in minor key
        shiftedChordProgression = []
        for bar in chordProgressionBar:
            chords = bar[1]
            keyPos,keyMajMin = bar[2]
            for ind in range(len(chords)):
                chordPos = chords[ind]%12
                chordMinMaj = chords[ind]//12
                if (modeDegree):
                    # [a-b in k(maj)] -> [(a-k)-(b-k) in 0(maj)] = [(a+12-k)-(b+12-k) in 0(maj)]
                    # [a-b in k(min)] -> [(a-k)-(b-k) in 0(min)] = [(a+12-k)-(b+12-k) in 0(min)]
                    chordPos = (chordPos-keyPos+chordNameCount)%chordNameCount
                else:
                    # [a-b in k(maj)] -> [(a-k)-(b-k) in 0(maj)] = [(a+12-k)-(b+12-k) in 0(maj)]
                    # [a-b in k(min)] -> [(a-(k-9))-(b-(k-9)) in 9(min)] -> [(a-k+21)-(b-k+21) in 9(min)] -> [(a-k+21)-(b-k+21) in 0(maj)]
                    if(keyMajMin==0):
                        chordPos = (chordPos-keyPos+chordNameCount)%chordNameCount
                    else:
                        chordPos = (chordPos-keyPos+chordNameCount+9)%chordNameCount
                chords[ind] = chordPos+chordMinMaj*chordNameCount
            shiftedChordProgression.append(chords)

        if(modeDegree):
            fout = open(directory+str(count)+"_degree_name_shift.txt","w")
        else:
            fout = open(directory+str(count)+"_chord_name_shift.txt","w")
        for i,cp in enumerate(shiftedChordProgression):
            barIndex = i+1
            chords = [idToChordMap[c] for c in cp]
            if(modeDegree):
                fout.write("{0}:{1} (key C/Cm)\n".format(barIndex," ".join(chords)))
            else:
                fout.write("{0}:{1} (key C/Am)\n".format(barIndex," ".join(chords)))
        fout.close()


        uniqueChordList = []
        lastChord = -1
        for barProg in shiftedChordProgression:
            for chord in barProg:
                if(lastChord != chord):
                    lastChord = chord
                    uniqueChordList.append(chord)
                    hist[chord]+=1

        if(modeDegree):
            fout = open(directory+str(count)+"_degree_name_shift_uniq.txt","w")
        else:
            fout = open(directory+str(count)+"_chord_name_shift_uniq.txt","w")
        fout.write(" ".join([idToChordMap[uc] for uc in uniqueChordList]))
        fout.close()

        # save degree 1,2,3,4-gram
        def makeDegreeNGram(gram):
            ngramDegree = []
            bag = []
            for chord in uniqueChordList:
                bag.append(chord)
                if(len(bag)>gram):
                    bag.pop(0)
                if(len(bag)==gram):
                    if(modeDegree):
                        ngramDegree.append("-".join([idToDegreeMap[uc] for uc in bag]))
                    else:
                        ngramDegree.append("-".join([idToChordMap[uc] for uc in bag]))
            if(modeDegree):
                fout = open(directory+str(count)+"_degree_"+str(gram)+"gram.txt","w")
            else:
                fout = open(directory+str(count)+"_chord_"+str(gram)+"gram.txt","w")
            fout.write(" ".join(ngramDegree)+"\n")
            fout.close()
#            print(ngramDegree)
        for gn in [1,2,3,4]:
            makeDegreeNGram(gn)

        print("{0}/{1} done".format(count+1,fileCount))

    if(modeDegree):
        fout = open(directory+"../"+directory.split("/")[-2]+"_degree_stat.txt","w")
    else:
        fout = open(directory+"../"+directory.split("/")[-2]+"_chord_stat.txt","w")
    for i,h in enumerate(hist):
        if(modeDegree):
            fout.write("{0} {1} {2}\n".format(i,h,idToDegreeMap[i]))
        else:
            fout.write("{0} {1} {2}\n".format(i,h,idToChordMap[i]))
    fout.close()
    print(hist)
