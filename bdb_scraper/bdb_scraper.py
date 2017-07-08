#!/usr/bin/python
""" Module for scraping images from dayviews. """

from __future__ import print_function

import os
import urllib
import HTMLParser
import shutil
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

def download_all(images, path, save_text=False):
    """ Downloads all images to path """
    if not os.path.exists(path):
        os.makedirs(path)
    for img in images:
        save_image(img, path, save_text)

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
            txtfile.write(img['text'])

def login(user, password):
    """ Login to account. Simple POST request. """
    session = requests.Session()
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

def get_user_from_url(url):
    """ Returns the username from a url """
    return url.split('/')[3]

def make_archive(starturl, path):
    """ Creates a zip-file of a directory """
    info = starturl.split('/')
    filename = info[3] + '-' + info[4]
    return shutil.make_archive(filename, 'zip', "./", path)

def scrape(starturl, **kwargs):
    """ Scrape a diary
        starturl: E.g. http://dayviews.com/farligast/179081381/
        Optional arguments:
           dest: Where to save files (default = images/)
           save_text: Whether or not to save image description
           create_zip: Whether or not to create a zip archive
           username: Your username
           password: Your password
    """
    if 'username' in kwargs and 'password' in kwargs:
        print("Using credentials.")
        session = login(kwargs['username'], kwargs['password'])
    else:
        session = requests.Session()
        # The cache messes with the login, so we only use it when anonymous
        requests_cache.install_cache('bdb_search_cache')
    if 'dest' in kwargs:
        save_dir = kwargs['dest']
    else:
        save_dir = DEFAULT_DIR
    if save_dir[-1:] != '/':
        save_dir += '/'
    print("Saving images in " + save_dir)
    if starturl is not None:
        print("Starting URL is " + starturl)
    else:
        exit(1)
    save_text = 'save_text' in kwargs and kwargs['save_text']
    create_zip = 'create_zip' in kwargs and kwargs['create_zip']
    user = get_user_from_url(starturl)
    num_of_uploads = get_number_of_uploads(user)
    print(user + " has uploaded " + str(num_of_uploads) + " images")
    all_images = get_list_of_all(starturl, session)
    print("Parsed all entries.")
    download_all(all_images, save_dir, save_text)
    print("Saved " + str(len(all_images)) + " images to " + save_dir)
    if create_zip:
        zipname = make_archive(starturl, save_dir)
        print("Created zip archive in " + zipname)

