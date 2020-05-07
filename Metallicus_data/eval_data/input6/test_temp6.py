
import pytest

@pytest.mark.parametrize('value,sign,op', [('yep-i-am-a-slug', '-', True), ])
def test_slug(value, sign, op):
    assert (is_slug(value, sign) == op)
