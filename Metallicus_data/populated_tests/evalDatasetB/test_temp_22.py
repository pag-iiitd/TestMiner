
import pytest
from pattern import en

@pytest.mark.parametrize('value,op', [('The cat was looking at me from up on the roof with interest.', 'The/DT/B-NP/O cat/NN/I-NP/O was/VBD/B-VP/O looking/VBG/I-VP/O at/IN/B-PP/B-PNP me/PRP/B-NP/I-PNP from/IN/B-PP/B-PNP up/IN/I-PP/I-PNP on/IN/I-PP/I-PNP the/DT/B-NP/I-PNP roof/NN/I-NP/I-PNP with/IN/B-PP/B-PNP interest/NN/B-NP/I-PNP ././O/O'), ("We will meet at eight o'clock on Thursday morning.", [('We', 'PRON'), ('will', 'AUX'), ('meet', 'VERB'), ('at', 'ADP'), ('eight', 'NUM'), ("o'clock", 'NOUN'), ('on', 'ADP'), ('Thursday', 'PROPN'), ('morning', 'NOUN'), ('.', 'PUNCT')]), ('This is a test . What is the result of two sentences ?', 'This_DT is_VBZ a_DT test_NN ._. What_WP is_VBZ the_DT result_NN of_IN two_CD sentences_NNS ?_.'), ('This is a test . What is the result of two sentences ?', 'This_DT is_VBZ a_DT test_NN ._. What_WP is_VBZ the_DT result_NN of_IN two_CD sentences_NNS ?_.')])
def test_parse(value, op):
    assert (parse(value) == op)
