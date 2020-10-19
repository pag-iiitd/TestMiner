import junit.framework.TestCase;

public class SampleTest extends TestCase {
	public void testnonempty() {
		assertEquals("hello", Validation.assertNonemptyString("hello"));
		
	}
}