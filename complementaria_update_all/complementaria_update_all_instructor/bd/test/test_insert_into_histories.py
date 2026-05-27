import pytest
from unittest import mock
import psycopg2
from db.insert_into_histories import InsertIntoHistories


def test_insert_calls_execute_and_commit():
    mock_connection = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_connection.connection.cursor.return_value = mock_cursor

    insert_histories = InsertIntoHistories(mock_connection)
    
    data = ("event", "previous_state", "new_state")
    
    insert_histories.insert(data)
    
    query = """INSERT INTO "LOG"."HISTORIES" ("USER_ID","EVENT","PREVIOUS_STATE","NEW_STATE") VALUES (1,%s,%s,%s)"""
    mock_cursor.execute.assert_called_once_with(query, data)
    
    mock_connection.connection.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    
def test_insert_handles_exception_and_rolls_back():
    mock_cursor = mock.MagicMock()
    mock_connection = mock.MagicMock()
    mock_connection.connection.cursor.return_value = mock_cursor

    mock_cursor.execute.side_effect = psycopg2.Error("Simulated database error")

    insert_histories = InsertIntoHistories(mock_connection)

    data = ("event", "previous_state", "new_state")
    
    insert_histories.insert(data)
    
    query = """INSERT INTO "LOG"."HISTORIES" ("USER_ID","EVENT","PREVIOUS_STATE","NEW_STATE") VALUES (1,%s,%s,%s)"""
    mock_cursor.execute.assert_called_once_with(query, data)
    
    mock_connection.connection.rollback.assert_called_once()
    
    mock_connection.connection.commit.assert_not_called()