from __future__ import annotations

import os
from contextlib import contextmanager

import psycopg as pg

from .util import coalesce
from .util import load_config


__all__ = [
    "Client",
]


class Client:
    """
    Creates and manages :py:class:`psycopg.Connection` objects
    when used as a context manager::

        client = Client(...)
        with client.connect() as conn
            with conn.cursor() as cursor:
                ...

    Alternatively, if you don't need to use the connection directly,
    you can also get a cursor::

        client = Client(...)
        with client.cursor() as cursor:
            ...

    Connection parameters are given as ``kwargs``.
    Common options are ``user``, ``dbname``, ``host``, and ``schema``
    (a shorthand for setting the ``search_path`` option).
    For the full list of available parameters, see
    https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS

    Parameters passed from Python take priority,
    but they may also be passed as environment variables
    ``SQLTRACK_DSN_<PARAM>`` (e.g., ``SQLTRACK_DSN_USER``),
    or loaded from a config file, by default ``./sqltrack.conf``.

    Experiment and Run objects obtain connections as required.
    Nested contexts reuse the same connection (reentrant),
    so they can be used to avoid connecting to the
    database multiple times over a short period.
    E.g., the following snippet will connect only once,
    with the caveat that everything happens within the same transaction::

        def do_queries(client, ...):
            with client.cursor() as cursor:
                cursor.execute(...)
                ...

        client = Client(...)
        with client.connect():
            do_queries(client, ...)
            do_queries(client, ...)
            do_queries(client, ...)

    Parameters:
        config_path: Path to config file,
            defaults to ``SQLTRACK_CONFIG_PATH`` environment variable,
            and finally ``./sqltrack.conf``
        kwargs: Connection parameters
    """
    def __init__(self, config_path: str = None, **kwargs):
        # get config values
        config = load_config(coalesce(config_path, os.getenv("SQLTRACK_CONFIG_PATH")))
        # update config from kwargs
        for k, v in kwargs.items():
            if v is not None:
                config[k] = v
        # user defaults to USER env var
        if config.get("user") is None:
            config["user"] = os.getenv("USER")
        # database defaults to user
        if config.get("dbname") is None:
            config["dbname"] = config["user"]
        # pop schema and put as search path
        self.schema = None
        if "schema" in config:
            schema = config.pop("schema")
            self.schema = schema
            config["options"] = f"--search_path={schema}"
        # the finished DSN
        self.dsn = " ".join(f"{k}={pg.sql.quote(v)}" for k, v in config.items())
        self._conn = None

    @contextmanager
    def connect(self) -> pg.Connection:
        """
        Context manager that connects to the DB.
        Use in with statement::

            with client.connect() as conn:
                ... connection things ...
                with client.cursor() as cursor:
                    ... cursor things ...
                ... connection things ...

        The connection is closed and any changes comitted
        when the with block ends.

        Nested contexts reuse the same connection (reentrant),
        so they can be used to avoid connecting to the
        database multiple times over a short period.
        E.g., the following snippet will connect only once,
        with the caveat that everything happens within the same transaction::

            def do_queries(client, ...):
                with client.cursor() as cursor:
                    cursor.execute(...)
                    ...

            client = Client(...)
            with client.connect():
                do_queries(client, ...)
                do_queries(client, ...)
                do_queries(client, ...)
        """
        if self._conn is not None:
            yield self._conn
            return
        self._conn = pg.connect(self.dsn)
        try:
            with self._conn:
                yield self._conn
        finally:
            self._conn = None

    def commit(self):
        """
        Convenience function to call commit on the DB connection.
        Raises :py:class:`RuntimeError` when not connected.
        """
        if self._conn is None:
            raise RuntimeError("not connected")
        self._conn.commit()

    def rollback(self):
        """
        Convenience function to call rollback on the DB connection.
        Raises :py:class:`RuntimeError` when not connected.
        """
        if self._conn is None:
            raise RuntimeError("not connected")
        self._conn.rollback()

    @contextmanager
    def cursor(self) -> pg.Cursor:
        """
        Connect to the DB and return a cursor.
        Use in with statement::

            with client.cursor() as cursor:
                ... cursor things ...

        The connection is closed and any changes comitted
        when the with block ends.
        """
        with self.connect() as conn:
            yield conn.cursor()
