#!/usr/bin/python
""" This module scrapes dayviews for images. """

import os
import argparse
import urllib
import HTMLParser
import requests
import requests_cache
import simplejson as json

DEFAULT_DIR = "images/"

def get_img(url, session):
    """ Parses an url into a dict.
        Retrieves image url, date and image text.
     """
    search_str = "var currentFullsizeImage = "
    date_str = "var thisDate = "
    year_str = "var thisYear = "
    req = session.get(url, stream=True)
    img = {'url': "", 'date': "", 'text': ""}
    year, month, day = "0", "0", "0"

    for line in req.iter_lines():
        if search_str in line:
            data = line[len(search_str):-1]
            json_data = json.loads(data)
            img['url'] = json_data['fullsizeSrc']
            img['text'] = HTMLParser.HTMLParser().unescape(
                json_data['strippedText']).encode("utf-8")
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

def get_next_url(url, session):
    """ Parses url for the next image """
    search_str = "class=\"nextDayHref navigationNav icon\">"
    take_next = False
    req = session.get(url, stream=True)
    for line in req.iter_lines():
        if search_str in line:
            take_next = True
        elif take_next is True:
            return line.split("\"")[1]
    return None

def get_list_of_all(start_url, session):
    """ Returns a list with all images, starting at start_url. """
    arr = []
    arr.append(get_img(start_url, session))
    nexturl = get_next_url(start_url, session)
    while nexturl is not None:
        arr.append(get_img(nexturl, session))
        nexturl = get_next_url(nexturl, session)
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
    while os.path.isfile(path):
        num += 1
        path = folder + img['date'] + "-#" + str(num)
    urllib.urlretrieve(img['url'], path + ".jpg")
    if save_text:
        with open(path + ".txt", 'w') as txtfile:
            print(img['text'])
            txtfile.write(img['text'])

def login(user, password):
    """ Login to account. Simple POST request. """
    session = requests.Session()
    print("Got user/pass")
    payload = {'action': 'login',
               'user': user,
               'pass': password,
               'crosslogin': 0,
               'bdbhdCampaign': 0,
               'topLoginNoJScript': 0,
               'ajaxlogin': 1,
               'doIframeLogin': 0,
               'json': 1
              }
    session.post("http://dayviews.com/", data=payload)
    return session

def get_number_of_uploads(username):
    """ Returns the number of uploaded images by username """
    url = "http://dayviews.com/p/ajax.html?action=getUserInfoJSON&username=" \
          + username + "&onFocus=0&json=1"
    req = requests.get(url)
    data = json.loads(req.content)
    return int(data['imagecount'].split(" ")[2])

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("start_url")
    parser.add_argument("-o", "--only-print", action="store_true",
                        default=False, help="Only print url/date/text")
    parser.add_argument("-d", "--dest", type=str, default="images/",
                        help="Where to save files. (default = images/)")
    parser.add_argument("-t", "--save-text", action="store_true", default=True,
                        help="Save image text")
    parser.add_argument("-u", "--username", type=str,
                        help="Your username")
    parser.add_argument("-p", "--password", type=str,
                        help="Your password")
    args = parser.parse_args()

    # Login
    if args.username and args.password:
        session = login(args.username, args.password)
    else:
        session = requests.Session()
        # The cache messes with the login, so we only use it when anonymous
        requests_cache.install_cache('bdb_search_cache')

    if not args.only_print:
        save_dir = args.dest if args.dest else DEFAULT_DIR
        if save_dir[-1:] != '/':
            save_dir += '/'
        print "Saving images in " + save_dir
    if args.start_url is not None:
        print "Starting URL is " + args.start_url

    all_images = get_list_of_all(args.start_url, session)
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

