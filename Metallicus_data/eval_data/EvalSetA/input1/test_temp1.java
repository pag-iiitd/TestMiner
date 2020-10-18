import junit.framework.TestCase;
import com.google.common.escape.CharEscaper;
public class XmlEscapersTest extends TestCase {
	public void testXmlAttributeEscaper() {
		assertEquals("a&quot;b&lt;c&gt;d&amp;e&quot;f", XmlEscapers.xmlAttributeEscaper().escape("a\"b<c>d&e\"f"));	
	}

	}