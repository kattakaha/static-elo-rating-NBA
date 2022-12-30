import csv
import os
import pandas

from staticelo.models.csv import Csv

from staticelo.settings import OUTPUT_DIR, TEAMS
from staticelo.settings import RATING_COLUMN_TEAM, RATING_COLUMN_RATING

INITIAL_RATING = 1500.0


class Rating(Csv):
    """csvモデルを継承したレイティングのモデル"""

    def __init__(self, season, csv_file=None, *args, **kwargs):
        self.season = season
        self.csv_file = self.find_ratings()

        # csvファイルが存在しない場合
        if not os.path.exists(self.csv_file, *args, **kwargs):
            super().__init__(self.csv_file, *args, **kwargs)
            self.init_ratings()

        self.data = []
        self.load_data()

    def _get_output_dir_path(self):
        """アウトプットディレクトリのパスを作成
        Returns:
            str: アウトプットディレクトリのパス
        """
        output_dir_path = os.path.join(OUTPUT_DIR, self.season)
        # ディレクトリが存在しない場合
        if not os.path.exists(output_dir_path):
            os.mkdir(output_dir_path)

        return output_dir_path

    def init_ratings(self):
        """レイティングのデータを初期化"""
        df = pandas.DataFrame(
            {
                RATING_COLUMN_TEAM: TEAMS,
                RATING_COLUMN_RATING: INITIAL_RATING,
            }
        )
        df.to_csv(self.csv_file, header=True, index=False)

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

            self.data = (
                pandas.DataFrame(dict_array)
                .set_index(RATING_COLUMN_TEAM)
                .astype(
                    {
                        RATING_COLUMN_RATING: float,
                    }
                )
            )

        return self.data


    def get_rating(self, team):
        """チームのレイティングを返します
        Args:
            team (str): チーム名
        Returns:
            float: 引数のチームのレイティング
        """
        return self.data.at[team, RATING_COLUMN_RATING]