# static-elo-rating-NBA

![APM](https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat)
![Editor](https://img.shields.io/badge/-Visual%20Studio%20Code-007ACC.svg?logo=visual-studio-code&style=flat)

NBA のシーズンを通して K 因子固定の Elo-rating

## DEMO

![demo](https://user-images.githubusercontent.com/58053010/210120770-13510656-2ba2-42e6-83a9-1f00b2468ed9.gif)

## Alogorithm

### Idea

Elo のレイティングは次に示す、最も汎用的で抽象的なレイティングの更新式に基づくものである。

\[r^{\prime} = r + K (S -\mu)\]

- \(r^{\prime}\):更新後
- \(r\):更新前のレイティング
- \(K\): \(K\)因子(定数)
- \(S\): プレイヤーの最近の成績
- \(\mu\): レイティングの平均

Elo はもともと\(K=10\)としていた．この更新式は各プレイヤーに対するレイティングが一旦確率されれたとき，そのレイティングを上下させるには，そのプレイヤーの成績がリーグ全体の平均からどの程度上下するかだけに依るとしている．

### K-factor

\(K\)因子(_K-factor_)とは，チェスの分野で有名でいまだに議論の余地がある定数である．\(K\)因子の目的は，実際のスコアと事前のレイティングに対して期待されるスコアの差を適切に調整することである．

\(K\)の値が大きすぎる場合は，実際のスコアと期待されるスコアの差にあまりに大きな重みが与えられ，レイティングに不安定さをもたらす結果となる．例えば，大きな\(K\)であれば，期待より少し良い成績を出せば大きなレイティングの変化を生む．

他方，\(K\)因子の値が小さすぎるとレイティングがあまり変化しないことになる．例えば，小さい\(K\)因子の場合あるプレイヤーの著しい改善であってもレイティングにさほど影響を与えないことからレイティングシステムとしてあまり適切とは言えない．

### Definition

ここで，当リポジトリで計算する Static Elo-rating のレイティングの定義を述べる．
チーム\(i,j\)に対して，\(\mu\_{ij}\)をそれぞれ次のように定義する．

$$
S_{ij} =
            \begin{cases}
                1   & i\text{が}j\text{に勝った場合}   \\
                0   & i\text{と}j\text{引き分けた場合} \\
                1/2 & i\text{が}j\text{に負けた場合}
            \end{cases}
$$

ロジスティクス関数を\(L(x) = 1/(1 + 10^{-x})\)として

$$
d_{ij} = r_i - r_j
        \;\; \text{に対して} \;\;
        \mu_{ij} = L(d_{ij}/400)=\frac{1}{1 + 10^{-d_{ij} / 400}}
$$

これらの\(S*{ij},\mu*{ij}\)に対してシーズンを通して固定の$K$因子を用いて次式で対戦に対してレイティングの更新を行う．

$$
\begin{cases}
                r^{\prime}_i = r_i + K(S_{ij} - \mu_{ij}) \\
                r^{\prime}_j = r_j + K(S_{ji} - \mu_{ji})
            \end{cases}
$$

- $r^{\prime}_i$ : チーム$i$の更新後のレイティング
- $r^{\prime}_j$ : チーム$j$の更新後のレイティング
- $r_i$ : チーム$i$の更新前のレイティング
- $r_j$ : チーム$j$の更新前のレイティング
- $K$ : $K$因子定数
- $S_{ij}$: チーム$i$のチーム$j$に対する得点
- $\mu_{ij}$: チーム$i$のチーム$j$に対する得点の期待値
- $S_{ji}$: チーム$j$のチーム$i$に対する得点
- $\mu_{ji}$: チーム$j$のチーム$i$に対する得点の期待値

## Features

コマンドライン引数でシーズンと K 因子を指定できます。

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

```plantext
[static-elo-rating-NBA] % python --version
Python 3.8.5
```

## Installation

python のパッケージは`requirements.txt`に記載してあります。直接インストールする際は

```bash
pip install -r requirements.txt
```

または Makefile からインストールできるようにしました。

```bash
make install
```

## Usage

### Exec directly

実行方法を簡単に説明します．

- `main.py` : コマンドライン引数に Elo レイティングを計算したいシーズンを入力します
  - `[season]` : スクレイピングしたいシーズンの開始年度
    - `[K-factor]`: K 因子定数

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

これらの年度のシーズンのデータから Elo レイティングを計算します。

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
└── staticelo # アプリケーションフォルダ
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
