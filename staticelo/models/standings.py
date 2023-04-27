import os
import pandas

from staticelo.models.csv import Csv
from staticelo.settings import OUTPUT_DIR, TEAMS
from staticelo.settings import (
    STANDING_COLUMN_TEAM,
    STANDING_COLUMN_N,
    STANDING_COLUMN_WIN,
    STANDING_COLUMN_LOSE,
    STANDING_COLUMN_WP,
)


STANDING_COLUMNS = [
    STANDING_COLUMN_TEAM,
    STANDING_COLUMN_N,
    STANDING_COLUMN_WIN,
    STANDING_COLUMN_LOSE,
    STANDING_COLUMN_WP,
]


class Standings(Csv):
    """csvモデルから継承した勝敗情報のクラス"""

    def __init__(self, season, name, csv_file=None, *args, **kwargs):
        """コンストラクタ
        Args:
            season (str)    : シーズンの開始年度 e.g: "2021"
            name (str)      : チーム名
            csv_file (str)  : csvのファイルパス
        """
        self.season = season
        self.name = name
        self.csv_file = self.find_standings()
        if not os.path.exists(self.csv_file):
            super().__init__(self.csv_file, *args, **kwargs)
            self.init_standings()
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
            os.makedirs(output_dir_path)

        return output_dir_path

    def find_standings(self):
        """csvファイルのパスを作成
        Returns:
            str: csvファイルのパスを返す
        """
        output_dir_path = self._get_output_dir_path()
        filename = self.name + ".csv"
        csv_file = os.path.join(output_dir_path, filename)
        return csv_file

    def init_standings(self):
        """勝敗情報を初期化"""
        df = pandas.DataFrame(
            {
                STANDING_COLUMN_TEAM: TEAMS,
                STANDING_COLUMN_N: 0,
                STANDING_COLUMN_WIN: 0,
                STANDING_COLUMN_LOSE: 0,
                STANDING_COLUMN_WP: 0.0,
            }
        )
        df.to_csv(self.csv_file, header=True, index=False)

    def load_data(self):
        """csvファイルのデータを読み込みます
        Returns:
            pandas.DataFrame: standingsのデータをpandas.DataFrame型で返します.
        """
        df = pandas.read_csv(self.csv_file)
        df = df.set_index(STANDING_COLUMN_TEAM).astype({
            STANDING_COLUMN_N: int,
            STANDING_COLUMN_WIN: int,
            STANDING_COLUMN_LOSE: int,
            STANDING_COLUMN_WP: float,
        })
        self.data = df
        return self.data
    
    
    def get_opponent_data(self, opponent):
        """対戦相手の情報を取得します
        Args:
            opponent (str): 対戦相手のチーム名
        Returns:
            pandas.Series: 対戦相手の情報を返します
        """
        self.load_data()
        return self.data.loc[opponent]
    
    def _calc_wp(self, opponent):
        """対戦相手の勝率を計算します
        Args:
            opponent (str): 対戦相手のチーム名
        Retuens:
            float: 対戦相手の勝率
        """
        n = self.data.at[opponent, STANDING_COLUMN_N]
        w = self.data.at[opponent, STANDING_COLUMN_WIN]
        return float(w/n)
    
    def update(self, opponent, winner):
        """standingsのデータをアップデートする
        Args:
            opponent(str): 対戦相手
            winner(str): 試合の勝者
        Retuens:
            pandas.DataFrame: 勝敗情報をpandas.DataFrameで返します
        """
        self.load_data()
        # 試合数をインクリメント
        self.data.at[opponent, STANDING_COLUMN_N] += 1
        # 勝者が対戦相手でないなら; 自分が勝ったら
        if winner != opponent:
            self.data.at[opponent, STANDING_COLUMN_LOSE] += 1
        else:
            self.data.at[opponent, STANDING_COLUMN_WIN] += 1
        
        # 勝率を計算
        self.data.at[opponent, STANDING_COLUMN_WP] = self._calc_wp(opponent)
        self.save()
        return self.data
    
    def save(self):
        """勝敗情報のcsvファイルを作成します"""
        self.data.to_csv(self.csv_file, header=True, index=True)
    
    def delete(self):
        """勝敗情報のcsvファイルを削除します"""
        os.remove(self.csv_file)