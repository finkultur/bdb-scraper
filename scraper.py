#!/usr/bin/python

import sys
import requests
import simplejson as json


def getUrl(url):
    searchStr = "var currentFullsizeImage = "
    r = requests.get(url, stream=True)
    for l in r.iter_lines():
        if searchStr in l:
            data = l[len(searchStr):-1]
            j = json.loads(data)
            return j['fullsizeSrc']

    return "not found"

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

if __name__ == '__main__':
    #print getUrl("http://dayviews.com/finkultur/36850186/")
    #print getNextUrl("http://dayviews.com/finkultur/36850186/")

    if len(sys.argv) != 2:
        sys.exit(1)

    url = sys.argv[1]
    print getUrl(url)

    nexturl = getNextUrl(url)
    while nexturl != "not found":
        print getUrl(nexturl)
        nexturl = getNextUrl(nexturl)         

