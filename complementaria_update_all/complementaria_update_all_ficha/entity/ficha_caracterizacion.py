import bd.db.queries as queries
from process.order_process import OrderProcess
from bd.db.record_manager import RecordManager
from entity.instructor_x_ficha import InstructorXFicha
from entity.registro_academico import RegistroAcademico
from entity.competencia import Competencia
from bd.db.insert_into_histories import InsertIntoHistories
import pdb
import logging
import traceback
from datetime import datetime


class FichaCaracterizacion(RecordManager):
    TABLE_NAME = "V_FICHA_CARACTERIZACION_B"
    NAME_ID = "FIC_ID"

    TABLE_NEWS_NAME = "NOVEDAD_FICHA_C"

    ACTIVE_STATES = [1, 7, 12]
    ENDED_FIC_STATE = 8

    actual_date = datetime.now()
    formatted_date = actual_date.strftime("%Y-%m-%d %H:%M:%S")

    def __init__(self, oc_connection, pg_connection, record=None, fic_id=None):
        super().__init__(oc_connection, pg_connection)
        self.oc_connection = oc_connection
        self.pg_connection = pg_connection
        self.eca_record = (
            record
            if record is not None
            else [0, 2, fic_id, None, None, None, None, self.formatted_date]
        )
        self.fic_id = fic_id

    def process(self):
        try:
            if self.eca_record[0] != 0:
                self._execute_process_from_ica()
            else:
                self._verify_record_is_execution_and_process(self.fic_id)
        except Exception as e:
            if self.eca_record[0] != 0:
                OrderProcess.insert_status_process(
                    self.pg_connection,
                    self.eca_record,
                    f"LA FICHA NO PUDO CREAR COMPLETAMENTE {e}",
                )
            logging.error("excepcionf %s", e)
            insert_into_histories = InsertIntoHistories(self.pg_connection)
            insert_into_histories.insert(
                (
                    f"Ocurrio una excepción al realizar operaciones {e} {traceback.format_exc()}",
                    "excepciónf",
                    "error",
                )
            )

    def _execute_process_from_ica(self):
        fic_id, column_name, new_value = self._get_info_from_record(self.eca_record)
        if self._exist_in_db(queries.query_ficha_caracterizacion_post(), fic_id):
            self._update_ficha(fic_id, column_name, new_value)
            OrderProcess.insert_status_process(
                self.pg_connection,
                self.eca_record,
                "LA FICHA SE ACTUALIZO CORRECTAMENTE",
            )
        else:
            self._verify_record_is_execution_and_process(fic_id)

    def _update_ficha(self, fic_id, column, value):
        columns_and_values = {column: value}
        self._register_newness_course_c(fic_id, int(value))
        self._update_column(self.TABLE_NAME, columns_and_values, self.NAME_ID, fic_id)

    def _register_newness_course_c(self, fic_id, value):
        if self._exist_in_db(queries.query_newness_course_c(), fic_id):
            self._update_visible_state(fic_id, value)
        else:
            self._create_newness_if_needed(fic_id, value)

    def _left_active_states(self, old_state, new_state):
        return (
            old_state != new_state
            and old_state in self.ACTIVE_STATES
            and new_state not in self.ACTIVE_STATES
        )

    def _entered_active_states(self, old_state, new_state):
        return (
            old_state != new_state
            and old_state not in self.ACTIVE_STATES
            and new_state in self.ACTIVE_STATES
        )

    def _create_newness_if_needed(self, fic_id, value):
        fic_record = self._get_record_by_id_pg(
            queries.query_ficha_caracterizacion_post(), fic_id
        )
        if fic_record is None or fic_record[21] is None:
            return

        fic_state = int(fic_record[17])
        if self._left_active_states(fic_state, value):
            print("ingresando novedad ficha")
            visible = 0
            operation = "U" if value == self.ENDED_FIC_STATE else "I"
            self._create_record(
                queries.insert_newness_course_c(),
                (
                    fic_id,
                    fic_record[21],
                    self.LMS_STATES["procesado"],
                    value,
                    visible,
                    operation,
                ),
            )

    def _update_visible_state(self, fic_id, value):
        fic_record = self._get_record_by_id_pg(
            queries.query_ficha_caracterizacion_post(), fic_id
        )
        if fic_record is None:
            return

        fic_state = int(fic_record[17])
        if self._left_active_states(fic_state, value):
            self._update_newness_ficha(0, value, fic_id)
        elif self._entered_active_states(fic_state, value):
            self._update_newness_ficha(1, value, fic_id)

    def _update_newness_ficha(self, visible, value, fic_id):
        print("actualizando novedad ficha")
        columns_and_values = {
            "visible": visible,
            "LMS_ESTADO": self.LMS_STATES["procesado"],
            "OPERATION": "U",
            "FIC_ESTADO": value,
        }
        self._update_column(
            self.TABLE_NEWS_NAME, columns_and_values, self.NAME_ID, fic_id
        )

    def _verify_record_is_execution_and_process(self, id):
        record = self.select_oc(queries.query_ficha_caracterizacion_ora(), {"id": id})
        if record is None:
            OrderProcess.insert_status_process(
                self.pg_connection,
                self.eca_record,
                "NO SE ENCONTRO LA FICHA EN SOFIA",
            )
        elif not self._exist_in_db(
            queries.query_ficha_caracterizacion_post(), record[0]
        ) and int(record[17]) in self.ACTIVE_STATES:
            self._create_all_records(record)
            OrderProcess.insert_status_process(
                self.pg_connection,
                self.eca_record,
                "LA FICHA SE CREO EXITOSAMENTE CON TODOS SUS DATOS",
            )
        else:
            self._update_ficha(record[0], "FIC_ESTADO", int(record[17]))

    def _create_all_records(self, fic_record):
        prf_id = fic_record[5]
        formation_program = self._get_record_by_id(
            queries.query_programa_formacion_ora(), prf_id
        )
        self._run_course_creation_process(formation_program, prf_id, fic_record)

    def _run_course_creation_process(self, formation_program, prf_id, fic_record):
        fic_list = list(fic_record)
        nfs_id = formation_program[4]
        ltc_id = formation_program[7]
        trd_id = formation_program[8]
        program_code = formation_program[1]
        fic_list.append(self.LMS_STATES["procesado"])
        fic_list.append(program_code)
        fic_list.append(0)
        fic_list.append("")
        fic_list.append(formation_program[6])
        fic_data = tuple(fic_list)
        if not self._exist_in_db(queries.query_programa_formacion_post(), prf_id):
            self._verify_or_create_record(
                queries.query_linea_tecnologica_post(),
                queries.insert_linea_tecnologica(),
                ltc_id,
                self._get_record_by_id(queries.query_linea_tecnologica_ora(), ltc_id),
            )
            self._verify_or_create_record(
                queries.query_nivel_formacion_post(),
                queries.insert_nivel_formacion(),
                nfs_id,
                self._get_record_by_id(queries.query_nivel_formacion_ora(), nfs_id),
            )
            self._verify_or_create_record(
                queries.query_tecnologia_red_post(),
                queries.insert_tecnologia_red(),
                trd_id,
                self._get_record_by_id(queries.query_tecnologia_red_ora(), trd_id),
            )
            self._create_record(queries.insert_programa_formacion(), formation_program)
        if not self._exist_in_db(
            queries.query_ficha_caracterizacion_post(), fic_record[0]
        ):
            self._create_record(queries.insert_ficha_caracterizacion(), fic_data)
        self._run_apprentice_creation_process(fic_record[0])
        self._run_instructor_creation_process(fic_record[0])
        self._run_competence_creation_process(prf_id)


    def _get_proyecto_aprendizaje_data(self, fic_id):
        record = self._get_record_by_id(
            queries.query_proyxregistro_academico_ora(), fic_id
        )
        if record is not None:
            pra_id = record[0]
            data = self._get_record_by_id(
                queries.query_proyecto_aprendizaje_ora(), pra_id
            )
            return data[0], data[1]

    def _run_competence_creation_process(self, prf_id):
        competencia = Competencia(self.oc_connection, self.pg_connection, prf_id)
        competencia.process()

    def _run_instructor_creation_process(self, fic_id):
        instructor_x_ficha = InstructorXFicha(
            self.oc_connection, self.pg_connection, None, fic_id
        )
        instructor_x_ficha.process()

    def _run_apprentice_creation_process(self, fic_id):
        registro_academico = RegistroAcademico(
            self.oc_connection, self.pg_connection, None, fic_id
        )
        registro_academico.process()

    def _run_competence_creation_process(self, prf_id):
        print("entro a competencia")
        competencia = Competencia(self.oc_connection, self.pg_connection, prf_id)
        competencia.process()

    def _create_programa_formacion(self, record):
        self.insert_or_update(queries.insert_programa_formacion(), record)
