# Essentia

---

[Essentia](http://essentia.upf.edu/)

EssentiaはC++で記述されているらしいかなり広範な音声解析のライブラリ群です。コード判定とかもできます。

Linuxからクロスコンパイルすることで、Windowsでもmingwで実行できるらしいですが、コケたのでやってないです。誰か出来たら教えてください。

exampleがあまり書かれていないのでpythonのバインディングから同曜日出せばいいのかかなり悩ましく感じるのですが、[TonalExtractor](http://essentia.upf.edu/documentation/reference/std_TonalExtractor.html)ですべて取り出すことができます。

だいたいこんな感じ
```python
from essentia.standard import *
loader = MonoLoader(filename="hoge.mp3")
audio = loader()
ret = TonalExtractor(audio)
chordProg = ret[4]
key = ret[2]
scale = ret[5]
```
です。

少し見た感じでは、HarmTraceの方が精度はいいように見えますが、多分ジャンルによりけりだと思います。
