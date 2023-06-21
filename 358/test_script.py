import pytest
from typer.testing import CliRunner

from script import app


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


def test_main(runner) -> None:
    result = runner.invoke(app, ["world"])
    assert result.exit_code == 0
    assert "Hello world!" in result.output


def test_main_help(runner) -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "The name of the person to greet." in result.output