from dataclasses import dataclass
from typing import Literal


@dataclass
class OptionValue:
    value: str
    pretty_value: str


@dataclass
class PrinterOption:
    name: str
    type: Literal["PickOne"]
    default_value: str
    values: list[OptionValue]
