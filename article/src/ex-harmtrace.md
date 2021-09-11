# HarmTrace

---

[hackage HarmTrace](https://hackage.haskell.org/package/HarmTrace)

[hackage HarmTrace-Base](https://hackage.haskell.org/package/HarmTrace-Base)

HarmTraceはこの分野では恐らく珍しく、Haskellで書かれたプログラムです。HarmTraceはコード進行自動変換サイトである[chordify](https://chordify.net)のバックエンドであり、商用になる程の精度を誇りながら無料という素晴らしいソフトです。

HarmTrace以外でコード進行をバッチで抽出できるライブラリですと、sonic-annotatorから呼び出せるvamp pluginsである、[Chordino and NNLS Chroma](http://www.isophonics.net/nnls-chroma)や、少しこのページでも紹介している[Essentia](http://essentia.upf.edu/)があります。この二つはharmtraceより格段にインストールが楽なので、harmtraceのインストールがだるくなったらこっちを使いましょう。

HarmTraceのパッケージはサービスが開発中であるためにユーザに向けてほとんどメンテされていないという事情があり、インストールの資料がほぼありません。さらに、最近はstackの存在により改善されたらしいものの、従来のHaskellはcabal hellと呼ばれるライブラリ依存環境の整備の困難さがありました。HarmTracehはstackのLTSがサポートする以前のGHC-7.6.3に依存するライブラリなので、最近の改善の恩恵を受けることができません。これらの事情から、HarmTraceのインストールは非常に難しくなっています。ネットでもインストール無理もうだめってブログだけが見つかるので相当アレです。


#### 仮想環境とGHC,cabalの用意
まず、Haskellの古いライブラリの多くがWindowsでインストールするとコケるので、おとなしくVirtualBoxなどの仮想環境上でUbuntsuなどを動かしましょう。私はLinuxMintの最新版を使用していました。

起動したらまず以下のコマンドを実行します。
```sh
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:hvr/ghc
sudo apt-get update
sudo apt-get install -y cabal-install-1.22 ghc-7.6.3
cat >> ~/.bashrc <<EOF
export PATH="\$HOME/.cabal/bin:/opt/cabal/1.22/bin:/opt/ghc/7.6.3/bin:\$PATH"
EOF
export PATH=~/.cabal/bin:/opt/cabal/1.22/bin:/opt/ghc/7.6.3/bin:$PATH
```

これでHaskellとcabalが入りパスが通りました。

#### 依存ライブラリのインストール
このままではzlibのライブラリ回りが足りないといわれるのでこれをインストールしておきます。また、gslとlapackの関係ライブラリも事前にいれておく必要があります。
```sh
sudo apt-get install libghc-zlib-dev libghc-zlib-bindings-dev
cabal update
cabal install cabal-install
cabal update
sudo apt-get install libgsl0-dev liblapack-dev
```

#### ビルド
先に言うと、以下のコマンドはエラーが出て失敗します。また、一個目のコマンドは一見無駄に見えますが、先にこれを実行しないと私の環境では依存関係が解決できなくなってしまうので、いったんバージョンを指定せずにHarmTraceのインストールを実行します。また、--force-reinstallにしないと、cabal-installのインストール時に追加されたライブラリが衝突してインストールできません。
```sh
cabal install HarmTrace　--force-reinstall
cabal install HarmTrace --with-ghc=ghc-7.6.3 --constraint="HarmTrace-Base==1.1.0.2" --constraint="uu-parsinglib installed" --allow-newer=uu-parsinglib,cabal
```
stackageによればHarmTrace-Baseの最新バージョンは1.1.0.2の次の1.4.0.1が出ていますが、これに対応するHarmTraceが出ていないので、1.1.0.2でインストールする必要があります。

ビルドに失敗したら、失敗の原因を解決します。

#### hmatrix-gsl-statの修正
エラーの原因はhmatrix-gsl-statsのパッケージにおいて、複数のライブラリの同じ名前の関数が衝突していることによります。よって、ローカルにライブラリをダウンロードして修正したうえでインストールします。まず、ソースコードを以下のコマンドでダウンロードします。
```sh
wget https://hackage.haskell.org/package/hmatrix-gsl-stats-0.4.1.1/hmatrix-gsl-stats-0.4.1.1.tar.gz
tar zxvf hmatrix-gsl-stats-0.4.1.1.tar.gz
```
このパッケージ内部の.hsファイルを開くと、殆どすべてのソースコード(たしかCommon.hs以外のすべて)で、
```haskell
Import Foreign
Import Foreign hiding(shift)
```
の二行のどちらかの行があるのですが、ここからインポートされるunsafePerformIOという関数が恐らく後からSystemにおいてサポートされ、名前が衝突してしまっているのがhmatrix-gsl-statsのビルドが通らない原因になっています。そこで、Foreign側のunsafePerformIOをインポートしないように書き換えることでエラーを回避できます。具体的には全ての上記の
```haskell
Import Foreign hiding(unsafePerformIO)
Import Foreign hiding(shift,unsafePerformIO)
```
とバッチでも手修正でもいいので、追記します。これで名前の衝突が回避できるので、.cabalファイルのあるディレクトリの一つ下まで移動し、
```sh
cabal install hmatrix-gsl-stats-0.4.1.1/hmatrix-gsl-stats.cabal
```
を実行することで、hmatrix-gsl-stats-0.4.1.1がインストールされます。
この後、改めて
```sh
cabal install HarmTrace --with-ghc=ghc-7.6.3 --constraint="HarmTrace-Base==1.1.0.2" --constraint="uu-parsinglib installed" --allow-newer=uu-parsinglib,cabal
```
を実行するとharmtraceのビルドが通り実行可能になると思います。
試しに、harmtraceコマンドを実行すると、
```sh
>harmtrace
harmtrace [COMMAND] ... [OPTIONS]
  Harmonic Analysis and Retrieval of Music

Commands:
  parse      Parse files into harmonic analysis trees
  match      Harmonic similarity matching
  recognise  Recognise chords from audio files

  -r=file            File to read flags from
  -?      --help     Display help message
  -V      --version  Print version information
```
と出れば成功です。


#### 依存環境の構築

harmtraceのコマンドは通るようになりましたが、必要な依存ファイルが無いとコード進行の抽出は失敗してしまいます。しかしながら、必要なファイルが何なのか書いてなので非常に困り、ソースコードを読んで頑張って読解しました。

答えから言うと、パスの通ったsonic-annotatorとqm-vampplugins、NNLS Chromaのプラグイン、およびこれらで変換を行うためのtransformファイルが必要になります。

sonic-annotatorのインストール自体についてはsonic-annotatorの環境構築の章を参照してください。qm-vamppluginsとNNLS Chromaのプラグインが正しく入っている前提から続きを書きます。

まず、workなどの適当な名前の作業ディレクトリを作ります。このとき、パスに日本語などが入っているとHaskellが死ぬので注意してください。このディレクトリに、feature,vamp,logの三つのフォルダを作成します。次に、vampフォルダに移動し、以下のコマンドを実行してスケルトンを作成します。
```sh
sonic-annotator -s vamp:nnls-chroma:nnls-chroma:bothchroma > both-chroma.txt
sonic-annotator -s vamp:qm-vamp-plugins:qm-barbeattracker:beats > beat-tracker-one.txt
sonic-annotator -s vamp:nnls-chroma:nnls-chroma:chroma > tuned-chroma.txt
```
こうすることで、sonic-annotatorによるtransformファイルが必要な名前で出力されます。

ただし、harmtraceはsoxでサンプルレートを半分にダウンサンプリングして解析を行うため、qm-barbeattrackerはデフォルトのtransformファイルだと変換がこけてしまいます。そこで、作成したbeat-tracker-one.txtを開き、7行目にあるstep_sizeの値を512から256に書き換えて保存します。これで、
```sh
harmtrace recognise -g pop -m mptree -v ./vamp/ -o ./ -f ./feature/ -w ./log/ -i hoge.wav
```
を実行することで、hoge.wavのコードが出力されるようになります。featureフォルダには中間解析ファイルであるsonic-annotatorによって抽出されたデータが、logには生成ログが格納されます。harmtraceは必要な解析ファイルがfeatureフォルダにあると再度の解析を省略するので、featureフォルダは作っておくと高速になります。
具体的な引数のバリエーションについては
```sh
harmtrace recognise -?
```
で見ることができます。

#### そのほかの注意点

パスに日本語が含まれるとコケます。
楽曲は事前にidを振ってid.wavにするなどして対応しましょう。

また、たまにsonic-annotatorの方が良くわからないこけ方をします。harmtraceがsonic-annotatorの処理の前で死んでいたら、sonic-annotator単体での特徴量抽出がうまく動くかを見てみてください。sonic-annotatorの使い方はsonic-annotatorの記事を見てください。
