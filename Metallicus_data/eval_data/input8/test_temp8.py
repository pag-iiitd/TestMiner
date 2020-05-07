import pytest

@pytest.mark.parametrize('value,op', [('me@foo.com', True)])
def test_email(value, op):
    assert (is_email(value) == op)
