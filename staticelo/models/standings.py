import csv
import os


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
        self.season = season
        self.name = name

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

    def find_standings(self):
        output_dir_path = self._get_output_dir_path()
        filename = self.name + ".csv"
        csv_file = os.path.join(output_dir_path, filename)
