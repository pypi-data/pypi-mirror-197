import sys
import typing
from contextlib import contextmanager
from dataclasses import InitVar, dataclass, field
from datetime import date, datetime, time
from enum import Enum, auto
from types import TracebackType
from typing import Any, Literal, Optional, TypeVar, Union, overload

if sys.version_info < (3, 9):
    from typing import Iterable, Iterator, List, Mapping, Sequence, Tuple, Type
else:
    from builtins import list as List, tuple as Tuple, type as Type
    from collections.abc import Iterable, Iterator, Mapping, Sequence

if sys.version_info < (3, 11):
    Self = TypeVar("Self", bound=Union["JayDeBeAPICursor", "JayDeBeAPIConnection"])
else:
    from typing import Self

import jaydebeapi
import pandas as pd

from bbg.secrets import Client
from ._typing import Connection

ET = TypeVar("ET", bound=BaseException)


@dataclass
class JayDeBeAPICursor:
    cursor: jaydebeapi.Cursor
    size: InitVar[int]

    def __post_init__(self, size: int) -> None:
        self.fetch_size = size

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[ET]] = None,
        exc_val: Optional[ET] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        self.close()

    def __iter__(self) -> Iterator[Tuple[Any, ...]]:
        return iter(self.fetchone, None)

    @property
    def description(self) -> Any:
        return self.cursor.description

    @property
    def fetch_size(self) -> int:
        return self._fetch_size

    @fetch_size.setter
    def fetch_size(self, size: int) -> None:
        self._fetch_size = size
        try:
            self.cursor._rs.setFetchSize(size)
        except:
            pass

    def close(self) -> None:
        self.cursor.close()

    def execute(
        self,
        query: str,
        parameters: Optional[Iterable[Any]] = None,
    ) -> None:
        if parameters is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, (*parameters,))
        try:
            self.cursor._rs.setFetchSize(size)
        except:
            pass

    def executemany(
        self,
        query: str,
        parameters: Iterable[Iterable[Any]],
    ) -> None:
        self.cursor.executemany(
            query,
            ((*params,) for params in parameters),
        )
        try:
            self.cursor._rs.setFetchSize(size)
        except:
            pass

    def fetchone(self) -> Optional[Tuple[Any, ...]]:
        return self.cursor.fetchone()

    def fetchmany(self, size: Optional[int] = None) -> List[Tuple[Any, ...]]:
        return self.cursor.fetchmany(size)

    def fetchall(self) -> List[Tuple[Any, ...]]:
        return self.cursor.fetchall()


@dataclass
class JayDeBeAPIConnection(Connection):
    connection: jaydebeapi.Connection

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[ET]] = None,
        exc_val: Optional[ET] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        self.close()

    def close(self) -> None:
        self.connection.close()

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()

    @contextmanager
    def cursor(self, fetch_size: int = 1024) -> Iterator[JayDeBeAPICursor]:
        with JayDeBeAPICursor(self.connection.cursor(), fetch_size) as cursor:
            yield cursor

    @overload
    def query(self, query: str, mode: Literal["read"] = ...) -> pd.DataFrame: ...

    @overload
    def query(self, query: str, mode: Literal["write"]) -> None: ...

    def query(self, query: str, mode: Literal["read", "write"] = "read") -> Optional[pd.DataFrame]:
        """
        Query the jaydebeapi connection.

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
        with self.cursor() as cursor:
            cursor.execute(query)
            if mode == "read":
                description = cursor.description
                return pd.DataFrame(
                    as_rows(cursor),
                    columns=[name for name, *_ in description],
                )


def as_rows(cursor: JayDeBeAPICursor) -> Iterator[Tuple[Any, ...]]:
    description = cursor.description
    timestamps = [
        i
        for i, (_, dtype, *_) in enumerate(description)
        if dtype.values == ["TIMESTAMP"]
    ]
    times = [
        i
        for i, (_, dtype, *_) in enumerate(description)
        if dtype.values == ["TIME"]
    ]
    dates = [
        i
        for i, (_, dtype, *_) in enumerate(description)
        if dtype.values == ["DATE"]
    ]
    for *row, in cursor:
        for i in timestamps:
            row[i] = datetime.strptime(row[i], "%Y-%m-%d %H:%M:%S.%f")
        for i in dates:
            raise NotImplementedError
        for i in times:
            raise NotImplementedError
        yield row

def connect(
    jclassname: str,
    url: str,
    driver_args: Optional[Union[
        Mapping[str, str], Sequence[str]
    ]] = None,
    jars: Optional[Sequence[str]] = None,
    libs: Optional[Sequence[str]] = None,
) -> JayDeBeAPIConnection:
    return JayDeBeAPIConnection(jaydebeapi.connect(
        jclassname,
        url,
        None
            if driver_args is None
            else
        dict(driver_args)
            if isinstance(driver_args, Mapping)
            else
        list(driver_args),
        jars if jars is None or isinstance(jars, str) else list(jars),
        libs if libs is None or isinstance(libs, str) else list(libs),
    ))
