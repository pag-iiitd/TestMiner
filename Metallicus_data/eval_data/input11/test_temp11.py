import pytest

@pytest.mark.parametrize('address,public,op', [('http://foobar.museum/foobar', False, True),])
def test_url(address, public, op):
    assert (url(address,public) == op)
