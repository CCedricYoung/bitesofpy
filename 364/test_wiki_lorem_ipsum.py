import pytest

from wiki_lorem_ipsum import wiki_lorem_ipsum, CONTENT


@pytest.fixture
def valid_words():
    return [
        "both",
        "article",
        "three",
        "to",
        "cymbirhynchus",
        "bird",
        "threatened",
        "along",
        "sometimes",
        "for",
        "species",
        "it",
        "forests",
        "inhabits",
        "twentyone",
        "genus",
        "the",
        "near",
        "due",
        "usually",
        "slightly",
        "have",
        "fourth",
        "or",
        "a",
        "black",
        "than",
        "extensive",
        "on",
        "family",
        "males",
        "they",
        "distinctive",
        "by",
        "deforestation",
        "songbird",
        "in",
        "hatching",
        "insects",
        "macrorhynchos",
        "habitats",
        "eggs",
        "indochina",
        "nest",
        "broadbill",
        "trade",
        "is",
        "only",
        "fish",
        "snails",
        "evaluated",
        "that",
        "breeds",
        "mollusks",
        "with",
        "borneo",
        "asian",
        "trapping",
        "over",
        "neckband",
        "iucn",
        "sumatra",
        "two",
        "full",
        "females",
        "beak",
        "smaller",
        "lowland",
        "runt",
        "found",
        "water",
        "upperparts",
        "blue",
        "yellow",
        "will",
        "population",
        "dry",
        "are",
        "building",
        "secondary",
        "its",
        "hunting",
        "days",
        "incubated",
        "has",
        "egg",
        "underparts",
        "sexes",
        "and",
        "disturbed",
        "maroon",
        "as",
        "conspicuous",
        "blackandred",
        "large",
        "leastconcern",
        "crustaceans",
        "clutches",
        "range",
        "season",
        "feeds",
        "but",
    ]


@pytest.mark.parametrize("sentences, expected", [
    (1, 1), (5, 5), (12, 12)
])
def test_number_of_sentences(sentences, expected):
    sentences = wiki_lorem_ipsum(CONTENT, sentences)
    assert len(sentences.split(". ")) == expected


def test_default_number():
    assert len(wiki_lorem_ipsum(CONTENT).split(". ")) == 5


def test_number_of_words():
    lorem = wiki_lorem_ipsum(CONTENT, 100).split(". ")
    for line in lorem:
        assert line[0].isupper()
        assert len(line.split()) < 16
        assert len(line.split()) > 4


@pytest.mark.parametrize("num_sentences", [0, -1])
def test_for_ValueError(num_sentences):
    with pytest.raises(ValueError):
        wiki_lorem_ipsum(CONTENT, num_sentences)


def test_all_words_are_correct(valid_words):
    lorem = wiki_lorem_ipsum(CONTENT, 100)
    assert all(word.rstrip(".").lower() in valid_words for word in lorem.split())