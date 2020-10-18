import junit.framework.TestCase;

public class EmptyTest extends TestCase {
	public void testEmpty() {
		assertEquals(true, StringUtils.isEmpty(""));
	}
}
