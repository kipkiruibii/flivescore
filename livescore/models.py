from django.db import models


class AllMatches(models.Model):
    hometeam = models.TextField(null=True)
    awayteam = models.TextField(null=True)
    hometeamColor = models.TextField(null=True)
    awayteamColor = models.TextField(null=True)
    homescore = models.TextField(null=True)
    awayscore = models.TextField(null=True)
    homeformation = models.TextField(null=True)
    awayFormation = models.TextField(null=True)
    lineUpConfirmed = models.BooleanField(default=False)
    status = models.TextField(null=True)
    matchid = models.TextField(null=True)
    statusCode = models.TextField(null=True)
    leagueId = models.TextField(null=True)
    leagueName = models.TextField(null=True)
    venue = models.TextField(null=True)
    isConf = models.BooleanField(null=True)
    hFormation = models.TextField(null=True)
    aFormation = models.TextField(null=True)

    countryName = models.TextField(null=True)
    startTime = models.TextField(null=True)
    def __str__(self):
        return f'{self.hometeam} V {self.awayteam}'


class NewsArticles(models.Model):
    title=models.TextField(null=True)
    author=models.TextField(null=True)
    description=models.TextField(null=True)
    datePublished=models.TextField(null=True)
    link=models.TextField(null=True)
    image_url=models.TextField(null=True)
    def __str__(self):
        return f'{self.title} '
class MatchInfo(models.Model):
    match=models.ForeignKey(AllMatches,on_delete=models.CASCADE)
    cornerkicksH=models.TextField(null=True)
    cornerkicksA=models.TextField(null=True)
    possesionH=models.TextField(null=True)
    possesionA=models.TextField(null=True)
    yellowCardsH=models.TextField(null=True)
    yellowCardsA=models.TextField(null=True)
    gkSavesH=models.TextField(null=True)
    gkSavesA=models.TextField(null=True)
    shotsH=models.TextField(null=True)
    shotsA=models.TextField(null=True)

    def __str__(self):
        return f'{self.match.hometeam} V {self.match.awayteam}'




class MatchLineUp(models.Model):
    match=models.ForeignKey(AllMatches,on_delete=models.CASCADE)
    player=models.TextField(null=True)
    number=models.TextField(null=True)
    position=models.TextField(null=True)
    isHomePlayer=models.BooleanField(default=False)
    def __str__(self):
        return f'{self.match.hometeam} V {self.match.awayteam}'



class LeagueHomeStandings(models.Model):
    league = models.TextField(null=True)
    team = models.TextField(null=True)
    rank = models.TextField(null=True)
    points = models.TextField(null=True)
    mp = models.TextField(null=True)
    gf = models.TextField(null=True)
    ga = models.TextField(null=True)
    wins = models.TextField(null=True)
    draws = models.TextField(null=True)
    losses = models.TextField(null=True)
    def __str__(self):
        return f'{self.league} '



class LeagueAwayStandings(models.Model):
    league = models.TextField(null=True)
    team = models.TextField(null=True)
    rank = models.TextField(null=True)
    points = models.TextField(null=True)
    mp = models.TextField(null=True)
    gf = models.TextField(null=True)
    ga = models.TextField(null=True)
    wins = models.TextField(null=True)
    draws = models.TextField(null=True)
    losses = models.TextField(null=True)
    def __str__(self):
        return f'{self.league} '


class LeagueOverallStandings(models.Model):
    league = models.TextField(null=True)
    team = models.TextField(null=True)
    rank = models.TextField(null=True)
    points = models.TextField(null=True)
    mp = models.TextField(null=True)
    gf = models.TextField(null=True)
    ga = models.TextField(null=True)
    wins = models.TextField(null=True)
    draws = models.TextField(null=True)
    losses = models.TextField(null=True)
    def __str__(self):
        return f'{self.league} '

class LeagueInfo(models.Model):
    # league
    league_id = models.TextField(null=True)
    league_name = models.TextField(null=True)
    league_image = models.TextField(null=True)
    current_league_week = models.TextField(null=True)
    league_importance = models.TextField(null=True)

    country_name = models.TextField(null=True)
    season_name = models.TextField(null=True)
    season_id = models.TextField(null=True)

    def __str__(self):
        return self.league_name

