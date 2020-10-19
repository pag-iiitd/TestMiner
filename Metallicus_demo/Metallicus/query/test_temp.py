import pytest

@pytest.mark.parametrize('value,op', [('255.255.10.1', True)])
def test_ip(value, op):
    assert (is_ip(value) == op)
