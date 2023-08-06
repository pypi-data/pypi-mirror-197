"""
Some fixtures are mocked to avoid having to connect to a real database.
A postgres database is available while running tests locally using docker-compose.
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
from blackline.adapters.postgres import PostgresAdapter
from blackline.constants import PROJECT_CONFIG_FILE
from blackline.models.catalogue import StoreCatalogue
from blackline.models.postgres import PostgresConfig
from blackline.parsers.catalogue import CatalogueParser
from blackline.query.query_factory import QueryFactory
from blackline.utils.data.mock_data import user_data, user_data_deidentified
from blackline.utils.testing.catalogue import catalogue_yaml as raw_catalogue_yaml
from psycopg import Connection
from psycopg.pq import PGconn
from pytest import MonkeyPatch


@pytest.fixture
def github_actions_pg() -> bool:
    if os.getenv("GITHUB_ACTIONS") == "true":
        """This will help testing the monkeypatches locally.
        If set to true, the connections to postgres will fail if not correctly mocked.
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
def postgres_store_name() -> str:
    return "test_postgres"


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
def postgres_user() -> str:
    return os.environ.get("POSTGRES_USER")


@pytest.fixture
def postgres_password() -> str:
    return os.environ.get("POSTGRES_PASSWORD")


@pytest.fixture
def postgres_host() -> str:
    return os.environ.get("POSTGRES_HOST")


@pytest.fixture
def postgres_port() -> str:
    if os.getenv("GITHUB_ACTIONS") == "true":
        """This will help testing the monkeypatches locally.
        If set to true, the connections to postgres will fail if not correctly mocked.
        """
        return 5555
    return os.environ.get("POSTGRES_PORT")


@pytest.fixture
def postgres_db() -> str:
    return os.environ.get("POSTGRES_DB")


@pytest.fixture
def stores_yaml(
    postgres_store_name: str,
    postgres_user: str,
    postgres_password: str,
    postgres_host: str,
    postgres_port: str,
    postgres_db: str,
) -> str:
    """https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS"""
    return f"""
    name: {postgres_store_name}
    profiles:
      dev:
        type: postgres
        config:
          connection:
            conninfo:
              host: {postgres_host}
              port: {postgres_port}
              dbname: {postgres_db}
              user: {postgres_user}
              password: {postgres_password}
        """


@pytest.fixture
def mock_data() -> List:
    return user_data()


@pytest.fixture
def deidentified_mock_data() -> List:
    return user_data_deidentified()


@pytest.fixture
def postgres_connection(
    postgres_user: str,
    postgres_password: str,
    postgres_host: str,
    postgres_port: str,
    postgres_db: str,
    github_actions_pg: bool,
    monkeypatch: MonkeyPatch,
) -> Connection:
    conninfo = f"host={postgres_host} port={postgres_port} dbname={postgres_db} user={postgres_user} password={postgres_password}"  # noqa: E501

    if github_actions_pg:

        def _connect(*args, **kwargs):
            conn_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"  # noqa: E501
            conn_str = f"host={postgres_host} port={postgres_port} dbname={postgres_db} user={postgres_user} password={postgres_password}"  # noqa: E501
            if args:
                assert args[0] == conn_str or args[0] == conn_url
            if kwargs:
                assert kwargs["conninfo"] == conn_str or kwargs["conninfo"] == conn_url
            return Connection(pgconn=PGconn(None))

        monkeypatch.setattr(Connection, "connect", _connect)

    return Connection.connect(conninfo)


@pytest.fixture
def load_database(
    postgres_connection: Connection, mock_data: List, test_table: str
) -> Connection:
    with postgres_connection as conn:
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
def postgres_adapter(
    stores_yaml: str,
    postgres_connection: Connection,
) -> PostgresAdapter:
    store_obj = yaml.safe_load(stores_yaml)
    postgres_obj = store_obj["profiles"]["dev"]
    pg_config = PostgresConfig.parse_obj(postgres_obj)
    return PostgresAdapter(config=pg_config.config)


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
def postgres_query_factory(
    postgres_adapter: PostgresAdapter,
    catalogue_parser: CatalogueParser,
    test_table: str,
    start_date: datetime,
) -> QueryFactory:
    table = catalogue_parser.catalogue.stores[0].tables[test_table]
    return QueryFactory(adapter=postgres_adapter, table=table, start_date=start_date)
