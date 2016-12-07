# toho_mir_ml
C90寄稿記事のソース　東方のbgmを分類したり特徴量を調べたりする。

やった内容の解説は[gitbook](https://www.gitbook.com/book/kodack64/toho_mir_ml)を読んでください

---

### 概要

楽曲を分類したり特徴量を調べたりします。  
やってるのは以下です

音声処理回り
- ffmpegでmp3ファイルをデコード
- librosaを使ったharmonic percussive sound separationとmfcc/mfcc-deltaの抽出
- harmtraceとsonic-annotatorを使ったコード進行と調の抽出、およびディグリーネームの読み替えとTFIDFベクトルへの変換
- rp_extractを使ったリズムパターンの抽出

機械学習回り
- scikit-learnとXGBoostを使った楽曲の2-class/3-class分類
- チューニングを繰り返し幾つかの分類モデルのROCを比べることで、楽曲分類の上でのモデルの優劣を比較
- 特徴選択を用いた重要な特徴量の選定やランク付け
- LinearSVMの係数やアンサンブル学習の部分依存グラフを用いた特徴と分類の相関の分析
- ランダムにテストセットをサンプリングしなおすことで判定の難しい楽曲（そのクラスらしくないっぽい楽曲）を検出
- MFCC、コード進行、リズムパターンの三つの特徴を利用したstacked generalization

### 必要なツール

Python関係  
- Anacondaに入ってるやつ
- librosa
- rp_extract (pipで取れないので、落としてconvertフォルダに置く）
- xgboost

Python以外でパス通ってる必要のある物
- HarmTrace
- sonic-annotator
- ffmpeg

### 注意点

- 途中からコード進行の処理を変えたので、一部の使わなくなったコード進行関係の関数が不整合になっているまま放置されています。
- 基本的にmir_execute.pyからconvertフォルダのモジュールを、ml_execute.pyからlearnフォルダのモジュールを呼び出す形になっています。しかし、後から機能をごちゃごちゃ追加したのでコマンドライン引数の説明が半分ぐらい間違えています
