
import numpy as np
import matplotlib.pyplot as plt
import pickle


pt = 0

if(pt==1):
    fin = open("../feature/id_rhythm_barkband.txt","r")
    bark = [int(v) for v in fin.readline().split(",")]
    fin.close()

    barkName = []
    for ind in range(len(bark)):
        if(ind==0):
            barkName.append("0-"+str(bark[ind])+"Hz")
        else:
            barkName.append(str(bark[ind-1])+"-"+str(bark[ind])+"Hz")
    flucName = ["{0:.0f}bpm".format(((v)+1)*0.17*60) for v in range(60)]

    fin = open("./data/rp_thbgm.pkl","rb")
    X = pickle.load(fin)
    fin.close()
    feat = np.mean(X,axis=0)

    fin = open("./data/rp_anison.pkl","rb")
    X_ = pickle.load(fin)
    fin.close()
    feat = feat-np.mean(X_,axis=0)

    vals = np.flipud(np.array(feat).reshape(60,24).T)
    barkName.reverse()
    plt.yticks(range(24),barkName)
    plt.xticks(range(60),flucName,rotation="vertical")
#    plt.imshow(vals)
    plt.imshow(vals,cmap="Greys_r")
    plt.savefig("_temp.png")
    plt.show()

if(pt==0):
    dataName = "anison"
#    id = 19
    dataName = "thbgm"
    id = 143

    fin = open("../feature/id_rhythm_barkband.txt","r")
    bark = [int(v) for v in fin.readline().split(",")]
    fin.close()

    barkName = []
    for ind in range(len(bark)):
        if(ind==0):
            barkName.append("0-"+str(bark[ind])+"Hz")
        else:
            barkName.append(str(bark[ind-1])+"-"+str(bark[ind])+"Hz")
    flucName = ["{0:.0f}bpm".format(((v)+1)*0.17*60) for v in range(60)]

    fin = open("./data/rp_"+dataName+".pkl","rb")
    X = pickle.load(fin)
    fin.close()
    print(np.array(X).shape)
    feat = X[id]
#    feat = np.mean(X,axis=0)
    vals = np.flipud(np.array(feat).reshape(60,24).T)
    barkName.reverse()
    plt.yticks(range(24),barkName)
    plt.xticks(range(60),flucName,rotation="vertical")
    plt.imshow(vals,cmap="Greys_r")
    plt.savefig("_temp2.png")
    plt.show()
