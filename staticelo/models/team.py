
from staticelo.models import standings
from staticelo.settings import TEAMS

class Team(object):
    """チームの基本クラス"""

    def __init__(self, season, name, *args, **kwargs):
        self.season = season
        self.name = name
        self.standings = standings.Standings(season=self.season, name=self.name)