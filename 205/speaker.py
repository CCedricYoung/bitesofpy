import os
from collections import Counter
from pathlib import Path
from urllib.request import urlretrieve

import gender_guesser.detector as gender
from bs4 import BeautifulSoup as Soup

TMP = Path(os.getenv("TMP", "/tmp"))
PYCON_HTML = TMP / "pycon2019.html"
PYCON_PAGE = "https://bites-data.s3.us-east-2.amazonaws.com/" "pycon2019.html"

if not PYCON_HTML.exists():
    urlretrieve(PYCON_PAGE, PYCON_HTML)


def _get_soup(html=PYCON_HTML):
    return Soup(html.read_text(encoding="utf-8"), "html.parser")


def get_pycon_speaker_first_names(soup=None):
    """Parse the PYCON_HTML using BeautifulSoup, extracting all
    speakers (class "speaker"). Note that some items contain
    multiple speakers so you need to extract them.
    Return a list of first names
    """
    if not soup:
        soup = _get_soup()

    speakers = [x.text.strip() for x in soup.find_all(attrs="speaker")]

    results = []
    for x in speakers:
        if "," in x:
            results.extend(x.split(","))
        elif "/" in x:
            results.extend(x.split("/"))
        else:
            results.append(x)

    results = [x.split()[0] for x in results]
    return results


def get_percentage_of_female_speakers(first_names):
    """Run gender_guesser on the names returning a percentage
    of female speakers (female and mostly_female),
    rounded to 2 decimal places."""
    detector = gender.Detector()
    results = Counter([detector.get_gender(x) for x in first_names])

    percent = round(
        100 * (results["female"] + results["mostly_female"]) / len(first_names), 2
    )
    return percent


if __name__ == "__main__":
    names = get_pycon_speaker_first_names()
    perc = get_percentage_of_female_speakers(names)
    print(perc)
