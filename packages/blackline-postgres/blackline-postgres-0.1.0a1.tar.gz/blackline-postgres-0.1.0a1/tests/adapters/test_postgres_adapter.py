import yaml
from blackline.adapters.postgres import PostgresAdapter
from blackline.models.postgres import PostgresConfig
from psycopg import Connection, Cursor
from pytest import MonkeyPatch


def test_connection(
    stores_yaml: str,
    monkeypatch: MonkeyPatch,
    postgres_connection: Connection,
    github_actions_pg: bool,
) -> None:
    # Setup
    store_obj = yaml.safe_load(stores_yaml)
    postgres_obj = store_obj["profiles"]["dev"]
    pg_config = PostgresConfig.parse_obj(postgres_obj)

    if github_actions_pg:

        def _execute(self, *args, **kwargs):
            def fetchone(self):
                return (1,)

            monkeypatch.setattr(Cursor, "fetchone", fetchone)
            return Cursor(self)

        monkeypatch.setattr(Connection, "execute", _execute)

    # Run
    postgres_adapter = PostgresAdapter(config=pg_config.config)
    with postgres_adapter.connection() as conn:
        cur = conn.execute("SELECT 1")
        result = cur.fetchone()

    # Assert
    assert result[0] == 1


def test_test_connection(
    postgres_adapter: PostgresAdapter, monkeypatch: MonkeyPatch, github_actions_pg: bool
) -> None:
    # Setup
    if github_actions_pg:
        monkeypatch.setattr(Connection, "closed", 0)

    # Run & Assert
    assert postgres_adapter.test_connection()
