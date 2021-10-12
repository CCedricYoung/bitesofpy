from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass, field
from datetime import date
from operator import itemgetter
from os import getenv
from pathlib import Path
from textwrap import dedent
from typing import Any, List, NamedTuple, Optional
from urllib.request import urlretrieve

from bs4 import BeautifulSoup as Soup  # type: ignore

TMP = getenv("TMP", "/tmp")
TODAY = date.today()
Candidate = namedtuple("Candidate", "name votes")
LeaderBoard = namedtuple(
    "LeaderBoard", "Candidate Average Delegates Contributions Coverage"
)


class Poll(NamedTuple):
    Poll: str
    Date: str
    Sample: str
    Sanders: float
    Biden: float
    Gabbard: float
    Spread: str


@dataclass
class File:
    name: str  # The filename that will be created on the filesystem.
    path: Path = field(init=False, hash=False)

    def __post_init__(self):
        self.path = Path(TMP, f"{TODAY}_{self.name}")

    @property
    def data(self) -> Optional[str]:
        return self.path.exists() and self.path.read_text() or None


@dataclass
class Web:
    """Web object.

    Web is an object that downloads the page from the url that is passed
    to it and stores it in the File instance that is passed to it. If the
    File already exists, it just reads the file, otherwise it downloads it
    and stores it in File.
    """

    url: str  # The url of the web page.
    file: File  # The File object to store the page data into.

    @property
    def data(self) -> Optional[str]:
        """Reads the data from the File object.

        First it checks if the File object has any data. If it doesn't, it retrieves
        it and saves it to the File. It then reads it from the File and returns it.

        Returns:
            Optional[str] -- The string data from the File object.
        """
        result = self.file.data
        if not result:
            urlretrieve(self.url, self.file.path)
            result = self.file.data

        return result

    @property
    def soup(self) -> Soup:
        """Converts string data from File into a BeautifulSoup object.

        Returns:
            Soup -- BeautifulSoup object created from the File.
        """
        return Soup(self.data, "html.parser")


@dataclass
class Site(ABC):
    """Site Abstract Base Class.

    Defines the structure for the objects based on this class and defines the interfaces
    that should be implemented in order to work properly.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        [abstractmethod]
        parse_rows: -> Union[List[LeaderBoard], List[Poll]] -- Parses a BeautifulSoup
            table element and returns the text found in the td elements as
            namedtuples.

        [abstractmethod]
        polls: -> Union[List[LeaderBoard], List[Poll]] -- Does the parsing of the table
            and rows for you. It takes the table index number if given, otherwise
            parses table 0.

        [abstractmethod]
        stats: -- Formats the results from polls into a more user friendly
            representation.
    """

    web: Web

    def cast_float(number: str):
        try:
            return float(number)
        except:
            return 0.0

    def cast_int(number: str):
        try:
            return int(number)
        except:
            return 0

    def find_table(self, loc: int = 0) -> str:
        """Finds the table elements from the Soup object

        Keyword Arguments:
            loc {int} -- Parses the Web object for table elements and
                returns the first one that it finds unless an integer representing
                the required table is passed. (default: {0})

        Returns:
            str -- The html table
        """
        return self.web.soup.find_all("table")[loc]

    @abstractmethod
    def parse_rows(self, table: Soup) -> List[Any]:
        """Abstract Method

        Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a BeautifulSoup table element and
                returns the text found in the td elements as NamedTuple.

        Returns:
            List[NamedTuple] -- List of NamedTuple that were created from the
                table data.
        """
        pass

    @abstractmethod
    def polls(self, table: int = 0) -> List[Any]:
        """Abstract Method

        Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[NamedTuple] -- List of NamedTuple that were created from the
                table data.
        """
        pass

    @abstractmethod
    def stats(self, loc: int = 0):
        """Abstract Method

        Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.
        """
        pass


@dataclass
class RealClearPolitics(Site):
    """RealClearPolitics object.

    RealClearPolitics is a custom class to parse a Web instance from the
    realclearpolitics website.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        parse_rows: -> List[Poll] -- Parses a BeautifulSoup table element and
            returns the text found in the td elements as Poll namedtuples.

        polls: -> List[Poll] -- Does the parsing of the table and rows for you.
            It takes the table index number if given, otherwise parses table 0.

        stats: -- Formats the results from polls into a more user friendly
            representation:

            Example:

            RealClearPolitics
            =================
                Biden: 214.0
              Sanders: 142.0
              Gabbard: 6.0

    """

    def parse_rows(self, table: Soup) -> List[Poll]:
        """Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a BeautifulSoup table element and
                returns the text found in the td elements as Poll namedtuples.

        Returns:
            List[Poll] -- List of Poll namedtuples that were created from the
                table data.
        """

        results = [
            Poll(*[x.contents[0].string for x in row.contents])
            for row in table.contents[2:]
        ]

        results = [
            Poll(
                x.Poll,
                x.Date,
                x.Sample,
                Site.cast_float(x.Biden),
                Site.cast_float(x.Sanders),
                Site.cast_float(x.Gabbard),
                x.Spread,
            )
            for x in results
        ]

        return results

    def polls(self, table: int = 0) -> List[Poll]:
        """Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[Poll] -- List of Poll namedtuples that were created from the
                table data.
        """
        table = self.find_table(table)
        return self.parse_rows(table)

    def stats(self, loc: int = 0):
        """Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.

        """
        polls = self.polls(loc)
        biden = sum([x.Biden for x in polls])
        sanders = sum([x.Sanders for x in polls])
        gabbard = sum([x.Gabbard for x in polls])
        results = sorted(
            [
                ("Biden", biden),
                ("Sanders", sanders),
                ("Gabbard", gabbard),
            ],
            key=itemgetter(1),
        )
        max_len = max([len(x[0]) for x in results]) + 2
        results = [f"{x[0]: >{max_len}}: {x[1]}" for x in results]

        title = "RealClearPolitics"
        message = [title, f'{"=" * len(title)}'] + results

        message = "\n" + "\n".join(message) + "\n"
        print(message)


@dataclass
class NYTimes(Site):
    """NYTimes object.

    NYTimes is a custom class to parse a Web instance from the nytimes website.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        parse_rows: -> List[LeaderBoard] -- Parses a BeautifulSoup table element and
            returns the text found in the td elements as LeaderBoard namedtuples.

        polls: -> List[LeaderBoard] -- Does the parsing of the table and rows for you.
            It takes the table index number if given, otherwise parses table 0.

        stats: -- Formats the results from polls into a more user friendly
            representation:

            Example:

            NYTimes
            =================================

                               Pete Buttigieg
            ---------------------------------
            National Polling Average: 10%
                   Pledged Delegates: 25
            Individual Contributions: $76.2m
                Weekly News Coverage: 3

    """

    web: Web

    def parse_rows(self, table: Soup) -> List[LeaderBoard]:
        """Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a BeautifulSoup table element and
                returns the text found in the td elements as LeaderBoard namedtuples.

        Returns:
            List[LeaderBoard] -- List of LeaderBoard namedtuples that were created from
            the table data.
        """
        results = [
            [
                [z.text.strip() for z in y.contents if not z == "\n"]
                for y in x.contents
                if not y == "\n"
            ]
            for x in table.contents
            if not x == "\n"
        ][1][:3]

        results = [
            LeaderBoard(
                Candidate=x[0],
                Average=x[1],
                Contributions=x[3],
                Delegates=Site.cast_int(x[2]),
                Coverage=Site.cast_int(x[4].replace("#", "")),
            )
            for x in results
        ]

        return results

    def polls(self, table: int = 0) -> List[LeaderBoard]:
        """Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[LeaderBoard] -- List of LeaderBoard namedtuples that were created from
                the table data.
        """
        table = self.find_table(table)
        return self.parse_rows(table)

    def stats(self, loc: int = 0):
        """Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.
        """
        polls = self.polls(loc)

        message = ["NYTimes", f'{"=" * 33}', ""]

        results = [
            dedent(
                f"""
            {x.Candidate: >33}
            ---------------------------------
            National Polling Average: {x.Average}
                   Pledged Delegates: {x.Delegates}
            Individual Contributions: {x.Contributions}
                Weekly News Coverage: {x.Coverage}
            """
            )
            for x in polls
        ]

        message = "\n" + "\n".join(message + results) + "\n"
        print(message)


def gather_data():
    rcp_file = File("realclearpolitics.html")
    rcp_url = "https://bites-data.s3.us-east-2.amazonaws.com/2020-03-10_realclearpolitics.html"
    rcp_web = Web(rcp_url, rcp_file)
    rcp = RealClearPolitics(rcp_web)
    rcp.stats(3)

    nyt_file = File("nytimes.html")
    nyt_url = "https://bites-data.s3.us-east-2.amazonaws.com/2020-03-10_nytimes.html"
    nyt_web = Web(nyt_url, nyt_file)
    nyt = NYTimes(nyt_web)
    nyt.stats()


if __name__ == "__main__":
    gather_data()
