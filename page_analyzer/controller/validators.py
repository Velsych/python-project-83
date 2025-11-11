from urllib.parse import urlparse

from bs4 import BeautifulSoup
from validators import url


def validator(new_url):
    if not url(new_url):
        return False
    non_normilized_url = urlparse(new_url)
    normilized_url = (non_normilized_url.scheme + "://" 
                      + non_normilized_url.hostname)
    return normilized_url


def html_parser(html):
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find('h1')
    if not h1:
        h1 = ''
    else:
        h1 = h1.text
    title = soup.find('title')
    if not title:
        title = ''
    else:
        title = title.text
    found_desc = soup.find_all(attrs={'name': "description"})
    if found_desc:
        first_meta_desc = found_desc[0]
        description = first_meta_desc['content']
    else:
        description = ''
    return h1, title, description
