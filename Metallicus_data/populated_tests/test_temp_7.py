from validators import *
import pytest

@pytest.mark.parametrize('value,op', [('123-12312-asdasda', True), (' nope', False), ('nope ', False), (' nope ', False), ('#nope', False), ('-nope-', False), ('-no-no-no-', False), ('100%no-slug!', False), ('NOT-AS-UPPERCASE', False), (1, False), (['xx'], False), ({
    
}, False), (False, False), ((1, 2, 3), False), ('<object object at 0x000002095EBA7F50>', False), ('yep-i-am-a-slug', True), ('yep-i-am-a-slug', True), ('yep.i.am.a.slug', True), ('yep_i_am_a_slug', True), ('2bc1c94f-0deb-43e9-92a1-4775189ec9f8', True), ('2bc1c94f-deb-43e9-92a1-4775189ec9f8', False), ('2bc1c94f-0deb-43e9-92a1-4775189ec9f', False), ('gbc1c94f-0deb-43e9-92a1-4775189ec9f8', False), ('2bc1c94f 0deb-43e9-92a1-4775189ec9f8', False)])
def test_slug(value, op):
    assert (slug(value) == op)
