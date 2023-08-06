import string
from typing import Literal
import pandas as pd


class Connection:
    """
    Generic connection class for querying a database.

    Requires subclasses to implement the query method.
    """

    def _clean(self, query: str) -> str:
        """
        Cleans the string by stripping whitespace and checking for
        invalid characters.
        """
        query = query.strip()
        for c in query:
            if c not in string.printable:
                raise ValueError(
                    "invalid character "
                    + repr(c)
                    + ", try typing it manually"
                )
        return query

    def query(self, query: str, mode: Literal["read"] = ...) -> pd.DataFrame:
        """
        Query the database and return a pandas dataframe.

        Parameters:
            query:
                A SQL query for the database connection.
            mode:
                If read, returns a Pandas DataFrame. Different connectors
                may support other modes.

        Returns:
            df:
                A Pandas DataFrame if mode="read".
        """
        raise NotImplementedError
