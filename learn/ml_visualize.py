import matplotlib.pyplot as plt
from sklearn.lda import LDA
from sklearn.decomposition import PCA
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report,accuracy_score
import pickle
import numpy as np
import ml_learn_tune
import itertools
import dataset
from sklearn.svm import SVC

allData = dataset.allData
def monochrome_style_generator():
    linestyle = ['-', '--', '-.', ':']
    markerstyle = ['h' ,'2', 'v', '^', 's', '<', '>', '1', '3', '4', '8', 'p', '*', 'H', '+', ',', '.', 'x', 'o', 'D', 'd', '|', '_']
    line_idx = 0
    marker_idx = 0
    while True:
        yield 'k' + linestyle[line_idx] + markerstyle[marker_idx]
        line_idx = (line_idx + 1) % len(linestyle)
        marker_idx = (marker_idx + 1) % len(markerstyle)
def visualize(useFeature,positive,negative):
    print("start visualize "+useFeature)

    col = ["r","g","b","y","k","c","m"]
#    sty = ["o","x","s","^","v",">","<"]
    sty = ["o","x","s","o","x","s"]
    plp = list(zip(col,sty))
    def drawPCA(X_true,X_false,X_test,suffix=""):
        # dimensionality reduction with PCA
        X=X_true+X_false
        plc = 0
        pca = PCA(n_components = 2)
        pca.fit(X)
        Xpca_true = pca.transform(X_true)
        Xpca_false = pca.transform(X_false)
        plt.scatter(Xpca_true[:,0],Xpca_true[:,1],color=plp[plc][0],marker=plp[plc][1],label="thbgm")
        plc+=1
        plt.scatter(Xpca_false[:,0],Xpca_false[:,1],color=plp[plc][0],marker=plp[plc][1],label="not thbgm")
        plc+=1
        if(len(X_test)>0):
            Xlda_test = lda.transform(X_test)
            plt.scatter(Xlda_test[:,0],Xlda_test[:,1],color=plp[plc][0],marker=plp[plc][1],label="test")
            plc+=1
        plt.xlabel("feature1")
        plt.ylabel("feature2")
        plt.title("Classification with "+useFeature)
        plt.legend()
        plt.savefig("./learn/visualize/pca_"+useFeature+suffix+".png")
        plt.clf()

    def drawLDA(X_true,X_false,X_test,suffix=""):
        X=X_true+X_false
        Y=[1]*len(X_true)+[0]*len(X_false)
        plc=0
        lda = LDA(solver="eigen",n_components=2)
        canfit=False
        hred = False
        try:
            lda.fit(X,Y)
            canfit=True
        except :
            try:
                print("fit error")
                X = np.array(X)
                X = X[:,:140]
                lda.fit(X,Y)
                canfit=True
                hred=True
            except:
                print("cannot visualize")
        if(not canfit):
            return
        if(hred):
            Xlda_true = lda.transform(np.array(X_true)[:,:140])
            Xlda_false = lda.transform(np.array(X_false)[:,:140])
        else:
            Xlda_true = lda.transform(X_true)
            Xlda_false = lda.transform(X_false)
        plt.scatter(Xlda_true[:,0],Xlda_true[:,1],color=plp[plc][0],marker=plp[plc][1],label="thbgm")
        plc+=1
        plt.scatter(Xlda_false[:,0],Xlda_false[:,1],color=plp[plc][0],marker=plp[plc][1],label="not thbgm")
        plc+=1
        if(len(X_test)>0):
            if(hred):
                Xlda_test = lda.transform(np.array(X_test)[:,:140])
            else:
                Xlda_test = lda.transform(np.array(X_test))
            plt.scatter(Xlda_test[:,0],Xlda_test[:,1],color=plp[plc][0],marker=plp[plc][1],label="test")
            plc+=1

        print(lda.coef_.shape)

        plt.xlabel("feature1")
        plt.ylabel("feature2")
        plt.title("Classification with "+useFeature)
        plt.legend()
        plt.savefig("./learn/visualize/lda_"+useFeature+suffix+".png")
        plt.clf()

    def drawLDA3Class(X_train,X_test,suffix=""):
        X=X_train[0]+X_train[1]+X_train[2]
        Y=[0]*len(X_train[0])+[1]*len(X_train[1])+[2]*len(X_train[2])
        Yt=[0]*len(X_test[0])+[1]*len(X_test[1])+[2]*len(X_test[2])
        featCount = len(X_train[0][0])
        X = np.array(np.array(X))
        lda = LDA(n_components=2)
        canfit=False
        fitFeat = featCount
        while(not canfit):
            try:
                X = X[:,:fitFeat]
                lda.fit(X,Y)
                canfit=True
            except :
                fitFeat = fitFeat//2
        Xlda = []
        Xldat = []
        for ind in range(3):
            trainFit = np.array(lda.transform(np.array(X_train[ind])[:,:fitFeat]))
            testFit = np.array(lda.transform(np.array(X_test[ind])[:,:fitFeat]))
            Xlda.append(trainFit)
            Xldat.append(testFit)
        Xlda = np.array(Xlda)
        Xldat = np.array(Xldat)
        plc=0

        Xs = np.vstack(Xlda)
        Xst = np.vstack(Xldat)
        clf = SVC(C=0.1,kernel="linear")
        clf.fit(Xs,Y)
        Yp = clf.predict(Xs)
        Ytp = clf.predict(Xst)
        print(accuracy_score(Y,Yp),accuracy_score(Yt,Ytp))


        Xsa = np.vstack([Xs,Xst])
        x_min, x_max = Xsa[:, 0].min() - 1, Xsa[:, 0].max() + 1
        y_min, y_max = Xsa[:, 1].min() - 1, Xsa[:, 1].max() + 1
        h = (x_max-x_min)/100.0
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        plt.contour(xx, yy, Z)
        gen = monochrome_style_generator()
        for ind in range(3):
            plt.scatter(Xlda[ind][:,0],Xlda[ind][:,1],color=plp[plc][0],marker=plp[plc][1],label="Class"+str(ind))
            plc+=1
        plt.xlabel("feature1")
        plt.ylabel("feature2")
        plt.title("Classification with {0} / Accuracy {1:.5f}".format(useFeature,accuracy_score(Y,Yp)))
        plt.legend()
        plt.savefig("./learn/visualize/lda3c_"+useFeature+suffix+"_trainData.png")
        plt.clf()

        plc=0
        Xsa = np.vstack([Xs,Xst])
        x_min, x_max = Xsa[:, 0].min() - 1, Xsa[:, 0].max() + 1
        y_min, y_max = Xsa[:, 1].min() - 1, Xsa[:, 1].max() + 1
        h = (x_max-x_min)/100.0
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        plt.contour(xx, yy, Z)
        for ind in range(3):
            plt.scatter(Xldat[ind][:,0],Xldat[ind][:,1],color=plp[plc][0],marker=plp[plc][1],label="Class"+str(ind))
            plc+=1
        plt.xlabel("feature1")
        plt.ylabel("feature2")
        plt.title("Classification with {0} / Accuracy {1:.5f}".format(useFeature,accuracy_score(Yt,Ytp)))
        plt.legend()
        plt.savefig("./learn/visualize/lda3c_"+useFeature+suffix+"_testData.png")
        plt.clf()

    fin = open("./learn/data/"+useFeature+"_"+positive+".pkl","rb")
    X_true = pickle.load(fin)
    fin.close()
    fin = open("./learn/data/"+useFeature+"_"+negative+".pkl","rb")
    X_false = pickle.load(fin)
    fin.close()

#    drawLDA(X_true,X_false,[],"_"+positive+"_"+negative+".png")

    for dataset in [data for data in allData if data not in [positive,negative]]:
        fin = open("./learn/data/"+useFeature+"_"+dataset+".pkl","rb")
        X_test = pickle.load(fin)
        fin.close()
        print(np.array(X_test).shape)
#        drawLDA(X_true,X_false,X_test,"_"+positive+"_"+negative+"_"+dataset+".png")

        X_true_train, X_true_test = train_test_split(X_true,test_size=0.33)
        X_false_train, X_false_test = train_test_split(X_false,test_size=0.33)
        X_test_train, X_test_test = train_test_split(X_test,test_size=0.33)
        drawLDA3Class([X_true_train,X_false_train,X_test_train],[X_true_test,X_false_test,X_test_test],"_"+positive+"_"+negative+"_"+dataset+".png")

#    X_true_train, X_true_test = train_test_split(X_true,test_size=0.3)
#    X_false_train, X_false_test = train_test_split(X_false,test_size=0.3)
#    drawLDA(X_true_train,X_false_train,X_true_test,"_"+positive+"_"+negative+"_genT.png")
#    drawLDA(X_true_train,X_false_train,X_false_test,"_"+positive+"_"+negative+"_genF.png")
