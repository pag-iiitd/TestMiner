
import pytest

@pytest.mark.parametrize('address,op', [('dead:beef:0:0:0:0:42:1', True),])
def test_ipv6(address, op):
    assert (ipv6(address) == op)
