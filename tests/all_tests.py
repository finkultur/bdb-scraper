#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
import requests
import os
import shutil
from bdb_scraper import *

class test_anonymous(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()
        self.img = get_img("http://dayviews.com/finkultur/195730454/", self.session)
        self.folder = "tests_tmp/"
        if os.path.exists(self.folder):
            shutil.rmtree(self.folder)
        os.makedirs(self.folder)

    def test_image_url(self):
        self.assertEqual(self.img['url'],
                         "http://cdn07.dayviews.com/25/_u1/_u3/_u0/_u6/_u5/u130659/50458_1208685717.jpg")

    def test_image_text(self):
        self.assertEqual(self.img['text'], "SOLEN SKINER ALLTID PÅ PALLBRYT".encode("utf-8"))

    def test_image_date(self):
        self.assertEqual(self.img['date'], "2008-04-19")

    def test_next_url(self):
        self.assertEqual(self.img['next_url'], "http://dayviews.com/finkultur/195731292/")

    def test_get_number_of_uploads(self):
        self.assertEqual(get_number_of_uploads("janisious"), 3427)

    def test_get_list_of_all_length(self):
        arr = get_list_of_all("http://dayviews.com/nilsheterjag/394939606/", self.session)
        self.assertEqual(len(arr), 3)
        arr2 = get_list_of_all("http://dayviews.com/nilsheterjag/390790559/", self.session)
        self.assertEqual(len(arr2), 14)

    def test_download_all(self):
        folder = self.folder + "download_all/"
        arr = get_list_of_all("http://dayviews.com/nilsheterjag/394939606/", self.session)
        download_all(arr, folder)
        num_of_files = len(os.listdir(folder))
        self.assertEqual(num_of_files, 3)

    def test_download_all_many(self):
        folder = self.folder + "download_all_many/"
        arr = get_list_of_all("http://dayviews.com/nilsheterjag/393684875/", self.session)
        download_all(arr, folder)
        num_of_files = len(os.listdir(folder))
        self.assertEqual(num_of_files, 10)

    def test_save_image(self):
        img = get_img("http://dayviews.com/nilsheterjag/395480047/", self.session)
        folder = self.folder + "save_image_test/"
        os.makedirs(folder)
        save_image(img, folder)
        num_of_files = len(os.listdir(folder))
        self.assertEqual(num_of_files, 1)

    def tearDown(self):
        shutil.rmtree(self.folder)
        pass
 
class test_logged_in(unittest.TestCase):
    def setUp(self):
        with open('credentials.txt', 'r') as f:
            creds = [ line.replace('\n', '') for line in f ]
        self.session = login(creds[0], creds[1])
        print(creds)
        self.img = get_img("http://dayviews.com/farligast/179081381/", self.session)

    def test_image_url(self):
        self.assertEqual(self.img['url'],
                         "http://cdn07.dayviews.com/18/_u1/_u0/_u4/_u5/u10451/74248_1205499756.jpg")

    def test_image_text(self):
        self.assertEqual(self.img['text'],
                         "Jag hittade en arvikabild någonstans som beskrev vad jag pysslade med rätt bra tror jag."
                         .encode("utf-8"))

    def test_image_date(self):
        self.assertEqual(self.img['date'], "2008-03-12")

    def test_next_url(self):
        self.assertEqual(self.img['next_url'], "http://dayviews.com/farligast/179005838/")

    def tearDown(self):
        pass

class test_static_functions(unittest.TestCase):
    def test_get_user_from_url(self):
        self.assertEqual("finkultur",
                         get_user_from_url("http://dayviews.com/finkultur/195730454/"))

    def test_zip_name_from_url(self):
        self.assertEqual("finkultur-195730454",
                         zip_name_from_url("http://dayviews.com/finkultur/195730454/"))

if __name__ == '__main__':
    unittest.main()
