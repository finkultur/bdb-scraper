#!/usr/bin/python2.7

from __future__ import absolute_import

import bdb_scraper
import argparse

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("start_url")
    parser.add_argument("-d", "--dest", type=str, default="images/",
                        help="Where to save files. (default = images/)")
    parser.add_argument("-t", "--save-text", action="store_true", default=False,
                        help="Save image text")
    parser.add_argument("-z", "--create-zip", action="store_true", default=False,
                        help="Creates a zip archive of downloaded contents")
    parser.add_argument("-u", "--username", type=str,
                        help="Your username")
    parser.add_argument("-p", "--password", type=str,
                        help="Your password")
    args = parser.parse_args()

    bdb_scraper.scrape(args.start_url,
                       dest=args.dest,
                       save_text=args.save_text,
                       create_zip=args.create_zip,
                       username=args.username,
                       password=args.password)

if __name__ == '__main__':
    main()

