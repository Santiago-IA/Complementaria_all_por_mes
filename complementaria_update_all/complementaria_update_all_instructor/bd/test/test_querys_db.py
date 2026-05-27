import pytest
from unittest import mock
from db.querys_db import QuerysDB
from exception.timeout_exception import TimeoutException
import psycopg2
import concurrent.futures
import cx_Oracle
import json


class MockOracleError(Exception):
    def __init__(self, message, code):
        super().__init__(message)  # Llama al constructor de Exception
        self.message = message
        self.code = code


@pytest.fixture
def mock_connections():
    oc_connection = mock.Mock()
    pg_connection = mock.Mock()
    return oc_connection, pg_connection


@pytest.fixture
def mock_oracle_error():
    mock_error = mock.MagicMock()
    mock_error.args = ("Test error", 1234)
    return mock_error


@pytest.fixture
def mock_insert_into_histories():
    with mock.patch("db.insert_into_histories.InsertIntoHistories") as mock_histories:
        mock_instance = mock_histories.return_value
        mock_instance.insert = mock.MagicMock()
        yield mock_instance


def test_select_oc_timeout(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = QuerysDB(oc_connection, pg_connection)

    query = "SELECT * FROM test_table"
    params = {}

    with mock.patch(
        "concurrent.futures.ThreadPoolExecutor.submit",
        side_effect=concurrent.futures.TimeoutError,
    ):
        with pytest.raises(TimeoutException):
            manager.select_oc(query, params)


def test_select_pg_success(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = QuerysDB(oc_connection, pg_connection)

    query = "SELECT * FROM test_table WHERE id = %s"
    params = (1,)
    expected_result = ("value1", "value2")

    mock_cursor = mock.MagicMock()
    mock_cursor.fetchone.return_value = expected_result
    pg_connection.connection.cursor.return_value = mock_cursor

    result = manager.select_pg(query, params)

    pg_connection.connection.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(query, params)

    assert result == expected_result

    mock_cursor.close.assert_called_once()


def test_select_pg_error(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = QuerysDB(oc_connection, pg_connection)

    query = "SELECT * FROM test_table"
    params = (1,)

    pg_connection.connection.cursor.side_effect = psycopg2.Error("Test error")

    with mock.patch("builtins.print") as mock_print:
        result = manager.select_pg(query, params)

        call_args = mock_print.call_args
        assert call_args is not None
        printed_message = call_args[0][0]

        assert "Error al consultar datos TEST_TABLE:" in printed_message
        assert result is None


def test_insert_or_update(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = QuerysDB(oc_connection, pg_connection)

    query = "INSERT INTO test_table (column1) VALUES (%s)"
    data = ("value1",)

    mock_insert_into_histories = mock.MagicMock()
    with mock.patch(
        "db.insert_into_histories.InsertIntoHistories", mock_insert_into_histories
    ):
        pg_connection.connection.cursor.side_effect = psycopg2.Error("Test error")

        with mock.patch("builtins.print") as mock_print:
            manager.insert_or_update(query, data)

            call_args = mock_print.call_args
            assert call_args is not None
            printed_message = call_args[0][0]

            assert "Error al insertar datos:" in printed_message


def test_execute_special_query(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = QuerysDB(oc_connection, pg_connection)

    query = "UPDATE test_table SET column1 = %s WHERE id = %s"
    data = ("value1", 1)

    mock_insert_into_histories = mock.MagicMock()
    with mock.patch(
        "db.insert_into_histories.InsertIntoHistories", mock_insert_into_histories
    ):
        pg_connection.connection.cursor.side_effect = psycopg2.Error("Test error")

        with mock.patch("logging.error") as mock_error:
            manager.execute_special_query(query, data)

            mock_error.assert_called_once_with("Error al insertar datos: %s", mock.ANY)


def test_table_name(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = QuerysDB(oc_connection, pg_connection)

    query = "SELECT * FROM test_table WHERE id = %s"
    table_name = manager._table_name(query)

    assert table_name == "TEST_TABLE"


def test_execute_query_oc_success(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = QuerysDB(oc_connection, pg_connection)

    cursor = mock.MagicMock()
    oc_connection.connection.cursor.return_value = cursor

    query = "SELECT * FROM test_table WHERE id = :id"
    params = {"id": 1}
    expected_result = [("value1",)]

    cursor.fetchone.return_value = expected_result

    result = manager._execute_query_oc(query, params, one=True)
    assert result == expected_result

    cursor.execute.assert_called_once_with(query, params)
    cursor.close.assert_called_once()


def test_operation_type_update(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = QuerysDB(oc_connection, pg_connection)

    query = "UPDATE test_table SET column1 = 'value1' WHERE id = 1".lower()
    result = manager._operation_type(query)
    assert result == "update"


def test_operation_type_truncate(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = QuerysDB(oc_connection, pg_connection)

    query = "TRUNCATE TABLE test_table".lower()
    result = manager._operation_type(query)
    assert result == "truncate"


def test_execute_special_query_psycopg2_error(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = QuerysDB(oc_connection, pg_connection)

    query = "UPDATE test_table SET column1 = %s WHERE id = %s"
    data = ("value1", 1)

    pg_connection.connection.cursor.side_effect = psycopg2.Error("Test psycopg2 error")

    with mock.patch("logging.error") as mock_log_error:
        with mock.patch("psycopg2.Error", psycopg2.Error):
            manager.execute_special_query(query, data)

            pg_connection.connection.rollback.assert_called_once()

            mock_log_error.assert_called_once_with(
                "Error al insertar datos: %s", mock.ANY
            )


def test_insert_or_update_success(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = QuerysDB(oc_connection, pg_connection)

    query = "INSERT INTO test_table (column1) VALUES (%s)"
    data = ("value1",)

    mock_cursor = mock.MagicMock()
    pg_connection.connection.cursor.return_value = mock_cursor

    with mock.patch(
        "db.insert_into_histories.InsertIntoHistories"
    ) as mock_insert_histories:
        manager.insert_or_update(query, data)

        pg_connection.connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(query, data)
        pg_connection.connection.commit.assert_called_once()

        mock_cursor.close.assert_called_once()

        mock_insert_histories.assert_not_called()


def test_insert_or_update_psycopg2_error(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = QuerysDB(oc_connection, pg_connection)

    query = "INSERT INTO test_table (column1) VALUES (%s)"
    data = ("value1",)

    pg_connection.connection.cursor.side_effect = psycopg2.Error("Test psycopg2 error")

    with mock.patch("builtins.print") as mock_print:
        manager.insert_or_update(query, data)

        pg_connection.connection.rollback.assert_called_once()
        mock_print.assert_called_once_with("Error al insertar datos:", mock.ANY)

@mock.patch("db.querys_db.InsertIntoHistories")
def test_select_oc_cx_oracle_error(mock_insert_into_histories,mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = QuerysDB(oc_connection, pg_connection)

    # Creamos un mock para simular el objeto _Error de cx_Oracle
    mock_error = mock.MagicMock()
    mock_error.code = 544
    mock_error.message = "Test error message"

    mock_insert_instance = mock.MagicMock()
    mock_insert_into_histories.return_value = mock_insert_instance
    
    # Simulamos un cx_Oracle.DatabaseError con el objeto _Error en args
    with mock.patch('concurrent.futures.ThreadPoolExecutor') as mock_executor:
        mock_future = mock.MagicMock()
        # Configuramos el side_effect para que lance la excepción
        mock_future.result.side_effect = cx_Oracle.DatabaseError(mock_error)  # Aquí va el objeto, no un tuple
        mock_executor.return_value.__enter__.return_value.submit.return_value = mock_future   

        # Añadimos un print para verificar que la consulta se está ejecutando
        print("Ejecutando consulta en Oracle...")

        # Llamamos a select_oc, que debería capturar la excepción
        result = manager.select_oc("SELECT * FROM test")
        
        mock_insert_into_histories.assert_called_once_with(pg_connection)

        mock_insert_instance.insert.assert_called_once_with(
                ("Error al ejecutar la consulta en TEST en SOFIA(Oracle): Test error message", 544, "error")
            )

        assert result is None
