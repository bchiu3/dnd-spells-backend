from typing import Callable


def validate_comma_separated_list(value: str, field_type: type, sanitizer: Callable[[str], str] = lambda x: x.strip()) -> list:
    split_v = value.split(",")
    return_list = [None for _ in split_v]
    for i, v in enumerate(split_v):
        return_list[i] = (field_type(sanitizer(v)))
    return return_list