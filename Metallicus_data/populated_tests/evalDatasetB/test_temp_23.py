
import pytest
from pattern import en

@pytest.mark.parametrize('value,op', [('A great day!', 1.0), ('Beautiful is better than ugly.', 0.0), ('Explicit is better than implicit.', 1.0), ('Simple is better than complex.', 0.0)])
def test_polarity(value, op):
    assert (polarity(value) == op)
