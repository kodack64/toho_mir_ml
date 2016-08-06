
import matplotlib.pyplot as plt
import numpy as np

#dataSet = ["thbgm","not_thbgm","anison","gtzan","thbgm_test"]
dataSet = ["thbgm","anison","gtzan"]

darr = []
xlabel = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B",
	"Cm","Dbm","Dm","Ebm","Em","Fm","Gbm","Gm","Abm","Am","Bbm","Bm"]
x = list(range(len(xlabel)))
for dn in dataSet:
	fin = open(dn+"_chord_stat.txt")
	arr = []
	sum = 0
	for line in fin:
		elem = line.split(" ")
		arr.append(float(elem[1]))
		sum += float(elem[1])
	fin.close()
	arr = np.array(arr)/sum
	plt.plot(x,arr,"o",label=dn)

plt.xlim(-1,24)
plt.xticks(x,xlabel,rotation="vertical")
plt.legend()
plt.xlabel("chord in key = C/Am")
plt.ylabel("ratio")
plt.savefig("chord_stat.eps")

