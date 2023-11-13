from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(AllMatches)
admin.site.register(NewsArticles)
admin.site.register(MatchInfo)
admin.site.register(MatchLineUp)
admin.site.register(LeagueHomeStandings)
admin.site.register(LeagueAwayStandings)
admin.site.register(LeagueOverallStandings)
admin.site.register(LeagueInfo)