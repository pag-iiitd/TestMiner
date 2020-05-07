from string_utils import *
import pytest

@pytest.mark.parametrize('value,sign,op', [('yep-i-am-a-slug','-', True), ('123-12312-asdasda', '-', True), ('123____123', '-', True), ('dsadasd-dsadas', '-', True), ('some.slug', '-', False), ('1231321%', '-', False), (21312, '-', False), ('123asda&', '-', False)])
def test_slug(value, sign, op):
    assert (is_slug(value,sign) == op)
