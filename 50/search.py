import re
from collections import namedtuple
from datetime import date

import feedparser

FEED = "https://bites-data.s3.us-east-2.amazonaws.com/all.rss.xml"

Entry = namedtuple("Entry", "date title link tags")
SPLIT_RE = re.compile("[|&]")


def _convert_struct_time_to_dt(stime):
    """Convert a time.struct_time as returned by feedparser into a
    datetime.date object, so:
    time.struct_time(tm_year=2016, tm_mon=12, tm_mday=28, ...)
    -> date(2016, 12, 28)
    """
    return date(year=stime.tm_year, month=stime.tm_mon, day=stime.tm_mday)


def get_feed_entries(feed=FEED):
    """Use feedparser to parse PyBites RSS feed.
    Return a list of Entry namedtuples (date = date, drop time part)
    """
    feed = feedparser.parse(feed)
    result = [
        Entry(
            date=_convert_struct_time_to_dt(x.published_parsed),
            title=x.title,
            link=x.link,
            tags=set(map(lambda y: y["term"].lower(), x.tags)),
        )
        for x in feed.entries
    ]
    return result


def filter_entries_by_tag(search, entry):
    """Check if search matches any tags as stored in the Entry namedtuple
    (case insensitive, only whole, not partial string matches).
    Returns bool: True if match, False if not.
    Supported searches:
    1. If & in search do AND match,
       e.g. flask&api should match entries with both tags
    2. Elif | in search do an OR match,
       e.g. flask|django should match entries with either tag
    3. Else: match if search is in tags
    """
    tags = set(SPLIT_RE.split(search.lower()))
    if "|" in search:
        return len(tags & entry.tags) > 0

    return tags <= entry.tags


def main():
    """Entry point to the program
    1. Call get_feed_entries and store them in entries
    2. Initiate an infinite loop
    3. Ask user for a search term:
       - if enter was hit (empty string), print 'Please provide a search term'
       - if 'q' was entered, print 'Bye' and exit/break the infinite loop
    4. Filter/match the entries (see filter_entries_by_tag docstring)
    5. Print the title of each match ordered by date ascending
    6. Secondly, print the number of matches: 'n entries matched'
       (use entry if only 1 match)
    """
    entries = get_feed_entries()
    while True:
        search = input()
        if search == "":
            print("Please provide a search term")
            continue

        if search == "q":
            print("Bye")
            break

        filtered = [x for x in entries if filter_entries_by_tag(search, x)]
        for x in sorted(filtered, key=lambda x: x.title):
            print(x.title)

        print(f"{len(filtered)} entr{len(filtered) == 1 and 'y' or 'ies'} matched")


if __name__ == "__main__":
    main()
