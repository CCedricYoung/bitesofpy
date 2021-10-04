import os
from pathlib import Path
from ipaddress import IPv4Network
from urllib.request import urlretrieve

import pytest

from ips import ServiceIPRange, parse_ipv4_service_ranges, get_aws_service_range

URL = "https://bites-data.s3.us-east-2.amazonaws.com/ip-ranges.json"
TMP = os.getenv("TMP", "/tmp")
PATH = Path(TMP, "ip-ranges.json")
IP = IPv4Network("192.0.2.8/29")


@pytest.fixture(scope="module")
def json_file():
    """Import data into tmp folder"""
    urlretrieve(URL, PATH)
    return PATH


def test_ips_service_range_parse(json_file):
    service_ranges = parse_ipv4_service_ranges(json_file)
    assert len(service_ranges) == 1886


def test_ips_service_range_str(json_file):
    service_ranges = parse_ipv4_service_ranges(json_file)
    desc = str(service_ranges[0])
    assert "is allocated" in desc
    assert "service in the " in desc
    assert " region" in desc


@pytest.mark.parametrize(
    "address, range_count", [("13.248.118.1", 2), ("192.0.2.8", 0)]
)
def test_ips_address_range_count(json_file, address, range_count):
    service_ranges = parse_ipv4_service_ranges(json_file)
    aws_ranges = get_aws_service_range(address=address, service_ranges=service_ranges)

    assert len(aws_ranges) == range_count


def test_ips_address_exception(json_file):
    service_ranges = parse_ipv4_service_ranges(json_file)

    with pytest.raises(ValueError) as err:
        aws_ranges = get_aws_service_range(
            address="hello world", service_ranges=service_ranges
        )
    assert "Address must be a valid IPv4 address" in str(err)