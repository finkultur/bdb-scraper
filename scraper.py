#!/usr/bin/python

import sys
import requests
import simplejson as json


def getImg(url):
    searchStr = "var currentFullsizeImage = "
    dateStr = "var thisDate = "
    yearStr = "var thisYear = "

    r = requests.get(url, stream=True)
    d = {'url': "", 'date': [0,0,0], 'text': ""}

    for l in r.iter_lines():
        if searchStr in l:
            data = l[len(searchStr):-1]
            j = json.loads(data)
            d['url'] = j['fullsizeSrc']
            d['text'] = j['strippedText']

        elif dateStr in l:
            x = l[:-2].split('month')[1].split('day') # Sorry not sorry
            d['date'][1] = int(x[0])
            d['date'][2] = int(x[1])
        elif yearStr in l:
            # Will not work after year 9999.
            # Fortunately, dayviews closes sometime in 2017.
            d['date'][0] = int(l[-6:-2])
    return d

def getNextUrl(url):
    searchStr = "class=\"nextDayHref navigationNav icon\">"

    takeNext = False
    r = requests.get(url, stream=True)

    for l in r.iter_lines():
        if searchStr in l:
            takeNext = True
        elif takeNext is True:
            return l.split("\"")[1]
    return "not found"

def getListOfAll(startUrl):
    """ Returns a list with all images, starting at startUrl. """
    arr = []
    arr.append(getImg(startUrl))
    nexturl = getNextUrl(startUrl)
    while nexturl != "not found":
        arr.append(getImg(nexturl))
        nexturl = getNextUrl(nexturl)
    return arr[:-1]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)

    url = sys.argv[1]
    a = getListOfAll(url)
    for pic in a:
        print pic
    print("Got " + str(len(a)) + " entries.")


