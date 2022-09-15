from tests.conftest import FakeGenerator


def test_option_name(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/basic.ppd")
    options = generator.get_ppd_options()

    assert options[0].name == "BuzzerStart"
    assert options[1].name == "BuzzerEnd"


def test_option_pretty_name(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/basic.ppd")
    options = generator.get_ppd_options()

    assert options[0].pretty_name == "Start Job Beeps"
    assert options[1].pretty_name == "End Job Beeps"


def test_option_type(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/basic.ppd")
    options = generator.get_ppd_options()

    assert options[0].type == "PickOne"
    assert options[1].type == "PickOne"


def test_option_default_value(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/basic.ppd")
    options = generator.get_ppd_options()

    assert options[0].default_value == "0Beeps"
    assert options[1].default_value == "1Beeps"


def test_option_values_count(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/basic.ppd")
    options = generator.get_ppd_options()

    assert len(options[0].values) == 9
    assert len(options[1].values) == 10


def test_option_value_content(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/basic.ppd")
    options = generator.get_ppd_options()

    assert options[0].values[0].content == "0"
    assert options[1].values[0].content == ""


def test_option_value_pretty_value(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/basic.ppd")
    options = generator.get_ppd_options()

    assert options[0].values[0].pretty_value == "0"
    assert options[1].values[1].pretty_value == "1"
