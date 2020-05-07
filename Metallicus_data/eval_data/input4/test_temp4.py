import pytest

@pytest.mark.parametrize('value,whitelist,op', [('email@here.com', None,True)])
def test_email(value,whitelist,op):
    assert (email(value,whitelist) == op)
