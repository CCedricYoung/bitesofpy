import re
from random import choice, randint

import requests
from bs4 import BeautifulSoup

# live data would be
# https://en.wikipedia.org/wiki/Wikipedia:Today%27s_featured_article/January_1,_2022
FEATURED_ARTICLE = "https://bites-data.s3.us-east-2.amazonaws.com/wiki_features_article_2022-01-01.html"
CONTENT = requests.get(FEATURED_ARTICLE).text


def wiki_lorem_ipsum(article: str = CONTENT, number_of_sentences: int = 5):
    """Create a lorem ipsum block of sentences from the words scraped from today's Wikipedia featured article

    :param article
    :type article: str
    :param number_of_sentences
    :type number_of_sentences: int
    :return: lorem ipsum text (Lorem ipsum is nonsense text used to test layouts for documents or websites)
    rtype: str
    """
    if number_of_sentences < 1:
        raise ValueError()

    soup = BeautifulSoup(article, "html.parser")
    feature_article = soup.select_one(".mw-parser-output p").get_text(" ", strip=True)

    words = list(
        {x.lower().replace("-", "") for x in re.findall("[A-Za-z-]+", feature_article)}
    )

    sentences = [
        " ".join([choice(words) for _ in range(randint(5, 15))]).capitalize() + "."
        for _ in range(number_of_sentences)
    ]

    return " ".join(sentences)