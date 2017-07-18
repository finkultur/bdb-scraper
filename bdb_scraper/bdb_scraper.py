#!/usr/bin/env python3
""" Module for scraping images from dayviews. """

import os
import urllib.request
import html.parser
import shutil
import requests
import requests_cache
import simplejson as json

DEFAULT_DIR = "images/"
SEARCH_STR = "var currentFullsizeImage = "
DATE_STR = "var thisDate = "
YEAR_STR = "var thisYear = "
NEXT_URL_STR = "class=\"nextDayHref navigationNav icon\">"

def get_img(url, session):
    """ Parses an url into a dict.
        Retrieves image url, date, image text and url to the next image.
     """
    req = session.get(url, stream=True)
    img = {'url': "", 'date': "", 'text': "", 'next_url': None}
    year, month, day = "0", "0", "0"

    next_is_url = False
    for line in req.iter_lines(decode_unicode=True):
        if SEARCH_STR in line:
            data = line[len(SEARCH_STR):-1]
            json_data = json.loads(data)
            img['url'] = json_data['fullsizeSrc']
            img['text'] = html.unescape(json_data['strippedText']).encode("utf-8")
        elif DATE_STR in line:
            date = line[:-2].split('month')[1].split('day') # Sorry not sorry
            month = date[0]
            day = date[1]
        elif YEAR_STR in line:
            # Will not work after year 9999.
            # Fortunately, dayviews closes sometime in 2017.
            year = line[-6:-2]
            img['date'] = year + "-" + month + "-" + day
        elif next_is_url:
            img['next_url'] = line.split("\"")[1]
            break
        elif NEXT_URL_STR in line:
            next_is_url = True
    return img

def get_list_of_all(start_url, session):
    """ Returns a list with all images, starting at start_url. """
    arr = []
    arr.append(get_img(start_url, session))
    i = 0
    while arr[i]['next_url'] is not None:
        arr.append(get_img(arr[i]['next_url'], session))
        i += 1
    return arr[:-1] # Skip the last one that is void

def download_all(images, path, save_text=False):
    """ Downloads all images to path """
    if not os.path.exists(path):
        os.makedirs(path)
    for img in images:
        save_image(img, path, save_text)

def save_image(img, folder, save_text=False):
    """ Saves an image to disk.
        Filename is on the form YYYY-MM-DD[-#N].jpg
    """
    num = 0
    path = folder + img['date'] + '-#' + str(num)
    while os.path.isfile(path):
        num += 1
        path = folder + img['date'] + "-#" + str(num)
    urllib.request.urlretrieve(img['url'], path + ".jpg")
    if save_text:
        with open(path + ".txt", 'wb') as txtfile:
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

def zip_name_from_url(url):
    """ Creates a string from a bdb-url.
        http://dayviews.com/username/12345678/ returns username-12345678
    """
    info = url.split('/')
    return info[3] + '-' + info[4]

def scrape(starturl, dest='images/', save_text=True, create_zip=True,
           zip_name=None, zip_base=None, username=None, password=None):
    """ Scrape a diary
        starturl: E.g. http://dayviews.com/farligast/179081381/
        Optional arguments:
           dest: Where to save files (default = images/)
           save_text: Whether or not to save image description
           create_zip: Whether or not to create a zip archive
           zip_name: Name of archive (optional)
           zip_base: basedir to start zipping (defaults to cwd) (optional)
           username: Your username
           password: Your password
    """
    if starturl:
        print("Starting URL is " + starturl)
    else:
        exit(1) # Pretty important with a starturl
    if not dest:
        dest = DEFAULT_DIR
    if dest[-1:] != '/':
        dest += '/' # Add trailing slash if there isn't one
    print("Saving images in " + dest)
    if username and password:
        print("Using credentials.")
        session = login(username, password)
    else:
        session = requests.Session()

    user = get_user_from_url(starturl)
    num_of_uploads = get_number_of_uploads(user)
    print(user + " has uploaded " + str(num_of_uploads) + " images in total.")
    all_images = get_list_of_all(starturl, session)
    print("Parsed all entries.")
    download_all(all_images, dest, save_text)
    print("Saved " + str(len(all_images)) + " images to " + dest)
    if create_zip:
        if not zip_name:
            zip_name = zip_name_from_url(starturl)
        if zip_base:
            if dest.startswith(zip_base):
                dest = dest[len(zip_base):]
            else:
                exit(2)
        shutil.make_archive(zip_name, 'zip', zip_base, dest)
        print("Created zip archive " + zip_name + ".zip")

