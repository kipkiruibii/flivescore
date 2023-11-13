from unidecode import unidecode
from datetime import datetime, timedelta, timezone
import sys
import os
import re
import django
import requests
from django.conf import settings

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


def getTodaysMatches():
    tmr_ = datetime.now(timezone.utc)
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
                            mif.yellowCardsH = fixIntTuple(ms.get('bookings', {}).get('yellowCards', {}).get('home', None))
                            mif.yellowCardsA = fixIntTuple(ms.get('bookings', {}).get('yellowCards', {}).get('away', None))
                            mif.gkSavesH = fixIntTuple(ms.get('defence', {}).get('goalkeeperSaves', {}).get('home', None))
                            mif.gkSavesA = fixIntTuple(ms.get('defence', {}).get('goalkeeperSaves', {}).get('away', None))
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
                                yellowCardsH=fixIntTuple(ms.get('bookings', {}).get('yellowCards', {}).get('home', None)),
                                yellowCardsA=fixIntTuple(ms.get('bookings', {}).get('yellowCards', {}).get('away', None)),
                                gkSavesH=fixIntTuple(ms.get('defence', {}).get('goalkeeperSaves', {}).get('home', None)),
                                gkSavesA=fixIntTuple(ms.get('defence', {}).get('goalkeeperSaves', {}).get('away', None)),
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


def getNews():
    api_endpoint = f'https://api.roniib.com/r-api-end/getSportsNews'
    bearer_token = APIKEY
    headers = {
        'Authorization': f'Token {bearer_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            val = response.json()
            rt = val.get('result', None)
            if rt:
                for r in rt:
                    title = r.get('title', '-')
                    source = r.get('source', '-')
                    description = r.get('description', '-')
                    datePublished = r.get('date_published', '-')
                    image = r.get('image', '-')
                    link = r.get('link', '-')

                    na = NewsArticles.objects.filter(title=title).first()
                    if not na:
                        na = NewsArticles(
                            title=title,
                            description=description,
                            author=source,
                            datePublished=datePublished,
                            link=link,
                            image_url=image)
                        na.save()
                    n = NewsArticles.objects.all()
                    if len(n) > 30:
                        n.first().delete()

    except requests.exceptions.RequestException as e:
        pass
    return None


def fixMatches():
    for m in AllMatches.objects.all():
        if fixIntTuple(m.statusCode) is None:
            if fixStrTuple(m.status.lower())=='not started' :
                m.statusCode=0
                m.save()
            if fixStrTuple(m.status.lower())=='ended' :
                m.statusCode=0
                m.save()
        if fixIntTuple(m.matchid) is None:
            m.delete()


if __name__ == "__main__":
    getTodaysMatches()
    getNews()
    fixMatches()

'''
    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
         return 301 https://$host$request_uri;
        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }


   server {
       listen       443 ssl http2 default_server;
       listen       [::]:443 ssl http2 default;
        server_name  app.footballcr7.net;
        root         /usr/share/nginx/html;

       ssl_certificate "/etc/pki/nginx/server.crt";
       ssl_certificate_key "/etc/pki/nginx/server.key";
       ssl_session_cache shared:SSL:1m;
       ssl_session_timeout  10m;
       ssl_ciphers PROFILE=SYSTEM;
       ssl_prefer_server_ciphers on;

       # Load configuration files for the default server block.
       include /etc/nginx/default.d/*.conf;

       location / {

       }

       error_page 404 /404.html;
           location = /40x.html {
       }

       error_page 500 502 503 504 /50x.html;
           location = /50x.html {
       }
   }

'''