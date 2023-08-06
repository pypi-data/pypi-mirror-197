import json

from typing import Any
from functools import lru_cache

from ._globals import get_global


@lru_cache()
def load_filename(filename: str) -> str:
    # Load the file.
    get_global("dbutils").fs.cp(
        f"dbfs:/mnt/{filename}", f"file:/tmp/{filename}"
    )

    return f"/tmp/{filename}"

def load_file(filename: str) -> Any:
    """
    Loads a file from "dbfs:/mnt/filename" to "file:/tmp/filename"
    to be used in databricks.

    Parameters:
        filename:
            The name of the file.

    Example:
        >>> metadata_file = load_file(
        ...     "metadata/processed/raw_to_processed_metadata.json"
        ... )
    """
    with open(load_filename(filename)) as file:
        return json.load(file)
    
