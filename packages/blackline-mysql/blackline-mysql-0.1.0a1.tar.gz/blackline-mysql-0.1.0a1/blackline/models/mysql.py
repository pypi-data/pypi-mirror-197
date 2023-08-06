"""
MySQL adapter configuration. This shouldn't be here but will move is
later and have it dynamically loaded from blackline-postgres.
"""

from typing import Literal, Optional

from blackline.models.adapter import AdapterConfig, ConnectionConfig
from pydantic import BaseModel, SecretStr


class MySQLConnectionConfig(ConnectionConfig):
    user: str
    password: SecretStr
    password1: Optional[SecretStr] = None
    password2: Optional[SecretStr] = None
    password3: Optional[SecretStr] = None
    database: str
    host: str = "127.0.0.1"
    port: int = 3306
    unix_socket: Optional[str] = None


class MySQLConfig(AdapterConfig):
    class Config(BaseModel):
        connection: MySQLConnectionConfig

    type: Literal["mysql"]
    config: Config
