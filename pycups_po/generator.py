import re

import cups
from typing import List

from .models import OptionValue, PrinterOption


class PrinterOptionsGenerator:
    regex = r"(^\*OpenUI .*\n)((.*\n)*?)(\*CloseUI.*)"

    def __init__(self, connection: cups.Connection, printer_name: str = None):
        self.connection = connection
        self.printer_name = printer_name

    def get_ppd_text(self, printer_name: str = None) -> str:
        ppd_path = self.connection.getPPD(printer_name)
        return open(ppd_path, "r").read()

    def get_ppd_options(self, printer_name: str = None) -> List[PrinterOption]:
        text = self.get_ppd_text(printer_name or self.printer_name)
        options_blocks = re.finditer(self.regex, text, re.MULTILINE)

        options = []

        for option_block in options_blocks:

            groups = option_block.groups()
            option_name, option_type = (i.strip() for i in groups[0].split(":"))
            option_name = option_name.split(" ", 1)[1].split("/")[0].removeprefix("*")
            default_value = ""

            option_values = []
            for option_value in groups[1].split("\n"):
                if len(option_value) == 0:
                    continue
                if option_value.startswith(f"*Default{option_name}"):
                    default_value = option_value.split(": ")[1]
                if option_value.startswith(f"*{option_name}"):
                    option_value, option_pretty_value = (
                        option_value.split(":")[0].split(" ", 1)[1].split("/", 1)
                    )
                    option_values.append(
                        OptionValue(
                            value=option_value, pretty_value=option_pretty_value
                        )
                    )

            options.append(
                PrinterOption(
                    name=option_name,
                    type=option_type,
                    default_value=default_value,
                    values=option_values,
                )
            )

        return options

    def generate_options_dataclass(self, printer_name: str = None) -> str:
        print_name = printer_name or self.printer_name
        options = self.get_ppd_options(printer_name)
        class_name = f"{print_name.replace('-', '').replace(' ', '')}Options"

        dataclass_file = "from typing import Literal\n"
        dataclass_file += "from dataclasses import dataclass, field\n\n"

        dataclass_file += "@dataclass\n"
        dataclass_file += f"class {class_name}:\n"
        for option in options:
            literal = f"""{', '.join(f'"{v.value}"' for v in option.values)}"""
            dataclass_file += (
                f'\t{option.name}: Literal[{literal}] = "{option.default_value}"\n'
            )

        return dataclass_file
