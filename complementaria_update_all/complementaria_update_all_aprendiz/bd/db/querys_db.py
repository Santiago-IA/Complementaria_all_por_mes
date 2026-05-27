import cx_Oracle
import psycopg2
from db.insert_into_histories import InsertIntoHistories
from psycopg2 import sql
import pdb
import traceback
import concurrent.futures
from exception.timeout_exception import TimeoutException
import logging


class QuerysDB:
    TIME_OUT = 300

    def __init__(self, oc_connection, pg_connection):
        self.oc_connection = oc_connection
        self.pg_connection = pg_connection

    def select_oc(self, query, params={}, one=True):
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self._execute_query_oc, query, params, one)
                logging.info(future)
                return future.result(timeout=self.TIME_OUT)
        except concurrent.futures.TimeoutError:
            logging.error(
                f"La consulta tomó más de {self.TIME_OUT/60} minutos y fue interrumpida."
            )
            raise TimeoutException(
                f"La consulta tomó más de {self.TIME_OUT/60} minutos y fue interrumpida."
            )
        except cx_Oracle.Error as e:
            (error,) = e.args
            table = self._table_name(query)
            logging.error(f"Error al consultar datos {table}: {e}")
            insert_into_histories = InsertIntoHistories(self.pg_connection)
            insert_into_histories.insert(
                (
                    f"Error al ejecutar la consulta en {table} en SOFIA(Oracle): {error.message}",
                    error.code,
                    "error",
                )
            )
            return None

    def select_pg(self, query, params=None, one=True):
        try:
            cursor = self.pg_connection.connection.cursor()
            cursor.execute(query, params)
            datos = cursor.fetchone() if one else cursor.fetchall()
            cursor.close()
            return datos
        except psycopg2.Error as e:
            self.pg_connection.connection.rollback()
            table = self._table_name(query)
            print(f"Error al consultar datos {table}:", e)

    def insert_or_update(self, query, data):
        table = self._table_name(query)
        try:
            cursor = self.pg_connection.connection.cursor()
            cursor.execute(query, data)
            self.pg_connection.connection.commit()
            cursor.close()
            print(f"Consulta ejecutada {query}")
            print(f"Valores de la consulta {data}")
        except psycopg2.Error as e:
            self.pg_connection.connection.rollback()
            print("Error al insertar datos:", e)
        except Exception as e:
            self.pg_connection.connection.rollback() 
            insert_into_histories = InsertIntoHistories(self.pg_connection)
            insert_into_histories.insert(
                (
                    f"Error al ejecutar la inserción en la tabla {table} INTEGRACION(Postgres): {e.args} {traceback.format_exc()}",
                    e,
                    "error",
                )
            )
            print("Error al insertar datos:", e)

    def execute_special_query(self, query, data=None):
        try:
            cursor = self.pg_connection.connection.cursor()
            cursor.execute(query, data)
            self.pg_connection.connection.commit()
            cursor.close()

        except psycopg2.Error as e:
            self.pg_connection.connection.rollback()
            logging.error("Error al insertar datos: %s", e)
        except Exception as e:
            insert_into_histories = InsertIntoHistories(self.pg_connection)
            insert_into_histories.insert(
                (
                    f"Error al ejecutar el siguiente SQL {query} (Postgres): {e.args} {traceback.format_exc()}",
                    e,
                    "error",
                )
            )
            logging.error("Error al insertar datos: %s", e)

    def _table_name(self, query):
        if isinstance(query, sql.Composed):
            query = query.as_string(self.pg_connection.connection)
        query = query.lower()
        words = query.split()
        search_word = self._operation_type(query)
        index_from = words.index(search_word)
        table = words[index_from + 1]
        table = table.rstrip(",;").upper()
        return table

    def _execute_query_oc(self, query, params, one):
        cursor = self.oc_connection.connection.cursor()
        cursor.execute(query, params)
        datos = cursor.fetchone() if one else cursor.fetchall()
        cursor.close()
        return datos

    def _operation_type(self, query):
        search_word = None
        if "insert into" in query:
            search_word = "into"
        elif "update" in query:
            search_word = "update"
        elif "select" in query:
            search_word = "from"
        elif "truncate" in query:
            search_word = "truncate"
        return search_word
