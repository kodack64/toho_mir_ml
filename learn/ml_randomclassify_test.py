
from sklearn.metrics import classification_report,accuracy_score
from sklearn.svm import SVC
import numpy as np
import matplotlib.pyplot as plt
from sklearn.lda import LDA

fx = list(range(200,201))
sc = []
cl = [231,1,1000]
#cl = [230]*3
sam = sum(cl)
for featNum in fx:
    X = np.random.rand(sam,featNum)
    Y = [0]*cl[0]+[1]*cl[1]+[2]*cl[2]

    clf = SVC()
    clf.fit(X,Y)
    Yp = clf.predict(X)
    svmsc = accuracy_score(Yp,Y)

    lda = LDA()
    lda.fit(X,Y)
    Xs = lda.transform(X)

    clf = SVC(kernel="linear")
    clf.fit(Xs,Y)
    Ysp = clf.predict(Xs)
    Xs = np.array(Xs)
    plt.scatter(Xs[:cl[0],0],Xs[:cl[0],1],color="r",marker="o")
    plt.scatter(Xs[cl[0]:cl[0]+cl[1],0],Xs[cl[0]:cl[0]+cl[1],1],color="g",marker="s")
    plt.scatter(Xs[cl[0]+cl[1]:,0],Xs[cl[0]+cl[1]:,1],color="b",marker="x")
    score = accuracy_score(Y,Ysp)
    Yr = np.random.randint(0,3,sam)
    rscore = accuracy_score(Y,Yr)
    print(featNum,score,rscore,svmsc)
    sc.append(score)
    plt.show()

#plt.plot(fx,sc,"-")
#plt.show()
