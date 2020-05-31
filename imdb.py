from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
import json

def getObj(data):
    content = {
        "name": data['name'],
        "img": data['image'],
        "genre": data['genre'],
        "actor": data['actor'],
        "description": data['description'],
    }
    return content

#parses imdb page, returns infomation dictionary.
def parseMedia(path):
    def getCountry(infoCountry):
        infoDetail = infoCountry.find_next_sibling()
        if infoDetail.getText() is not None:
            return infoDetail.getText()

    def getInfo(soup):
        info = soup.find('script', {'type':'application/ld+json'})
        infoStr = (str(info)[len('<script type="application/ld+json">'):-len('</script>')])
        return json.loads(infoStr)

    baseURL = 'https://www.imdb.com'
    URL = "{0}{1}".format(baseURL, path)
    page = urlopen(URL)
    soup = BeautifulSoup(page, "html.parser")
    infoItems = soup.findAll('div', {'class' : 'txt-block'})
    for infoItem in infoItems:
        infoHeader = infoItem.find('h4')
        if infoHeader is not None and infoHeader.getText() == "Country:":
            if getCountry(infoHeader).upper() == "NEPAL":
                return getInfo(soup)
            else:
                return None

#searches for a matching imdb content page.
def findMedia(name):
    baseURL = 'https://www.imdb.com/find?q='
    URL = "{0}{1}".format(baseURL, quote(name))
    page = urlopen(URL)
    soup = BeautifulSoup(page, "html.parser")
    movieList = soup.find('div', {'class' : 'findSection'})
    if movieList is None: return None
    movieListItems = movieList.findAll('tr')
    if movieListItems is None: return None

    for movieListItem in movieListItems:
        print(movieListItem.find('a')['href'])
        data = parseMedia(movieListItem.find('a')['href'])
        if data is not None:
            #returns the first nepali content match.
            return getObj(data)
        else: print("Content {0} not found.".format(name))
    return None

#print(findMedia("gdfgdfdgfdgf"))
#print(parseMovie("/title/tt11724834/"))