import junit.framework.TestCase;

public class SampleTest extends TestCase {

    public void testemail() {
        assertEquals("email@example.com", Validation.assertValidEmailAddress("email@example.com"));
        assertEquals(true, Validation.assertValidEmailAddress("email@here.com"));
        assertEquals(true, Validation.assertValidEmailAddress("weirder-email@here.and.there.com"));
        assertEquals(true, Validation.assertValidEmailAddress("email@[127.0.0.1]"));
        assertEquals(true, Validation.assertValidEmailAddress("example@valid-----hyphens.com"));
        assertEquals(true, Validation.assertValidEmailAddress("example@valid-with-hyphens.com"));
        assertEquals(true, Validation.assertValidEmailAddress("test@domain.with.idn.tld.\\xe0\\xa4\\x89\\xe0\\xa4\\xa6\\xe0\\xa4\\xbe\\xe0\\xa4\\xb9\\xe0\\xa4\\xb0\\xe0\\xa4\\xa3.\\xe0\\xa4\\xaa\\xe0\\xa4\\xb0\\xe0\\xa5\\x80\\xe0\\xa4\\x95\\xe0\\xa5\\x8d\\xe0\\xa4\\xb7\\xe0\\xa4\\xbe"));
        assertEquals(true, Validation.assertValidEmailAddress("email@localhost"));
        assertEquals(true, Validation.assertValidEmailAddress("email@localdomain"));
        assertEquals(true, Validation.assertValidEmailAddress("\"test@test\"@example.com"));
        assertEquals(true, Validation.assertValidEmailAddress("\"\\\t\"@here.com"));
        assertEquals(false, Validation.assertValidEmailAddress(null));
        assertEquals(false, Validation.assertValidEmailAddress(""));
        assertEquals(false, Validation.assertValidEmailAddress("abc"));
        assertEquals(false, Validation.assertValidEmailAddress("abc@"));
        assertEquals(false, Validation.assertValidEmailAddress("abc@bar"));
        assertEquals(false, Validation.assertValidEmailAddress("a @x.cz"));
        assertEquals(false, Validation.assertValidEmailAddress("abc@.com"));
        assertEquals(false, Validation.assertValidEmailAddress("something@@somewhere.com"));
        assertEquals(false, Validation.assertValidEmailAddress("email@127.0.0.1"));
        assertEquals(false, Validation.assertValidEmailAddress("example@invalid-.com"));
        assertEquals(false, Validation.assertValidEmailAddress("example@-invalid.com"));
        assertEquals(false, Validation.assertValidEmailAddress("example@inv-.alid-.com"));
        assertEquals(false, Validation.assertValidEmailAddress("example@inv-.-alid.com"));
        assertEquals(false, Validation.assertValidEmailAddress("\"\\\n\"@here.com"));
           }
}
