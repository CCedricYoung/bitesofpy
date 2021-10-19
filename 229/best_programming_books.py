import os
from dataclasses import dataclass
from pathlib import Path
from urllib.request import urlretrieve

from bs4 import BeautifulSoup

url = "https://bites-data.s3.us-east-2.amazonaws.com/" "best-programming-books.html"
tmp = Path(os.getenv("TMP", "/tmp"))
html_file = tmp / "books.html"

if not html_file.exists():
    urlretrieve(url, html_file)


@dataclass
class Book:
    """Book class should instantiate the following variables:

    title - as it appears on the page
    author - should be entered as lastname, firstname
    year - four digit integer year that the book was published
    rank - integer rank to be updated once the books have been sorted
    rating - float as indicated on the page
    """

    title: str
    author: str
    year: int
    rank: int
    rating: float

    def _ordering(book):
        return (book.rating * -1, book.year, book.title.title(), book.author.split()[0])

    def __lt__(self, other):
        return Book._ordering(self) < Book._ordering(other)

    def __str__(self):
        result = f"[{self.rank:03}] {self.title} ({self.year})"
        result += f"\n      {self.author} {self.rating:.2f}"
        if '00' == result[-2:]:
            result = result[:-1]

        if '0' == result[-1] and '.' == result[-3]:
            result = result[:-1]

        return result


def _get_soup(file):
    return BeautifulSoup(file.read_text(), "html.parser")


def display_books(books, limit=10, year=None):
    """Prints the specified books to the console

    :param books: list of all the books
    :param limit: integer that indicates how many books to return
    :param year: integer indicating the oldest year to include
    :return: None
    """
    results = [x for x in books if not year or x.year >= year][:limit]

    for x in results:
        print(x)


def load_data():
    """Loads the data from the html file

    Creates the soup object and processes it to extract the information
    required to create the Book class objects and returns a sorted list
    of Book objects.

    Books should be sorted by rating, year, title, and then by author's
    last name. After the books have been sorted, the rank of each book
    should be updated to indicate this new sorting order.The Book object
    with the highest rating should be first and go down from there.
    """
    soup = _get_soup(html_file)

    books = []
    for x in soup.find_all(attrs={"class": "book"}):
        try:
            title = x.find(attrs={"class": "main"}).text
            rating = float(x.find(attrs={"class": "rating"}).text)
            year = int(x.find(attrs={"class": "date"}).contents[2])
            author = x.find(attrs={"class": "authors"}).contents[0].text.split()
            author = f'{author[-1]}, {" ".join(author[0:-1])}'
            if "python" in title.lower():
                books.append(
                    Book(title=title, author=author, year=year, rating=rating, rank=-1)
                )
        except:
            pass

    books.sort()
    for x, y in enumerate(books):
        y.rank = x + 1

    return books


def main():
    books = load_data()
    display_books(books, limit=5, year=2017)
    """If done correctly, the previous function call should display the
    output below.
    """


if __name__ == "__main__":
    main()

"""
[001] Python Tricks (2017)
      Bader, Dan 4.74
[002] Mastering Deep Learning Fundamentals with Python (2019)
      Wilson, Richard 4.7
[006] Python Programming (2019)
      Fedden, Antony Mc 4.68
[007] Python Programming (2019)
      Mining, Joseph 4.68
[009] A Smarter Way to Learn Python (2017)
      Myers, Mark 4.66
"""
