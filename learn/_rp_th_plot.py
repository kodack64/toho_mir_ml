
import numpy as np
import matplotlib.pyplot as plt
import pickle

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
barkName.reverse()


#plt.subplot(3,1,1)
plt.figure(figsize=(16,12))
fin = open("./data/rp_thbgm.pkl","rb")
X_true = pickle.load(fin)
fin.close()
print(np.array(X_true).shape)
Xmean = np.mean(X_true,axis=0)
vals = np.flipud(Xmean.reshape((60,24)).T)
print(Xmean.shape)

plt.yticks(range(24),barkName)
plt.xticks(range(60),flucName,rotation="vertical")
#plt.imshow(vals)
plt.imshow(vals,cmap="Greys_r")
#plt.show()
plt.savefig("_rp_th.png")
plt.clf()

#plt.subplot(3,1,2)
fin = open("./data/rp_anison.pkl","rb")
X_true = pickle.load(fin)
fin.close()
print(np.array(X_true).shape)
Xmean = np.mean(X_true,axis=0)
vals = np.flipud(Xmean.reshape((60,24)).T)
print(Xmean.shape)

plt.yticks(range(24),barkName)
plt.xticks(range(60),flucName,rotation="vertical")
#plt.imshow(vals)
plt.imshow(vals,cmap="Greys_r")
plt.savefig("_rp_anison.png")
plt.clf()


#plt.subplot(3,1,2)
fin = open("./data/rp_gtzan.pkl","rb")
X_true = pickle.load(fin)
fin.close()
print(np.array(X_true).shape)
Xmean = np.mean(X_true,axis=0)
vals = np.flipud(Xmean.reshape((60,24)).T)
print(Xmean.shape)

plt.yticks(range(24),barkName)
plt.xticks(range(60),flucName,rotation="vertical")
#plt.imshow(vals)
plt.imshow(vals,cmap="Greys_r")
plt.savefig("_rp_gtzan.png")


#plt.subplot(3,1,3)
fin = open("./feature/rp_feature_rank.txt")
vals = []
for line in fin:
	elem = line.split(" ")
	vals.append(float(elem[1]))
fin.close()
Xmean = np.array(vals)
vals = np.flipud(Xmean.reshape((60,24)).T)
print(Xmean.shape)

plt.yticks(range(24),barkName)
plt.xticks(range(60),flucName,rotation="vertical")
plt.imshow(vals,cmap="Greys_r")
plt.savefig("_rp_feature.png")
#plt.imshow(vals,cmap="Greys_r")

plt.show()