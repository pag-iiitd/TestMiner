import pytest

@pytest.mark.parametrize('value,op', [('123-12312-asdasda', True)])
def test_slug(value, op):
    assert (slug(value) == op)
