import pytest

@pytest.mark.parametrize('pattern,op', [("<Donald Duck & Co>", "&lt;Donald Duck &amp; Co&gt;")])
def test_escape(pattern, op):
    assert (escape(pattern) == op)
