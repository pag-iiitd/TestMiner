import junit.framework.TestCase;

public class SampleTest extends TestCase {
	public void testemail() {
		assertEquals("email@example.com", Validation.assertValidEmailAddress("email@example.com"));
		
	}
}