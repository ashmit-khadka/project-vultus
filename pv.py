import requests
from requests.exceptions import HTTPError
from datetime import timedelta, datetime
import isodate
from db import query
import dateutil.parser
from YPT import *

api_key = "AIzaSyAGOmlQHZQibXpeoTRl3Sa7DBYWFBTGCAQ"
channel_id = "UCxCoea3ulOukfXiYAm87ZIA"

def parseContent(videoId):

    #video snippit to get title -> determin the duration to see if movie to episode
    url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={0}&key={1}".format(videoId, getAPIKey())
    videoSnippet = parseURL(url)
    title = videoSnippet['items'][0]['snippet']['title']
    name = getMediaName(title)
    if name is None: return None

    mediaType = getMediaType(videoId, title)

    if mediaType == 'MOVIE':
        print(title, 'is movie')
        contentData = getContentObj(videoSnippet, name, 'M')
        query("INSERT INTO content VALUES('{0}','{1}','{2}','{3}')".format(contentData['name'],contentData['img'],contentData['type'],contentData['name'].replace(' ', '').lower()), "execute")

    elif mediaType == 'EPISODE':
        print(title, 'is episode')
        contentData = getContentObj(videoSnippet, name, 'E')
        instalment = getInstalments(title)
        print(instalment)
        if query("SELECT COUNT(*) FROM content WHERE name = '{0}'".format(name), 'fetchone')[0]:
            if not query("SELECT COUNT(*) FROM season WHERE id = '{0}'".format('_'.join([contentData['name'].replace(' ', ''),str(instalment[0])]).lower()), 'fetchone')[0]:
                query("INSERT INTO season VALUES('{0}','{1}','{2}')".format(contentData['name'],instalment[0],'_'.join([contentData['name'].replace(' ', ''),str(instalment[0])]).lower()), "execute")
            query("INSERT INTO episode VALUES('{0}','{1}', '{2}')".format(title, instalment[1], videoId), "execute")
        else:
            query("INSERT INTO content VALUES('{0}','{1}','{2}','{3}')".format(contentData['name'],contentData['img'],contentData['type'],contentData['name'].replace(' ', '').lower()), "execute")
            query("INSERT INTO season VALUES('{0}','{1}','{2}')".format(contentData['name'],instalment[0],'_'.join([contentData['name'].replace(' ', ''),str(instalment[0])]).lower()), "execute")
            query("INSERT INTO episode VALUES('{0}','{1}', '{2}')".format(title, instalment[1], videoId), "execute")
    else:
        print('Ignoring', title)

#looks for videos uploaded past the initial date, then video is processed.
def parseChannel(uploadsPlaylistId, initDate, nextPageToken=''): 
    url = "https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={0}&key={1}&pageToken={2}".format(uploadsPlaylistId, getAPIKey(), nextPageToken) 
    print(url)
    data = parseURL(url)
    print(len(data['items']))
    for item in data['items']:
        if dateutil.parser.parse(item["contentDetails"]["videoPublishedAt"]) > initDate:
            parseContent(item["contentDetails"]["videoId"])
    
                #findMedia(title)
    #if data['nextPageToken'] is not None: parseChannel(channelId, data['nextPageToken'])

#https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={}&key={}
uploadsPlaylistId = "UUeyxmrDWk6UUy1k6JVSy8Ww" 
initDate = dateutil.parser.parse("2020-01-01T00:00:00Z")
parseChannel(uploadsPlaylistId, initDate)
