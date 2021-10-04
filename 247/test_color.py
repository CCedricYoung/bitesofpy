from unittest.mock import patch

import pytest

import color


@pytest.fixture(scope="module")
def gen():
    return color.gen_hex_color()


def test_gen_hex_color(gen):
    with patch("color.sample") as mock_sample:
        mock_sample.return_value = (0, 256, 255)
        val = next(gen)
        mock_sample.assert_called_with(range(0, 256), 3)
        assert val == "#00100FF"