#!/usr/bin/env python3
"""
Module that provides functionality to filter and obfuscate
log messages
"""


import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Returns obfuscated log message with specified fields.

    Args:
        firlds: a list of string which represents fields to be obfuscated
        redaction: a string representing what the field will be obfuscated to.
        message: a field representing the log line
        separator: a string representing by which charater is
        is separating all fields in the log line.


    Returns:
        A string of the obfuscated log messages.
    """
    pattern = f'({"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, lambda m: f'{m.group().split("=")[0]}={redaction}', message)
