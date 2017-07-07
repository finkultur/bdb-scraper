#!/usr/bin/python

import sys
import requests
import simplejson as json
import argparse


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
            d['date'][1] = x[0]
            d['date'][2] = x[1]
        elif yearStr in l:
            # Will not work after year 9999.
            # Fortunately, dayviews closes sometime in 2017.
            d['date'][0] = l[-6:-2]
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

def prettyPrint(img):
    print(img['date'][0] + "-" + img['date'][1] + "-" + img['date'][2])
    print(img['url'])
    print(img['text'])
    print("\n")

def saveImage(img):
    pass

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("startUrl")
    parser.add_argument("-s", "--save", type=str,
                        help="Save files to directory")
    args = parser.parse_args()

    if args.save:
        print "Saving images in " + args.save
    if args.startUrl is not None:
        print "starturl is " + args.startUrl

    a = getListOfAll(args.startUrl)

    if not args.save:
       for pic in a:
           prettyPrint(pic)
    else:
        for pic in a:
            saveImage(img)

    #url = sys.argv[1]
    #a = getListOfAll(url)
    #for pic in a:
    #    print pic
    #print("Got " + str(len(a)) + " entries.")


