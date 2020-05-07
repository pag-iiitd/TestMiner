import junit.framework.TestCase;

public class EmailValidatorTest extends TestCase {

    EmailValidator validator = EmailValidator.getInstance();

    public void testEmail() {
        assertEquals(true, validator.isValid("jsmith@apache.org"));
        assertEquals(true, validator.isValid("email@here.com"));
        assertEquals(true, validator.isValid("weirder-email@here.and.there.com"));
        assertEquals(true, validator.isValid("email@[127.0.0.1]"));
        assertEquals(true, validator.isValid("example@valid-----hyphens.com"));
        assertEquals(true, validator.isValid("example@valid-with-hyphens.com"));
        assertEquals(true, validator.isValid("test@domain.with.idn.tld.\\xe0\\xa4\\x89\\xe0\\xa4\\xa6\\xe0\\xa4\\xbe\\xe0\\xa4\\xb9\\xe0\\xa4\\xb0\\xe0\\xa4\\xa3.\\xe0\\xa4\\xaa\\xe0\\xa4\\xb0\\xe0\\xa5\\x80\\xe0\\xa4\\x95\\xe0\\xa5\\x8d\\xe0\\xa4\\xb7\\xe0\\xa4\\xbe"));
        assertEquals(true, validator.isValid("email@localhost"));
        assertEquals(true, validator.isValid("email@localdomain"));
        assertEquals(true, validator.isValid("\"test@test\"@example.com"));
        assertEquals(true, validator.isValid("\"\\\t\"@here.com"));
        assertEquals(false, validator.isValid(null));
        assertEquals(false, validator.isValid(""));
        assertEquals(false, validator.isValid("abc"));
        assertEquals(false, validator.isValid("abc@"));
        assertEquals(false, validator.isValid("abc@bar"));
        assertEquals(false, validator.isValid("a @x.cz"));
        assertEquals(false, validator.isValid("abc@.com"));
        assertEquals(false, validator.isValid("something@@somewhere.com"));
        assertEquals(false, validator.isValid("email@127.0.0.1"));
        assertEquals(false, validator.isValid("example@invalid-.com"));
        assertEquals(false, validator.isValid("example@-invalid.com"));
        assertEquals(false, validator.isValid("example@inv-.alid-.com"));
        assertEquals(false, validator.isValid("example@inv-.-alid.com"));
        assertEquals(false, validator.isValid("\"\\\n\"@here.com"));
    }
}
