import junit.framework.TestCase;

public class WordUtilsTest extends TestCase {

    public void testwrap() {
        assertEquals("Here is one line of\ntext that is going\nto be wrapped after\n20 columns.", WordUtils.wrap("Here is one line of text that is going to be wrapped after 20 columns.", 20, "\n", false,"\n"));

    }
}