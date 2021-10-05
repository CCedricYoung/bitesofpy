import re


class DomainException(Exception):
    """Raised when an invalid is created."""


class Domain:
    def __init__(self, name):
        if not re.match(r".*\.[a-z]{2,3}$", name):
            raise DomainException(f"{name} is an invalid domain")

        self.name = name

    def __str__(self) -> str:
        return self.name

    def parse_url(url):
        return Domain(url.split("//")[-1].split("/")[0])

    def parse_email(email):
        return Domain(email.split("@")[-1])
