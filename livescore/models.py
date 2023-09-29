from django.db import models


class TodaysMatches(models.Model):
    hometeam = models.TextField(default='t')
    awayteam = models.TextField(default='t')
    hometeamColor = models.TextField(default='t')
    awayteamColor = models.TextField(default='t')
    homescore = models.TextField(default='-')
    awayscore = models.TextField(default='-')
    status = models.TextField(default='s')
    matchid = models.IntegerField(default=0)
    statusCode = models.IntegerField(default=0)
    league = models.IntegerField(default=0)
    startTime = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.hometeam} V {self.awayteam}'

class AllMatches(models.Model):
    hometeam = models.TextField(default='t')
    awayteam = models.TextField(default='t')
    hometeamColor = models.TextField(default='t')
    awayteamColor = models.TextField(default='t')
    homescore = models.TextField(default='-')
    awayscore = models.TextField(default='-')
    status = models.TextField(default='s')
    matchid = models.IntegerField(default=0)
    statusCode = models.IntegerField(default=0)
    league = models.IntegerField(default=0)
    startTime = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.hometeam} V {self.awayteam}'


class NewsArticles(models.Model):
    title=models.TextField(default='-')
    author=models.TextField(default='-')
    link=models.TextField(default='-')
    image_url=models.TextField(default='-')
    def __str__(self):
        return f'{self.title} '


class MatchInfo(models.Model):
    match=models.ForeignKey(AllMatches,on_delete=models.CASCADE)
    cornerkicksH=models.TextField(default='-')
    cornerkicksA=models.TextField(default='-')
    possesionH=models.TextField(default='-')
    possesionA=models.TextField(default='-')
    yellowCardsH=models.TextField(default='-')
    yellowCardsA=models.TextField(default='-')
    gkSavesH=models.TextField(default='-')
    gkSavesA=models.TextField(default='-')
    shotsH=models.TextField(default='-')
    shotsA=models.TextField(default='-')


class MatchLineUp(models.Model):
    match=models.ForeignKey(AllMatches,on_delete=models.CASCADE)
    player=models.TextField(default='-')
    number=models.TextField(default='-')
    position=models.TextField(default='-')
    isHomePlayer=models.BooleanField(default=False)
    def __str__(self):
        return f'{self.player} '


class LeagueHomeStandings(models.Model):
    league = models.IntegerField(default=0)
    leaguename = models.TextField(default='ln')
    team = models.TextField(default='ln')
    rank = models.IntegerField(default=0)
    mp = models.IntegerField(default=0)
    gf = models.IntegerField(default=0)
    ga = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.leaguename} '



class LeagueAwayStandings(models.Model):
    league = models.IntegerField(default=0)
    leaguename = models.TextField(default='ln')
    team = models.TextField(default='ln')
    rank = models.IntegerField(default=0)
    mp = models.IntegerField(default=0)
    gf = models.IntegerField(default=0)
    ga = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.leaguename} '


class LeagueOverallStandings(models.Model):
    league = models.IntegerField(default=0)
    leaguename = models.TextField(default='ln')
    team = models.TextField(default='ln')
    rank = models.IntegerField(default=0)
    mp = models.IntegerField(default=0)
    gf = models.IntegerField(default=0)
    ga = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.leaguename} '


class LeagueResults(models.Model):
    league = models.IntegerField(default=0)
    leaguename = models.TextField(default='ln')
    hometeam = models.TextField(default='t')
    awayteam = models.TextField(default='t')
    hometeamColor = models.TextField(default='t')
    awayteamColor = models.TextField(default='t')
    homescore = models.TextField(default='-')
    awayscore = models.IntegerField(default='-')
    status = models.TextField(default='s')
    matchid = models.IntegerField(default=0)
    statusCode = models.IntegerField(default=0)
    startTime = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.hometeam} V {self.awayteam}'


class LeagueFixures(models.Model):
    league = models.IntegerField(default=0)
    leaguename = models.TextField(default='ln')
    hometeam = models.TextField(default='t')
    awayteam = models.TextField(default='t')
    hometeamColor = models.TextField(default='t')
    awayteamColor = models.TextField(default='t')
    homescore = models.TextField(default='-')
    awayscore = models.IntegerField(default='-')
    status = models.TextField(default='s')
    matchid = models.IntegerField(default=0)
    statusCode = models.IntegerField(default=0)
    startTime = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.hometeam} V {self.awayteam}'
