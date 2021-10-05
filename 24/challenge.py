from abc import ABC, abstractmethod


class Challenge(ABC):
    def __init__(self, number, title) -> None:
        super().__init__()
        self.number = number
        self.title = title

    @abstractmethod
    def verify(self, something):
        pass

    @property
    @abstractmethod
    def pretty_title(self):
        pass


class BlogChallenge(Challenge):
    def __init__(self, number, title, merged_prs) -> None:
        super().__init__(number, title)
        self.merged_prs = merged_prs

    def verify(self, pr: int):
        return pr in self.merged_prs

    @property
    def pretty_title(self):
        return f"PCC{self.number} - {self.title}"


class BiteChallenge(Challenge):
    def __init__(self, number, title, result) -> None:
        super().__init__(number, title)
        self.result = result

    def verify(self, result: str):
        return result == self.result

    @property
    def pretty_title(self):
        return f"Bite {self.number}. {self.title}"
