import junit.framework.TestCase;

public class BlankTest extends TestCase {
	public void testblank() {
		assertEquals(true, StringUtils.isBlank(" "));
	}
}