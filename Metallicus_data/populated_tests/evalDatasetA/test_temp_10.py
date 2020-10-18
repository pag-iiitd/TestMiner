from xml.sax.saxutils import escape
import pytest

@pytest.mark.parametrize('pattern,op', [('<Donald Duck & Co>', '&lt;Donald Duck &amp; Co&gt;'), ('a<b>c"d\'e&f', 'a&lt;b&gt;c&quot;d&apos;e&amp;f'), ('a\tb\nc\nd', 'a\tb\nc\nd'), ('a\x00\x01\x08\x0b\x0c\x0e\x1fb', 'ab'), ('a\ud7ff\ud800 \udfff \ue000b', 'a\ud7ff  \ue000b'), ('a�\ufffe\uffffb', 'a�b'), ('a~\x7f\x84\x85\x86\x9f\xa0b', 'a~&#127;&#132;\x85&#134;&#159;\xa0b')])
def test_escape(pattern, op):
    assert (escape(pattern) == op)
