import junit.framework.TestCase;

public class LenTest extends TestCase {

    public void testlength() {
        assertEquals(4, StringUtils.length("test"));
        assertEquals(5, StringUtils.length("Hello"));
        assertEquals(true, StringUtils.length("password"));
        assertEquals(true, StringUtils.length("password"));
        assertEquals(true, StringUtils.length("password"));
        assertEquals(true, StringUtils.length("password"));
        assertEquals(true, StringUtils.length("something"));
        assertEquals(true, StringUtils.length("something"));
        assertEquals(true, StringUtils.length("something"));
        assertEquals(true, StringUtils.length("something"));
        assertEquals(0, StringUtils.length(""));
        assertEquals(0, StringUtils.length(""));
        assertEquals(1, StringUtils.length("A"));
        assertEquals(1, StringUtils.length(" "));
        assertEquals(8, StringUtils.length("ABCDEFGH"));
        assertEquals(0, StringUtils.length(""));
        assertEquals(1, StringUtils.length("A"));
        assertEquals(1, StringUtils.length(" "));
        assertEquals(8, StringUtils.length("ABCDEFGH"));
        assertEquals(0, StringUtils.length(0));
        assertEquals(0, StringUtils.length(0));
        assertEquals(0, StringUtils.length(0));
        assertEquals(1, StringUtils.length(1));
        assertEquals(1, StringUtils.length(1));
        assertEquals(8, StringUtils.length(8));
        assertEquals(0, StringUtils.length(""));
        assertEquals(0, StringUtils.length(""));
        assertEquals(1, StringUtils.length("A"));
        assertEquals(1, StringUtils.length(" "));
        assertEquals(8, StringUtils.length("ABCDEFGH"));
    }
}
