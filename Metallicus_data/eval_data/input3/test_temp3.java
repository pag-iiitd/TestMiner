import junit.framework.TestCase;
public class EmailValidatorTest extends TestCase {
	EmailValidator validator=EmailValidator.getInstance();
	public void testEmail() {
		assertEquals(true, validator.isValid("jsmith@apache.org"));
	
	}

	}