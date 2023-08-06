from __future__ import annotations

from typing import Union

import pandas as pd
import psycopg as pg
from psycopg.sql import SQL


def query_dataframe(cursor: pg.Cursor, query: Union[str, SQL], parameters=()) -> pd.DataFrame:
    """
    Run a query and return the result as a Pandas DataFrame.

    Parameters:
        cursor: The psycopg Cursor to use
        query: The query to retrieve data
        parameters: Optional set of parameters passed to the cursor
    """
    cursor.execute(query, parameters)
    return pd.DataFrame(cursor, columns=[col.name for col in cursor.description])
