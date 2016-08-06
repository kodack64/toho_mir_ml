
import numpy as np
import matplotlib.pyplot as plt
import pickle
import codecs

useDatas = ["mfcc","tfidf_2gram","ssd"]

dic = {}
for useData in useDatas:
	fin = open("./stat/stat_"+useData+"_th_rank.txt")
	for line in fin:
		elem = line.split(",")
		prob = float(elem[2])
		name = elem[3].strip()
		if(name in dic):
			dic[name] = dic[name]+prob
		else:
			dic[name] = prob
	fin.close()
lis = [[p[1]/3.0,p[0]] for p in dic.items()]
lis.sort()
fout = open("./stat/stat_all_th_rank.txt","w")
for item in lis:
	fout.write("{0} {1}\n".format(item[0],item[1]))
fout.close()

ndic = {}
for useData in useDatas:
	fin = codecs.open("./stat/stat_"+useData+"_nth_rank.txt","r","utf-8")
	for line in fin:
		elem = line.split(",")
		prob = float(elem[2])
		name = elem[3].strip()
		if(name in ndic):
			ndic[name] = ndic[name]+prob
		else:
			ndic[name] = prob
	fin.close()
lis = [[p[1]/3.0,p[0]] for p in ndic.items()]
lis.sort()
fout = codecs.open("./stat/stat_all_nth_rank.txt","w","utf-8")
for item in lis:
	fout.write("{0} {1}\n".format(item[0],item[1]))
fout.close()
	