import pytest
from pattern import en

@pytest.mark.parametrize('value,op', [("weren't", "be")])
def test_lemma(value, op):
    assert (lemma(value) == op) #en.inflect.lemma
