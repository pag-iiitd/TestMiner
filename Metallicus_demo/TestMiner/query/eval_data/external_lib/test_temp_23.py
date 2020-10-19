import pytest
from pattern import en

@pytest.mark.parametrize('value,op', [("A great day!", 0.1)])
def test_polarity(value, op):
    assert (polarity(value) == op)
