from __future__ import annotations

from typing import Union

import psycopg as pg
from psycopg.sql import SQL


__all__ = [
    "first_row",
    "first_value",
    "first_values",
]


def first_row(cursor: pg.Cursor, query: Union[str, SQL], parameters=()):
    """
    Execute a query and return the first matching row, if any.

    Parameters:
        cursor: Cursor to use
        query: Query to execute
        parameters: Optional parameters
    """
    cursor.execute(query, parameters)
    return cursor.fetchone()


def first_value(cursor: pg.Cursor, query: Union[str, SQL], parameters=()):
    """
    Execute a query and return the first value of the first matching row, if any.

    Parameters:
        cursor: Cursor to use
        query: Query to execute
        parameters: Optional parameters
    """
    row = first_row(cursor, query, parameters)
    if row is None:
        return None
    return row[0]


def first_values(cursor: pg.Cursor, query: Union[str, SQL], parameters=()):
    """
    Execute a query and return the first value of each matching row.

    Parameters:
        cursor: Cursor to use
        query: Query to execute
        parameters: Optional parameters
    """
    cursor.execute(query, parameters)
    return [row[0] for row in cursor]
