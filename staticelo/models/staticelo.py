import math

from staticelo.models.rating import Rating
from staticelo.models.game import Game, game_info
from staticelo.models.team import Team

from staticelo.views import console

from staticelo.settings import (
    GAME_COLUMN_HOME,
    GAME_COLUMN_AWAY,
    GAME_COLUMN_HOME_SCORE,
    GAME_COLUMN_AWAY_SCORE,
)


def get_winner(game):
    """試合情報から勝者を決定
    Args:
        game (pandas.Series) : 試合情報のpandas.Series
    Returns:
        str: 勝ちチームのチーム名
    """
    if game[GAME_COLUMN_HOME_SCORE] >= game[GAME_COLUMN_AWAY_SCORE]:
        return game[GAME_COLUMN_HOME]
    else:
        return game[GAME_COLUMN_AWAY]

class StaticElo(object):
    """Static Elo-ratingの基本クラス"""

    def __init__(self, season, K, XI, *args, **kwargs):
        self.season = season
        self.K = K
        self.XI = XI
        self.games = Game(season=self.season)
        self.ratings = Rating(season=self.season, K=K)

    def infomation(self):
        """Eloレイティングの基本情報を描画"""
        template = console.get_template("information.txt", color="red")
        print(
            template.substitute(
                {
                    "season": self.season,
                    "K": self.K,
                    "XI": self.XI,
                }
            )
        )

    def elo_rating(self, game):
        """Eloレイティングを計算してレイティングデータを更新"""

        def S(hscore, ascore):
            """Calculate Score in Elo Rating
            Args:
                hscore (int) : home team score
                ascore (int) : away team score
            Returns:
                int: 1 if home team wins.
            """
            if hscore > ascore:
                return 1
            else:
                return 0

        def mu(r_i, r_j, XI):
            def L(x):
                return 1 / (1 + math.pow(10, -x))

            d = r_i - r_j
            return L(d / XI)

        K = self.K
        XI = self.XI

        i = game[GAME_COLUMN_HOME]
        j = game[GAME_COLUMN_AWAY]
        s_i = int(game[GAME_COLUMN_HOME_SCORE])
        s_j = int(game[GAME_COLUMN_AWAY_SCORE])

        r_i = self.ratings.get_rating(i)
        r_j = self.ratings.get_rating(j)

        old_r_i = r_i
        old_r_j = r_j

        tmp = r_i
        r_i = r_i + K * (S(s_i, s_j) - mu(r_i, r_j, XI))
        r_j = r_j + K * ((1 - S(s_i, s_j)) - mu(r_j, tmp, XI))

        delta_i = r_i - old_r_i
        delta_j = r_j - old_r_j

        # レイティングを更新
        self.ratings.update(team=i, rating=r_i)
        self.ratings.update(team=j, rating=r_j)

        # レイティング更新情報を描画
        contents = console.rating_info(i, r_i, delta_i) + console.rating_info(
            j, r_j, delta_j
        )
        print(contents)

    def elo_system(self):
        """全試合でEloレイティングを計算"""
        games = self.games.data
        for index, game in games.iterrows():
            game_info(index, game)
            home = Team(season=self.season, name=game[GAME_COLUMN_HOME])
            away = Team(season=self.season, name=game[GAME_COLUMN_AWAY])
            winner = get_winner(game)
            home.standings.update(opponent=game[GAME_COLUMN_AWAY], winner=winner)
            away.standings.update(opponent=game[GAME_COLUMN_HOME], winner=winner)
            self.elo_rating(game)