#!/usr/bin/python

import sys
import os
import requests
import urllib
import simplejson as json
import argparse

DEFAULT_DIR = "images/"

def getImg(url):
    """ Parses an url into a dict.
        Retrieves image url, date and image text.
     """
    searchStr = "var currentFullsizeImage = "
    dateStr = "var thisDate = "
    yearStr = "var thisYear = "
    r = requests.get(url, stream=True)
    d = {'url': "", 'date': "", 'text': ""}
    year, month, day = "0","0","0"

    for l in r.iter_lines():
        if searchStr in l:
            data = l[len(searchStr):-1]
            j = json.loads(data)
            d['url'] = j['fullsizeSrc']
            d['text'] = j['strippedText']
        elif dateStr in l:
            x = l[:-2].split('month')[1].split('day') # Sorry not sorry
            month = x[0]
            day = x[1]
        elif yearStr in l:
            # Will not work after year 9999.
            # Fortunately, dayviews closes sometime in 2017.
            year = l[-6:-2]

    d['date'] = year + "-" + month + "-" + day
    return d

def getNextUrl(url):
    """ Parses url for the next image """
    searchStr = "class=\"nextDayHref navigationNav icon\">"
    takeNext = False
    r = requests.get(url, stream=True)
    for l in r.iter_lines():
        if searchStr in l:
            takeNext = True
        elif takeNext is True:
            return l.split("\"")[1]
    return None

def getListOfAll(startUrl):
    """ Returns a list with all images, starting at startUrl. """
    arr = []
    arr.append(getImg(startUrl))
    nexturl = getNextUrl(startUrl)
    while nexturl is not None:
        arr.append(getImg(nexturl))
        nexturl = getNextUrl(nexturl)
    return arr[:-1] # Skip the last one that is void

def prettyPrint(img):
    """ Very pretty printing. """
    print(img['date'])
    print(img['url'])
    print(img['text'])
    print("\n")

def saveImage(img, folder, save_text=False):
    """ Saves an image to disk.
        Filename is on the form YYYY-MM-DD[-#N].jpg
    """
    num = 0
    path = folder + img['date'] + '-#' + str(num)
    while (os.path.isfile(path)):
        num += 1
        path = folder + img['date'] + "-#" + str(num)
    urllib.urlretrieve(img['url'], path + ".jpg")
    with open(path + ".txt", 'w') as txtfile:
        txtfile.write(img['text'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("startUrl")
    parser.add_argument("-s", "--save", action="store_true",
                        help="Save files to directory")
    parser.add_argument("-p", "--path", type=str, default="images/",
                        help="Where to save files")
    parser.add_argument("-t", "--save-text", action="store_true",
                        help="Save image text")
    args = parser.parse_args()

    if args.save:
        save_dir = args.path if args.path else DEFAULT_DIR
        if save_dir[-1:] != '/': save_dir += '/'
        print "Saving images in " + save_dir
    if args.startUrl is not None:
        print "Starting URL is " + args.startUrl

    a = getListOfAll(args.startUrl)
    print("Parsed all entries.")

    if not args.save:
       for img in a:
           prettyPrint(img)
    else:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        for img in a:
            saveImage(img, save_dir, args.save_text)
        print("Saved " + str(len(a)) + " images to " + save_dir)

