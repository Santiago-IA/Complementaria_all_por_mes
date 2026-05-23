import cx_Oracle
import psycopg2
import time
from dotenv import load_dotenv
import os
from db.insert_into_histories import InsertIntoHistories
from exception.connection_attemps_error import ConnectionAttemptsError

load_dotenv()


class ConnectionDB:
    def __init__(self, db_type, host, database, user, password, port):
        self.db_type = db_type
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        attempts = 0
        max_attempts = 3
        while attempts < max_attempts:
            try:
                if self.db_type == "oracle":
                    dsn = cx_Oracle.makedsn(
                        self.host, self.port, service_name=self.database
                    )
                    self.connection = cx_Oracle.connect(self.user, self.password, dsn)
                elif self.db_type == "postgres":
                    self.connection = psycopg2.connect(
                        host=self.host,
                        database=self.database,
                        user=self.user,
                        password=self.password,
                        port=self.port,
                        options="-c client_encoding=latin1",
                    )
                else:
                    print("Tipo de base de datos no soportado")
                    return

                print(f"Conexión exitosa a la base de datos {self.db_type}")
                return
            except cx_Oracle.Error as e:
                (error,) = e.args
                message = f"Error al conectar con SOFIA(Oracle): {error.message}"
                code = f"código de error: {error.code}"
                print(f"Error al conectar a Oracle: {error}")
                self._save_into_histories(message, code)
            except psycopg2.Error as e:
                print(f"Error al conectar a PostgreSQL: {e}")
                self._save_into_histories(str(e), "Código de error no disponible")

            attempts += 1
            print(f"Reintentando conexión {self.host} ({attempts}/{max_attempts})...")
            time.sleep(2)

        raise ConnectionAttemptsError(
            f"No se pudo establecer la conexión después de {max_attempts} intentos."
        )

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")

    def is_connected(self):
        return self.connection is not None

    def _connect_to_postgres(self, user, password, host, port, database):
        attempts = 0
        max_attempts = 3
        while attempts < max_attempts:
            try:
                connection = psycopg2.connect(
                    user=user,
                    password=password,
                    host=host,
                    port=port,
                    database=database,
                )
                print("Conexión a PostgreSQL establecida")
                return connection
            except psycopg2.Error as e:
                print(f"Error al conectar a PostgreSQL: {e}")
                attempts += 1
                print(f"Reintentando conexión ({attempts}/{max_attempts})...")
                time.sleep(2)

        raise ConnectionAttemptsError(
            f"No se pudo establecer la conexión a PostgreSQL después de {max_attempts} intentos."
        )

    def _save_into_histories(self, message, code):
        connection = self._connect_to_postgres(
            os.getenv("USER_PG"),
            os.getenv("PASS_PG"),
            os.getenv("HOST_PG"),
            os.getenv("PORT_PG"),
            os.getenv("SSID_PG"),
        )
        print("Conexión a PostgreSQL establecida para el historial")
        insert_into_histories = InsertIntoHistories(connection)
        print("Instancia de InsertIntoHistories creada")
        insert_into_histories.insert((message, code, "sin conexión"))
        print(
            "Método insert llamado con los argumentos:", (message, code, "sin conexión")
        )
        connection.close()
