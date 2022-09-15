from tests.conftest import FakeGenerator


def test_option_name(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/comments.ppd")
    options = generator.get_ppd_options()

    assert options[0].name == "PaperType"
    assert options[1].name == "BuzzerStart"


def test_option_values_count(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/comments.ppd")
    options = generator.get_ppd_options()

    assert len(options[0].values) == 2
    assert len(options[1].values) == 10
