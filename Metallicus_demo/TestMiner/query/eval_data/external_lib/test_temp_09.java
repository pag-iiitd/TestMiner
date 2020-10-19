import junit.framework.TestCase;

public class TruncTest extends TestCase {

    public void testtruncate() {
        assertEquals("te", StringUtils.truncate("test", 2, "START", false, "<...>"));
}
}