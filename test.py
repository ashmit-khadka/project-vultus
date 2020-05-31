from imdb import findMedia
import requests
from requests.exceptions import HTTPError
from datetime import timedelta, datetime
import isodate
from imdb import findMedia


def parseURL(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except Exception as err:
        print(f"Generic error: {err}")




def parseContent(videoId):
 
    url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={0}&key=AIzaSyAGOmlQHZQibXpeoTRl3Sa7DBYWFBTGCAQ".format(videoId)
    print(url)
    return parseURL(url)

def getContentObj(videoId, mediaType):
    responseIMDB = findMedia('Meri Bsdfdsfdfssdfdsfassai')
    response = {}
    if responseIMDB is not None:
        response = {
            "name" : responseIMDB['name'],
            "img" : responseIMDB['img'],
            "type" : mediaType
        }
        return response
    else:
        responseYT = parseContent(videoId) #todo if not none
        response = {
            "name" : responseYT['items'][0]['snippet']['title'],
            "img" : responseYT['items'][0]['snippet']['thumbnails']['high']['url'],
            "type" : mediaType
        }
        return response
    #print(responceIMDB)


print(getContentObj('WHRR6QGSALI', 'episode'))