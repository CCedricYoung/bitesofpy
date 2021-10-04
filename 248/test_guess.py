from unittest.mock import patch

import pytest

from guess import GuessGame, InvalidNumber, MAX_NUMBER


@pytest.mark.parametrize(
    "value, message",
    [
        ("some string", "Not a number"),
        (-1, "Negative number"),
        (MAX_NUMBER + 1, "Number too high"),
    ],
)
def test_guess_exception(value, message):
    with pytest.raises(InvalidNumber) as err:
        GuessGame(value)

    assert str(err.value) == message


@pytest.mark.parametrize("secret", range(0, MAX_NUMBER + 1))
def test_guess(secret):
    game = GuessGame(secret)
    assert game


@pytest.mark.parametrize("max_guesses", range(6))
def test_guess_max_tries(max_guesses, capsys):
    with patch("guess.input") as mock_input:
        mock_input.return_value("1")
        game = GuessGame(3, max_guesses=max_guesses)
        game()
        assert mock_input.call_count == max_guesses
        assert capsys.readouterr().out.count("Too low") == max_guesses


def test_guess_default_max_tries(capsys):
    with patch("guess.input") as mock_input:
        mock_input.return_value("1")
        game = GuessGame(3)
        game()
        assert mock_input.call_count == 5
        assert capsys.readouterr().out.count("Too low") == 5


def test_guess_wrong(capsys):
    with patch("guess.input") as mock_input:
        mock_input.return_value("1")
        max_guesses = 1
        game = GuessGame(3, max_guesses=max_guesses)
        game()
        assert mock_input.called

        output = capsys.readouterr().out.splitlines()
        assert output[0] == "Guess a number: "
        assert output[1] == "Too low"
        assert output[2] == "Sorry, the number was 3"


def test_guess_right(capsys):
    with patch("guess.input") as mock_input:
        mock_input.side_effect = ["4", "2", "something", "3"]
        max_guesses = 20
        game = GuessGame(3, max_guesses=max_guesses)
        game()
        assert mock_input.call_count == 4

        output = capsys.readouterr().out.splitlines()
        assert output[0] == "Guess a number: "
        assert output[1] == "Too high"
        assert output[2] == "Guess a number: "
        assert output[3] == "Too low"
        assert output[4] == "Guess a number: "
        assert output[5] == "Enter a number, try again"
        assert output[6] == "Guess a number: "
        assert output[7] == "You guessed it!"
