from dataclasses import dataclass
from typing import Literal, List, Optional


@dataclass
class OptionValue:
    value: str
    pretty_value: str
    content: str


@dataclass
class PrinterOption:
    name: str
    pretty_name: Optional[str]
    type: Literal["PickOne"]
    default_value: str
    values: List[OptionValue]
