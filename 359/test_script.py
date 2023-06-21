import pytest
from typer.testing import CliRunner

from script import app


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


def test_subtract(runner) -> None:
    result = runner.invoke(app, ["subtract", "1", "2"])
    assert result.exit_code == 0
    assert "The delta is -1" in result.output


def test_subtract_help(runner) -> None:
    result = runner.invoke(app, ["subtract", "--help"])
    assert result.exit_code == 0
    assert "The value of the first summand" in result.output
    assert "The value of the second summand" in result.output


@pytest.mark.parametrize(
    "c,d,comparison", [(1, 2, "greater"), (4, 3, "not greater"), (5, 5, "not greater")]
)
def test_compare(runner, c, d, comparison) -> None:
    result = runner.invoke(app, ["compare", f"{c}", f"{d}"])
    assert result.exit_code == 0
    assert f"d={d} is {comparison} than c={c}" in result.output


def test_compare_help(runner) -> None:
    result = runner.invoke(app, ["compare", "--help"])
    assert result.exit_code == 0
    assert "First number to compare against." in result.output
    assert "Second number that is compared against first number." in result.output