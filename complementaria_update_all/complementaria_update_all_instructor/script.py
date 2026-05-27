import argparse
import logging
import traceback
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
import sys
import requests
import re

sys.path.append(os.path.join(os.path.dirname(__file__), 'bd'))

from bd.db.connection_db import ConnectionDB
from bd.db.querys_db import QuerysDB
from process.order_process import OrderProcess
from process.excel_process import ExcelProcess
from process.internal_process import InternalProcess
import bd.db.queries as queries
from bd.exception.timeout_exception import TimeoutException

load_dotenv()

STATUS_FILE = "process_status.json"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1310646916257939538/SJmWC6GeFB2a_FN5ryG8iL0vqShIrlv5a4mjAepYWWAJNtmm44sFQGGKvXawh-D12Ksb"

class DiscordLogger:
    def __init__(self, webhook_url, log_file="discord_log.txt"):
        self.webhook_url = webhook_url
        self.log_file = log_file

        # Limpia el archivo al inicio
        with open(self.log_file, "w") as file:
            file.write("")

    def check_internet_connection(self):
        try:
            requests.get("https://www.google.com", timeout=3)
            return True
        except requests.ConnectionError:
            return False

    def send_to_discord(self, message):
        if self.webhook_url and self.check_internet_connection():
            payload = {
                "content": message,
                "username": "Script compl. update all. instr",
                "avatar_url": "https://images.apifyusercontent.com/ylJFnQIrJeoB6NfMLwpoA_nh3d-0z_koAfJhgQqfLsU/rs:fill:250:250/aHR0cHM6Ly9hcGlmeS1pbWFnZS11cGxvYWRzLXByb2QuczMuYW1hem9uYXdzLmNvbS9XTDZXTmd1Vk9peDU1OWJ1aC85WG9NeVlUMnZyWHhva0o0cS1weXRob24tbG9nby5wbmc.webp",
            }
            try:
                requests.post(self.webhook_url, json=payload)
            except Exception as e:
                print(f"Error al enviar mensaje a Discord: {e}")

    def log_to_file(self, message):
        with open(self.log_file, "a") as file:
            file.write(message + "\n")

    def send_log_file(self):
        if self.webhook_url and self.check_internet_connection():
            with open(self.log_file, "rb") as file:
                payload = {
                    "content": "Log del script:",
                    "username": "Script compl. update all. instr",
                    "avatar_url": "https://images.apifyusercontent.com/ylJFnQIrJeoB6NfMLwpoA_nh3d-0z_koAfJhgQqfLsU/rs:fill:250:250/aHR0cHM6Ly9hcGlmeS1pbWFnZS11cGxvYWRzLXByb2QuczMuYW1hem9uYXdzLmNvbS9XTDZXTmd1Vk9peDU1OWJ1aC85WG9NeVlUMnZyWHhva0o0cS1weXRob24tbG9nby5wbmc.webp",
                }
                try:
                    response = requests.post(
                        self.webhook_url,
                        files={"file": (self.log_file, file)},
                        data=payload,
                    )
                    return True
                except Exception as e:
                    print(f"Error al enviar el archivo: {e}")

    def write(self, message):
        message = message.strip()
        if message:
            self.log_to_file(message)
            sys.__stdout__.write(message + "\n")  # Mantener salida en consola

    def flush(self):
        pass

def get_database_connections():
    return (
        ConnectionDB(
            "oracle",
            os.getenv("HOST_ORCL"),
            os.getenv("SSID_ORCL"),
            os.getenv("USER_ORCL"),
            os.getenv("PASS_ORCL"),
            os.getenv("PORT_ORCL"),
        ),
        ConnectionDB(
            "postgres",
            os.getenv("HOST_PG"),
            os.getenv("SSID_PG"),
            os.getenv("USER_PG"),
            os.getenv("PASS_PG"),
            os.getenv("PORT_PG"),
        ),
    )


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--excel", type=str, default="n", help="Ejecutar desde Excel s(si) n(no)"
    )
    parser.add_argument("--entity", type=int, default=6, help="Entidad a ejecutar")
    parser.add_argument(
        "--ica_id", type=int, default=0, help="Indice de cambio a ejecutar"
    )
    parser.add_argument(
        "--internal",
        type=str,
        default="s",
        help="Crea los diferentes registros a partir de las fichas internas ",
    )
    parser.add_argument(
        "--type_search",
        type=str,
        default="all",
        help="Determina como se cargarán las fichas a procesar, año, mes o todas",
    )
    parser.add_argument(
        "--periodo",
        type=str,
        default=None,
        help="Periodo en formato MM_YY ejemplo 02_26",
    )
    
    return parser.parse_args()


def read_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as file:
            return json.load(file)
    return {}


def write_status(status):
    with open(STATUS_FILE, "w") as file:
        json.dump(status, file)


def main():

    status = read_status()
    if status.get("in_progress", False):
        print("El proceso ya está en ejecución.")
        return

    start_time = time.time()
    start_time_readable = datetime.fromtimestamp(start_time).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    postgres_connection = None
    status["in_progress"] = True
    write_status(status)

    try:
        oracle_connection, postgres_connection = get_database_connections()
        oracle_connection.connect()
        postgres_connection.connect()

        args = parse_arguments()
        if args.type_search == "all":
            if not args.periodo:
                print("Error: Debe enviar --periodo en formato MM_YY (ej: 02_26)")
                return
            if not re.match(r"^\d{2}_\d{2}$", args.periodo):
                print("Error: Formato inválido. Use MM_YY (ej: 02_26)")
                return

        if args.excel == "s":
            excel_process = ExcelProcess(oracle_connection, postgres_connection)
            excel_process.execute()
        elif args.internal == "s":
            internal_process = InternalProcess(oracle_connection, postgres_connection)
            internal_process.execute(args.entity, args.type_search, args.periodo)
        else:
            query_db = QuerysDB(oracle_connection, postgres_connection)
            if args.ica_id != 0:
                data = query_db.select_pg(
                    queries.get_last_row_processed(), (args.entity,)
                )
                order_process = OrderProcess(oracle_connection, postgres_connection)
                order_process.execute(args.ica_id, args.entity)
            else:
                data = query_db.select_oc(queries.get_max_id_from_ica())
                order_process = OrderProcess(oracle_connection, postgres_connection)
                order_process.execute(data[0], args.entity)
    except TimeoutException as e:
        logging.error("Ocurrió una excepción-T: %s", e)
        return
    except Exception as e:
        logging.error("Ocurrió una excepciónS: %s", e)
        logging.error("Error: %s", traceback.format_exc())
    finally:
        end_time = time.time()
        end_time_readable = datetime.fromtimestamp(end_time).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        if postgres_connection is not None:
            try:
                query_db = QuerysDB(None, postgres_connection)
                count_fichas = query_db.select_pg(
                    queries.query_count_fichas(),
                    (start_time_readable, f"{end_time_readable}.999"),
                )
                count_aprendices = query_db.select_pg(
                    queries.query_count_aprendiz_formacion_c(),
                    (start_time_readable, f"{end_time_readable}.999"),
                )
                count_instructores = query_db.select_pg(
                    queries.query_count_instructor_formacion_c(),
                    (start_time_readable, f"{end_time_readable}.999"),
                )
                query_db.insert_or_update(
                    queries.insert_execution_report(),
                    (
                        count_fichas[0] or 0,
                        count_aprendices[0] or 0,
                        count_instructores[0] or 0,
                        start_time_readable,
                        end_time_readable,
                    ),
                )
            except Exception as e:
                logging.error("Error al registrar reporte de ejecución: %s", e)
        execution_time = end_time - start_time
        print("Tiempo de inicio:", start_time_readable, "segundos")
        print("Tiempo de finalización:", end_time_readable, "segundos")
        print("Tiempo de ejecución:", execution_time, "segundos")

        status["in_progress"] = False
        write_status(status)
        oracle_connection.disconnect()
        postgres_connection.disconnect()
        discord_logger.send_log_file()
        try:

            os.remove('discord_log.txt')
        except Exception as e:
            e


if __name__ == "__main__":
    discord_logger = DiscordLogger(DISCORD_WEBHOOK_URL)
    sys.stdout = discord_logger
    main()
