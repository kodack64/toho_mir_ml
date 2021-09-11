# XGBoost

---

[XGBoost](https://github.com/dmlc/xgboost)

XGBoostの使い方で参考になったブログ  
[http://tjo.hatenablog.com/entry/2015/05/15/190000](http://tjo.hatenablog.com/entry/2015/05/15/190000)  
[http://yag.xyz/blog/2015/08/08/xgboost-python/](http://yag.xyz/blog/2015/08/08/xgboost-python/)  
[http://puyokw.hatenablog.com/entry/2015/04/11/040941](http://puyokw.hatenablog.com/entry/2015/04/11/040941)  
[http://puyokw.hatenablog.com/entry/2015/08/07/220906](http://puyokw.hatenablog.com/entry/2015/08/07/220906)  

パラメータチューニングの手続き
[http://www.analyticsvidhya.com/blog/2016/03/complete-guide-parameter-tuning-xgboost-with-codes-python/](http://www.analyticsvidhya.com/blog/2016/03/complete-guide-parameter-tuning-xgboost-with-codes-python/)

Kaggle Higgs Competitionを見てる時に知りました。界隈では定番らしいです。

XGBoostは人気のあるツールなので、かなり多くのページで導入のイントロダクションがあるのですが、Windows+Pythonの環境に導入しようとするとgitでとってくる方法は最新のgccをとってきてもgccのバージョンがおかしいと言われ、うまくビルドが通りませんでした。

俺は、結局gitからcloneせずに、githubのページの安定板のリリースを用いました。githubのページのreleasesにある、0.4xは少し古いですが、これにはVisual Studioのワークスペースがついているので、Visual Studioを入れてビルドすることで正しくインストールができます。安定板なのでバージョンは少し落ち、実際最新版である機能が一部使えなかったり変わっていたりするのですが、適当に遊ぶ分には十分です。じっくり使う場合はWindowsじゃなくてLinuxにOSを変えた方がよいように思えます。VisualStudioのワークスペースだけを引っ張ってきて、最新版のgitのフォルダにおけば通るという話も見かけましたが、やってないのでわかりません。
