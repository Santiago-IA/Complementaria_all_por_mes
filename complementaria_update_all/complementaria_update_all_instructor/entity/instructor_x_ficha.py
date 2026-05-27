import bd.db.queries as queries
from process.order_process import OrderProcess
from bd.db.record_manager import RecordManager
from bd.db.insert_into_histories import InsertIntoHistories
import pdb
import logging
import traceback


class InstructorXFicha(RecordManager):
    TABLE_NAME = "V_INSTRUCTORXFICHA_B"
    NAME_ID = "INF_ID"

    TABLE_NEWS_NAME = "NOVEDAD_ENROLL_C"

    NAME_ID_ENROLL_C = "ID_USUARIO_LMS_ENROLL"

    ACTIVE_STATES = ["V"]
    
    COL_DOC_TYPES = ["CC", "TI"]

    def __init__(self, oc_connection, pg_connection, record=None, fic_id=None):
        super().__init__(oc_connection, pg_connection)
        self.oc_connection = oc_connection
        self.pg_connection = pg_connection
        self.eca_record = record
        self.fic_id = fic_id

    def process(self):
        try:
            if self.eca_record is not None:
                self._update_depending_on_the_call()
            else:
                intructores_x_ficha = self._get_instructores_x_ficha(self.fic_id)
                self._iterate_on_records(intructores_x_ficha)
        except Exception as e:
            logging.error("excepcionI %s", e)
            if self.eca_record[0] != 0:
                OrderProcess.insert_status_process(
                    self.pg_connection,
                    self.eca_record,
                    f"EL INSTRUCTOR POR FICHA NO SE PUDO CREAR COMPLETAMENTE {e}",
                )
            insert_into_histories = InsertIntoHistories(self.pg_connection)
            insert_into_histories.insert(
                (
                    f"Ocurrio una excepción al realizar operaciones {e} {traceback.format_exc()}",
                    "excepciónI",
                    "error",
                )
            )

    def _iterate_on_records(self, records):
        print("Ingresando instructores por ficha")
        for ixf in records:
            self._validate_and_update_or_create_record(ixf)

    def _validate_and_update_or_create_record(self, ixf):
        if self._exist_in_db(queries.query_instructorxficha_post(), ixf[0]):
            self._update_depending_on_the_call(ixf)
        else:
            self._verify_intructor_or_create(ixf)

    def _update_depending_on_the_call(self, ixf=None):
        if self.eca_record is not None:
            self._update_from_eca_record()
        elif ixf is not None:
            self._update_all_row(ixf)

    def _update_from_eca_record(self):
        if self._exist_in_db(queries.query_instructorxficha_post(), self.eca_record[2]):
            inf_id, column_name, new_value = self._get_info_from_record(self.eca_record)
            columns_and_values = {column_name: new_value}
            self._register_newness_enroll_t(inf_id, new_value)
            self._update_column(
                self.TABLE_NAME, columns_and_values, self.NAME_ID, inf_id
            )
            OrderProcess.insert_status_process(
                self.pg_connection,
                self.eca_record,
                "EL INSTRUCTOR POR FICHA SE ACTUALIZO CORRECTAMENTE",
            )
        else:
            self._validate_if_fic_exist_and_create_or_update()

    def _register_newness_enroll_t(self, inf_id, value):
        if self._exist_in_db(queries.query_newness_enroll_ixf_c(), inf_id):
            self._update_suspend_state(inf_id, value)
        else:
            self._create_newness_enroll_if_needed(inf_id, value)

    def _create_newness_enroll_if_needed(self, inf_id, value):
        ixf_record = self._get_record_by_id_pg(
            queries.query_instructorxficha_post(), inf_id
        )
        # if ixf_record is None:
        nis = ixf_record[1]
        fic_id = ixf_record[2]
        ixf_state = ixf_record[3]

        enrollment = self._get_enrollment_by_nis_and_fic_id(nis, fic_id)

        if enrollment is not None:
            fic_data = self._get_info_ficha_for_enroll(inf_id)
            fun_record = self._get_record_by_id_pg(
                queries.query_funcionario_post(), ixf_record[1]
            )
            if (
                ixf_state != value
                and ixf_state in self.ACTIVE_STATES
                and value not in self.ACTIVE_STATES
                and fun_record[15] is not None
            ):
                suspend = 1
                print("ingresando novedad enroll instructor")
                self._create_record(
                    queries.insert_newness_ixf_enroll_c(),
                    (
                        inf_id,
                        value,
                        self.LMS_STATES["procesado"],
                        fun_record[0],
                        fun_record[15],
                        suspend,
                        "I",
                        fic_data[0],
                        fic_data[1],
                        3,
                    ),
                )

    def _update_suspend_state(self, inf_id, value):
        ixf_record = self._get_record_by_id_pg(
            queries.query_instructorxficha_post(), inf_id
        )
        ixf_state = ixf_record[3]
        print("actualizando novedad enroll instructor")
        if (
            ixf_state != value
            and ixf_state in self.ACTIVE_STATES
            and value not in self.ACTIVE_STATES
        ):
            suspend = 1
            self._update_newnewss_enroll(suspend, value, inf_id)
        elif (
            ixf_state != value
            and ixf_state not in self.ACTIVE_STATES
            and value in self.ACTIVE_STATES
        ):
            suspend = 0
            self._update_newnewss_enroll(suspend, value, inf_id)

    def _update_newnewss_enroll(self, suspend, value, inf_id):
        columns_and_values = {
            "suspend": suspend,
            "LMS_ESTADO": self.LMS_STATES["procesado"],
            "OPERATION": "U",
            "roleid": 3,
            "INF_ESTADO": value,
        }
        self._update_column(
            self.TABLE_NEWS_NAME, columns_and_values, self.NAME_ID, inf_id
        )

    def _get_info_ficha_for_enroll(self, inf_id):
        result = self.select_pg(queries.get_courseid_and_fic_id_by_inf_id(), (inf_id,))
        return result

    def _validate_if_fic_exist_and_create_or_update(self):
        intructor_x_ficha = self._get_intructor_x_ficha(self.eca_record[2])
        if intructor_x_ficha is not None:
            fic_id = intructor_x_ficha[2]
            if self._exist_in_db(queries.query_ficha_caracterizacion_post(), fic_id):
                self._verify_intructor_or_create(intructor_x_ficha)
            else:
                OrderProcess.insert_status_process(
                    self.pg_connection,
                    self.eca_record,
                    f"NO SE ENCONTRO LA FICHA DEL INSTRUCTOR {self.eca_record[2]}",
                )
        else:
            OrderProcess.insert_status_process(
                self.pg_connection,
                self.eca_record,
                f"NO SE ENCONTRO EL INSTRUCTOR X FICHA {self.eca_record[2]}",
            )

    def _update_all_row(self, ixf):
        self._register_newness_enroll_t(ixf[0], ixf[3])
        self.insert_or_update(
            queries.update_instructorxficha_row(), self._swap_first_and_last(ixf)
        )

    def _get_enrollment_by_nis_and_fic_id(self, nis, fic_id):
        result = self.select_pg(queries.get_enrollment_c_user(), (nis, fic_id))
        return result

    def _get_temporary_enrollment_by_nis_and_fic_id(self, nis, fic_id):
        result = self.select_pg(
            queries.get_temporary_user_enrollment_ixf_c(), (fic_id, nis)
        )
        return result

    def _get_intructor_x_ficha(self, inf_id):
        record = self.select_oc(
            queries.query_instructorxficha_by_inf_id_ora(), {"id": inf_id}
        )
        return record

    def _verify_intructor_or_create(self, ixf):
        inf_id = ixf[0]
        nis = ixf[1]
        fic_id = ixf[2]
        inf_state = ixf[3]
        if inf_state in self.ACTIVE_STATES:
            instructor_record = self._get_record_by_id(
                queries.query_funcionario_ora(), nis
            )
            if instructor_record is not None:
                print("ingresando funcionario")
                num_doc_concat = self._setup_user_if_identification_exist(instructor_record)
                instructor_list = list(instructor_record)
                instructor_list.append(self.LMS_STATES["procesado"])
                instructor_list.append(num_doc_concat)
                self._verify_or_create_record(
                    queries.query_funcionario_post(),
                    queries.insert_funcionario(),
                    nis,
                    tuple(instructor_list),
                )
                ixf_list = list(ixf)
                ixf_list.append(num_doc_concat)
                self._verify_or_create_record(
                    queries.query_instructorxficha_post(),
                    queries.insert_instructorxficha(),
                    nis,
                    tuple(ixf_list),
                )
                instructor_list_1 = list(instructor_record)
                instructor_list_1.append(inf_id)
                instructor_list_1.append(fic_id)
                self._add_instructor_user_lsm(tuple(instructor_list_1))
            else:
                print(f"\033[93m El instructor de NIS {nis}, no se encuentra en V_FUNCIONARIO_B\033[0m")

    def _swap_first_and_last(self, ixf):
        ixf_list = list(ixf)
        if len(ixf_list) >= 2:
            ixf_list[0], ixf_list[-1] = ixf_list[-1], ixf_list[0]
        ixf_tuple = tuple(ixf_list)
        return ixf_tuple

    def _add_instructor_user_lsm(self, record):
        print("ingresando usuario lms")
        user_data = self._get_user_data(record)
        self._verify_or_create_record(
            queries.query_usuario_lms(),
            queries.insert_instructor_lms(),
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
            type_doc_post = person[1]
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
        #num_doc_concat = self._setup_user_if_identification_exist(record)
        user_lms_data = []
        user_lms_data.append(record[0])  # nis
        user_lms_data.append(record[len(record) - 2])  #!inf_id
        user_lms_data.append(record[3])  # nombre
        user_lms_data.append(f"{record[4]} {seg_apellido} ")  # apellidos
        user_lms_data.append(record[6])  # correo
        user_lms_data.append(record[len(record) - 1])  #!fic_id
        user_lms_data.append(self.USER_TYPE["instructor"])  # user_tipo
        user_lms_data.append(self.LMS_STATES["procesado"])  # lms_estado
        user_lms_data.append(record[1])  # tipo_doc
        user_lms_data.append(record[2])  # num_doc
        #user_lms_data.append(num_doc_concat)  # num_doc_concat
        return tuple(user_lms_data)

    def _get_instructores_x_ficha(self, fic_id):
        records = self.select_oc(
            queries.query_instructorxficha_ora(), {"id": fic_id}, False
        )
        return records
