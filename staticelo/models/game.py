import csv
import os
import pandas

from staticelo.settings import INPUT_DIR
from staticelo.settings import GAME_COLUMN_HOME_SCORE, GAME_COLUMN_AWAY_SCORE


class NoInputfileError(Exception):
    """インプットファイルが存在しないエラー"""


class Game(object):
    """試合情報のクラス"""

    def __init__(self, season, csv_file=None, *args, **kwargs):
        self.season = season
        self.csv_file = self.get_csv_file_path()
        self.data = []
        self.load_data()

    def get_csv_file_path(self):
        """csvファイルのパスを作成
        Return:
            str: csvファイルのパスを返すs
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
        dict_array = []
        with open(self.csv_file, mode="r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                dict_array.append(row)
            
            self.data = pandas.DataFrame(dict_array).astype({
                GAME_COLUMN_HOME_SCORE: int,
                GAME_COLUMN_AWAY_SCORE: int,
            })
        
        return self.data