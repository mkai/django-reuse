import httplib
import urllib
import urllib2
import json

FACEBOOK_GRAPH_API_URL = 'https://graph.facebook.com'


def facebook_request(relative_url, access_token):
    """
    Loads data from the Facebook Graph API using a single requests.

    Raises ValueError if the specified OAuth access token has become invalid.

    """
    url = '%s/%s' % (FACEBOOK_GRAPH_API_URL, relative_url)
    url += ('&' if '?' in relative_url else '?') + 'access_token=%s' % (
        access_token,)
    try:
        data = urllib2.urlopen(url).read()
    except (httplib.HTTPException, urllib2.HTTPError, urllib2.URLError), e:
        if e.code == 400:  # OAuth token invalid
            raise ValueError(e)

    # TODO: do error handling in the exception handler, not here
    response = json.loads(data)
    error = response.get('error')
    if error:
        if error['type'] == 'OAuthException':
            raise ValueError(error['message'])
        else:
            raise Exception(str(error))
    return response


def facebook_batch_request(requests, access_token):
    """
    Loads multiple sets of data from the Facebook Graph API in a single,
    batched request.

    Raises ValueError if the specified OAuth access token has become invalid.

    """
    if not requests:
        return []

    url = '%s/?access_token=%s' % (FACEBOOK_GRAPH_API_URL, access_token)
    payload = urllib.urlencode({'batch': json.dumps(requests), })
    try:
        data = urllib2.urlopen(url, payload).read()
    except (httplib.HTTPException, urllib2.HTTPError, urllib2.URLError):
        return []

    responses = json.loads(data)
    if not isinstance(responses, list):
        error = responses.get('error')
        if error['type'] == 'OAuthException':
            raise ValueError(error['message'])
        else:
            raise Exception(str(error))
    return responses
