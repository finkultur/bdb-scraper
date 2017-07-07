#!/usr/bin/python

import unittest
from scraper import *

class TestStuff(unittest.TestCase):
    def setUp(self):
        pass

    def test_single_image(self):
        self.assertEqual(getUrl("http://dayviews.com/finkultur/36850186/"),
                         "http://cdn07.dayviews.com/6/_u1/_u3/_u0/_u6/_u5/u130659/14655_1174453141.jpg")
 
if __name__ == '__main__':
    unittest.main()
