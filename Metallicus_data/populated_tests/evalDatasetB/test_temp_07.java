import junit.framework.TestCase;

public class RevTest extends TestCase {

    public void testreverse() {
        assertEquals("ddcc bbaa", StringUtils.reverse("aabb ccdd"));
        assertEquals("", StringUtils.reverse(""));
        assertEquals("x", StringUtils.reverse("x"));
        assertEquals("!!!", StringUtils.reverse("!!!"));
        assertEquals("dlrow olleh", StringUtils.reverse("hello world"));
    }
}
