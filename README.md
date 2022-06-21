# denormalized-number-performance-experiment
正規化数と非正規化数の計算速度を比較する実験プログラム

## 動作環境

* Linux 64bit OS
* x86_64(amd64) or arm64 CPU

### 動作確認済み環境

* Ubuntu Server 22.04 LTS 64bit (Intel/AMD CPU, Raspberry Pi 4 Model B)

## 環境構築

下記パッケージをインストールします.
* `numpy`
* `cpuinfo`

## 実行方法

### 1. 測定

* `python main.py`
  * FTZフラグとDAZフラグを無効にして, 測定を開始します
* `python main.py --ftz`
  * FTZフラグとDAZフラグを有効にして, 測定を開始します
* 結果は `main.log` に json 形式で追記されます.

### 2. 測定結果を棒グラフとして視覚化

* `python draw_graph.py`
* 注) 測定結果は, `CPU1 (ftz=false)`, `CPU1 (ftz=true)`, `CPU2 (ftz=false)`, ... の順に `main.log` に保存されている必要があります.
