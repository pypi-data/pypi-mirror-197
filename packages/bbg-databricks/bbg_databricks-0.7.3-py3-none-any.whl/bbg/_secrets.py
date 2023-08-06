import sys
from contextlib import contextmanager
from types import TracebackType
from typing import Optional, TypeVar

if sys.version_info < (3, 9):
    from typing import Iterator, Type
else:
    from builtins import type as Type
    from collections.abc import Iterator

if sys.version_info < (3, 11):
    Self = TypeVar("Self", bound="Client")
else:
    from typing import Self

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

from ._globals import get_global, set_globals

ET = TypeVar("ET", bound=BaseException)

def get_db_secret(key: str) -> str:
    """
    Get a global key from the azure databricks secrets.

    First checks for a global variable. If the global variable is not
    found, attempts to get the key from azure databricks and saves the
    key as a global variable.

    Parameters:
        key:
            The key from azure databricks.

    Returns:
        secret:
            The value of the secret.

    Example:
        >>> get_db_secret("environment")
        'dev'
    """
    try:
        return get_global(key)
    except KeyError:
        pass
    try:
        dbutils = get_global("dbutils")
    except KeyError as e:
        raise NameError(
            "missing global 'dbutils', set it using\n"
            "    from bbg import set_globals\n"
            "    set_globals(dbutils=dbutils)"
        ) from e
    secret = dbutils.secrets.get(scope="azure", key=key)
    set_globals({key: secret})
    return secret


class Client:
    """
    Helper class for getting secrets from the key vault.

    Example:
        >>> with Client.connect() as client:
        ...     secret = client.get_secret("SFlakeServiceAccountUser")
        ... 
    """
    _client: Optional[SecretClient]

    def __init__(
        self,
        vault_url: str,
        credential: ClientSecretCredential,
    ) -> None:
        self._client = SecretClient(
            vault_url=vault_url, credential=credential
        )

    def __enter__(self: Self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[ET]] = None,
        exc_value: Optional[ET] = None,
        traceback: Optional[TracebackType] = None
    ) -> None:
        self._client = None

    @staticmethod
    def connect() -> "Client":
        """
        Helper method for connecting to the secret key vault.

        Returns:
            client:
                Creates a client object connected to the secret key
                vault. Disconnects the client at the end of the context
                block.

        Example:
            >>> with Client.connect() as client:
            ...     secret = client.get_secret("SFlakeServiceAccountUser")
            ... 
        """
        credential = ClientSecretCredential(
            client_id=get_db_secret(key="DatabricksAppId"),
            client_secret=get_db_secret(key="DatabricksAppSecret"),
            tenant_id=get_db_secret(key="TenantId"),
        )
        environment = get_db_secret(key="environment")
        base_name = get_db_secret(key="BaseName")
        base_scope = get_db_secret(key="BaseScope")
        url = f"https://{base_name}-{base_scope}-{environment}-keyvault.vault.azure.net/"
        return Client(url, credential)

    def get_secret(self, name: str) -> str:
        """
        Helper method for connecting to the secret key vault.

        First checks for a global variable. If the global variable is
        not found, attempts to get the key from secret key vault and
        saves the key as a global variable.

        Parameters:
            name:
                The name of the secret in the key vault.

        Returns:
            secret:
                The value of the secret from the key vault.

        Raises:
            KeyError:
                If the global secret is not found (using bbg.get_global)
                and the client is disconnected, raise KeyError(name).

        Example:
            >>> with Client.connect() as client:
            ...     secret = client.get_secret("SFlakeServiceAccountUser")
            ... 
        """
        try:
            return get_global(name)
        except KeyError:
            pass
        if self._client is None:
            raise KeyError(name)
        secret = self._client.get_secret(name).value
        set_globals({name: secret})
        return secret
