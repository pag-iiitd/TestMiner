import junit.framework.TestCase;

public class AnagramTest extends TestCase {
	public void testAnagram() {
		assertEquals(true, StringUtils.areAnagram("adba ajna", "njaaaadb "));
	}
}