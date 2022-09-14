from dataclasses import dataclass
from typing import Literal, List


@dataclass
class OptionValue:
    value: str
    pretty_value: str
    content: str


@dataclass
class PrinterOption:
    name: str
    type: Literal["PickOne"]
    default_value: str
    values: List[OptionValue]
