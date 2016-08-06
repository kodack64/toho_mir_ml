
import matplotlib.pyplot as plt
import numpy as np
thnum = 224
totFreq = [0.0]*thnum*2

fin = open("./ids/id_music_thbgm.txt")
mlist = []
for line in fin:
	mlist.append(line.split("\\")[-1].strip())
fin.close()
fin = open("./ids/id_music_thbgm_name.txt")
mnlist = []
for line in fin:
	mnlist.append(line.strip())
fin.close()

x = np.linspace(0,1,thnum)
plt.xlim(0,1)
plt.plot([0,1],[0.5,0.5],label="random classifier")

def plotState(name,pname,topn=10,worn=10):
	# read mean predict proba as test
	fin = open("./stat/stat_"+name+".txt","r")
	freq = []
	count = 0
	for line in fin:
		elem = [float(val) for val in line.split(",")]
		freq.append([elem[1]/elem[0],count])
		if(elem[1]>0):
			if(count in imp):
				imp.remove(count)
		count += 1
	fin.close()
	freq_th = freq[:thnum]
	freq_nth = [[1-fr[0],fr[1]] for fr in freq[thnum:]]
	freq_th.sort()
	freq_nth.sort()

	plt.plot(x,[e[0] for e in freq_th],label=pname+" toho")
	plt.plot(x,[e[0] for e in freq_nth],label=pname+" not toho")

	# accum total frequency
	for pid in freq:
		if(pid[1]<thnum):
			totFreq[pid[1]] = max(pid[0],totFreq[pid[1]])
		else:
			totFreq[pid[1]] = max(1-pid[0],totFreq[pid[1]])

	for rank in range(topn):
		idt = freq_th[rank][1]
		print("{0}:p={1:.5f}:{2}->{3}".format(rank+1,freq_th[rank][0],mlist[idt],mnlist[idt]))
	for rank in range(len(freq_th)-worn,len(freq_th)):
		idt = freq_th[rank][1]
		print("{0}:p={1:.5f}:{2}->{3}".format(rank+1,freq_th[rank][0],mlist[idt],mnlist[idt]))

imp = list(range(255))
print("mfccs")
plotState("mfccs","MFCC")
print("tfidf_2gram")
plotState("tfidf_2gram","Chord")
print("ssd")
plotState("ssd","Rhythm")
print("best proba")

totFreq_th = totFreq[:thnum]
totFreq_nth = totFreq[thnum:]
totFreq_th = [[fr,i] for i,fr in enumerate(totFreq_th)]
totFreq_nth = [[fr,i] for i,fr in enumerate(totFreq_nth)]
totFreq_th.sort()
totFreq_nth.sort()
plt.plot(x,[e[0] for e in totFreq_th],label="Best toho")
plt.plot(x,[e[0] for e in totFreq_nth],label="Best not toho")
for rank in range(20):
	idt = totFreq_th[rank][1]
	print("{0}:p={1:.5f}:{2}->{3}".format(rank+1,totFreq_th[rank][0],mlist[idt],mnlist[idt]))

#plotState("rh")
#print("rhythm patterns : {0}".format(imp))

'''
imp = list(range(255))
plotState("mfccs")
plotState("hmfccs")
plotState("pmfccs")
print("hpss mfccs : {0}".format(imp))
'''

'''
imp = list(range(255))
plotState("ssd_rh")
print("rhythm combi : {0}".format(imp))

imp = list(range(255))
plotState("tfidf_2gram")
plotState("tfidf_4gram")
print("chord tfidf : {0}".format(imp))

imp = list(range(255))
plotState("all")
print("mfccs and rhythms : {0}".format(imp))
'''

plt.xlabel("data")
plt.ylabel("precision")
plt.legend(loc=4)
plt.show()
