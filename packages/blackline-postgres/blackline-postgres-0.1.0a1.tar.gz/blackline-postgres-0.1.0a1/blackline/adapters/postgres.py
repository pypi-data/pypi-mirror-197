from blackline.adapters.sql import SQLAdapter
from blackline.models.postgres import PostgresConfig
from psycopg import Connection


class PostgresAdapter(SQLAdapter):
    def __init__(self, config: PostgresConfig.Config, *args, **kwargs):
        super().__init__(config=config, *args, **kwargs)

    def connection(self) -> Connection:
        conn = self.config.connection.dict()
        conninfo = conn["conninfo"]
        conn[
            "conninfo"
        ] = f"postgresql://{conninfo['user']}:{conninfo['password'].get_secret_value()}@{conninfo['host']}:{conninfo['port']}/{conninfo['dbname']}"  # noqa: E501
        return Connection.connect(**conn)

    def test_connection(self) -> bool:
        return not self.connection().closed

    def mask_template(self) -> str:
        return "{{ name }} = REGEXP_REPLACE(ip,'\\w',%({{ value }})s,'g')"
