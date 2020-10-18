import junit.framework.TestCase;

public class EmptyTest extends TestCase {

    public void testEmpty() {
        assertEquals(true, StringUtils.isEmpty(""));
        assertEquals(true, StringUtils.isEmpty(""));
        assertEquals(false, StringUtils.isEmpty(" "));
        assertEquals(false, StringUtils.isEmpty("bob"));
        assertEquals(false, StringUtils.isEmpty("  bob  "));
        assertEquals("", StringUtils.isEmpty(null));
        assertEquals("", StringUtils.isEmpty(""));
        assertEquals("abc", StringUtils.isEmpty("abc"));
        assertEquals(null, StringUtils.isEmpty(null));
        assertEquals(null, StringUtils.isEmpty(null));
        assertEquals("    ", StringUtils.isEmpty(""));
        assertEquals("ab", StringUtils.isEmpty("ab"));
        assertEquals("ab", StringUtils.isEmpty("ab"));
        assertEquals("ab", StringUtils.isEmpty("ab"));
        assertEquals("    ", StringUtils.isEmpty(""));
        assertEquals(" ab ", StringUtils.isEmpty("ab"));
        assertEquals("abcd", StringUtils.isEmpty("abcd"));
        assertEquals(" a  ", StringUtils.isEmpty("a"));
        assertEquals("  a  ", StringUtils.isEmpty("a"));
        assertEquals("xxaxx", StringUtils.isEmpty("a"));
        assertEquals(null, StringUtils.isEmpty(null));
        assertEquals(null, StringUtils.isEmpty(null));
        assertEquals("    ", StringUtils.isEmpty(""));
        assertEquals("ab", StringUtils.isEmpty("ab"));
        assertEquals("ab", StringUtils.isEmpty("ab"));
        assertEquals("ab", StringUtils.isEmpty("ab"));
        assertEquals("    ", StringUtils.isEmpty(""));
        assertEquals(" ab ", StringUtils.isEmpty("ab"));
        assertEquals("abcd", StringUtils.isEmpty("abcd"));
        assertEquals(" a  ", StringUtils.isEmpty("a"));
        assertEquals("  a  ", StringUtils.isEmpty("a"));
        assertEquals("xxaxx", StringUtils.isEmpty("a"));
    }
}
