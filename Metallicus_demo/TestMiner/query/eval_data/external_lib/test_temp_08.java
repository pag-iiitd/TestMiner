import junit.framework.TestCase;

public class KebabCaseTest extends TestCase {
	public void testkebabcase() {
		assertEquals("test-test", StringUtils.toKebabCase("test test"));
	}
}
