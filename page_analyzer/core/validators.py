from urllib.parse import urlparse

from validators import url


def validator(new_url):
    if not url(new_url):
        return False
    non_normilized_url = urlparse(new_url)
    normilized_url = (non_normilized_url.scheme + "://" 
                      + non_normilized_url.hostname)
    return normilized_url

