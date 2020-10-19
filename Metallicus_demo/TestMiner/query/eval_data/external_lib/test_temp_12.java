import junit.framework.TestCase;

public class SampleTest extends TestCase {
	public void testhost() {
		assertEquals("192.192.129.112", Validation.assertValidHostname("192.192.129.112"));
		assertEquals("google.com", Validation.assertValidHostname("google.com"));
		
	}
}