"""
Contains all of the sql connection classes for typing.
"""
from ._typing import Connection
from ._jaydebeapi import JayDeBeAPICursor, JayDeBeAPIConnection
from ._pyspark import PySparkConnection, PySparkQuery
from ._hana import Hana
from ._watermarks import Watermarks
from ._snowflake import SnowflakeConnection, SnowflakeConnections
