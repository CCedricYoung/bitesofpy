import re
from collections import namedtuple
from operator import itemgetter

import bs4
import requests
from bs4 import BeautifulSoup

# feed = https://news.python.sc/, to get predictable results we cached
# first two pages - use these:
# https://bites-data.s3.us-east-2.amazonaws.com/news.python.sc/index.html
# https://bites-data.s3.us-east-2.amazonaws.com/news.python.sc/index2.html

Entry = namedtuple("Entry", "title points comments")


def _create_soup_obj(url):
    """Need utf-8 to properly parse emojis"""
    resp = requests.get(url)
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser")


def _find_nearest_re_int(soup, regex):
    match = regex.search(soup.text)
    if match:
        return int(match.group())

    for x in soup.next_elements:
        if isinstance(x, bs4.element.NavigableString):
            target = x.string.strip()
        else:
            target = x.text.strip()

        match = regex.search(target)
        if match:
            return int(match.group())

    return 0


def get_top_titles(url, top=5):
    """Parse the titles (class 'title') using the soup object.
    Return a list of top (default = 5) titles ordered descending
    by number of points and comments.
    """
    soup = _create_soup_obj(url)

    re_points = re.compile(r"(\d+)(?= points)")
    re_comments = re.compile(r"(\d+)(?= comments)")

    entries = []
    for x in soup.find_all(attrs={"class": "title"}):
        title = x.text.strip()
        points = _find_nearest_re_int(x, re_points)
        comments = _find_nearest_re_int(x, re_comments)
        entries.append(Entry(title=title, points=points, comments=comments))

    return sorted(entries, key=itemgetter(1, 2), reverse=True)[:top]
