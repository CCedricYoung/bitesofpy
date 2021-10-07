scores = [10, 50, 100, 175, 250, 400, 600, 800, 1000]
ranks = "white yellow orange green blue brown black paneled red".split()
BELTS = dict(zip(scores, ranks))


class NinjaBelt:
    def __init__(self, score=0):
        self._score = score
        self._last_earned_belt = None

    def _get_belt(self, new_score):
        indexes = [x for x, val in enumerate(scores) if val <= new_score]
        return indexes and ranks[indexes[-1]] or "None"

    def _get_score(self):
        return self._score

    def _set_score(self, new_score):
        if not isinstance(new_score, int):
            raise ValueError("Score takes an int")

        if new_score < self.score:
            raise ValueError("Cannot lower score")

        rank = self._get_belt(new_score)
        self._score = new_score
        if rank != self._last_earned_belt:
            print(
                f"Congrats, you earned {new_score} points obtaining the PyBites Ninja {rank.capitalize()} Belt"
            )
            self._last_earned_belt = rank
        else:
            print(f"Set new score to {new_score}")

    score = property(_get_score, _set_score)
