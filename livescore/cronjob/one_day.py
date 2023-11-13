from datetime import datetime, timedelta, timezone
import sys
import os
import django
import requests
from django.conf import settings
from unidecode import unidecode

sys.path.append('/home/footywvb/mobileapp/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "livescorecz.settings")
django.setup()
from livescorecz.settings import APIKEY
from livescore.models import *


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


def getLeagueFixtures(league):
    api_endpoint = f'https://api.roniib.com/r-api-end/getLeagueUpcomingMatches/?league_id={league}'
    bearer_token = APIKEY
    headers = {
        'Authorization': f'Token {bearer_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            val = response.json()
            r = val.get('result', None)
            if r:
                for res in r:
                    matchid = fixIntTuple(res.get('matchid', None))
                    if not matchid:
                        continue
                    alm = AllMatches.objects.filter(matchid=matchid).first()
                    if alm:
                        continue
                    ht_ = fixStrTuple(res.get('homeTeamName', None))
                    at_ = fixStrTuple(res.get('awayTeamName', None))
                    statusCode = fixIntTuple(res.get('statusCode', None))
                    status = fixStrTuple(res.get('status', None))
                    startTime = fixIntTuple(res.get('startTime', None))

                    alm = AllMatches(
                        hometeam=ht_,
                        awayteam=at_,
                        homescore='-',
                        awayscore='-',
                        status=status,
                        matchid=matchid,
                        statusCode=statusCode,
                        leagueId=league,
                        startTime=startTime
                    )
                    alm.save()
    except requests.exceptions.RequestException as e:
        pass


def getLeagueResults(league):
    api_endpoint = f'https://api.roniib.com/r-api-end/getLeaguePastMatches/?league_id={league}'
    bearer_token = APIKEY
    headers = {
        'Authorization': f'Token {bearer_token}',
        'Content-Type': 'application/json'
    }
    # try:
    response = requests.get(api_endpoint, headers=headers)
    if response.status_code == 200:
        val = response.json()
        r = val.get('result', None)
        if r:
            for res in r:
                matchid = fixIntTuple(res.get('matchid', None))
                if not matchid:
                    continue
                alm = AllMatches.objects.filter(matchid=matchid).first()
                if alm:
                    alm.leagueId=league
                    alm.save()
                    continue
                ht_ = fixStrTuple(res.get('homeTeamName', None))
                at_ = fixStrTuple(res.get('awayTeamName', None))
                statusCode = fixIntTuple(res.get('statusCode', None))
                status = fixStrTuple(res.get('status', None))
                startTime = fixIntTuple(res.get('startTime', None))
                hs = fixIntTuple(res.get('score', {}).get('total', {}).get('home', None))
                ats = fixIntTuple(res.get('score', {}).get('total', {}).get('away', None))

                alm = AllMatches(
                    hometeam=ht_,
                    awayteam=at_,
                    homescore=hs,
                    awayscore=ats,
                    status=status,
                    statusCode=statusCode,
                    leagueId=league,
                    startTime=startTime
                )
                alm.save()
    #
    # except requests.exceptions.RequestException as e:
    #     pass


def leagueInfo(league):
    li = LeagueInfo.objects.filter(league_id=league).first()
    if li:
        return
    api_endpoint = f'https://api.roniib.com/r-api-end/getLeagueInfo/?league_id={league}'
    bearer_token = APIKEY
    headers = {
        'Authorization': f'Token {bearer_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            e_r = response.json()
            res = e_r.get('result', None)
            if res:
                leagueId = fixIntTuple(res.get('leagueId',None))
                leagueName = fixStrTuple(res.get('leagueName', None))
                leagueImage = fixStrTuple(res.get('leagueImage', None))
                leagueWeek = fixIntTuple(res.get('leagueWeek', None))
                countryName = fixStrTuple(res.get('countryName', None))
                seasonID = fixIntTuple(res.get('seasonID', None))
                seasonName = fixStrTuple(res.get('seasonName', None))

                li = LeagueInfo(
                    league_id=leagueId,
                    league_name=leagueName,
                    league_image=leagueImage,
                    current_league_week=leagueWeek,
                    country_name=countryName,
                    season_name=seasonName,
                    season_id=seasonID,
                )
                li.save()


    except requests.exceptions.RequestException as e:
        pass


def getLeagueHomeStandings(league):
    api_endpoint = f'https://api.roniib.com/r-api-end/getLeagueHomeStandings/?league_id={league}'
    bearer_token = APIKEY
    headers = {
        'Authorization': f'Token {bearer_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            e_r = response.json()
            res_ = e_r.get('result', None)
            if res_:
                ls = LeagueHomeStandings.objects.filter(league=league)
                if ls:
                    ls.delete()

                for res in res_:
                    rank = fixIntTuple(res.get('rank', 0))
                    teamName = fixStrTuple(res.get('teamName', 0))
                    matchesPlayed = fixIntTuple(res.get('matchesPlayed', 0))
                    wins = fixIntTuple(res.get('wins', 0))
                    draws = fixIntTuple(res.get('draws', 0))
                    losses = fixIntTuple(res.get('losses', 0))
                    goalFor = fixIntTuple(res.get('goalFor', 0))
                    goalAgainst = fixIntTuple(res.get('goalAgainst', 0))
                    points = fixIntTuple(res.get('points', 0))

                    lhs = LeagueHomeStandings(
                        league=league,
                        team=teamName,
                        rank=rank,
                        mp=matchesPlayed,
                        gf=goalFor,
                        ga=goalAgainst,
                        wins=wins,
                        draws=draws,
                        losses=losses,
                        points=points,
                    )
                    lhs.save()
    except requests.exceptions.RequestException as e:
        pass


def getLeagueAwayStandings(league):
    api_endpoint = f'https://api.roniib.com/r-api-end/getLeagueAwayStandings/?league_id={league}'
    bearer_token = APIKEY
    headers = {
        'Authorization': f'Token {bearer_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            e_r = response.json()
            res_ = e_r.get('result', None)
            if res_:
                ls = LeagueAwayStandings.objects.filter(league=league)
                if ls:
                    ls.delete()

                for res in res_:
                    rank = fixIntTuple(res.get('rank', 0))
                    teamName = fixStrTuple(res.get('teamName', 0))
                    matchesPlayed = fixIntTuple(res.get('matchesPlayed', 0))
                    wins = fixIntTuple(res.get('wins', 0))
                    draws = fixIntTuple(res.get('draws', 0))
                    losses = fixIntTuple(res.get('losses', 0))
                    goalFor = fixIntTuple(res.get('goalFor', 0))
                    goalAgainst = fixIntTuple(res.get('goalAgainst', 0))
                    points = fixIntTuple(res.get('points', 0))

                    lhs = LeagueAwayStandings(
                        league=league,
                        team=teamName,
                        rank=rank,
                        mp=matchesPlayed,
                        gf=goalFor,
                        ga=goalAgainst,
                        wins=wins,
                        draws=draws,
                        losses=losses,
                        points=points,
                    )
                    lhs.save()


    except requests.exceptions.RequestException as e:
        pass


def getLeagueOverallStandings(league):
    api_endpoint = f'https://api.roniib.com/r-api-end/getLeagueOverallStandings/?league_id={league}'
    bearer_token = APIKEY
    headers = {
        'Authorization': f'Token {bearer_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            e_r = response.json()
            res_ = e_r.get('result', None)
            if res_:
                ls = LeagueOverallStandings.objects.filter(league=league)
                if ls:
                    ls.delete()

                for res in res_:
                    rank = fixIntTuple(res.get('rank', 0))
                    teamName = fixStrTuple(res.get('teamName', 0))
                    matchesPlayed = fixIntTuple(res.get('matchesPlayed', 0))
                    wins = fixIntTuple(res.get('wins', 0))
                    draws = fixIntTuple(res.get('draws', 0))
                    losses = fixIntTuple(res.get('losses', 0))
                    goalFor = fixIntTuple(res.get('goalFor', 0))
                    goalAgainst = fixIntTuple(res.get('goalAgainst', 0))
                    points = fixIntTuple(res.get('points', 0))

                    lhs = LeagueOverallStandings(
                        league=league,
                        team=teamName,
                        rank=rank,
                        mp=matchesPlayed,
                        gf=goalFor,
                        ga=goalAgainst,
                        wins=wins,
                        draws=draws,
                        losses=losses,
                        points=points,
                    )
                    lhs.save()


    except requests.exceptions.RequestException as e:
        pass


def getTomorrowsFixtures():
    tmr_ = datetime.now(timezone.utc) + timedelta(days=1)
    day_ = tmr_.day
    month_ = tmr_.month
    year_ = tmr_.year
    api_endpoint = f'https://api.roniib.com/r-api-end/getMatchesByDate/?day={day_}&month={month_}&year={year_}'
    bearer_token = APIKEY
    headers = {
        'Authorization': f'Token {bearer_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            val = response.json()
            saveMatches(val)
    except requests.exceptions.RequestException as e:
        pass
    return None


def getYesterdaysMatches():
    tmr_ = datetime.now(timezone.utc) - timedelta(days=1)
    day_ = tmr_.day
    month_ = tmr_.month
    year_ = tmr_.year
    api_endpoint = f'https://api.roniib.com/r-api-end/getMatchesByDate/?day={day_}&month={month_}&year={year_}'
    bearer_token = APIKEY
    headers = {
        'Authorization': f'Token {bearer_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            val = response.json()
            saveMatches(val)
    except requests.exceptions.RequestException as e:
        pass
    return None


def saveMatches(res):
    try:
        res = res.get('result', None)
        if res:
            for m in res:
                matchid = m.get('matchid', None)
                homeTeamName = m.get('homeTeamName', None)
                awayTeamName = m.get('awayTeamName', None)
                status = m.get('status', None)
                statusCode = m.get('statusCode', None)
                startTime = m.get('startTime', None)

                hs = m.get('score', {}).get('total', {}).get('home', None)
                ats = m.get('score', {}).get('total', {}).get('away', None)

                amm = AllMatches.objects.filter(matchid=matchid).first()
                if amm:
                    amm.hometeam = unidecode(homeTeamName)
                    amm.awayteam = unidecode(awayTeamName)
                    amm.homescore = fixIntTuple(hs)
                    amm.awayscore = fixIntTuple(ats)
                    amm.status = fixStrTuple(status)
                    amm.matchid = fixIntTuple(matchid)
                    amm.statusCode = fixIntTuple(statusCode)
                    amm.startTime = fixIntTuple(startTime)
                    amm.save()
                else:
                    am = AllMatches(
                        hometeam=unidecode(homeTeamName),
                        awayteam=unidecode(awayTeamName),
                        homescore=fixIntTuple(hs),
                        awayscore=fixIntTuple(ats),
                        status=fixStrTuple(status),
                        matchid=fixIntTuple(matchid),
                        statusCode=fixIntTuple(statusCode),
                        startTime=fixIntTuple(startTime), )
                    am.save()
                amm = AllMatches.objects.filter(matchid=matchid).first()
                if fixIntTuple(statusCode) == 6 or fixIntTuple(statusCode) == 7:
                    ms = getMatchStats(matchid)
                    if ms:
                        mif = MatchInfo.objects.filter(match=amm).first()
                        if mif:
                            mif.cornerkicksH = fixIntTuple(ms.get('corners', {}).get('home', None))
                            mif.cornerkicksA = fixIntTuple(ms.get('corners', {}).get('away', None))
                            mif.possesionH = fixIntTuple(ms.get('possession', {}).get('home', None))
                            mif.possesionA = fixIntTuple(ms.get('possession', {}).get('away', None))
                            mif.yellowCardsH = fixIntTuple(
                                ms.get('bookings', {}).get('yellowCards', {}).get('home', None))
                            mif.yellowCardsA = fixIntTuple(
                                ms.get('bookings', {}).get('yellowCards', {}).get('away', None))
                            mif.gkSavesH = fixIntTuple(
                                ms.get('defence', {}).get('goalkeeperSaves', {}).get('home', None))
                            mif.gkSavesA = fixIntTuple(
                                ms.get('defence', {}).get('goalkeeperSaves', {}).get('away', None))
                            mif.shotsH = fixIntTuple(ms.get('attack', {}).get('shots', {}).get('home', None))
                            mif.shotsA = fixIntTuple(ms.get('attack', {}).get('shots', {}).get('away', None))
                            mif.save()
                        else:
                            mif = MatchInfo(
                                match=amm,
                                cornerkicksH=fixIntTuple(ms.get('corners', {}).get('home', None)),
                                cornerkicksA=fixIntTuple(ms.get('corners', {}).get('away', None)),
                                possesionH=fixIntTuple(ms.get('possession', {}).get('home', None)),
                                possesionA=fixIntTuple(ms.get('possession', {}).get('away', None)),
                                yellowCardsH=fixIntTuple(
                                    ms.get('bookings', {}).get('yellowCards', {}).get('home', None)),
                                yellowCardsA=fixIntTuple(
                                    ms.get('bookings', {}).get('yellowCards', {}).get('away', None)),
                                gkSavesH=fixIntTuple(
                                    ms.get('defence', {}).get('goalkeeperSaves', {}).get('home', None)),
                                gkSavesA=fixIntTuple(
                                    ms.get('defence', {}).get('goalkeeperSaves', {}).get('away', None)),
                                shotsH=fixIntTuple(ms.get('attack', {}).get('shots', {}).get('home', None)),
                                shotsA=fixIntTuple(ms.get('attack', {}).get('shots', {}).get('away', None)),
                            )
                            mif.save()

                    lgid = amm.leagueId
                    if lgid is None:
                        isp = getPrematchInfo(amm.matchid)
                        if isp:
                            leagueName = fixStrTuple(isp.get('leagueInfo', {}).get('name', None))
                            leagueId = fixIntTuple(isp.get('leagueInfo', {}).get('id', None))
                            country = fixStrTuple(isp.get('leagueInfo', {}).get('country', None))

                            h_formation = fixStrTuple(isp.get('lineUp', {}).get('homeFormation', None))
                            a_formation = fixStrTuple(isp.get('lineUp', {}).get('awayFormation', None))
                            isConf = isp.get('lineUp', {}).get('isConfirmed', False)

                            amm.leagueId = leagueId
                            amm.leagueName = leagueName
                            amm.countryName = country
                            amm.homeformation = h_formation
                            amm.awayFormation = a_formation
                            amm.lineUpConfirmed = isConf
                            amm.save()
                    getMatchLineup(matchid)
    except:
        pass


def getMatchStats(matchid):
    api_endpoint = f'https://api.roniib.com/r-api-end/getMatchStats/match_id={matchid}'
    bearer_token = APIKEY
    headers = {
        'Authorization': f'Token {bearer_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            val = response.json()
            res = val.get('result', None)
            return res

    except requests.exceptions.RequestException as e:
        pass
    return None


def getMatchLineup(matchid):
    mi = AllMatches.objects.filter(matchid=matchid).first()
    if not mi:
        return
    ml = MatchLineUp.objects.filter(match=mi).first()
    if ml:
        return
    api_endpoint = f'https://api.roniib.com/r-api-end/getMatchLineup/?match_id={matchid}'
    bearer_token = APIKEY
    headers = {
        'Authorization': f'Token {bearer_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            val = response.json()

            res = val.get('result', None)
            if res:
                isConf = res.get('isConfirmed', False)
                hFormation = fixStrTuple(res.get('home', {}).get('formation', None))
                aFormation = fixStrTuple(res.get('home', {}).get('formation', None))

                mi.isConf = isConf
                mi.hFormation = hFormation
                mi.aFormation = aFormation
                mi.save()

                hplyrs = res.get('home', {}).get('players', None)
                if hplyrs:
                    for r in hplyrs:
                        playerJerseyNo = fixIntTuple(r.player_shirt_no)
                        playerName = fixStrTuple(r.player_name)
                        playerPosition = fixIntTuple(r.player_position)

                        ml = MatchLineUp(
                            match=mi,
                            player=playerName,
                            number=playerJerseyNo,
                            position=playerPosition,
                            isHomePlayer=True
                        )
                        ml.save()

                hplyrs = res.get('away', {}).get('players', None)
                if hplyrs:
                    for r in hplyrs:
                        playerJerseyNo = fixIntTuple(r.player_shirt_no)
                        playerName = fixStrTuple(r.player_name)
                        playerPosition = fixIntTuple(r.player_position)

                        ml = MatchLineUp(
                            match=mi,
                            player=playerName,
                            number=playerJerseyNo,
                            position=playerPosition,
                            isHomePlayer=False
                        )
                        ml.save()
    except:
        return


def getPrematchInfo(matchid):
    api_endpoint = f'https://api.roniib.com/r-api-end/getPreMatchInfo/match_id={matchid}'
    bearer_token = APIKEY
    headers = {
        'Authorization': f'Token {bearer_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            val = response.json()
            res = val.get('result', None)
            return res

    except requests.exceptions.RequestException as e:
        pass
    return None


def getLeaguesStats(league):
    getLeagueFixtures(league)
    getLeagueResults(league)
    getLeagueHomeStandings(league)
    getLeagueAwayStandings(league)
    getLeagueOverallStandings(league)
    leagueInfo(league)
    getYesterdaysMatches()
    getTomorrowsFixtures()


if __name__ == "__main__":
    available_leagues = [17, 34, 35, 23, 8]
    for r in available_leagues:
        getLeaguesStats(r)
