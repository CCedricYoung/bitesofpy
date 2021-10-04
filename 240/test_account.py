import pytest

from account import Account


@pytest.fixture()
def mine():
    return Account("myself")


def test_account(mine):
    assert mine.owner == "myself"


def test_account__repr__(mine):
    assert repr(mine) == "Account('myself', 0)"


def test_account__str__(mine):
    assert str(mine) == "Account of myself with starting amount: 0"


def test_account_add_transaction_exception(mine):
    with pytest.raises(ValueError) as err:
        mine.add_transaction("boo")

    assert str(err.value) == "please use int for amount"


def test_account_add_transaction(mine):
    mine.add_transaction(1)
    assert mine.balance == 1


def test_account_add_transaction_2(mine):
    mine.add_transaction(2)
    assert mine.balance == 2


@property
def test_account_balance(mine):
    assert mine.balance == 1


def test_account__len__(mine):
    assert len(mine) == 0
    mine.add_transaction(1)
    assert len(mine) == 1


def test_account__getitem__(mine):
    mine.add_transaction(1)
    mine.add_transaction(2)
    mine.add_transaction(5)
    assert mine[2] == 5


def test_account__eq__(mine):
    theirs = Account("theirs")
    assert mine == theirs


def test_account__lt__(mine):
    theirs = Account("theirs")
    theirs.add_transaction(1)
    assert mine < theirs
    assert not mine < mine


def test_account__add__(mine):
    theirs = Account("theirs", 1)
    theirs.add_transaction(2)
    mine += theirs
    assert mine.balance == 3
    assert mine.owner == "myself&theirs"