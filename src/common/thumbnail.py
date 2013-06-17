import urllib2
from urllib2 import HTTPError

def get_youtube_thumbnail(id):
    return 'http://img.youtube.com/vi/{0}/0.jpg'.format(id)

def get_vimeo_thumbnail(id):
    import urllib2
    url = 'http://vimeo.com/api/v2/video/{0}.json'.format(id)
    try:
        openurl = urllib2.urlopen(url)
    except HTTPError:
        print "Failed to fetch url: {0}".format(url)
        return ''
    else:
        result = openurl.read()
        return json.loads(result)[0]['thumbnail_large']
