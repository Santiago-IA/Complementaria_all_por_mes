import importlib
import time
from bd.db.querys_db import QuerysDB
import bd.db.queries as queries
from bd.db.insert_into_histories import InsertIntoHistories
import pdb
from datetime import datetime
import logging
import traceback
import concurrent.futures
from bd.exception.timeout_exception import TimeoutException
from .shared import get_class_name

class OrderProcess:
    ENTITY = {
        2: "ficha_caracterizacion",
        4: "registro_academico",
        6: "instructor_x_ficha"
    }

    def __init__(self, oc_connection, pg_connection):
        self.oc_connection = oc_connection
        self.pg_connection = pg_connection

    def execute(self, starting_id, entity):
        print(starting_id, entity)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            try:
                if starting_id is not None:
                    future = executor.submit(
                        self._get_row_to_process, starting_id, entity
                    )
                    next_records = future.result(timeout=60)
                    print(next_records)
                    if len(next_records) >= 1:
                        print(f"25-{len(next_records)}-{starting_id}")
                        for record in next_records:
                            print("entro")
                            ent_id = record[1]
                            self._define_what_process_run(record, ent_id)
                            time.sleep(0.3)
                    else:
                        actual_date = datetime.now()
                        formatted_date = actual_date.strftime("%Y-%m-%d %H:%M:%S")
                        record = [
                            starting_id,
                            entity,
                            0,
                            None,
                            None,
                            None,
                            None,
                            formatted_date,
                        ]
                        OrderProcess.insert_status_process(
                            self.pg_connection,
                            tuple(record),
                            f"NO SE ENCONTRARON MÁS REGISTROS DE FICHA DESDE EL ICA_ID {starting_id}",
                        )
                        return

                time.sleep(0.3)
                start_id = self._get_next_id_to_start(entity)
                self.execute(start_id, entity)
                print(
                    f"No se encontraron mas registros para procesar en la tabla INDICE_CAMBIO desde el ICA_ID {starting_id} "
                )
            except concurrent.futures.TimeoutError:
                logging.error("La consulta tomó más de 15 minutos y fue interrumpida.")
                #self.oc_connection.disconnect()
                raise TimeoutException(
                    "La consulta tomó más de 15 minutos y fue interrumpida."
                )
            except Exception as e:
                logging.error("exepcionO %s", e)
                insert_into_histories = InsertIntoHistories(self.pg_connection)
                insert_into_histories.insert(
                    (
                        f"Ocurrio una excepción al realizar operaciones {e} {traceback.format_exc()}",
                        "excepciónO",
                        "error",
                    )
                )

    def _get_row_to_process(self, id, entity):
        oc_query = QuerysDB(self.oc_connection, self.pg_connection)
        query_params = {"ica_id": id, "entity": entity}
        order_query = self._get_order_query_other_entities(entity)
        results = oc_query.select_oc(order_query, query_params, False)
        return results

    def _get_next_id_to_start(self, entity):
        oc_query = QuerysDB(self.oc_connection, self.pg_connection)
        result = oc_query.select_pg(queries.get_last_row_processed(), (entity,))
        return result[0] if result is not None else None

    def _define_what_process_run(self, record, ent_id):
        print(f"40 {record}")
        module_name = f"entity.{self.ENTITY[ent_id]}"
        module = importlib.import_module(module_name)
        class_name = get_class_name(module_name.replace("_", " "))
        import_class = getattr(module, class_name)
        instance_class = import_class(self.oc_connection, self.pg_connection, record)
        instance_class.process()

    @classmethod
    def insert_status_process(cls, pg_connection, record, state):
        # print(f'70-{record}')
        pg_query = QuerysDB(None, pg_connection)
        print(record[0], record[1], record[2], state)
        pg_query.insert_or_update(
            OrderProcess.insert_to_icap(),
            (record[0], record[1], record[2], record[7], state),
        )

    def _get_order_query_ficha(self):
        return """
        SELECT
            ICA_ID,
            ENI_ID,
            ICA_ID_TABLA,
            ICA_NOMBRE_COLUMNA,
            ICA_VLR_ANTERIOR_COLUMNA,
            ICA_VLR_NUEVO_COLUMNA,
            ICA_OPERACION,
            ICA_FCH_OPERACION
        FROM
            (
                SELECT
                    CAM.ICA_ID,
                    CAM.ENI_ID,
                    CAM.ICA_ID_TABLA,
                    CAM.ICA_NOMBRE_COLUMNA,
                    CAM.ICA_VLR_ANTERIOR_COLUMNA,
                    CAM.ICA_VLR_NUEVO_COLUMNA,
                    CAM.ICA_OPERACION,
                    CAM.ICA_FCH_OPERACION,
                    ROW_NUMBER() OVER (
                        PARTITION BY CAM.ICA_ID_TABLA
                        ORDER BY
                            CAM.ICA_FCH_OPERACION DESC
                    ) AS rn
                FROM
                    INTEGRACION.INDICE_CAMBIO CAM
                    INNER JOIN INTEGRACION.V_REGISTRO_ACADEMICO_B RGA ON RGA.RGA_ID = CAM.ICA_ID_TABLA
                    INNER JOIN INTEGRACION.V_PROGRAMA_FORMACION_B PRF ON RGA.PRF_ID = PRF.PRF_ID
                    AND PRF.PRF_TIPO_PROGRAMA = 'C'
                WHERE
                    CAM.ICA_ID < :ica_id
                    AND CAM.ENI_ID = :entity
                    AND CAM.ICA_VLR_NUEVO_COLUMNA IS NOT NULL
                    AND CAM.ICA_VLR_ANTERIOR_COLUMNA != CAM.ICA_VLR_NUEVO_COLUMNA
                    AND CAM.ICA_FCH_OPERACION >= TO_DATE('2023-10-01', 'YYYY-MM-DD')
            )
        WHERE
            rn = 1
            AND ROWNUM <= 45000
        ORDER BY
            ICA_ID DESC
        """

    def _get_order_query_other_entities(self, entity):
        queries_entity = {
            2: self._get_order_query_ficha(),
            4: self._get_order_query_registro_academico(),
            6: self._get_order_query_instructor_x_ficha(),
            7: self._get_order_query_calificaciones(),
        }
        return queries_entity[entity]

    def _get_order_query_registro_academico(self):
        return """
        SELECT
            ICA_ID,
            ENI_ID,
            ICA_ID_TABLA,
            ICA_NOMBRE_COLUMNA,
            ICA_VLR_ANTERIOR_COLUMNA,
            ICA_VLR_NUEVO_COLUMNA,
            ICA_OPERACION,
            ICA_FCH_OPERACION
        FROM
            (
                SELECT
                    CAM.ICA_ID,
                    CAM.ENI_ID,
                    CAM.ICA_ID_TABLA,
                    CAM.ICA_NOMBRE_COLUMNA,
                    CAM.ICA_VLR_ANTERIOR_COLUMNA,
                    CAM.ICA_VLR_NUEVO_COLUMNA,
                    CAM.ICA_OPERACION,
                    CAM.ICA_FCH_OPERACION,
                    ROW_NUMBER() OVER (
                        PARTITION BY CAM.ICA_ID_TABLA
                        ORDER BY
                            CAM.ICA_FCH_OPERACION DESC
                    ) AS rn
                FROM
                    INTEGRACION.INDICE_CAMBIO CAM
                    INNER JOIN INTEGRACION.V_REGISTRO_ACADEMICO_B RGA ON RGA.RGA_ID = CAM.ICA_ID_TABLA
                    INNER JOIN INTEGRACION.V_PROGRAMA_FORMACION_B PRF ON RGA.PRF_ID = PRF.PRF_ID
                    AND PRF.PRF_TIPO_PROGRAMA = 'C'
                WHERE
                    CAM.ICA_ID < :ica_id
                    AND CAM.ENI_ID = :entity
                    AND CAM.ICA_VLR_NUEVO_COLUMNA IS NOT NULL
                    AND CAM.ICA_VLR_ANTERIOR_COLUMNA != CAM.ICA_VLR_NUEVO_COLUMNA
                    AND CAM.ICA_FCH_OPERACION >= TO_DATE('2023-10-01', 'YYYY-MM-DD')
            )
        WHERE
            rn = 1
            AND ROWNUM <= 45000
        ORDER BY
            ICA_ID DESC
        """

    def _get_order_query_instructor_x_ficha(self):
        return """
        SELECT
            ICA_ID,
            ENI_ID,
            ICA_ID_TABLA,
            ICA_NOMBRE_COLUMNA,
            ICA_VLR_ANTERIOR_COLUMNA,
            ICA_VLR_NUEVO_COLUMNA,
            ICA_OPERACION,
            ICA_FCH_OPERACION
        FROM
            (
                SELECT
                    CAM.ICA_ID,
                    CAM.ENI_ID,
                    CAM.ICA_ID_TABLA,
                    CAM.ICA_NOMBRE_COLUMNA,
                    CAM.ICA_VLR_ANTERIOR_COLUMNA,
                    CAM.ICA_VLR_NUEVO_COLUMNA,
                    CAM.ICA_OPERACION,
                    CAM.ICA_FCH_OPERACION,
                    ROW_NUMBER() OVER (
                        PARTITION BY CAM.ICA_ID_TABLA
                        ORDER BY
                            CAM.ICA_FCH_OPERACION DESC
                    ) AS rn
                FROM
                    INTEGRACION.INDICE_CAMBIO CAM
                    INNER JOIN INTEGRACION.V_INSTRUCTORXFICHA_B IXF ON IXF.INF_ID = CAM.ICA_ID_TABLA
                    INNER JOIN INTEGRACION.V_FICHA_CARACTERIZACION_B FIC ON IXF.FIC_ID = FIC.FIC_ID
                    AND FIC.FIC_MOD_FORMACION IN ('V', 'A')
                    AND FIC.FIC_ESTADO IN (1,7)
                    INNER JOIN INTEGRACION.V_PROGRAMA_FORMACION_B PRF ON FIC.PRF_ID = PRF.PRF_ID
                    AND PRF.PRF_TIPO_PROGRAMA = 'C'
                WHERE
                    CAM.ICA_ID < :ica_id
                    AND CAM.ENI_ID = :entity
                    AND CAM.ICA_VLR_NUEVO_COLUMNA IS NOT NULL
                    AND CAM.ICA_VLR_ANTERIOR_COLUMNA != CAM.ICA_VLR_NUEVO_COLUMNA
                    AND CAM.ICA_FCH_OPERACION >= TO_DATE('2023-10-01', 'YYYY-MM-DD')
                ORDER BY
                    CAM.ICA_ID ASC
            )
        WHERE
            rn = 1
            AND ROWNUM <= 45000
        ORDER BY
            ICA_ID DESC
        """

    def _get_order_query_calificaciones(self):
        return """
        SELECT
            ICA_ID,
            ENI_ID,
            ICA_ID_TABLA,
            ICA_NOMBRE_COLUMNA,
            ICA_VLR_ANTERIOR_COLUMNA,
            ICA_VLR_NUEVO_COLUMNA,
            ICA_OPERACION,
            ICA_FCH_OPERACION
        FROM
            (
                SELECT
                    CAM.ICA_ID,
                    CAM.ENI_ID,
                    CAM.ICA_ID_TABLA,
                    CAM.ICA_NOMBRE_COLUMNA,
                    CAM.ICA_VLR_ANTERIOR_COLUMNA,
                    CAM.ICA_VLR_NUEVO_COLUMNA,
                    CAM.ICA_OPERACION,
                    CAM.ICA_FCH_OPERACION,
                    ROW_NUMBER() OVER (
                        PARTITION BY CAM.ICA_ID_TABLA
                        ORDER BY
                            CAM.ICA_FCH_OPERACION DESC
                    ) AS rn
                FROM
                    INTEGRACION.INDICE_CAMBIO CAM
                    INNER JOIN INTEGRACION.V_FICHA_CARACTERIZACION_B FIC ON CAM.ICA_ID_TABLA = FIC.FIC_ID
                    AND FIC.FIC_MOD_FORMACION IN ('V', 'A')
                    AND FIC.FIC_ESTADO IN (1,7)
                    INNER JOIN INTEGRACION.V_PROGRAMA_FORMACION_B PRF ON FIC.PRF_ID = PRF.PRF_ID
                    AND PRF.PRF_TIPO_PROGRAMA = 'C'
                WHERE
                    CAM.ICA_ID < :ica_id
                    AND CAM.ENI_ID = :entity
                    AND CAM.ICA_VLR_NUEVO_COLUMNA IS NOT NULL
                    AND CAM.ICA_FCH_OPERACION >= TO_DATE('2023-10-01', 'YYYY-MM-DD')
                ORDER BY
                    CAM.ICA_ID ASC
            )
        WHERE
            rn = 1
            AND ROWNUM <= 45000
        ORDER BY
            ICA_ID DESC
        """

    @classmethod
    def insert_to_icap(cls):
        return """
        INSERT INTO "INTEGRACION"."INDICE_CAMBIO_PROCESADO_C"
                ("ICA_ID", "ENI_ID", "ICA_ID_TABLA","ICA_FCH_OPERACION","ESTADO")
                VALUES(%s,%s,%s,%s,%s);
        """
