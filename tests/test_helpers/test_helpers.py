from pycups_po.helpers import remove_prefix


def test_remove_prefix_normal():
    assert remove_prefix("*BuzzerStart", "*") == "BuzzerStart"


def test_remove_prefix_without_prefix():
    assert remove_prefix("*BuzzerStart", "%") == "*BuzzerStart"


def test_remove_prefix_prefix_with_space():
    assert remove_prefix(" *BuzzerStart", "*") == " *BuzzerStart"
