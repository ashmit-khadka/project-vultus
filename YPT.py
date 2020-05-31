import requests
from requests.exceptions import HTTPError
from datetime import timedelta, datetime
import isodate
from imdb import findMedia

def getInstalments(title):
    def getInstalment(title, period):
        try:
            remain = title[title.upper().index(period)+len(period):]
            start = None
            end = None
            for idx, char in enumerate(remain):
                if char.isnumeric() and start is None:
                    start = idx
                if char.isspace() and start is not None and end is None:
                    end = idx                
            value = int(remain[start:end])
            return value
        except:
            return None

    season = None
    episode = None

    if 'EPISODE' not in title.upper():
        return None

    episode = getInstalment(title, "EPISODE")

    if 'SEASON' in title.upper():
        season = getInstalment(title, "SEASON")
    else:
        season = 0
    

    return season, episode

def getMediaName(title):  
    delimiterList = ['|', '-', 'I']
    for idx, char in enumerate(title):
        if char in delimiterList:
            name = title[:idx].strip()
            if 'MOVIE' in name.upper():
                return getMediaName(title[idx+1:])
            return title[:idx].strip()
    return None

def parseURL(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except Exception as err:
        print(f"Generic error: {err}")

def raiseFlag(videoId):
    return None


def getContentObj(videoSnippit, name, mediaType):

    responseIMDB = findMedia(name)
    response = {}
    if responseIMDB is not None:
        response = {
            "name" : responseIMDB['name'],
            "img" : responseIMDB['img'],
            "type" : mediaType
        }
        return response
    else:
        response = {
            "name" : name,
            "img" : videoSnippit['items'][0]['snippet']['thumbnails']['high']['url'],
            "type" : mediaType
        }
    return response

def getMediaType(videoId, title):

    url = "https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={0}&key={1}".format(videoId, getAPIKey())
    data = parseURL(url)

    duration = isodate.parse_duration(data['items'][0]['contentDetails']['duration']).seconds
    if 'MOVIE' in title.upper() and duration > 60*60:
        return 'MOVIE'
    if 'EPISODE' in title.upper() and duration > 60*13:
        return 'EPISODE'
    return None

def getAPIKey(): return "AIzaSyAGOmlQHZQibXpeoTRl3Sa7DBYWFBTGCAQ"

    
#print(getInstalments("The Voice of Nepal Season 2 - 2019 - Episode 30 (LIVE Performance)"))