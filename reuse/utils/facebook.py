from django.utils import simplejson as json
import urllib

FACEBOOK_GRAPH_API_URL = 'https://graph.facebook.com'

"""

"""
def facebook_request(relative_url, access_token):
    try:
        url = '%s/%s' % (FACEBOOK_GRAPH_API_URL, relative_url)
        url += ('&' if '?' in relative_url else '?') + 'access_token=%s' % (access_token,)

        data = urllib.urlopen(url).read()
        response = json.loads(data)

        return response
    except:
        raise


"""

"""
def facebook_batch_request(requests, access_token):
    try:
        url = '%s/?access_token=%s' % (FACEBOOK_GRAPH_API_URL, access_token)
        payload = urllib.urlencode({
            'batch': json.dumps(requests),
        })
        data = urllib.urlopen(url, payload).read()
        responses = json.loads(data)

        return responses
    except:
        raise
