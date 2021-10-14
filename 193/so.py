import requests
from bs4 import BeautifulSoup

cached_so_url = "https://bites-data.s3.us-east-2.amazonaws.com/so_python.html"


def top_python_questions(url=cached_so_url):
    """Use requests to retrieve the url / html,
    parse the questions out of the html with BeautifulSoup,
    filter them by >= 1m views ("..m views").
    Return a list of (question, num_votes) tuples ordered
    by num_votes descending (see tests for expected output).
    """
    soup = BeautifulSoup(requests.get(cached_so_url).text, "html.parser")
    questions = sorted(
        [
            (
                q.find(attrs="question-hyperlink").text.strip(),
                int(q.find(attrs="vote-count-post").text.strip()),
            )
            for q in soup.find_all("div", "question-summary")
            if "m views" in q.find(attrs="views").text.strip()
        ],
        key=lambda x: x[1],
        reverse=True,
    )
    return questions
