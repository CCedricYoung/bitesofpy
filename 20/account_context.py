class Account:
    def __init__(self):
        self._transactions = []

    @property
    def balance(self):
        return sum(self._transactions)

    def __add__(self, amount):
        self._transactions.append(amount)

    def __sub__(self, amount):
        self._transactions.append(-amount)

    def __enter__(self):
        self._prev_index = len(self._transactions)
        return self

    def __exit__(self, type, value, traceback):
        if self.balance < 0:
            self._transactions = self._transactions[: self._prev_index]
            del self._prev_index
