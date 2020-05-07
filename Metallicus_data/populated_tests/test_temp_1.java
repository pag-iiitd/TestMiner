import junit.framework.TestCase;
import com.google.common.escape.CharEscaper;

public class XmlEscapersTest extends TestCase {

    public void testXmlContentEscaper() {
        assertEquals("a&quot;b&lt;c&gt;d&amp;e&quot;f", XmlEscapers.xmlAttributeEscaper().escape("a\"b<c>d&e\"f"));
        assertEquals("a&lt;b&gt;c&quot;d&apos;e&amp;f", XmlEscapers.xmlAttributeEscaper("a<b>c\"d'e&f"));
        assertEquals("a\tb\nc\nd", XmlEscapers.xmlAttributeEscaper("a\tb\nc\nd"));
        assertEquals("ab", XmlEscapers.xmlAttributeEscaper("a 
b"));
        assertEquals("a\ud7ff  \ue000b", XmlEscapers.xmlAttributeEscaper("a\ud7ff\ud800 \udfff \ue000b"));
        assertEquals("a\ufffdb", XmlEscapers.xmlAttributeEscaper("a\ufffd\ufffe\uffffb"));
        assertEquals("a&lt;b&gt;c&quot;d&apos;e&amp;f", XmlEscapers.xmlAttributeEscaper("a<b>c\"d'e&f"));
        assertEquals("a\tb\nc\nd", XmlEscapers.xmlAttributeEscaper("a\tb\nc\nd"));
        assertEquals("ab", XmlEscapers.xmlAttributeEscaper("a b"));
        assertEquals("a&#1;&#8;&#11;&#12;&#14;&#31;b", XmlEscapers.xmlAttributeEscaper("a
b"));
        assertEquals("a\ud7ff  \ue000b", XmlEscapers.xmlAttributeEscaper("a\ud7ff\ud800 \udfff \ue000b"));
        assertEquals("a\ufffdb", XmlEscapers.xmlAttributeEscaper("a\ufffd\ufffe\uffffb"));
    }
}