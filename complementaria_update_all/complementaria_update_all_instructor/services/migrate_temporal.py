from bd.db.record_manager import RecordManager
import bd.db.queries as queries
import traceback
import pdb


class MigrateTemporal(RecordManager):

    TABLE_PERSON = "V_PERSONA_B"
    NAME_ID = "NIS"
    ACTIVE_STATES = [4, 7, 8]

    def __init__(self, oc_connection, pg_connection, rga):
        self.oc_connection = oc_connection
        self.pg_connection = pg_connection
        self.rga = rga
        self.nis = rga[2]
        self.fic_id = rga[6]

    def migrate(self):
        try:
            if int(self.rga[10]) in self.ACTIVE_STATES:
                print(f"Migrando de temporal {self.nis}")
                self._create_registro_academico()
                self._migrate_person()
                self._migrate_usuario_lms()
                self._migrate_usuario_lms_enroll_c()
        except Exception as e:
            print(f"Error migrando datos de temporal: {e}", traceback.format_exc())

    def _create_registro_academico(self):
        self._create_record(queries.insert_registro_academico(), self.rga)

    def _migrate_person(self):
        person = self._get_record_by_id_pg(queries.query_person_temporal(), self.nis)
        if person is not None:
            self._verify_or_create_record(
                queries.query_persona_post(),
                queries.insert_persona_from_temporal(),
                self.nis,
                person,
            )
            columns_and_values = {"FLAG": 1}
            self._update_column(
                self.TABLE_PERSON,
                columns_and_values,
                self.NAME_ID,
                self.nis,
                self.SCHEMA_TEMPORAL,
            )

    def _migrate_usuario_lms(self):
        user_lms = self._get_record_by_id_pg(
            queries.query_usuario_lms_temporal(), self.nis
        )
        if user_lms is not None:
            self._verify_or_create_record(
                queries.query_usuario_lms(),
                queries.insert_usuario_lms_from_temporal(),
                self.nis,
                user_lms,
            )

    def _migrate_usuario_lms_enroll_c(self):
        user_lms_enroll = self.select_pg(
            queries.query_usuario_lms_enroll_c_temporal(), (self.fic_id, self.nis)
        )
        if user_lms_enroll is not None:
            user_lms_enroll_c = self._setup_new_rga_state(user_lms_enroll)
            self._create_record(
                queries.insert_usuario_lms_enroll_c(), user_lms_enroll_c
            )

    def _setup_new_rga_state(self, user_lms_enroll):
        user_lms_enroll_c = list(user_lms_enroll)
        user_lms_enroll_c[len(user_lms_enroll) - 1] = self.rga[10]
        return tuple(user_lms_enroll_c)
