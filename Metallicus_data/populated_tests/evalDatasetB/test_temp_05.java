import junit.framework.TestCase;

public class PalTest extends TestCase {

    public void testpalindrome() {
        assertEquals(true, StringUtils.isPalindrome("aabbsbbaa"));
        assertEquals(false, StringUtils.isPalindrome(""));
        assertEquals(false, StringUtils.isPalindrome(" "));
        assertEquals(false, StringUtils.isPalindrome(" \n\t "));
        assertEquals(false, StringUtils.isPalindrome("nope!"));
        assertEquals(true, StringUtils.isPalindrome("i topi non avevano nipoti"));
        assertEquals(true, StringUtils.isPalindrome("otto"));
        assertEquals(false, StringUtils.isPalindrome(1));
        assertEquals(false, StringUtils.isPalindrome(new Object[] { "xx" }));
        assertEquals(false, StringUtils.isPalindrome(false));
        assertEquals(false, StringUtils.isPalindrome("<object object at 0x00000222525A7F70>"));
        assertEquals(false, StringUtils.isPalindrome("nope!"));
        assertEquals(false, StringUtils.isPalindrome("i topi non avevano nipoti"));
        assertEquals(true, StringUtils.isPalindrome("otto"));
        assertEquals("", StringUtils.isPalindrome(null));
        assertEquals("", StringUtils.isPalindrome(""));
        assertEquals("abc", StringUtils.isPalindrome("abc"));
    }
}
