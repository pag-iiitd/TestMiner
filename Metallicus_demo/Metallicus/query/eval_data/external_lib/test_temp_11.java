import junit.framework.TestCase;

public class SampleTest extends TestCase {
	public void testport() {
		assertEquals(2991, Validation.assertValidPortNumber(2991));
	}
}