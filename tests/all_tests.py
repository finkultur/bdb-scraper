#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
import requests
from bdb_scraper import *

class test_anonymous(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()
        self.img = get_img("http://dayviews.com/finkultur/195730454/", self.session)

    def test_image_url(self):
        self.assertEqual(self.img['url'],
                         "http://cdn07.dayviews.com/25/_u1/_u3/_u0/_u6/_u5/u130659/50458_1208685717.jpg")

    def test_image_text(self):
        self.assertEqual(self.img['text'], "SOLEN SKINER ALLTID PÅ PALLBRYT".encode("utf-8"))

    def test_image_date(self):
        self.assertEqual(self.img['date'], "2008-4-19")

    def test_next_url(self):
        self.assertEqual(self.img['next_url'], "http://dayviews.com/finkultur/195731292/")

    def test_get_number_of_uploads(self):
        self.assertEqual(get_number_of_uploads("janisious"), 3427)

    def tearDown(self):
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
        self.assertEqual(self.img['date'], "2008-3-12")

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
