from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.homeintro,name='homeintro'),
    path('getLivescore/', views.getLivescore,name='getLivescore'),
    path('getTodaysMatches/', views.getTodaysMatches,name='getTodaysMatches'),
    path('getMatchesByDate/', views.getMatchesByDate,name='getMatchesByDate'),
    path('getMatchInfo/', views.getMatchInfo,name='getMatchInfo'),
    path('getMatchLineUp/', views.getMatchLineUp,name='getMatchLineUp'),
    path('getLeagueOverallStandings/', views.getLeagueOverallStandings,name='getLeagueOverallStandings'),
    path('getLeagueHomeStandings/', views.getLeagueHomeStandings,name='getLeagueHomeStandings'),
    path('getLeagueAwayStandings/', views.getLeagueAwayStandings,name='getLeagueAwayStandings'),
    path('getLeagueFixtures/', views.getLeagueFixtures,name='getLeagueFixtures'),
    path('getLeagueResults/', views.getLeagueResults,name='getLeagueResults'),
    path('getLatestNews/', views.getLatestNews,name='getLatestNews'),
    path('searchMatch/', views.searchMatch,name='searchMatch'),
]
