import junit.framework.TestCase;

public class BlankTest extends TestCase {

    public void testblank() {
        assertEquals(true, StringUtils.isBlank(" "));
        assertEquals(true, StringUtils.isBlank(null));
        assertEquals(true, StringUtils.isBlank(""));
        assertEquals(true, StringUtils.isBlank(" "));
        assertEquals(false, StringUtils.isBlank("bob"));
        assertEquals(false, StringUtils.isBlank("  bob  "));
        assertEquals(false, StringUtils.isBlank(null));
        assertEquals(false, StringUtils.isBlank(""));
        assertEquals(false, StringUtils.isBlank(" "));
        assertEquals(true, StringUtils.isBlank("bob"));
        assertEquals(true, StringUtils.isBlank("  bob  "));
        assertEquals(false, StringUtils.isBlank(""));
        assertEquals(false, StringUtils.isBlank(" "));
        assertEquals(false, StringUtils.isBlank("\n            \n\n            \n\n            \n\n        "));
        assertEquals(true, StringUtils.isBlank("ciao"));
        assertEquals(true, StringUtils.isBlank(" hi "));
        assertEquals(true, StringUtils.isBlank(1));
        assertEquals(true, StringUtils.isBlank(" @*& "));
        assertEquals(true, StringUtils.isBlank(Ellipsis));
    }
}

