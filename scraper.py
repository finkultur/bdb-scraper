#!/usr/bin/python

import sys
import requests
import simplejson as json

searchStr = "var currentFullsizeImage = "

def getUrl(url):

    r = requests.get(url, stream=True)
    for l in r.iter_lines():
        if searchStr in l:
            data = l[len(searchStr):-1]
            j = json.loads(data)
            return j['fullsizeSrc']

    return "not found"

if __name__ == '__main__':
    print getUrl("http://dayviews.com/finkultur/36850186/")

