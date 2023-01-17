import keywords
from typing import Union

def is_digit(char: Union[str, None]) -> bool:
    if empty_char(char):
        return False
    return ((char >= "0") and (char <= "9"))

def is_alpha(char: Union[str, None]) -> bool:
    if empty_char(char):
        return False
    is_lower = char >= 'a' and char <= 'z'
    is_upper = char >= 'A' and char <= 'Z'
    return (is_lower or is_upper or char == '_')

def is_alpha_numeric(char: Union[str, None]) -> bool:
    return is_digit(char) or is_alpha(char)

def is_special_char(char: Union[str, None]) -> bool:
    if empty_char(char):
        return False
    return char in ["@", "$", "_" , "~", "#", "&", ";", "?", "!"]

def empty_char(char: Union[str, None]) -> bool:
    return char in (None, "")
