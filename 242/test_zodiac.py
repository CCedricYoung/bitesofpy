from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from urllib.request import urlretrieve

import pytest

from zodiac import (
    get_signs,
    get_sign_with_most_famous_people,
    signs_are_mutually_compatible,
    get_sign_by_date,
)

# original source: https://zodiacal.herokuapp.com/api
URL = "https://bites-data.s3.us-east-2.amazonaws.com/zodiac.json"
TMP = os.getenv("TMP", "/tmp")
PATH = Path(TMP, "zodiac.json")


@pytest.fixture(scope="module")
def data():
    if not PATH.exists():
        urlretrieve(URL, PATH)
    with open(PATH) as f:
        data = json.loads(f.read())
    return data


@pytest.fixture(scope="module")
def signs(data):
    return get_signs(data)


def test_get_signs(data):
    signs = get_signs(data)
    assert len(signs) == 12
    assert signs[0].name == "Aries"
    assert signs[-1].name == "Pisces"
    assert str(signs[0].__class__) == "<class 'zodiac.Sign'>"


def test_get_sign_with_most_famous_people(signs):
    most_famous = get_sign_with_most_famous_people(signs)
    assert most_famous == ("Scorpio", 35)


def test_signs_are_mutually_compatible(signs):
    assert signs_are_mutually_compatible(signs, "Aries", "Leo")
    assert signs_are_mutually_compatible(signs, "Leo", "Aries")
    assert not signs_are_mutually_compatible(signs, "Aries", "Aries")


def test_get_sign_by_date(signs):
    start = datetime.strptime(signs[0].sun_dates[0], "%B %d")
    end = datetime.strptime(signs[0].sun_dates[1], "%B %d")
    a_day = timedelta(days=1)

    assert get_sign_by_date(signs, start) == signs[0].name
    assert get_sign_by_date(signs, end) == signs[0].name

    assert get_sign_by_date(signs, start + a_day) == signs[0].name
    assert get_sign_by_date(signs, end - a_day) == signs[0].name

    assert get_sign_by_date(signs, start - a_day) != signs[0].name
    assert get_sign_by_date(signs, end + a_day) != signs[0].name
