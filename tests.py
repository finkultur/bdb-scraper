#!/usr/bin/python

import unittest
from scraper import *

class TestStuff(unittest.TestCase):
    def setUp(self):
        self.img = getImg("http://dayviews.com/finkultur/195730454/")

    def test_image_url(self):
        self.assertEqual(self.img['url'],
                         "http://cdn07.dayviews.com/25/_u1/_u3/_u0/_u6/_u5/u130659/50458_1208685717.jpg")

    def test_image_text(self):
        self.assertEqual(self.img['text'],
                         "SOLEN SKINER ALLTID P&Aring; PALLBRYT")

    def test_image_date(self):
        self.assertEqual(self.img['date'],
                         [2008, 4, 19])

    def test_get_next_url(self):
        self.assertEqual(getNextUrl("http://dayviews.com/finkultur/36850186/"),
                         "http://dayviews.com/finkultur/37715304/")
 
if __name__ == '__main__':
    unittest.main()
