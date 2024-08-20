#!/usr/bin/env python3
"""
Module that handles sensitive data reaction and
and logging with redaction.
"""


import os
import re
import mysql.connector
from mysql.connector import connection
import logging
from typing import List, Tuple


PII_FIELDS = ('name', 'email', 'pone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for PII data.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] user_data INFO %(asctime)s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record and apply redaction
        """
        message = super(RedactingFormatter, self).format(record)
        return self.redact(message, self.fields)

    def redact(self, message: str, fields: Tuple[str]) -> str:
        """
        Redact sensitive fields in the massage.
        """
        for field in fields:
            message = re.sub(f"(?<={field}=)[^;]*", self.REDACTION, message)
            return message


def get_logger() -> logging.Logger:
    """
    Creates a logger with specific setting for PII redaction
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propage = False

    strem_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Replace specific fileds in the message with redaction.
    """
    for field in fields:
        message = re.sub(f"(?<={field}=)[^{separator}]*", redaction, message)
        return message


def get_db() -> connection.MySQLConnection:
    """
    Returns a connector to MySQL database using
    environment variables.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    conn = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=db_name
            )
    return conn


def main():
    """
    Main function that reads and log data from users table.
    """
    db_conn = get_db()
    cursor = db_conn.cursor()

    corsor.execute("SELECT * FROM users")
    rows = consor.fetchall()

    logger = get_logger()

    for row in rows:
        log_message = "; ".join(
                f"{desc[0]}={value}" for desc, value in zip(cursor.description, row)
                )
        logger.info(log_message)
    cursor.close()
    db_conn.close()


if __name__ == "__main__":
    main()
