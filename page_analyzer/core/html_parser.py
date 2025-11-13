from bs4 import BeautifulSoup


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
