from django.urls import path,include
from . import views

urlpatterns = [
    path('getLivescore/', views.getLivescore,'getLivescore'),
    path('getTodaysMatches/', views.getTodaysMatches,'getTodaysMatches'),
    path('getMatchesByDate/', views.getMatchesByDate,'getMatchesByDate'),
    path('getMatchInfo/', views.getMatchInfo,'getMatchInfo'),
    path('getMatchStats/', views.getMatchStats,'getMatchStats'),
    path('getMatchLineUp/', views.getMatchLineUp,'getMatchLineUp'),
    path('getLeagueOverallStandings/', views.getLeagueOverallStandings,'getLeagueOverallStandings'),
    path('getLeagueHomeStandings/', views.getLeagueHomeStandings,'getLeagueHomeStandings'),
    path('getLeagueAwayStandings/', views.getLeagueAwayStandings,'getLeagueAwayStandings'),
    path('getLeagueFixtures/', views.getLeagueFixtures,'getLeagueFixtures'),
    path('getLeagueResults/', views.getLeagueResults,'getLeagueResults'),
    path('getLatestNews/', views.getLatestNews,'getLatestNews'),
    path('searchMatch/', views.searchMatch,'searchMatch'),
]
