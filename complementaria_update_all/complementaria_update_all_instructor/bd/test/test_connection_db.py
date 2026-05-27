import pytest
from unittest import mock
import psycopg2
import cx_Oracle
from db.connection_db import ConnectionDB
from db.insert_into_histories import InsertIntoHistories
import os


@pytest.fixture
def mock_env_variables(monkeypatch):
    monkeypatch.setenv("USER_PG", "test_user")
    monkeypatch.setenv("PASS_PG", "test_pass")
    monkeypatch.setenv("HOST_PG", "localhost")
    monkeypatch.setenv("PORT_PG", "5432")
    monkeypatch.setenv("SSID_PG", "test_db")


def test_connect_postgres_successful_connection():
    db = ConnectionDB(
        db_type="postgres",
        host="localhost",
        database="testdb",
        user="user",
        password="password",
        port=5432,
    )

    with mock.patch("psycopg2.connect") as mock_connect:
        mock_connect.return_value = mock.Mock()

        db.connect()

        mock_connect.assert_called_once_with(
            host="localhost",
            database="testdb",
            user="user",
            password="password",
            port=5432,
            options="-c client_encoding=latin1",
        )
        assert db.is_connected()


def test_connect_postgres_retries_on_failure():
    db = ConnectionDB(
        db_type="postgres",
        host="localhost",
        database="testdb",
        user="user",
        password="password",
        port=5432,
    )

    with mock.patch(
        "psycopg2.connect", side_effect=psycopg2.OperationalError
    ), mock.patch("time.sleep"):
        with pytest.raises(
            Exception,
            match="No se pudo establecer la conexión a PostgreSQL después de 3 intentos.",
        ):
            db.connect()

        assert not db.is_connected()


def test_connect_oracle_successful_connection():
    db = ConnectionDB(
        db_type="oracle",
        host="localhost",
        database="orcl",
        user="user",
        password="password",
        port=1521,
    )

    with mock.patch("cx_Oracle.connect") as mock_connect, mock.patch(
        "cx_Oracle.makedsn", return_value="dsn"
    ):
        mock_connect.return_value = mock.Mock()  # Simula una conexión exitosa

        db.connect()

        cx_Oracle.makedsn.assert_called_once_with(
            "localhost", 1521, service_name="orcl"
        )
        mock_connect.assert_called_once_with("user", "password", "dsn")
        assert db.is_connected()


# def test_connect_oracle_retries_on_failure():
#     db = ConnectionDB(db_type="oracle", host="localhost", database="orcl", user="user", password="password", port=1521)

#     with mock.patch("cx_Oracle.connect", side_effect=cx_Oracle.Error), mock.patch("cx_Oracle.makedsn", return_value=("dsn",)), mock.patch("time.sleep"):
#         with pytest.raises(Exception, match="No se pudo establecer la conexión después de 3 intentos."):
#             db.connect()

#         assert not db.is_connected()


@mock.patch("db.connection_db.InsertIntoHistories")
@mock.patch("db.connection_db.ConnectionDB._connect_to_postgres")
def test_save_into_histories(
    mock_connect_to_postgres, mock_insert_into_histories, mock_env_variables
):
    db = ConnectionDB(
        db_type="postgres",
        host="localhost",
        database="testdb",
        user="user",
        password="password",
        port=5432,
    )

    mock_connection = mock.MagicMock()
    mock_connect_to_postgres.return_value = mock_connection

    mock_insert_instance = mock.MagicMock()
    mock_insert_into_histories.return_value = mock_insert_instance

    db._save_into_histories("Test message", 123)

    mock_connect_to_postgres.assert_called_once_with(
        "test_user", "test_pass", "localhost", "5432", "test_db"
    )

    mock_insert_into_histories.assert_called_once_with(mock_connection)

    mock_insert_instance.insert.assert_called_once_with(
        ("Test message", 123, "sin conexión")
    )

    mock_connection.close.assert_called_once()


def test_disconnect_closes_connection():
    db = ConnectionDB(
        db_type="postgres",
        host="localhost",
        database="testdb",
        user="user",
        password="password",
        port=5432,
    )
    db.connection = mock.Mock()

    db.disconnect()

    db.connection.close.assert_called_once()
