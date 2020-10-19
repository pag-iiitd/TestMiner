import pytest
from pattern import en

@pytest.mark.parametrize('value,op', [("The cat was looking at me from up on the roof with interest.", "The/DT/B-NP/O cat/NN/I-NP/O was/VBD/B-VP/O looking/VBG/I-VP/O at/IN/B-PP/B-PNP me/PRP/B-NP/I-PNP from/IN/B-PP/B-PNP up/IN/I-PP/I-PNP on/IN/I-PP/I-PNP the/DT/B-NP/I-PNP roof/NN/I-NP/I-PNP with/IN/B-PP/B-PNP interest/NN/B-NP/I-PNP ././O/O")])
def test_parse(value, op):
    assert (parse(value) == op)
