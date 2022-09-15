from tests.conftest import FakeGenerator


def test_option_name(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/without_pretty_name.ppd")
    options = generator.get_ppd_options()

    assert options[0].name == "PaperType"


def test_option_pretty_name(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/without_pretty_name.ppd")
    options = generator.get_ppd_options()

    assert options[0].pretty_name is None
