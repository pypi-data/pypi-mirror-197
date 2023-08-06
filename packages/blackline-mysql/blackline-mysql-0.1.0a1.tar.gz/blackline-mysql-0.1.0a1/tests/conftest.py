"""
Some fixtures are mocked to avoid having to connect to a real database.
A mysql database is available while running tests locally using docker-compose.
The database is not available when running tests on github actions.
The envionment variable GITHUB_ACTIONS is set to true when running on github actions.
https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables
"""


import os
from datetime import datetime
from pathlib import Path
from typing import List

import pytest
import yaml
from blackline.adapters.mysql import MySQLAdapter
from blackline.constants import PROJECT_CONFIG_FILE
from blackline.models.catalogue import StoreCatalogue
from blackline.models.mysql import MySQLConfig
from blackline.parsers.catalogue import CatalogueParser
from blackline.query.query_factory import QueryFactory
from blackline.utils.data.mock_data import user_data, user_data_deidentified
from blackline.utils.testing.catalogue import catalogue_yaml as raw_catalogue_yaml
from mysql.connector import MySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.cursor import MySQLCursor
from pytest import MonkeyPatch


@pytest.fixture
def github_actions_pg() -> bool:
    if os.getenv("GITHUB_ACTIONS") == "true":
        """This will help testing the monkeypatches locally.
        If set to true, the connections to mysql will fail if not correctly mocked.
        """
        return True
    return False


@pytest.fixture
def project_root() -> Path:
    return Path("foo/bar")


@pytest.fixture
def fake_project_name() -> str:
    return "fake-project"


@pytest.fixture
def mysql_store_name() -> str:
    return "test_mysql"


@pytest.fixture
def test_table() -> str:
    return "test_table"


@pytest.fixture
def project_config_file() -> Path:
    return Path(PROJECT_CONFIG_FILE)


@pytest.fixture
def profile() -> str:
    return "dev"


@pytest.fixture
def start_date() -> str:
    return datetime(2023, 1, 1)


@pytest.fixture
def mysql_user() -> str:
    return os.environ.get("MYSQL_USER")


@pytest.fixture
def mysql_password() -> str:
    return os.environ.get("MYSQL_PASSWORD")


@pytest.fixture
def mysql_host() -> str:
    return os.environ.get("MYSQL_HOST")


@pytest.fixture
def mysql_port() -> str:
    if os.getenv("GITHUB_ACTIONS") == "true":
        """This will help testing the monkeypatches locally.
        If set to true, the connections to mysql will fail if not correctly mocked.
        """
        return 5555
    return int(os.environ.get("MYSQL_PORT"))


@pytest.fixture
def mysql_db() -> str:
    return os.environ.get("MYSQL_DB")


@pytest.fixture
def stores_yaml(
    mysql_store_name: str,
    mysql_user: str,
    mysql_password: str,
    mysql_host: str,
    mysql_port: str,
    mysql_db: str,
) -> str:
    """https://www.mysqlql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS"""
    return f"""
    name: {mysql_store_name}
    profiles:
      dev:
        type: mysql
        config:
          connection:
            user: {mysql_user}
            password: {mysql_password}
            database: {mysql_db}
            host: {mysql_host}
            port: {mysql_port}
        """


@pytest.fixture
def mock_data() -> List:
    return user_data()


@pytest.fixture
def deidentified_mock_data() -> List:
    return user_data_deidentified()


@pytest.fixture
def mysql_connection(
    mysql_user: str,
    mysql_password: str,
    mysql_host: str,
    mysql_port: str,
    mysql_db: str,
    github_actions_pg: bool,
    monkeypatch: MonkeyPatch,
) -> MySQLConnection:
    if github_actions_pg:

        def __init__(self, **kwargs):
            self._consume_results: bool = False
            self._unread_result: bool = False
            if kwargs:
                self.connect(**kwargs)

        def cursor(self, *args, **kwargs) -> MySQLCursor:
            return MySQLCursor(self)

        monkeypatch.setattr(MySQLConnection, "__init__", __init__)
        monkeypatch.setattr(MySQLConnection, "close", lambda self: None)
        monkeypatch.setattr(MySQLConnection, "cursor", cursor)
        monkeypatch.setattr(MySQLConnection, "commit", lambda self: None)
        monkeypatch.setattr(MySQLConnection, "is_connected", lambda self: True)
        monkeypatch.setattr(
            MySQLConnectionAbstract, "connect", lambda self, **kwargs: None
        )

    return MySQLConnection(
        user=mysql_user,
        password=mysql_password,
        host=mysql_host,
        port=mysql_port,
        database=mysql_db,
    )


@pytest.fixture
def load_database(
    mysql_connection: MySQLConnection, mock_data: List, test_table: str
) -> MySQLConnection:
    with mysql_connection as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {test_table}")
            cursor.execute(
                f"CREATE TABLE {test_table} (created_at TIMESTAMP, name VARCHAR(255), email VARCHAR(255), postal_code VARCHAR(15), active BOOLEAN, ip VARCHAR(15))"  # noqa: E501
            )
            cursor.executemany(
                f"INSERT INTO {test_table} (created_at, name, email, postal_code, active, ip) VALUES (%s, %s, %s, %s, %s, %s)",  # noqa: E501
                mock_data,
            )
            conn.commit()

            yield conn

            cursor.execute(f"DROP TABLE IF EXISTS {test_table}")


@pytest.fixture
def mysql_adapter(
    stores_yaml: str,
    mysql_connection: MySQLConnection,
) -> MySQLAdapter:
    store_obj = yaml.safe_load(stores_yaml)
    mysql_obj = store_obj["profiles"]["dev"]
    pg_config = MySQLConfig.parse_obj(mysql_obj)
    return MySQLAdapter(config=pg_config.config)


@pytest.fixture
def catalogue_yaml() -> str:
    return raw_catalogue_yaml()


@pytest.fixture
def catalogue_parser(catalogue_yaml: str, monkeypatch: MonkeyPatch) -> CatalogueParser:
    path = Path("foo", "bar")

    def _parse_store_catalogues(self, *args, **kwargs) -> List[StoreCatalogue]:
        return [self._parse_yml()]

    def _parse_yml(self, *args, **kwargs) -> StoreCatalogue:
        info = yaml.safe_load(catalogue_yaml)
        info = {"name": self._store_name(path=path), "tables": info}
        return StoreCatalogue.parse_obj(info)

    monkeypatch.setattr(
        CatalogueParser, "_parse_store_catalogues", _parse_store_catalogues
    )
    monkeypatch.setattr(CatalogueParser, "_parse_yml", _parse_yml)

    return CatalogueParser(path=path)


@pytest.fixture
def mysql_query_factory(
    mysql_adapter: MySQLAdapter,
    catalogue_parser: CatalogueParser,
    test_table: str,
    start_date: datetime,
) -> QueryFactory:
    table = catalogue_parser.catalogue.stores[0].tables[test_table]
    return QueryFactory(adapter=mysql_adapter, table=table, start_date=start_date)
