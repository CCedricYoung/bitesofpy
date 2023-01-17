import re
from random import randint, shuffle

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

    soup = BeautifulSoup(CONTENT, "html.parser")
    article = (
        soup.find("div", class_="mw-parser-output").find("p").get_text(" ", strip=True)
    )

    words = list(
        {x.lower().replace("-", "") for x in re.findall("[A-Za-z-]+", article)}
    )

    min_num = min(5, len(words))
    max_num = min(16, len(words))
    shuffle(words)
    ix = 0
    sentences = []
    for _ in range(number_of_sentences):
        length = randint(min_num, max_num - 1)
        if ix + length <= len(words) - 1:
            sentences.append(" ".join(words[ix : ix + length]).capitalize() + ".")
            ix += length
        else:
            line = words[ix:]
            shuffle(words)
            line += words[: length - len(line)]
            ix = 0
            sentences.append(" ".join(line).capitalize() + ".")

    return " ".join(sentences)


# wiki_lorem_ipsum(number_of_sentences=5)