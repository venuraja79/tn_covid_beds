import pytest

from config import COVID_BEDS_URL
from bed_data import get_bed_data

def test_get_data():
    df = get_bed_data(COVID_BEDS_URL)
    assert df.shape[0] > 0
