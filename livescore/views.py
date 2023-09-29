from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLivescore(request):
    return Response('success livescore')

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getTodaysMatches(request):
    return Response('success livescore')

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getMatchesByDate(request):
    return Response('success livescore')

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getMatchInfo(request):
    return Response('success livescore')

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getMatchStats(request):
    return Response('success livescore')

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getMatchLineUp(request):
    return Response('success livescore')

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLeagueOverallStandings(request):
    return Response('success livescore')

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLeagueHomeStandings(request):
    return Response('success livescore')

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLeagueAwayStandings(request):
    return Response('success livescore')

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLeagueFixtures(request):
    return Response('success livescore')

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLeagueResults(request):
    return Response('success livescore')

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLatestNews(request):
    return Response('success livescore')

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def searchMatch(request):
    return Response('success livescore')
