
'''
make degree name list from  chord name list and key
'''

import glob
import os

gramN = [1,2,4]
barN = [1,2,4]

chordName = {
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
idToDegreeMaj = {
    -1:"NC"
    ,0:"I"
    ,1:"bII"
    ,2:"II"
    ,3:"bIII"
    ,4:"III"
    ,5:"IV"
    ,6:"bV"
    ,7:"V"
    ,8:"bVI"
    ,9:"VI"
    ,10:"bVII"
    ,11:"VII"
    ,12:"Im"
    ,13:"bIIm"
    ,14:"IIm"
    ,15:"bIIIm"
    ,16:"IIIm"
    ,17:"IVm"
    ,18:"bVm"
    ,19:"Vm"
    ,20:"bVIm"
    ,21:"VIm"
    ,22:"bVIIm"
    ,23:"VIIm"
    }
idToDegreeMin = idToDegreeMaj
'''
{
    -1:"NC"
    ,0:"I"
    ,1:"bII"
    ,2:"II"
    ,3:"III"
    ,4:"bIV"
    ,5:"IV"
    ,6:"bV"
    ,7:"V"
    ,8:"VI"
    ,9:"bVII"
    ,10:"VII"
    ,11:"bI"
    ,12:"Im"
    ,13:"bIIm"
    ,14:"IIm"
    ,15:"IIIm"
    ,16:"bIVm"
    ,17:"IVm"
    ,18:"bVm"
    ,19:"Vm"
    ,20:"VIm"
    ,21:"bVIIm"
    ,22:"VIIm"
    ,23:"bIm"
    }
'''
minmajName = {"maj":0,"min":1}
chordNameCount = 12

def makeDegreeFromChord(directory,fileCount):
    for count in range(fileCount):
        chordProgression = []

        # read chord names
        firstBar = -1
        fin = open(directory+str(count)+"_chord.txt","r")
        for line in fin:
            (beat,chord,start,end) = line.split(";")
            beat = int(beat)
            if(beat == 1  & firstBar==-1):
                firstBar = len(chordProgression)
            chordElem = chord.split(":")
            if(chordElem[0] is "N"):
                chord=-1
                minmaj=0
            else:
                chord = chordName[chordElem[0]]
                minmaj = minmajName[chordElem[1]]
            start = float(start)
            chordProgression.append([beat,chord,minmaj,start])
        fin.close()

        # packing in each bar
        chordProgressionBar = []
        chords = []
        start = 0.0
        first = True
        for beatCount in range(firstBar,len(chordProgression)):
            currentBeat = chordProgression[beatCount][0]
            chordId = chordProgression[beatCount][1]+chordProgression[beatCount][2]*12
            if(currentBeat==1):
                if(first):
                    first = False
                else:
                    chordProgressionBar.append([start,chords])
                chords = [chordId,]
                start = chordProgression[beatCount][3]
            else:
                if(not first):
                    if(chords[-1] != chordId):
                        chords.append(chordId)

        # read key change
        keyProgression = []
        fin = open(directory+str(count)+"_key.csv","r")
        for line in fin:
            elem = line.split(",")
            start = float(elem[1])
            keyid = int(elem[2])
            key = (keyid-1)%12
            minmaj = (keyid-1)//12
            keyProgression.append([key,minmaj,start])
        fin.close()

        # fix key change timing to the nearest beggining of bar
        for keyProg in keyProgression:
            time = keyProg[2]
            difTime = [abs(bar[0]-time) for bar in chordProgressionBar]
            keyProg.append(difTime.index(min(difTime)))

        # calculate degree from chord progression and current key
        currentKey = keyProgression[0][0]
        currentMajmin = keyProgression[0][1]
        keyCount = 1
        barCount = 0
        for bar in chordProgressionBar:
            if(keyCount < len(keyProgression)):
                if(keyProgression[keyCount][3] == barCount):
                    currentKey = keyProgression[keyCount][0]
                    currentMajmin = keyProgression[keyCount][1]
                    keyCount += 1
            bar.append(currentKey)
            bar.append(currentMajmin)
            barCount += 1

        # degree-minmaj to id
        # -1:NC 0-11 = C-B , 12-23 = Cm-Bm
        # degreeProgression : len = #bar
        # degreeProgression[i][0] = list of degree id at i-th bar
        # degreeProgression[i][1] = the key of i-th bar is major or minor
        degreeProgression = []
        for bar in chordProgressionBar:
            chords = bar[1]
            key = bar[2]
            majmin = bar[3]
            for ind in range(len(chords)):
                if(chords[ind]!=-1):
                    chn = chords[ind]%12
                    minmaj = chords[ind]//12
                    chn = (chn+12-key)%12
                    chords[ind] = chn+minmaj*12
            degreeProgression.append([chords,majmin])

        # save degrees
        fout = open(directory+str(count)+"_degree.txt","w")
        barCount = 0
        for degrees in degreeProgression:
            fout.write(str(barCount)+","+str(degrees[1])+","+";".join(list(map(str,degrees[0])))+"\n")
            barCount += 1
        fout.close()

        # save degree 2,4,8-gram
        def makeDegreeNGram(gram):
            bags = []
            bag = []
            for degrees in degreeProgression:
                for degree in degrees[0]:
                    # not use NC
                    if(degree==-1):
                        continue
                    # if empty, simply append
                    if(len(bag)==0):
                        bag.append(degree)
                        continue
                    # not use continuous same degree
                    if(bag[-1]==degree):
                        continue;

                    # append
                    bag.append(degree)
                    # pop front if need
                    if(len(bag)>gram):
                        bag.pop(0)

                    if(len(bag)==gram):
                        bags.append("t".join(list(map(str,bag))))

            fout = open(directory+str(count)+"_degree_"+str(gram)+"gram.txt","w")
            fout.write(" ".join(bags)+"\n")
            fout.close()
        for gn in gramN:
            makeDegreeNGram(gn)

        # save degree 2,4-bar-gram
        def makeDegreeBarGram(bars):
            degs = []
            degns = []
            for barCount in range(len(degreeProgression)+1-bars):

                fourBar = []
                for ind in range(bars):
                    fourBar += degreeProgression[barCount+ind][0]

                # not use NC
                if(-1 in fourBar):
                    continue

                # erase continuous same degree
                cnc = 0
                while (cnc+1<len(fourBar)):
                    if(fourBar[cnc]==fourBar[cnc+1]):
                        fourBar.pop(cnc)
                    else:
                        cnc += 1

                # id-list to str
                deg = "t".join(list(map(str,fourBar)))
                degs.append(deg)

                # make degree-name str
                fourBarStr = []
                for ind in range(bars):
                    minmaj = degreeProgression[barCount+ind][1]
                    degp = degreeProgression[barCount+ind][0]
                    if(minmaj==0):
                        fourBarStr += [idToDegreeMaj[d] for d in degp]
                    else:
                        fourBarStr += [idToDegreeMin[d] for d in degp]
                # erase continuous same degree name
                cnc = 0
                while (cnc+1<len(fourBarStr)):
                    if(fourBarStr[cnc] is fourBarStr[cnc+1]):
                        fourBarStr.pop(cnc)
                    else:
                        cnc += 1
                degn = "-".join(fourBarStr)
                degns.append(degn)

            fout = open(directory+str(count)+"_degree_"+str(bars)+"bar.txt","w")
            fout.write(" ".join(degs)+"\n")
            fout.close()
            fout = open(directory+str(count)+"_degree_name_"+str(bars)+"bar.txt","w")
            fout.write(" ".join(degns)+"\n")
            fout.close()
        for bn in barN:
            makeDegreeBarGram(bn)

        print("{0}/{1} done".format(count+1,fileCount))
