#!/usr/bin/python
""" This module scrapes dayviews for images. """

import os
import argparse
import urllib
import requests
import simplejson as json

DEFAULT_DIR = "images/"

def get_img(url):
    """ Parses an url into a dict.
        Retrieves image url, date and image text.
     """
    search_str = "var currentFullsizeImage = "
    date_str = "var thisDate = "
    year_str = "var thisYear = "
    req = requests.get(url, stream=True)
    img = {'url': "", 'date': "", 'text': ""}
    year, month, day = "0", "0", "0"

    for line in req.iter_lines():
        if search_str in line:
            data = line[len(search_str):-1]
            json_data = json.loads(data)
            img['url'] = json_data['fullsizeSrc']
            img['text'] = json_data['strippedText']
        elif date_str in line:
            date = line[:-2].split('month')[1].split('day') # Sorry not sorry
            month = date[0]
            day = date[1]
        elif year_str in line:
            # Will not work after year 9999.
            # Fortunately, dayviews closes sometime in 2017.
            year = line[-6:-2]

    img['date'] = year + "-" + month + "-" + day
    return img

def get_next_url(url):
    """ Parses url for the next image """
    search_str = "class=\"nextDayHref navigationNav icon\">"
    take_next = False
    req = requests.get(url, stream=True)
    for line in req.iter_lines():
        if search_str in line:
            take_next = True
        elif take_next is True:
            return line.split("\"")[1]
    return None

def get_list_of_all(start_url):
    """ Returns a list with all images, starting at start_url. """
    arr = []
    arr.append(get_img(start_url))
    nexturl = get_next_url(start_url)
    while nexturl is not None:
        arr.append(get_img(nexturl))
        nexturl = get_next_url(nexturl)
    return arr[:-1] # Skip the last one that is void

def pretty_print(img):
    """ Very pretty printing. """
    print(img['date'])
    print(img['url'])
    print(img['text'])
    print("\n")

def save_image(img, folder, save_text=False):
    """ Saves an image to disk.
        Filename is on the form YYYY-MM-DD[-#N].jpg
    """
    num = 0
    path = folder + img['date'] + '-#' + str(num)
    while (os.path.isfile(path)):
        num += 1
        path = folder + img['date'] + "-#" + str(num)
    urllib.urlretrieve(img['url'], path + ".jpg")
    if save_text:
        with open(path + ".txt", 'w') as txtfile:
            txtfile.write(img['text'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("start_url")
    parser.add_argument("-o", "--only-print", action="store_true", default=False,
                        help="Only print url/date/text")
    parser.add_argument("-p", "--path", type=str, default="images/",
                        help="Where to save files. (default = images/)")
    parser.add_argument("-t", "--save-text", action="store_true", default=True,
                        help="Save image text")
    args = parser.parse_args()

    if args.save:
        save_dir = args.path if args.path else DEFAULT_DIR
        if save_dir[-1:] != '/': save_dir += '/'
        print "Saving images in " + save_dir
    if args.start_url is not None:
        print "Starting URL is " + args.start_url

    all_images = get_list_of_all(args.start_url)
    print("Parsed all entries.")

    if args.only_print:
        for image in all_images:
            pretty_print(image)
    else:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        for image in all_images:
            save_image(image, save_dir, args.save_text)
        print("Saved " + str(len(all_images)) + " images to " + save_dir)

