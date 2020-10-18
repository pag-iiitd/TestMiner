import junit.framework.TestCase;

public class ContainsTest extends TestCase {

    public void testcontains() {
        assertEquals(true, StringUtils.contains("testcases", "TE", true));
        assertEquals(true, StringUtils.contains("testcases", "abcdefghijklmnopqrstuvwxyz", true));
        assertEquals(true, StringUtils.contains("testcases", "abcdefghijklmnopqrstuvwxyz", true));
        assertEquals(true, StringUtils.contains("testcases", "abcdefghijklmnopqrstuvwxyz", true));
        assertEquals(false, StringUtils.contains("testcases", "abcdefghijklmnopqrstuvwxyz", true));
        assertEquals(true, StringUtils.contains("abcdefghijklmnopqrstuvwxyz", "a", true));
        assertEquals(true, StringUtils.contains("abcdefghijklmnopqrstuvwxyz", "pq", true));
        assertEquals(true, StringUtils.contains("abcdefghijklmnopqrstuvwxyz", "z", true));
        assertEquals(false, StringUtils.contains("abcdefghijklmnopqrstuvwxyz", "zyx", true));
        assertEquals(true, StringUtils.contains("abcdefghijklmnopqrstuvwxyz", "a", true));
        assertEquals(true, StringUtils.contains("abcdefghijklmnopqrstuvwxyz", "pq", true));
        assertEquals(true, StringUtils.contains("abcdefghijklmnopqrstuvwxyz", "z", true));
        assertEquals(false, StringUtils.contains("abcdefghijklmnopqrstuvwxyz", "zyx", true));
    }
}