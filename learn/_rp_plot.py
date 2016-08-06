
import numpy as np
import matplotlib.pyplot as plt

fin = open("../feature/id_rhythm_barkband.txt","r")
bark = [int(v) for v in fin.readline().split(",")]
fin.close()

fin = open("./feature/gtzan_rp.txt")
barkName = []
for ind in range(len(bark)):
    if(ind==0):
        barkName.append("0-"+str(bark[ind])+"Hz")
    else:
        barkName.append(str(bark[ind-1])+"-"+str(bark[ind])+"Hz")

flucName = ["{0:.0f}bpm".format(((v)+1)*0.17*60) for v in range(60)]

vals = np.zeros((24,60))
print(vals.shape)

for line in fin:
	elem = line.split(" ")
	val = float(elem[2])
	flucId = int(elem[1])%60
	bandId = 23-int(elem[1])//60
	vals[bandId,flucId] = val
fin.close()
barkName.reverse()
plt.yticks(range(24),barkName)
plt.xticks(range(60),flucName,rotation="vertical")
plt.imshow(vals,cmap="Greys_r")
plt.show()