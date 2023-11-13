# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from unidecode import unidecode

from .models import *
from datetime import datetime, timezone
import pytz


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def homeintro(request):
    return Response('success livescore')


def fixIntTuple(value):
    if value:
        tuple_string = str(value)
        cleaned_string = tuple_string.strip('(,)')
        if cleaned_string == 'None':
            return None
        else:
            try:
                sc = int(cleaned_string)
                return sc
            except:
                return None
    return None


def fixStrTuple(value):
    if value:
        tuple_string = str(value)
        cleaned_string = tuple_string.strip('(,)')
        if cleaned_string == 'None':
            return None
        else:
            try:
                sc = str(cleaned_string.strip('"'))
                return sc
            except:
                return None
    else:
        return None


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLivescore(request):
    mtc = AllMatches.objects.filter(Q(statusCode=6) | Q(statusCode=7))
    res = []
    for m in mtc:
        tsp = fixIntTuple(m.startTime)
        if tsp is not None:
            if fixStrTuple(m.hometeam) is None or fixStrTuple(m.awayteam) is None or fixIntTuple(m.statusCode) is None:
                continue

            telps = '-'
            tmet = datetime.fromtimestamp(fixIntTuple(m.startTime))
            if fixIntTuple(m.statusCode) == 6 or fixIntTuple(m.statusCode) == 7:
                try:
                    timediff = datetime.now()
                    ltme = datetime.fromtimestamp(fixIntTuple(m.startTime))
                    telps = (timediff - ltme).total_seconds() / 60
                except:
                    pass
            if fixIntTuple(m.startTime) is not None:
                ltme = datetime.fromtimestamp(fixIntTuple(m.startTime))
                tmet = ltme.strftime('%H:%M')
            val = {
                'homeTeam': fixStrTuple(unidecode(m.hometeam)),
                'awayTeam': fixStrTuple(unidecode(m.awayteam)),
                'matchId': fixStrTuple(m.matchid),
                'homeScore': fixStrTuple(m.homescore),
                'awayScore': fixStrTuple(m.awayscore),
                'status': fixStrTuple(m.status),
                'statusCode': fixIntTuple(m.statusCode),
                'leagueName': fixStrTuple(m.leagueName),
                'leagueId': fixStrTuple(m.leagueId),
                'startTime': tmet,
                'timeElapsed': fixStrTuple(telps),
            }
            res.append(val)
        vall = {
            'result': res
        }
        return Response(vall)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getTodaysMatches(request):
    mtc = AllMatches.objects.all()
    res = []
    timez_ = request.GET.get('timezone', 'utc')
    for m in mtc:
        startTime = m.startTime
        try:
            tz = pytz.timezone(timez_)
            tme = datetime.fromtimestamp(fixIntTuple(startTime))
            tmet = datetime.now(tz)
            dy = tme.day
            if dy == tmet.day:
                if fixStrTuple(m.hometeam) is None or fixStrTuple(m.awayteam) is None or fixIntTuple(
                        m.statusCode) is None:
                    continue
                homesc = fixIntTuple(m.homescore)
                awaysc = fixIntTuple(m.awayscore)
                if fixIntTuple(m.homescore) is None or fixIntTuple(m.awayscore) is None:
                    homesc = '-'
                    awaysc = '-'

                val = {
                    'homeTeam': unidecode(m.hometeam),
                    'awayTeam': unidecode(m.awayteam),
                    'matchId': m.matchid,
                    'homeScore': homesc,
                    'awayScore': awaysc,
                    'status': m.status,
                    'statusCode': fixIntTuple(m.statusCode),
                    'leagueName': m.leagueName,
                    'leagueId': m.leagueId,
                    'startTime': tme.strftime('%H:%M'),
                }
                res.append(val)
        except:
            pass
    vall = {
        'result': res
    }
    return Response(vall)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getMatchesByDate(request):
    mtc = AllMatches.objects.all()
    res = []
    day = request.GET.get('day', '')
    month = request.GET.get('month', '')
    year = request.GET.get('year', '')
    for m in mtc:
        startTime = m.startTime
        # try:
        if fixStrTuple(m.hometeam) is None or fixStrTuple(m.awayteam) is None or fixIntTuple(
                m.statusCode) is None or fixIntTuple(startTime) is None:
            continue
        tmetl = '-'
        telps = '-'
        tmet = datetime.fromtimestamp(fixIntTuple(startTime))
        if tmet.day == int(day) and tmet.month == int(month) and tmet.year == int(year):
            telps = '-'
            if fixIntTuple(m.statusCode) == 6 or fixIntTuple(m.statusCode) == 7:
                try:
                    timediff = datetime.now()
                    ltme = datetime.fromtimestamp(fixIntTuple(m.startTime))
                    telps = (timediff - ltme).total_seconds() / 60
                except:
                    pass

        if fixIntTuple(m.startTime) is not None:
            ltme = datetime.fromtimestamp(fixIntTuple(m.startTime))
            tmetl = ltme.strftime('%H:%M')
        homesc = fixIntTuple(m.homescore)
        awaysc = fixIntTuple(m.awayscore)
        if fixIntTuple(m.homescore) is None or fixIntTuple(m.awayscore) is None:
            homesc = '-'
            awaysc = '-'

        val = {
            'homeTeam': unidecode(m.hometeam),
            'awayTeam': unidecode(m.awayteam),
            'matchId': m.matchid,
            'homeScore': homesc,
            'awayScore': awaysc,
            'status': m.status,
            'statusCode': fixIntTuple(m.statusCode),
            'leagueName': m.leagueName,
            'leagueId': m.leagueId,
            'startTime': tmetl,
            'timeElapsed': telps,
        }

        res.append(val)
        # except:
        #     pass
    vall = {
        'result': res
    }
    return Response(vall)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getMatchInfo(request):
    vale = []
    mt_id = request.GET.get('matchId', None)
    if mt_id:
        try:
            mtc = AllMatches.objects.filter(matchid=mt_id).first()
            if mtc:
                if fixStrTuple(mtc.hometeam) is None or fixStrTuple(mtc.awayteam) is None or fixIntTuple(
                        mtc.statusCode) is None or fixIntTuple(mtc.startTime) is None:
                    val = {
                        'result': vale
                    }
                    return Response(val)
                tmet = datetime.fromtimestamp(fixIntTuple(mtc.startTime))
                telps = '-'
                if fixIntTuple(mtc.statusCode) == 6 or fixIntTuple(mtc.statusCode) == 7:
                    try:
                        timediff = datetime.now()
                        ltme = datetime.fromtimestamp(fixIntTuple(mtc.startTime))
                        telps = (timediff - ltme).total_seconds() / 60
                    except:
                        pass

                m = MatchInfo.objects.filter(match=mtc).first()
                if m:
                    corners_h = m.cornerkicksH
                    corners_a = m.cornerkicksA
                    possesion_h = (m.possesionH / 100)
                    possesion_a = m.possesionA / 100

                    yellow_h = m.yellowCardsH
                    yellow_a = m.yellowCardsA
                    saves_h = m.gkSavesH
                    saves_a = m.gkSavesA

                    t_saves = saves_a + saves_h
                    saves_a = (saves_a / t_saves) * 100
                    saves_h = (saves_h / t_saves) * 100

                    shots_h = m.shotsH
                    shots_a = m.shotsA
                else:
                    corners_h = 0.0
                    corners_a = 0.0
                    possesion_h = 0.0
                    possesion_a = 0.0
                    yellow_h = 0.0
                    yellow_a = 0.0
                    saves_h = 0.0
                    saves_a = 0.0
                    shots_h = 0.0
                    shots_a = 0.0

                val = {
                    'homeTeam': unidecode(mtc.hometeam) if mtc.hometeam is not None else '-',
                    'awayTeam': unidecode(mtc.awayteam) if mtc.awayteam is not None else '-',
                    'homeScore': mtc.homescore if mtc.homescore is not None else '-',
                    'awaycore': mtc.awayscore if mtc.awayscore is not None else '-',
                    'venue': mtc.venue if mtc.venue is not None else '-',
                    'countryName': mtc.countryName if mtc.countryName is not None else '-',
                    'leagueName': mtc.leagueName if mtc.leagueName is not None else '-',
                    'leagueId': mtc.leagueId if mtc.leagueId is not None else '-',
                    'status': mtc.status if mtc.status is not None else '-',
                    'statusCode': fixIntTuple(mtc.statusCode) if fixIntTuple(mtc.statusCode) is not None else 0,
                    'startTime': tmet.strftime('%H:%M'),
                    'hFormation': mtc.hFormation if mtc.hFormation is not None else '-',
                    'aFormation': mtc.aFormation if mtc.aFormation is not None else '-',
                    'timeElapsed': telps,

                    'cornerkicksH': corners_h,
                    'cornerkicksA': corners_a,
                    'possesionH': possesion_h,
                    'possesionA': possesion_a,
                    'yellowCardsH': yellow_h,
                    'yellowCardsA': yellow_a,
                    'gkSavesH': saves_h,
                    'gkSavesA': saves_a,
                    'shotsH': shots_h,
                    'shotsA': shots_a,

                }
                vale.append(val)
        except:
            pass
    val = {
        'result': vale
    }
    return Response(val)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getMatchLineUp(request):
    home = []
    away = []
    hmf = ''
    amf = ''
    isc = False
    mt_id = request.GET.get('matchId', None)
    if mt_id:
        try:
            mtc = AllMatches.objects.filter(matchid=mt_id).first()
            if mtc:
                hmf = mtc.hFormation
                amf = mtc.aFormation
                isc = mtc.isConf

                mtc = MatchLineUp.objects.filter(match=mtc)
                for m in mtc:
                    val = {
                        'player': m.player,
                        'number': m.number,
                        'position': m.position,
                    }
                    if m.isHomePlayer:
                        home.append(val)
                    else:
                        away.append(val)
        except:
            pass
    val = {
        'homeFormation': hmf,
        'awayFormation': amf,
        'isConfirmed': isc,
        'home': home,
        'away': away,
    }
    return Response(val)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLeagueOverallStandings(request):
    teams = []
    lg_id = request.GET.get('leagueId', None)
    if lg_id:
        try:
            mtc = LeagueOverallStandings.objects.filter(league=lg_id)
            if mtc:
                for m in mtc:
                    val = {
                        'team': unidecode(m.team),
                        'rank': fixIntTuple(m.rank) if fixIntTuple(m.rank) is not None else 0,
                        'points': fixIntTuple(m.points) if fixIntTuple(m.points) is not None else 0,
                        'mp': fixIntTuple(m.mp) if fixIntTuple(m.mp) is not None else 0,
                        'gf': fixIntTuple(m.gf) if fixIntTuple(m.gf) is not None else 0,
                        'ga': fixIntTuple(m.ga) if fixIntTuple(m.ga) is not None else 0,
                        'wins': fixIntTuple(m.wins) if fixIntTuple(m.wins) is not None else 0,
                        'draws': fixIntTuple(m.draws) if fixIntTuple(m.draws) is not None else 0,
                        'losses': fixIntTuple(m.losses) if fixIntTuple(m.losses) is not None else 0,
                    }
                    teams.append(val)
        except:
            pass
    val = {
        'table': teams[::-1],
    }
    return Response(val)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLeagueHomeStandings(request):
    teams = []
    lg_id = request.GET.get('leagueId', None)
    if lg_id:
        try:
            mtc = LeagueOverallStandings.objects.filter(league=lg_id)
            if mtc:
                for m in mtc:
                    val = {
                        'team': unidecode(m.team),
                        'rank': fixIntTuple(m.rank) if fixIntTuple(m.rank) is not None else 0,
                        'points': fixIntTuple(m.points) if fixIntTuple(m.points) is not None else 0,
                        'mp': fixIntTuple(m.mp) if fixIntTuple(m.mp) is not None else 0,
                        'gf': fixIntTuple(m.gf) if fixIntTuple(m.gf) is not None else 0,
                        'ga': fixIntTuple(m.ga) if fixIntTuple(m.ga) is not None else 0,
                        'wins': fixIntTuple(m.wins) if fixIntTuple(m.wins) is not None else 0,
                        'draws': fixIntTuple(m.draws) if fixIntTuple(m.draws) is not None else 0,
                        'losses': fixIntTuple(m.losses) if fixIntTuple(m.losses) is not None else 0,
                    }
                    teams.append(val)
        except:
            pass
    val = {
        'table': teams[::-1],
    }
    return Response(val)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLeagueAwayStandings(request):
    teams = []
    lg_id = request.GET.get('leagueId', None)
    if lg_id:
        try:
            mtc = LeagueAwayStandings.objects.filter(league=lg_id)
            if mtc:
                for m in mtc:
                    val = {
                        'team': unidecode(m.team),
                        'rank': fixIntTuple(m.rank) if fixIntTuple(m.rank) is not None else 0,
                        'points': fixIntTuple(m.points) if fixIntTuple(m.points) is not None else 0,
                        'mp': fixIntTuple(m.mp) if fixIntTuple(m.mp) is not None else 0,
                        'gf': fixIntTuple(m.gf) if fixIntTuple(m.gf) is not None else 0,
                        'ga': fixIntTuple(m.ga) if fixIntTuple(m.ga) is not None else 0,
                        'wins': fixIntTuple(m.wins) if fixIntTuple(m.wins) is not None else 0,
                        'draws': fixIntTuple(m.draws) if fixIntTuple(m.draws) is not None else 0,
                        'losses': fixIntTuple(m.losses) if fixIntTuple(m.losses) is not None else 0,
                    }
                    teams.append(val)
        except:
            pass
    val = {
        'table': teams[::-1],
    }
    return Response(val)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLeagueFixtures(request):
    leagueid = request.GET.get('leagueId', None)
    res = []
    if leagueid:
        mtc = AllMatches.objects.filter(Q(leagueId=leagueid))
        for m in mtc:
            startTime = m.startTime
            if fixStrTuple(m.hometeam) is None or fixStrTuple(m.awayteam) is None or fixIntTuple(
                    m.statusCode) is None or fixIntTuple(startTime) is None:
                continue
            if fixIntTuple(m.statusCode) not in [0, 6, 7, 31]:
                continue
            tmetl = '-'
            telps = '-'
            if fixIntTuple(m.startTime) is not None:
                ltme = datetime.fromtimestamp(fixIntTuple(m.startTime))
                tmetl = ltme.strftime('%H:%M')
            homesc = fixIntTuple(m.homescore)
            awaysc = fixIntTuple(m.awayscore)
            if fixIntTuple(m.homescore) is None or fixIntTuple(m.awayscore) is None:
                homesc = '-'
                awaysc = '-'

            val = {
                'homeTeam': unidecode(m.hometeam),
                'awayTeam': unidecode(m.awayteam),
                'matchId': m.matchid,
                'homeScore': homesc,
                'awayScore': awaysc,
                'status': m.status,
                'statusCode': fixIntTuple(m.statusCode),
                'leagueName': m.leagueName,
                'leagueId': m.leagueId,
                'startTime': tmetl,
                'timeElapsed': telps,
            }

            res.append(val)

    vall = {
        'result': res
    }
    return Response(vall)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLeagueResults(request):
    leagueid = request.GET.get('leagueId', None)
    res = []
    if leagueid:
        mtc = AllMatches.objects.filter(Q(leagueId=leagueid))
        for m in mtc:
            startTime = m.startTime
            if fixStrTuple(m.hometeam) is None or fixStrTuple(m.awayteam) is None or fixIntTuple(
                    m.statusCode) is None or fixIntTuple(startTime) is None:
                continue
            if fixIntTuple(m.statusCode) not in [100, 60, 120, 70, 92, 110, 91]:
                continue

            tmetl = '-'
            telps = '-'
            if fixIntTuple(m.startTime) is not None:
                ltme = datetime.fromtimestamp(fixIntTuple(m.startTime))
                tmetl = ltme.strftime('%H:%M')
            homesc = fixIntTuple(m.homescore)
            awaysc = fixIntTuple(m.awayscore)
            if fixIntTuple(m.homescore) is None or fixIntTuple(m.awayscore) is None:
                homesc = '-'
                awaysc = '-'

            val = {
                'homeTeam': unidecode(m.hometeam),
                'awayTeam': unidecode(m.awayteam),
                'matchId': m.matchid,
                'homeScore': homesc,
                'awayScore': awaysc,
                'status': m.status,
                'statusCode': fixIntTuple(m.statusCode),
                'leagueName': m.leagueName,
                'leagueId': m.leagueId,
                'startTime': tmetl,
                'timeElapsed': telps,
            }

            res.append(val)
    vall = {
        'result': res
    }
    return Response(vall)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def getLatestNews(request):
    res = []
    mtc = NewsArticles.objects.all()
    for m in mtc:
        val = {
            'title': unidecode(m.title),
            'author': unidecode(m.author),
            'description': unidecode(m.description),
            'link': m.link,
            'datePublished': m.datePublished,
            'image_url': m.image_url,
        }
        res.append(val)
    vall = {
        'result': res
    }
    return Response(vall)


def matches_order(word, order):
    order_w = [i for i in order]
    for char in word:
        if char in order_w:
            n_index = order_w.index(char)
            order_w = order_w[n_index:]
        else:
            return False

    return True


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def searchMatch(request):
    team_h = request.GET.get('team', '')
    res = []
    if team_h:
        mtc = AllMatches.objects.all()
        team = team_h.lower()
        for m in mtc:
            if fixIntTuple(m.statusCode) is None:
                continue
            present = False
            if m.hometeam is None or m.awayteam is None:
                continue
            hteam = m.hometeam.lower()
            ateam = m.awayteam.lower()
            if matches_order(team, hteam):
                present = True
            elif matches_order(team, ateam):
                present = True

            if present:

                tmet = '-'
                telps = '-'
                if fixIntTuple(m.statusCode) == 6 or fixIntTuple(m.statusCode) == 7:
                    try:
                        timediff = datetime.now()
                        ltme = datetime.fromtimestamp(fixIntTuple(m.startTime))
                        telps = (timediff - ltme).total_seconds() / 60
                    except:
                        pass
                if fixIntTuple(m.startTime) is not None:
                    ltme = datetime.fromtimestamp(fixIntTuple(m.startTime))
                    tmet = ltme.strftime('%H:%M')

                val = {
                    'homeTeam': unidecode(m.hometeam),
                    'awayTeam': unidecode(m.awayteam),
                    'matchId': m.matchid,
                    'homeScore': m.homescore,
                    'awayScore': m.awayscore,
                    'status': m.status,
                    'statusCode': fixIntTuple(m.statusCode),
                    'leagueName': m.leagueName,
                    'leagueId': m.leagueId,
                    'startTime': tmet,
                    'timeElapsed': telps,
                }
                res.append(val)
    vall = {
        'result': res
    }
    return Response(vall)


