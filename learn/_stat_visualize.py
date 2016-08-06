
import numpy as np
import matplotlib.pyplot as plt
import pickle
import codecs

useDatas = ["mfcc","tfidf_2gram","ssd"]
xl = ["mfcc th", "mfcc nth","tfidf_2gram th" , "tfidf_2gram nth","ssd th" , "ssd nth"]

pos = 0
for useData in useDatas:
	fin = open("./stat/stat_"+useData+"_th_rank.txt")
	probs = []
	for line in fin:
		probs.append(float(line.split(",")[2]))
	fin.close()
	plt.plot([pos]*len(probs),probs,"o")
	pos +=1

	fin = codecs.open("./stat/stat_"+useData+"_nth_rank.txt","r","utf-8")
	probs = []
	for line in fin:
		probs.append(1-float(line.split(",")[2]))
	fin.close()
	plt.plot([pos]*len(probs),probs,"o")
	pos+=1

plt.xticks(list(range(pos)),xl,rotation="vertical")
plt.ylabel("thbgm probability")
plt.ylim(0,1)
plt.xlim(-0.5,pos-0.5)
plt.savefig("_stat_hist.png")
plt.show()
