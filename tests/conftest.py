import pytest as pytest

from pycups_po import PrinterOptionsGenerator


class FakeGenerator(PrinterOptionsGenerator):
    def __init__(self, conn=None, printer_name=None):
        self.printer_name = printer_name
        self.ppd_text = None

    def set_ppd_path(self, ppd_path: str):
        with open(ppd_path, "r") as f:
            ppd_text = f.read()
        self.ppd_text = ppd_text

    def get_ppd_text(self, printer_name: str = None) -> str:
        return self.ppd_text


@pytest.fixture
def generator():
    return FakeGenerator(printer_name="FakePPD")
