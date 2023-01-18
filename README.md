# static-elo-rating-NBA

![APM](https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat)
![Editor](https://img.shields.io/badge/-Visual%20Studio%20Code-007ACC.svg?logo=visual-studio-code&style=flat)
![AUR last modified](https://img.shields.io/aur/last-modified/google-chrome)

NBAのシーズンを通してK因子固定のElo-rating

## DEMO


![demo](https://user-images.githubusercontent.com/58053010/210120770-13510656-2ba2-42e6-83a9-1f00b2468ed9.gif)

## Features

コマンドライン引数でシーズンとK因子を指定できます。

## Requirement

### Interpreter

- Python


### Packages

#### Python

- os
- pandas
- termcolor
- sys

## ENV

実行環境

```
[static-elo-rating-NBA] % python --version
Python 3.8.5
```

## Installation

pythonのパッケージは`requirements.txt`に記載してあります。直接インストールする際は
```bash
pip install -r requirements.txt
```

またはMakefileからインストールできるようにしました。
```bash
make install
```

## Usage

### Exec directly

実行方法を簡単に説明します．

- `main.py` : コマンドライン引数にEloレイティングを計算したいシーズンを入力します
	- `[season]` : スクレイピングしたいシーズンの開始年度
    - `[K-factor]`: K因子定数

```bash
git clone https://github.com/kkml4220/static-elo-rating-NBA.git
cd static-elo-rating-NBA
python main.py [season] [K-factor]
```

### Use Makefile

`Makefile`で簡単に実行できるようにしました．

- 2018
- 2019
- 2020
- 2021

これらの年度のシーズンのデータからEloレイティングを計算します。


## Directory structure

ディレクトリ構成

```
.
├── LICENSE
├── Makefile
├── README.md
├── input　# 入力ファイルのディレクトリ
│   ├── 2018.csv
│   ├── 2019.csv
│   ├── 2020.csv
│   └── 2021.csv
├── main.py
├── output # 出力ファイルのディレクトリ
├── requirements.txt
├── staticelo # アプリケーションフォルダ
    ├── controller
    │   └── calc.py
    ├── models
    │   ├── csv.py
    │   ├── game.py
    │   ├── rating.py
    │   ├── standings.py
    │   ├── staticelo.py
    │   └── team.py
    ├── settings.py
    ├── templates
    │   ├── debug.txt
    │   ├── game_info.txt
    │   └── information.txt
    └── views
        └── console.py
```


## Author

- 作成者 : 高橋 克征 (Takahashi Katsuyuki)
- E-mail : [Takahashi.Katsuyuki.github@gmail.com](Takahashi.Katsuyuki.github@gmail.com)

## License

"static-elo-rating-NBA" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
