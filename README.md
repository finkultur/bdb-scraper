# bdb-scraper
Fetches all your public stuff from dayviews/bilddagboken.
Hurry 'cause it will close 2017-09-01.
Beware that it could take a while to do this.

## Prerequisites
Git, Python2.7, pip

## Installation
```
clone repo
pip install -r requirements.txt
```

## Usage
```
scraper.py [-h] [-o] [-d DEST] [-t] [-u USERNAME] [-p PASSWORD]
                  start_url

positional arguments:
  start_url

optional arguments:
  -h, --help            show this help message and exit
  -o, --only-print      Only print url/date/text
  -d DEST, --dest DEST  Where to save files. (default = images/)
  -t, --save-text       Save image text
  -u USERNAME, --username USERNAME
                        Your username
  -p PASSWORD, --password PASSWORD
                        Your password
```

Go to the starting image of the bilddagbok that you want to fetch and copy the url.
Then simply do this to fetch both images and descriptions:
```
./scraper.py -t http://dayviews.com/<username>/<id_of_first_image>/
``` 
To fetch all simpaons stuff for example, do this (if you're his friend). Or exchange for some other username/id.
```
./scraper.py -t -u <your_username> -p <your_password> http://dayviews.com/farligast/974579/
```

