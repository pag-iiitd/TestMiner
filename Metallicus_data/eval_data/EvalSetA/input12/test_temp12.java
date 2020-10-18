import junit.framework.TestCase;
public class UrlValidatorTest extends TestCase {
	UrlValidator validator = new UrlValidator();
	public void testUrl() {
		assertEquals(true, validator.isValid("http://localhost/test/index.html"));
	
	}

	}