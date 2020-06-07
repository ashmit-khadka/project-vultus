import requests
from requests.exceptions import HTTPError
from datetime import timedelta, datetime
import isodate
#from db import query
import dateutil.parser
from YPT import *

from mongoDB import getCollection

api_key = "AIzaSyAGOmlQHZQibXpeoTRl3Sa7DBYWFBTGCAQ"
channel_id = "UCxCoea3ulOukfXiYAm87ZIA"

def parseContent(videoSnippet):

    collection = getCollection('pre')

    #video snippit to get title -> determin the duration to see if movie to episode

    title = videoSnippet['title']
    name = getMediaName(title)
    if name is None: return None

    mediaType = getMediaType(videoSnippet['resourceId']['videoId'], title)

    if mediaType == 'MOVIE':
        print(title, 'is movie')
        contentData = getContentObj(videoSnippet, name, 'M')
        contentMeta = {
            "name":contentData['name'],
            "img":contentData['img'],
            "type":contentData['type'],
            "id":contentData['name'].replace(' ', '').lower(),
        }
        collection.insert_one(contentMeta)

        #query("INSERT INTO content VALUES('{0}','{1}','{2}','{3}')".format(contentData['name'],contentData['img'],contentData['type'],contentData['name'].replace(' ', '').lower()), "execute")

    elif mediaType == 'EPISODE':
        print(title, 'is episode')
        contentData = getContentObj(videoSnippet, name, 'E')
        instalment = getInstalments(title)
        #print(instalment)
        #print(collection.find_one({"id":contentData['name'].replace(' ', '').lower()}))
        if collection.find_one({"id":contentData['name'].replace(' ', '').lower()}) is None:
            contentMeta = {
                "name":contentData['name'],
                "img":contentData['img'],
                "type":contentData['type'],
                "id":contentData['name'].replace(' ', '').lower(),
                "seasons":[{
                    "season":instalment[0],
                    "episodes": [{
                        "title": title,
                        "episode": instalment[1],
                        "id":videoSnippet['resourceId']['videoId']
                    }]
                }]
            }
            collection.insert_one(contentMeta)
        else:
            collection.update_one({
                "id":contentData['name'].replace(' ', '').lower(),
                "seasons.season": instalment[0]
            }, {
                "$push": {
                    "seasons.$.episodes": {
                        "title": title,
                        "episode": instalment[1],
                        "id":videoSnippet['resourceId']['videoId']
                    }
                }
            })
        '''
        if query("SELECT COUNT(*) FROM content WHERE name = '{0}'".format(name), 'fetchone')[0]:
            if not query("SELECT COUNT(*) FROM season WHERE id = '{0}'".format('_'.join([contentData['name'].replace(' ', ''),str(instalment[0])]).lower()), 'fetchone')[0]:
                query("INSERT INTO season VALUES('{0}','{1}','{2}')".format(contentData['name'],instalment[0],'_'.join([contentData['name'].replace(' ', ''),str(instalment[0])]).lower()), "execute")
            query("INSERT INTO episode VALUES('{0}','{1}', '{2}')".format(title, instalment[1], videoId), "execute")
        else:
            query("INSERT INTO content VALUES('{0}','{1}','{2}','{3}')".format(contentData['name'],contentData['img'],contentData['type'],contentData['name'].replace(' ', '').lower()), "execute")
            query("INSERT INTO season VALUES('{0}','{1}','{2}')".format(contentData['name'],instalment[0],'_'.join([contentData['name'].replace(' ', ''),str(instalment[0])]).lower()), "execute")
            query("INSERT INTO episode VALUES('{0}','{1}', '{2}')".format(title, instalment[1], videoId), "execute")
        '''
    else:
        print('Ignoring', title)

#looks for videos uploaded past the initial date, then video is processed.
def parseChannel(uploadsPlaylistId, initDate, nextPageToken=''): 
    url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={0}&key={1}&pageToken={2}".format(uploadsPlaylistId, getAPIKey(), nextPageToken) 
    #print(url)
    data = parseURL(url)
    #print(len(data['items']))
    cnt = 0
    for item in data['items']:
        if dateutil.parser.parse(item["snippet"]["publishedAt"]) > initDate:
            parseContent(item["snippet"])
            cnt = cnt + 11
            #print(item['snippet']['title'])

        else:
            return print(cnt)
    
                #findMedia(title)
    if data['nextPageToken'] is not None: parseChannel(uploadsPlaylistId, initDate, data['nextPageToken'])

#https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={}&key={}
#UUAclVGCh7QyLH41jJGQVhaw
#UUeyxmrDWk6UUy1k6JVSy8Ww
uploadsPlaylistId = "UUAclVGCh7QyLH41jJGQVhaw" 
initDate = dateutil.parser.parse("2020-01-01T00:00:00Z")
parseChannel(uploadsPlaylistId, initDate)
