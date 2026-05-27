import bd.db.queries as queries
from process.order_process import OrderProcess
from bd.db.record_manager import RecordManager
from bd.db.insert_into_histories import InsertIntoHistories
import bd.db.queries as queries
import pdb
import logging
import traceback
from services.migrate_temporal import MigrateTemporal


class RegistroAcademico(RecordManager):
    TABLE_NAME = "V_REGISTRO_ACADEMICO_B"
    NAME_ID = "RGA_ID"

    TABLE_NEWS_NAME = "NOVEDAD_ENROLL_C"

    NAME_ID_ENROLL_C = "ID_USUARIO_LMS_ENROLL"

    ACTIVE_STATES = [4, 7, 8]

    COL_DOC_TYPES = ["CC", "TI"]

    def __init__(self, oc_connection, pg_connection, record=None, fic_id=None):
        super().__init__(oc_connection, pg_connection)
        self.oc_connection = oc_connection
        self.pg_connection = pg_connection
        self.fic_id = fic_id
        self.eca_record = record

    def process(self):
        try:
            if self.eca_record is not None:
                self._update_depending_on_the_call()
            else:
                self._get_and_iterate_on_rgas()
        except Exception as e:
            logging.error("excepcionR %s", e)
            if self.eca_record is not None:
                OrderProcess.insert_status_process(
                    self.pg_connection,
                    self.eca_record,
                    f"EL REGISTRO ACADEMICO NO SE PUDO CREAR COMPLETAMENTE {e}",
                )
            insert_into_histories = InsertIntoHistories(self.pg_connection)
            insert_into_histories.insert(
                (
                    f"Ocurrio una excepción al realizar operaciones {e} {traceback.format_exc()}",
                    "excepciónR",
                    "error",
                )
            )

    def _get_and_iterate_on_rgas(self):
        registros_academicos = self._get_registros_academicos(self.fic_id)
        if registros_academicos is not None:
            self._iterate_on_records(registros_academicos)

    def _iterate_on_records(self, records):
        print("ingresando registros academicos")
        for rga in records:
            self._validate_and_update_or_create_record(rga)

    def _validate_and_update_or_create_record(self, rga):
        if self._exist_in_db(queries.query_registro_academico_post(), rga[0]):
            self._update_depending_on_the_call(rga)
        elif self._exist_in_db(queries.query_registro_academico_post_temp(), rga[0]):
            migrate_temporal = MigrateTemporal(
                self.oc_connection, self.pg_connection, rga
            )
            migrate_temporal.migrate()
        else:
            self._verify_apprentice_and_create(rga)

    def _update_depending_on_the_call(self, rga=None):
        print(f"67-{self.eca_record}-{rga}")
        if self.eca_record is not None:
            self._update_from_eca_record()
        elif rga is not None:
            self._update_all_row(rga)

    def _update_from_eca_record(self):
        if self._exist_in_db(
            queries.query_registro_academico_post(), self.eca_record[2]
        ):
            rga_id, column_name, new_value = self._get_info_from_record(self.eca_record)
            columns_and_values = {column_name: new_value}
            self._register_newness_enroll_c(rga_id, int(new_value))
            self._update_column(
                self.TABLE_NAME, columns_and_values, self.NAME_ID, rga_id
            )

        else:
            self._validate_if_fic_exist_and_create_or_update()

    def _register_newness_enroll_c(self, rga_id, value):
        if self._exist_in_db(queries.query_newness_enroll_rga_c(), rga_id):
            self._update_suspend_state(rga_id, value)
        else:
            self._create_newness_enroll_if_needed(rga_id, value)

    def _create_newness_enroll_if_needed(self, rga_id, value):
        rga_record = self._get_record_by_id_pg(
            queries.query_registro_academico_post(), rga_id
        )

        rga_state = rga_record[10]
        nis = rga_record[2]
        fic_id = rga_record[6]

        enrollment = self._get_enrollment_by_nis_and_fic_id(nis, fic_id)

        if enrollment is not None:
            fic_data = self._get_info_ficha_for_enroll(rga_id)
            person_record = self._get_record_by_id_pg(
                queries.query_persona_post(), rga_record[2]
            )
            if (
                rga_state != value
                and rga_state in self.ACTIVE_STATES
                and value not in self.ACTIVE_STATES
                and person_record[6] != 0
            ):
                suspend = 1
                print("ingresando novedad enroll aprendiz")
                self._create_record(
                    queries.insert_newness_rga_enroll_c(),
                    (
                        rga_id,
                        value,
                        self.LMS_STATES["procesado"],
                        person_record[0],
                        person_record[6],
                        suspend,
                        "I",
                        fic_data[0],
                        fic_data[1],
                        5,
                    ),
                )
                self._update_enroll_record_if_need(rga_id, fic_id, value)

    def _update_suspend_state(self, rga_id, value):
        rga_record = self._get_record_by_id_pg(
            queries.query_registro_academico_post(), rga_id
        )
        rga_state = rga_record[10]
        print("actualizando novedad enroll aprendiz")
        if (
            rga_state != value
            and rga_state in self.ACTIVE_STATES
            and value not in self.ACTIVE_STATES
        ):
            suspend = 1
            self._update_newnewss_enroll(suspend, value, rga_id)
        elif (
            rga_state != value
            and rga_state not in self.ACTIVE_STATES
            and value in self.ACTIVE_STATES
        ):
            suspend = 0
            self._update_newnewss_enroll(suspend, value, rga_id)
            self._update_enroll_record_if_need(rga_record[0], rga_record[6], value)

    def _update_newnewss_enroll(self, suspend, value, rga_id):
        columns_and_values = {
            "suspend": suspend,
            "LMS_ESTADO": self.LMS_STATES["procesado"],
            "OPERATION": "U",
            "roleid": 5,
            "RGA_ESTADO": value,
        }
        self._update_column(
            self.TABLE_NEWS_NAME, columns_and_values, self.NAME_ID, rga_id
        )

    def _get_info_ficha_for_enroll(self, rga_id):
        result = self.select_pg(queries.get_courseid_and_fic_id_by_rga_id(), (rga_id,))
        return result

    def _update_all_row(self, rga):
        self._register_newness_enroll_c(rga[0], int(rga[10]))
        self.insert_or_update(
            queries.update_registro_academico_row(), self._swap_first_and_last(rga)
        )

    def _update_enroll_record_if_need(self, rga_id, fic_id, value):
        rga_record = self._get_record_by_id_pg(
            queries.query_registro_academico_post(), rga_id
        )
        if rga_record is not None:
            enrollment = self._get_enrollment_by_nis_and_fic_id(rga_record[2], fic_id)
            if enrollment is not None:
                columns_and_values = {
                    "RGA_ESTADO": value,
                }
                table_name = "USUARIO_LMS_ENROLL_C"
                name_id = "ID_USUARIO_LMS_ENROLL"
                self._update_column(
                    table_name, columns_and_values, name_id, enrollment[0]
                )
        else:
            print(
                f"No se encontro el registro en postgres para el registro academico {rga_id}"
            )

    def _validate_if_fic_exist_and_create_or_update(self):
        registro_academico = self._get_registro_academico(self.eca_record[2])
        if registro_academico is not None:
            fic_id = registro_academico[6]
            if self._exist_in_db(queries.query_ficha_caracterizacion_post(), fic_id):
                self._verify_apprentice_and_create(registro_academico)
        else:
            OrderProcess.insert_status_process(
                self.pg_connection,
                self.eca_record,
                f"NO SE ENCONTRO EL REGISTRO ACADEMICO {self.eca_record[2]}",
            )

    def _swap_first_and_last(self, rga):
        rga_list = list(rga)
        if len(rga_list) >= 2:
            rga_list[0], rga_list[-1] = rga_list[-1], rga_list[0]
        rga_tuple = tuple(rga_list)
        return rga_tuple

    def _get_temporary_enrollment_by_nis_and_fic_id(self, nis, fic_id):
        result = self.select_pg(
            queries.get_temporary_user_enrollment_c(), (fic_id, nis)
        )
        return result

    def _get_enrollment_by_nis_and_fic_id(self, nis, fic_id):
        result = self.select_pg(queries.get_enrollment_c_user(), (nis, fic_id))
        return result

    def _verify_apprentice_and_create(self, rga):
        rga_id = rga[0]
        nis = rga[2]
        fic_id = rga[6]
        rga_estado = int(rga[10])
        if rga_estado in self.ACTIVE_STATES:
            person_record = self._get_record_by_id(queries.query_persona_ora(), nis)
            if person_record is not None:
                self._create_person(person_record, nis)
                num_doc_concat = self._setup_user_if_identification_exist(person_record)
                self._create_registro_academico(rga_id, rga,num_doc_concat)
                person_list = list(person_record)
                person_list.append(rga_id)
                person_list.append(fic_id)
                self._add_apprentice_user_lms(tuple(person_list))
            else:
                print(f"\033[93m El aprendiz de NIS {nis}, no se encuentra en V_PERSONA_B \033[0m")

    def _create_person(self, person_record, nis):
        print("ingresando persona")
        num_doc_concat = self._setup_user_if_identification_exist(person_record)
        person_list = list(person_record)
        person_list.append(self.LMS_STATES["procesado"])
        person_list.append(num_doc_concat)
        self._verify_or_create_record(
            queries.query_persona_post(),
            queries.insert_persona(),
            nis,
            tuple(person_list),
        )

    def _create_registro_academico(self, rga_id, rga,num_doc_concat):
        rga_list = list(rga)
        rga_list.append(num_doc_concat)
        self._verify_or_create_record(
            queries.query_registro_academico_post(),
            queries.insert_registro_academico(),
            rga_id,
            tuple(rga_list),
        )

    def _get_registros_academicos(self, fic_id):
        records = self.select_oc(
            queries.query_registros_academicos_ora(), {"id": fic_id}, False
        )
        return records

    def _get_registro_academico(self, rga_id):
        records = self.select_oc(queries.query_registro_academico_ora(), {"id": rga_id})
        return records

    def _add_apprentice_user_lms(self, record):
        print("inrgesando usuario lms")
        user_data = self._get_user_data(record)
        self._verify_or_create_record(
            queries.query_usuario_lms(),
            queries.insert_aprendiz_lms(),
            record[0],
            user_data,
        )

    def _setup_user_if_identification_exist(self, person):
        type_doc_ora = person[1]
        num_doc_ora = person[2]
        person = self._get_record_by_id_pg(
            queries.query_persona_document_post(), num_doc_ora
        )
        if person is not None:
            type_doc_post = person[12]
            if (
                type_doc_ora in self.COL_DOC_TYPES
                and type_doc_post in self.COL_DOC_TYPES
            ):
                return ""
            elif (
                (
                    type_doc_ora not in self.COL_DOC_TYPES
                    and type_doc_post in self.COL_DOC_TYPES
                )
                or (
                    type_doc_ora in self.COL_DOC_TYPES
                    and type_doc_post not in self.COL_DOC_TYPES
                )
                or (
                    type_doc_ora not in self.COL_DOC_TYPES
                    and type_doc_post not in self.COL_DOC_TYPES
                )
            ):
                return f"{num_doc_ora}{type_doc_ora.lower()}"
        else:
            return f"{num_doc_ora}{type_doc_ora.lower()}"

    def _get_user_data(self, record):
        seg_apellido = record[5] if record[5] is not None else " "
        # num_doc_concat = self._setup_user_if_identification_exist(record)
        user_lms_data = []
        user_lms_data.append(record[0])  # nis
        user_lms_data.append(record[len(record) - 2])  #!rga_id
        user_lms_data.append(record[3])  # nombre
        user_lms_data.append(f"{record[4]} {seg_apellido} ")  # apellidos
        user_lms_data.append(record[6])  # correo
        user_lms_data.append(record[len(record) - 1])  #!fic_id
        user_lms_data.append(self.USER_TYPE["aprendiz"])  # user_tipo
        user_lms_data.append(self.LMS_STATES["procesado"])  # lms_estado
        user_lms_data.append(record[1])  # tipo_doc
        user_lms_data.append(record[2])  # num_doc
        # user_lms_data.append(num_doc_concat)  # num_doc_concat
        return tuple(user_lms_data)
