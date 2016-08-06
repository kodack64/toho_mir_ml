# toho_mir_ml
C90寄稿記事のソース　東方のbgmを分類したり特徴量を調べたりする

---

必要なツール

Python関係  
- Anacondaに入ってるやつ
- librosa
- rp_extract (pipで取れないので、落としてconvertフォルダに置く）
- xgboost

Python以外でパス通ってる必要のある物
- HarmTrace
- sonic-annotator
- ffmpeg

注意点

- 途中からコード進行の処理を変えたので、一部の使わなくなったコード進行関係の関数が不整合になっているまま放置されています。
- 基本的にmir_execute.py,ml_execute.pyから色々処理しますが、機能をごちゃごちゃ追加したのでコマンドライン引数の説明が半分ぐらい間違えています
- 解説は[gitbook](https://www.gitbook.com/book/kodack64/toho_mir_ml)を読んでください
