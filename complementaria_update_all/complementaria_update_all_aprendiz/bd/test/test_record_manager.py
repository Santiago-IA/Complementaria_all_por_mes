import pytest
from unittest import mock
from db.record_manager import RecordManager
from psycopg2 import sql


@pytest.fixture
def mock_connections():
    oc_connection = mock.Mock()
    pg_connection = mock.Mock()
    return oc_connection, pg_connection


def test_verify_or_create_record(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = RecordManager(oc_connection, pg_connection)

    query_select = "SELECT * FROM test WHERE id = %s"
    query_insert = "INSERT INTO test (id, value) VALUES (%s, %s)"
    id = 1
    record = (id, "value")

    with mock.patch.object(manager, "_exist_in_db", return_value=False):
        with mock.patch.object(manager, "_create_record") as mock_create_record:
            manager._verify_or_create_record(query_select, query_insert, id, record)
            mock_create_record.assert_called_once_with(query_insert, record)


def test_get_record_by_id_oc(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = RecordManager(oc_connection, pg_connection)

    query_select = "SELECT * FROM test WHERE id = :id"
    id = 1
    record = {"id": id, "value": "test"}

    with mock.patch.object(manager, "select_oc", return_value=record):
        result = manager._get_record_by_id(query_select, id)
        assert result == record


def test_get_record_by_id_pg(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = RecordManager(oc_connection, pg_connection)

    query_select = "SELECT * FROM test WHERE id = %s"
    id = 1
    record = {"id": id, "value": "test"}

    with mock.patch.object(manager, "select_pg", return_value=record):
        result = manager._get_record_by_id_pg(query_select, id)
        assert result == record


def test_update_column(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = RecordManager(oc_connection, pg_connection)

    table = "test_table"
    columns_and_values = {"column1": "value1", "column2": "value2"}
    name_id = "id"
    id = 1
    schema = "INTEGRACION"

    expected_query = sql.SQL("UPDATE {}.{} SET {} WHERE {} = %s").format(
        sql.Identifier(schema),
        sql.Identifier(table),
        sql.SQL(", ").join(
            [
                sql.SQL("{} = %s").format(sql.Identifier(col))
                for col in columns_and_values
            ]
        ),
        sql.Identifier(name_id),
    )

    with mock.patch.object(manager, "insert_or_update") as mock_insert_or_update:
        manager._update_column(table, columns_and_values, name_id, id, schema)
        mock_insert_or_update.assert_called_once_with(
            expected_query, tuple(columns_and_values.values()) + (id,)
        )


def test_get_info_from_record(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = RecordManager(oc_connection, pg_connection)

    eca_record = [None, None, 123, "column_name", None, "new_value"]

    id, column_name, new_value = manager._get_info_from_record(eca_record)

    assert id == 123
    assert column_name == "column_name"
    assert new_value == "new_value"


def test_get_enrollment_by_nis_and_fic_id(mock_connections):
    oc_connection, pg_connection = mock_connections
    manager = RecordManager(oc_connection, pg_connection)

    mock_query = "SELECT * FROM enrollments WHERE nis = %s AND fic_id = %s"
    nis = "some_nis"
    fic_id = "some_fic_id"
    expected_result = {"enrollment_data": "some_data"}
    manager.select_pg = mock.MagicMock(return_value=expected_result)

    result = manager._get_enrollment_by_nis_and_fic_id(mock_query, nis, fic_id)

    manager.select_pg.assert_called_once_with(mock_query, (nis, fic_id))

    assert result == expected_result
