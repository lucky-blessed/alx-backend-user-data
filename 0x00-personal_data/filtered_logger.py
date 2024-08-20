#!/usr/bin/env python3
"""
Module that handles sensitive data reaction and
and logging with redaction.
"""


import re
import logging
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
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]+", f"{field}={redaction}", message)
        return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with the given fields to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the record, redact sensitive fields.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
