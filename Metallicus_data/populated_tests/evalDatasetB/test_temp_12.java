import junit.framework.TestCase;

public class SampleTest extends TestCase {

    public void testhost() {
        assertEquals("192.192.129.112", Validation.assertValidHostname("192.192.129.112"));
        assertEquals("google.com", Validation.assertValidHostname("google.com"));
        assertEquals(true, Validation.assertValidHostname("24.25.231.12"));
        assertEquals(false, Validation.assertValidHostname("2.41.32.324"));
        assertEquals(true, Validation.assertValidHostname("135.14.44.12"));
        assertEquals(false, Validation.assertValidHostname("154.123.441.123"));
        assertEquals(true, Validation.assertValidHostname("213.25.224.32"));
        assertEquals(false, Validation.assertValidHostname("201.543.23.11"));
        assertEquals(true, Validation.assertValidHostname("229.35.159.6"));
        assertEquals(false, Validation.assertValidHostname("231.54.11.987"));
        assertEquals(true, Validation.assertValidHostname("248.85.24.92"));
        assertEquals(false, Validation.assertValidHostname("250.21.323.48"));
        assertEquals(false, Validation.assertValidHostname("124.14.32.abc"));
        assertEquals(false, Validation.assertValidHostname("23.64.12"));
        assertEquals(false, Validation.assertValidHostname("26.34.23.77.234"));
        assertEquals(true, Validation.assertValidHostname("2001:0438:FFFE:0000:0000:0000:0000:0A35"));
        assertEquals(true, Validation.assertValidHostname("127.0.0.1"));
        assertEquals(true, Validation.assertValidHostname("255.255.255.255"));
        assertEquals(true, Validation.assertValidHostname("140.211.11.130"));
        assertEquals(true, Validation.assertValidHostname("72.14.253.103"));
        assertEquals(true, Validation.assertValidHostname("199.232.41.5"));
        assertEquals(true, Validation.assertValidHostname("216.35.123.87"));
        assertEquals(true, Validation.assertValidHostname("0:0:0:0:0:0:13.1.68.3"));
        assertEquals(true, Validation.assertValidHostname("0:0:0:0:0:FFFF:129.144.52.38"));
        assertEquals(true, Validation.assertValidHostname("::13.1.68.3"));
        assertEquals(true, Validation.assertValidHostname("::FFFF:129.144.52.38"));
        assertEquals(false, Validation.assertValidHostname("::ffff:192.168.1.1:192.168.1.1"));
        assertEquals(false, Validation.assertValidHostname("::192.168.1.1:192.168.1.1"));
           }
}
