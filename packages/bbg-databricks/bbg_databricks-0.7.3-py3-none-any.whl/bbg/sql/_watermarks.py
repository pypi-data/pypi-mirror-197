import sys
from contextlib import contextmanager
from enum import Enum
from typing import Any, Literal, Optional, overload

if sys.version_info < (3, 9):
    from typing import Iterator
else:
    from collections.abc import Iterator

import pandas as pd
import pyspark.sql

from bbg.secrets import Client, get_db_secret
from ._typing import Connection
from ._jaydebeapi import JayDeBeAPIConnection, JayDeBeAPICursor, connect


class Watermarks(Connection, Enum):
    """The Watermarks SQL connection."""
    _connection: Optional[JayDeBeAPIConnection]

    CONNECTION = None

    def __init__(self, value: None) -> None:
        self._connection = None

    def _ensure_connection(self) -> JayDeBeAPIConnection:
        if self._connection is not None:
            return self._connection
        environment = get_db_secret("environment")
        base_name = get_db_secret("BaseName")
        base_scope = get_db_secret("BaseScope")
        with Client.connect() as client:
            user = client.get_secret("metadatadbadminuser")
            password = client.get_secret("metadatadbadminpass")
        connection = connect(
            "com.microsoft.sqlserver.jdbc.SQLServerDriver",
            "jdbc:sqlserver://{hostname}:{port};database={database};user={user};password={password};".format(
                hostname=f"{base_name}-{base_scope}-{environment}-sqlserver.database.windows.net",
                port=1433,
                database=f"{base_name}{base_scope}{environment}metadatadb",
                user=user,
                password=password,
            ),
            [user, password],
        )
        self._connection = connection
        return connection

    @contextmanager
    def cursor(self, fetch_size: int = 1024) -> Iterator[JayDeBeAPICursor]:
        with self._ensure_connection().cursor(fetch_size) as cursor:
            yield cursor

    @overload
    def query(self, query: str, mode: Literal["read"] = ...) -> pd.DataFrame: ...

    @overload
    def query(self, query: str, mode: Literal["write"]) -> None: ...

    def query(self, query: str, mode: Literal["read", "write"] = "read") -> Optional[pd.DataFrame]:
        """
        Query the Watermarks connection and cache any missing metadata from
        the Azure key vault if missing. This requires the dbutils
        global variable to be set before running.

        Parameters:
            query:
                A SQL table query.
            mode:
                Either read, append, overwrite, ignore, or error.
                If read, results are returned as a dataframe.
                Otherwise, None is returned.

        Returns:
            df:
                A PySpark DataFrame if mode="read".

        Returns:
            df:
                A Pandas DataFrame if mode="read".

        Example:
            >>> query = '''
            ...     select
            ...         COUNT(DISTINCT "OrderID")
            ...     from
            ...         "SUPPLYCHAIN"."csg.Models.SupplyChain.Data::SalesOrders"
            ... '''
            >>> df = connection.query(query)
        """
        return self._ensure_connection().query(self._clean(query), mode)


watermarks = Watermarks.CONNECTION
