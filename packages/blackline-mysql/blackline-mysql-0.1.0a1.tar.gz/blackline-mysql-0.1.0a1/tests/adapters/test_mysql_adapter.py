import yaml
from blackline.adapters.mysql import MySQLAdapter
from blackline.models.mysql import MySQLConfig
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from pytest import MonkeyPatch


def test_connection(
    stores_yaml: str,
    monkeypatch: MonkeyPatch,
    mysql_connection: MySQLConnection,
    github_actions_pg: bool,
) -> None:
    # Setup
    store_obj = yaml.safe_load(stores_yaml)
    mysql_obj = store_obj["profiles"]["dev"]
    mysql_config = MySQLConfig.parse_obj(mysql_obj)

    if github_actions_pg:

        def execute(self, *args, **kwargs):
            return None

        monkeypatch.setattr(MySQLCursor, "execute", execute)

        def fetchone(self):
            return (1,)

        monkeypatch.setattr(MySQLCursor, "fetchone", fetchone)

    # Run
    mysql_adapter = MySQLAdapter(config=mysql_config.config)
    with mysql_adapter.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            result = cur.fetchone()

    # Assert
    assert result[0] == 1


def test_is_connected(
    mysql_adapter: MySQLAdapter, monkeypatch: MonkeyPatch, github_actions_pg: bool
) -> None:
    # Run & Assert
    assert mysql_adapter.is_connected()
