
fout = open("id_mfcc.txt","w")
stat = ["mean","var","skew","kurtosis","median","min","max"]
ty = ["mfcc", "mfcc-delta"]
ind = 0
for t in ty:
	for st in stat:
		for bank in range(20):
			fout.write("{0},{1} mel-{2} {3}\n".format(ind,t,bank,st))
			ind += 1
fout.close()