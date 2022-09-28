import re


def remove_prefix(self: str, prefix: str) -> str:
    if self.startswith(prefix):
        return self[len(prefix) :]
    else:
        return self[:]


def string_to_valid_variable_name(string: str, prefix: str = None, suffix: str = None, separator: str = ""):
    valid_variable_name = re.sub("\W|^(?=\d)", separator, string).strip(separator)
    variable_name = f"{prefix or ''}{separator}{valid_variable_name}"
    if suffix is not None:
        variable_name += f"{separator}{suffix}"
    return variable_name
