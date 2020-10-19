import pytest
from pattern import en

@pytest.mark.parametrize('value,op', [("The cat is eating (e.g., a fish). Yum.", ["The cat is eating ( e.g. , a fish ) .", "Yum ."])])
def test_tokenize(value, op):
    assert (tokenize(value) == op)
