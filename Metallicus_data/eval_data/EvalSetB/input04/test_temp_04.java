import junit.framework.TestCase;

public class ContainsTest extends TestCase {
	public void testcontains() {
		assertEquals(true, StringUtils.contains("testcases", "TE", true));
	}
}
