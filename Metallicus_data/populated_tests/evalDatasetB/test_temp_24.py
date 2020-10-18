
import pytest
from pattern import en

@pytest.mark.parametrize('value,op', [("weren't", 'be'), ('A man was walking in the rain.', 'a man be walk in the rain .')])
def test_lemma(value, op):
    assert (lemma(value) == op)
