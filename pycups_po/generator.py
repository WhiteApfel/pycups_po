import re
from typing import List

import cups

from .helpers import remove_prefix, string_to_valid_variable_name
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
        option_blocks = re.finditer(self.regex, text, re.MULTILINE)

        options = []

        for option_block in option_blocks:
            # option_block:
            # *OpenUI *BuzzerStart/Start Job Beeps: PickOne
            # *DefaultBuzzerStart: 0Beeps
            # *BuzzerStart 0Beeps/0: ""
            # *BuzzerStart 1Beeps/1: ""
            # *BuzzerStart 2Beeps/2: ""
            # *BuzzerStart 3Beeps/3: ""
            # *BuzzerStart 4Beeps/4: ""
            # *BuzzerStart 5Beeps/5: ""
            # *BuzzerStart 6Beeps/6: ""
            # *BuzzerStart 7Beeps/7: ""
            # *BuzzerStart 8Beeps/8: ""
            # *BuzzerStart 9Beeps/9: ""
            # *CloseUI: *BuzzerStart
            #

            groups = option_block.groups()

            # groups[0] == "*OpenUI *BuzzerStart/Start Job Beeps: PickOne"
            # option_name == "*OpenUI *BuzzerStart/Start Job Beeps"
            # option_type == "PickOne"
            option_name, option_type = (i.strip() for i in groups[0].split(":"))

            if "/" not in option_name:
                # In case a pretty name isn't set
                # For example groups[0] == "*OpenUI *PageRegion: PickOne"
                option_name = f"{option_name}/"

            # "*OpenUI *BuzzerStart/Start Job Beeps" -> "*BuzzerStart/Start Job Beeps"
            # "*BuzzerStart/Start Job Beeps" ->
            # option_name == "*BuzzerStart"
            # option_name_pretty == "Start Job Beeps"
            option_name, option_name_pretty = option_name.split(" ", 1)[1].split("/", 1)

            # In case a pretty name isn't set
            option_name_pretty = option_name_pretty or None

            # option_name == "BuzzerStart"
            option_name = remove_prefix(option_name, "*")
            default_value = ""

            option_values = []

            # groups[1]:
            # *DefaultBuzzerStart: 0Beeps
            #
            # *BuzzerStart 0Beeps/0: ""
            # *BuzzerStart 1Beeps/1: ""
            # *BuzzerStart 2Beeps/2: ""
            # *BuzzerStart 3Beeps/3: ""
            # *BuzzerStart 4Beeps/4: ""
            # *BuzzerStart 5Beeps/5: ""
            # *BuzzerStart 6Beeps/6: ""
            # *BuzzerStart 7Beeps/7: ""
            # *BuzzerStart 8Beeps/8: ""
            # *BuzzerStart 9Beeps/9: ""
            for option_value in groups[1].split("\n"):
                if len(option_value) == 0:
                    # empty string
                    continue
                if option_value.startswith(f"*Default{option_name}"):
                    # option_value == "*DefaultBuzzerStart: 0Beeps"
                    default_value = option_value.split(": ")[1]
                if option_value.startswith(f"*{option_name}"):
                    # option_value == '*BuzzerStart 0Beeps/0: ""'

                    # option_value == "*BuzzerStart 0Beeps/0"
                    # content == '""'
                    option_value, content = option_value.split(":")

                    # option_value == "0Beeps/0"
                    option_value = option_value.split(" ", 1)[1]

                    # option_valur == "0Beeps"
                    # option_value_pretty == "0"
                    option_value, option_value_pretty = option_value.split("/", 1)

                    content = content.strip().strip('"')
                    option_values.append(
                        OptionValue(
                            value=option_value,
                            pretty_value=option_value_pretty,
                            content=content,
                        )
                    )

            options.append(
                PrinterOption(
                    name=option_name,
                    pretty_name=option_name_pretty,
                    type=option_type,
                    default_value=default_value,
                    values=option_values,
                )
            )

        return options

    def generate_options_dataclass(self, printer_name: str = None) -> str:
        print_name = printer_name or self.printer_name
        options = self.get_ppd_options(printer_name)
        class_name = string_to_valid_variable_name(
            printer_name, prefix="Printer", suffix="Options"
        )

        dataclass_file = "from typing import Literal, Union\n"
        dataclass_file += "from dataclasses import dataclass, field\n"
        dataclass_file += "from enum import Enum\n\n"

        dataclass_file += "@dataclass\n"
        dataclass_file += f"class {class_name}:\n"
        for option in options:
            option_class_name = string_to_valid_variable_name(
                option.name, prefix="Option", suffix="Values"
            )
            dataclass_file += f"\tclass {option_class_name}(str, Enum):\n"
            for option_value in option.values:
                option_value_variable = string_to_valid_variable_name(
                    option_value.value, prefix="value", separator="_",
                )
                dataclass_file += (
                    f'\t\t{option_value_variable}: str = "{option_value.value}"'
                    f'  # {option_value.pretty_value} / "{option_value.content}"\n'
                )
            dataclass_file += "\t\n"
        for option in options:
            # literal = f"""{', '.join(f'"{v.value}"' for v in option.values)}"""
            option_class_name = string_to_valid_variable_name(
                option.name, prefix="Option", suffix="Values"
            )
            dataclass_file += (
                f'\t{option.name}: Union[str, {option_class_name}] = "{option.default_value}"\n'
            )

        return dataclass_file
