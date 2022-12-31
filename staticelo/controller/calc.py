from staticelo.models import staticelo


def rating(season, K, XI):
    calculator = staticelo.StaticElo(season, K, XI)
    calculator.infomation()
    calculator.elo_system()
    calculator.ratings.rating_info()
    calculator.ratings.save()
