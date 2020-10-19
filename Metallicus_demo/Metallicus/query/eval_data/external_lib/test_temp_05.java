import junit.framework.TestCase;

public class PalTest extends TestCase {
	public void testpalindrome() {
		assertEquals(true, StringUtils.isPalindrome("aabbsbbaa"));
	}
}
