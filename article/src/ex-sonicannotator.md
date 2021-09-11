# sonic-annotator

---

[Sonic Annotator](http://www.vamp-plugins.org/sonic-annotator/)  
[使い方](https://code.soundsoftware.ac.uk/projects/sonic-annotator/wiki)  
[Vamp pluginsのリスト](http://www.vamp-plugins.org/download.html)

sonic-annotatorはvamp-pluginsと呼ばれる一連のmusic analysisのプラグインのホストです。Windows/Mac/Linux用のバイナリが配られているので、ダウンロードするだけで簡単に使用できます。頻繁に使用するので、パスを通しておくとよいと思います。

vamp pluginsはかなり多彩なものを抽出することができるので、ツールを使って音声の分析をしようとしたときに非常に便利です。俺はpythonからsubprocessでコマンドを叩いて使用しましたが、[pythonのバインディング](http://www.vamp-plugins.org/vampy.html)もあるようです。

### 使い方

#### プラグインのダウンロード
上記のvamp pluginsのリストから、利用したいプラグインをダウンロードします。デフォルトで入れるべきpluginsのフォルダはVamp pluginsのダウンロードページの一番下のHow to installに書いてあります。Windowsなら、"C:\\Program Files\\Vamp Plugins"です。harmtraceの実行には、Queen Mary plugin setとChordino and NNLS Chromaが必要になります。

正しい位置にプラグインがあるとき、
```sh
sonic-annotator -l
```
を実行すると、実行可能なプラグインの出力のリストが列挙されます。

#### スケルトンの作成
上の出力可能なものの一覧から抽出したい特徴が決まったら、その名前を以下のように入れます。
```sh
sonic-annotator -s [name] > [outputname].txt
```
こうすることで、[outputname].txtの中にスケルトンの内容が流し込まれます。このテキストを編集すると、変換の設定を編集できます。


#### 変換
実際に変換を実行するには、
```sh
sonic-annotator -t [outputname].txt  hoge.wav -w csv --csv-one-file [outputpath]
```
としておくと、outputpathにhoge_[name]のテキストが作成されます。sonic-annotatorはデフォルトでは出力を上書きしようとするエラーが出るので、バッチ処理する場合には、--csv-forceを指定しておくといい感じです。


#### 変換のフォーマット
出力されたものはcsvになっています。csvの中身の数字が何を意味しているのかはだいたいの場合勘でわかるかと思いますが、一部の内容はわかりづらいことがあります。その場合、作成したスケルトンファイル末尾にあるURLにアクセスします。すると、変換可能な内容のリストのテキストにアクセスできるので、出力したいものの名前で検索すると、そのdescriptionの項に具体的な内容などが書いてあります。

#### エラーが出てしまう場合
サンプルレートなどが想定と違う場合は、実行時にエラーが出力されます。恐らくエラーの中に「○○のパラメータが要求と違う」ということが書いてあるはずなので、該当する名前のパラメータをスケルトンファイルの中から探して調整することでほとんどの場合解決できます。

例えば、qm-vamppuginsのkeydetectorは一部のファイルでは失敗するのですが、その場合はstep_sizeとblock_sizeを半分にしたスケルトンで再度トライすることでほとんどの場合成功します。
