# 環境構築

---

この分析ではいくつものライブラリに投げっぱなしで分析を行っていますが、いくつかのライブラリは日本語の使用方法の文献が無かったり、そもそも英語の文献すらなかったり、あってもWindowsへのインストールが困難だったりします。ぶっちゃけ全体で一番大変なのがライブラリのインストールで、次がデータ集め、分析はその次ぐらいです。


そこで、ここではそれなりに導入に苦労した、あるいは導入に関する資料が少ないharmtrace,sonic-annotator,xgboost,essentiaについてはこの記事のプログラムを書いた当時でのインストールの情報を書いておきます。


記事のデータに使用したかを別に、通して少しでも利用したライブラリ/データは以下です。

- Windows10 64bit
- VirtualBox 5.0.20
  - Linux Mint 17.3 Rosa Cinnamon 32bit
  - Ubuntsu 14.04 64bit
- Python (Aaconda3 2.3.0 64bit Python3.4)
  - condaの仮想環境でPython 2.7
  - numpy/scipy/matplotlib/scikit-learn
  - librosa
  - xgboost
  - hyperopt
  - imbalanced-learn
- XGBoost
- ffmpeg
- sonic-annotator
  - Chordino and NNLS Chroma
  - MELODIA
  - Queen Mary plugin set
  - Silvet Note Transcription
- Essentia
- GHC-7.6.3/cabal1.22
  - HarmTrace-2.2.0
  - HarmTrace-Base-1.1.0.2
- GTZAN Genre Collection
- MagnaTagATune
- 東方シリーズ
- J-アニソン神曲シリーズ
