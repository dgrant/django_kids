import urllib2
from urllib2 import HTTPError

import json
import urllib2

def get_youtube_thumbnail(id):
    return 'http://img.youtube.com/vi/{0}/0.jpg'.format(id)

def get_vimeo_thumbnail(id):
    url = 'http://vimeo.com/api/v2/video/{0}.json'.format(id)
    try:
        result = read_from_url(url)
    except HTTPError:
        print "Failed to fetch url: {0}".format(url)
        return ''
    else:
        return json.loads(result)[0]['thumbnail_large']

def read_from_url(url): # pragma: no cover
    return urllib2.urlopen(url).read()
