
import matplotlib.pyplot as plt
import numpy as np

def plotScatter(nameX,nameY):
	X = []
	Y = []
	count = 0
	fin = open("./stat/stat_"+nameX+".txt","r")
	for line in fin:
		elem = [float(val) for val in line.split(",")]
		X.append(elem[1]/elem[0])
		count += 1
	fin.close()
	fin = open("./stat/stat_"+nameY+".txt","r")
	for line in fin:
		elem = [float(val) for val in line.split(",")]
		Y.append(elem[1]/elem[0])
		count += 1
	fin.close()

	X = np.array(X[0:225])
	Y = np.array(Y[0:225])
	plt.scatter((X),(Y))
	plt.xlim(-0.1,1.1)
	plt.ylim(-0.1,1.1)
	plt.xlabel("SSD Score")
	plt.ylabel("chord Score")
	plt.savefig("./pic/score_"+nameX+"_"+nameY+".png")
	plt.show()


plotScatter("ssd","tfidf_2gram")
