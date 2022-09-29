from tests.conftest import FakeGenerator


def test_basic_class(generator: FakeGenerator):
    generator.set_ppd_path("tests/data/basic.ppd")
    options = generator.generate_options_dataclass()
    print(options)
    with open("tests/data/basic.dataclass", "r") as f:
        assert options == f.read()
