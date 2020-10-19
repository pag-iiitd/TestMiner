import junit.framework.TestCase;

public class RevTest extends TestCase {

    public void testreverse() {
        assertEquals("ddcc bbaa", StringUtils.reverse("aabb ccdd"));
            }
}

