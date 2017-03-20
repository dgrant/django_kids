import logging

logger = logging.getLogger(__name__)

import urllib.request, urllib.error, urllib.parse
from urllib.error import HTTPError

import json
import urllib.request, urllib.error, urllib.parse

def get_youtube_thumbnail(id):
    return 'http://img.youtube.com/vi/{0}/0.jpg'.format(id)

def get_vimeo_thumbnail(id):
    url = 'http://vimeo.com/api/v2/video/{0}.json'.format(id)
    try:
        result = read_from_url(url)
    except Exception as e:
        logger.warning(str(e))
        return ''
    else:
        return json.loads(result)[0]['thumbnail_large']

def read_from_url(url): # pragma: no cover
    try:
        return urllib.request.urlopen(url).read()
    except HTTPError:
        trace = sys.exc_info()[2]
        raise Exception("Failed to fetch url: {0}".format(url)).with_traceback(trace)
