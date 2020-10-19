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
    }
}
