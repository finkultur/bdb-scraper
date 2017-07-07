# bdb-scraper
Fetches all your public stuff from dayviews/bilddagboken.
Hurry 'cause it will close 2017-09-01.
Beware that it could take a while to do this.
At the moment this only supports dagboks that are open to everyone.

## Usage
```
$ ./scraper.py -h
usage: scraper.py [-h] [-o] [-p PATH] [-t] start_url

positional arguments:
  start_url

optional arguments:
  -h, --help            show this help message and exit
  -o, --only-print      Only print url/date/text
  -p PATH, --path PATH  Where to save files. (default = images/)
  -t, --save-text       Save image text
```

Go to the starting image of the bilddagbok that you want to fetch and copy the url.
Then simply do this to fetch both images and descriptions:
```
./scraper.py -t http://dayviews.com/<username>/<id_of_first_image>/
``` 
To fetch all simpaons stuff for example, do this. Or exchange for your own username/id.
```
./scraper.py -t http://dayviews.com/farligast/974579/
```

