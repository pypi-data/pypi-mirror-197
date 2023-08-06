from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Literal, Optional, overload

import pandas as pd
import snowflake.connector as connector
import snowflake.connector.cursor as cursor

from bbg.secrets import Client
from ._typing import Connection


@dataclass
class SnowflakeConnection(Connection):
    """
    Base class for snowflake connections to SQL databases. Additionally
    supports cursors.
    """
    connection: connector.SnowflakeConnection

    @contextmanager
    def cursor(self) -> cursor.SnowflakeCursor:
        """
        Creates a cursor for more efficient SQL querying or getting
        results in other formats than a dataframe.

        Example:
            >>> with connection.cursor() as cursor:
            ...     for query in queries:
            ...         cursor.execute(query)
            ... 
            >>> # Cursor is closed automatically at the end.
        """
        cursor = self.connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    @overload
    def query(self, query: str, mode: Literal["read"] = ...) -> pd.DataFrame: ...

    @overload
    def query(self, query: str, mode: Literal["write"]) -> None: ...

    def query(self, query: str, mode: Literal["read", "write"] = "read") -> Optional[pd.DataFrame]:
        """
        Query the snowflake connection.

        Parameters:
            query:
                A SQL table query.
            mode:
                Either read or write. If read, results are returned as
                a pandas dataframe. If write, None is returned.

        Returns:
            df:
                A Pandas DataFrame if mode="read".

        Example:
            TODO: Add an example here.
        """
        query = self._clean(query)
        with self.cursor() as cursor:
            cursor.execute(query)
            if mode == "read":
                return cursor.fetch_pandas_all()


class SnowflakeConnections(Connection, Enum):
    """
    The snowflake SQL connections with the snowflake
    connection cached the first time this is used.
    """
    _connection: Optional[SnowflakeConnection]

    DATA_LOADER = auto()
    DBT_TRANSFORMER = auto()

    def __init__(self, value: None) -> None:
        self._connection = None

    @property
    def connection(self) -> SnowflakeConnection:
        """
        Create the snowflake connection if it does not already exist.
        """
        if self._connection is not None:
            return self._connection
        elif self is SnowflakeConnections.DATA_LOADER:
            with Client.connect() as client:
                self._connection = SnowflakeConnection(connector.connect(
                    user=
                        client.get_secret("SFlakeServiceAccountUser"),
                    password=
                        client.get_secret("SFlakeServiceAccountSecret"),
                    account=
                        client.get_secret("SFlakeAccountName"),
                ))
        elif self is SnowflakeConnections.DBT_TRANSFORMER:
            with Client.connect() as client:
                self._connection = SnowflakeConnection(connector.connect(
                    user=
                        client.get_secret("SFlakeCuratedServiceAccountName"),
                    password=
                        client.get_secret("SFlakeCuratedServiceAccountSecret"),
                    account=
                        client.get_secret("SFlakeAccountName"),
                ))
        else:
            assert False, self
        return self._connection

    @contextmanager
    def cursor(self) -> cursor.SnowflakeCursor:
        """
        Creates a cursor for more efficient SQL querying or getting
        results in other formats than a dataframe.

        Example:
            >>> with connection.cursor() as cursor:
            ...     for query in queries:
            ...         cursor.execute(query)
            ... 
            >>> # Cursor is closed automatically at the end.
        """
        with self.connection.cursor() as cursor:
            yield cursor

    @overload
    def query(self, query: str, mode: Literal["read"] = ...) -> pd.DataFrame: ...

    @overload
    def query(self, query: str, mode: Literal["write"]) -> None: ...

    def query(self, query: str, mode: Literal["read", "write"] = "read") -> Optional[pd.DataFrame]:
        """
        Query the snowflake connection.

        Parameters:
            query:
                A SQL table query.
            mode:
                Either read or write. If read, results are returned as
                a pandas dataframe. If write, None is returned.

        Returns:
            df:
                A Pandas DataFrame if mode="read".

        Example:
            TODO: Add an example here.
        """
        query = self._clean(query)
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            if mode == "read":
                return cursor.fetch_pandas_all()


data_loader = SnowflakeConnections.DATA_LOADER
dbt_transformer = SnowflakeConnections.DBT_TRANSFORMER
