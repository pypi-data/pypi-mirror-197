from contextlib import contextmanager

from blackline.adapters.sql import SQLAdapter
from blackline.models.mysql import MySQLConfig
from mysql.connector import MySQLConnection


class MySQLAdapter(SQLAdapter):
    def __init__(self, config: MySQLConfig.Config, *args, **kwargs):
        super().__init__(config=config, *args, **kwargs)

    @contextmanager
    def connection(self) -> MySQLConnection:
        conn_args = self.config.connection.dict()
        conn_args["password"] = conn_args["password"].get_secret_value()
        conn = MySQLConnection(**conn_args)
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()

    def test_connection(self) -> bool:
        return self.is_connected()

    def is_connected(self) -> bool:
        with self.connection() as conn:
            return conn.is_connected()

    def mask_template(self) -> str:
        return "{{ name }} = REGEXP_REPLACE(ip,'[:alnum:]',%({{ value }})s)"
