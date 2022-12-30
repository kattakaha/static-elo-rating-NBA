import os
import pathlib


class Csv(object):
    """csvの基本モデル"""

    def __init__(self, csv_file):
        self.csv_file = csv_file
        # csvファイルが存在しない場合
        if not os.path.exists(self.csv_file):
            pathlib.Path(csv_file).touch()
