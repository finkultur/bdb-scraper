# bdb-scraper
Fetches all your (or someone else's stuff from dayviews/bilddagboken.
Hurry 'cause it will close 2017-09-01.
Beware that it could take a while to do this.

## Prerequisites
Git, Python3.5, pip

## Installation
```
git clone git@github.com:finkultur/bdb-scraper.git
sudo pip3 install -r bdb-scraper/
```

## Usage
```
usage: bdb-scraper [-h] [-d DEST] [-t] [-z] [-u USERNAME] [-p PASSWORD]
                   start_url

positional arguments:
  start_url

optional arguments:
  -h, --help            show this help message and exit
  -d DEST, --dest DEST  Where to save files. (default = images/)
  -t, --save-text       Save image text
  -z, --create-zip      Creates a zip archive of downloaded contents
  -u USERNAME, --username USERNAME
                        Your username
  -p PASSWORD, --password PASSWORD
                        Your password
```

Go to the starting image of the bilddagbok that you want to fetch and copy the url.
Then simply do this to fetch all images.
```
bdb-scraper http://dayviews.com/<username>/<id_of_first_image>/
``` 
To fetch all simpaons stuff for example, do this (if you're his friend). Or exchange for some other
username/id. Also creates a zip-archive with images and their descriptions.
```
bdb-scraper -d save_it_here/ -t -z -u <your_username> -p <your_password> http://dayviews.com/farligast/974579/
```

