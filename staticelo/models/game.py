import os
import pandas

from staticelo.views import console

from staticelo.settings import INPUT_DIR
from staticelo.settings import (
    GAME_COLUMN_DATE,
    GAME_COLUMN_HOME,
    GAME_COLUMN_AWAY,
    GAME_COLUMN_HOME_SCORE,
    GAME_COLUMN_AWAY_SCORE,
)


class NoInputfileError(Exception):
    """インプットファイルが存在しないエラー"""


class Game(object):
    """試合情報のクラス"""

    def __init__(self, season, csv_file=None, *args, **kwargs):
        """コンストラクタ
        Args:
            season (str): シーズンの開始年度 e.g:"2021"
            csv_file (str): csvのファイルパス
        """
        self.season = season
        self.csv_file = self.get_csv_file_path()
        self.data = []
        self.load_data()

    def get_csv_file_path(self):
        """csvファイルのパスを作成
        Return:
            str: csvファイルのパスを返す
        """
        filename = self.season + ".csv"
        csv_file_path = os.path.join(INPUT_DIR, filename)

        if not os.path.exists(csv_file_path):
            raise NoInputfileError("Could not find {}".format(csv_file_path))

        return csv_file_path

    def load_data(self):
        """csvファイルのデータを読み込みます
        Retuerns:
            pandas.DataFrame: 試合データをpandas.DataFrameで返します
        """
        df = pandas.read_csv(self.csv_file).astype({
            GAME_COLUMN_HOME_SCORE: int,
            GAME_COLUMN_AWAY_SCORE: int,
        })
        self.data = df
        return self.data


def game_info(index, game):
    """試合情報を描画"""
    template = console.get_template("game_info.txt", color="yellow")
    print(
        template.substitute(
            {
                "index": index,
                "date": game[GAME_COLUMN_DATE],
                "home": game[GAME_COLUMN_HOME],
                "away": game[GAME_COLUMN_AWAY],
                "hscore": game[GAME_COLUMN_HOME_SCORE],
                "ascore": game[GAME_COLUMN_AWAY_SCORE],
            }
        )
    )
