from tests.conftest import FakeGenerator


def test_option_name(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/grouped.ppd")
    options = generator.get_ppd_options()

    assert options[0].name == "PaperType"
    assert options[1].name == "BuzzerStart"
    assert options[2].name == "BuzzerEnd"


def test_options_count(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/grouped.ppd")
    options = generator.get_ppd_options()

    assert len(options) == 3
