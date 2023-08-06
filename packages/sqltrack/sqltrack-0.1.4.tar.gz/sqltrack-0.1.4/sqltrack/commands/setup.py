from __future__ import annotations

from typing import Iterable
from typing import Tuple
from typing import Union
from pathlib import Path

import psycopg as pg

from ..client import Client
from ..queries import first_values


__all__ = [
    "setup"
]


SQL_DIR = (Path(__file__).parent.parent / "sql").absolute()


def _apply_script(cursor, script, applied_names):
    path = None
    code = None
    # determine whether script is file or code
    if isinstance(script, (str, Path)):
        path = Path(script)
        name = str(path.name)
    else:
        name, code = script

    if name in applied_names:
        print("(OK)", name)
    else:
        # load code from file
        if code is None:
            with path.open(encoding='UTF-8') as fp:
                code = fp.read()
        # finally, execute the script
        cursor.execute(code)
        cursor.execute(
            "INSERT INTO applied_migrations (name) VALUES (%s)",
            (name,),
        )
        print("(NEW)", name)


def setup(client: Client, scripts: Iterable[Union[str, Path, Tuple[str, str]]]):
    """
    Execute SQL scripts to setup (or update) the database.
    The included ``base.sql`` script is always executed first.
    User-defined scripts are run in the given order.

    Scripts can be loaded from files,
    or defined directly as tuples :python:`(name, script)`,
    where :python:`script` is the SQL code to execute.

    A script is never run twice.
    Whether a script has already been run before is determined by filename,
    the rest of the path is ignored.
    Thus ``base.sql`` cannot be used as filename for user-defined scripts.

    Example script with timestamps, loss and accuracies for
    training, validation, and test phases:

    .. code-block:: SQL

        BEGIN;

        ALTER TABLE metrics
            ADD COLUMN train_start TIMESTAMP WITH TIME ZONE,
            ADD COLUMN train_end TIMESTAMP WITH TIME ZONE,
            ADD COLUMN train_loss FLOAT,
            ADD COLUMN train_top1 FLOAT,
            ADD COLUMN train_top5 FLOAT,
            ADD COLUMN val_start TIMESTAMP WITH TIME ZONE,
            ADD COLUMN val_end TIMESTAMP WITH TIME ZONE,
            ADD COLUMN val_loss FLOAT,
            ADD COLUMN val_top1 FLOAT,
            ADD COLUMN val_top5 FLOAT,
            ADD COLUMN test_start TIMESTAMP WITH TIME ZONE,
            ADD COLUMN test_end TIMESTAMP WITH TIME ZONE,
            ADD COLUMN test_loss FLOAT,
            ADD COLUMN test_top1 FLOAT,
            ADD COLUMN test_top5 FLOAT;

        END;

    Parameters:
        client: Client to connect to the database
        scripts: Paths to SQL scripts or tuples :python:`(name, script)`;
            executed in the given order
    """
    with client.connect() as conn, conn.cursor() as cursor:
        # create the schema if it does not exist
        if client.schema is not None:
            schema = client.schema
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
            conn.commit()
            print("Schema:", schema)
        # try to get names of applied migration files
        try:
            applied_names = set(first_values(
                cursor, "SELECT name FROM applied_migrations;"))
        except pg.ProgrammingError:
            applied_names = set()
            conn.rollback()
        # base schema file always goes first
        base = SQL_DIR / "base.sql"
        for script in (base,) + tuple(scripts):
            _apply_script(cursor, script, applied_names)
