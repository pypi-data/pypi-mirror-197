"""
DESCRIPTION!!!!!!!!!!!!!!!!!!!!
"""

# Use `bbg.sql.typing` for type-hinting classes.
from . import typing

# Import class instances and helper functions.
from ._pyspark import count_of
from ._hana import hana
from ._snowflake import data_loader, dbt_transformer
from ._snowflake import data_loader as snowflake
from ._watermarks import watermarks

def reconnect() -> None:
    """
    Reconnect to all databases. Useful if a very long query needs to be
    ran. This should be ran right before a database is needed but the
    time since the last query is long.
    """
    dbt_transformer._connection = None
    hana._connection = None
    snowflake._connection = None
    watermarks._connection = None
