from bd.db.record_manager import RecordManager
import bd.db.queries as queries
from bd.db.insert_into_histories import InsertIntoHistories
import logging
import traceback


class Competencia(RecordManager):
    def __init__(self, oc_connection, pg_connection, prf_id):
        super().__init__(oc_connection, pg_connection)
        self.oc_connection = oc_connection
        self.pg_connection = pg_connection
        self.prf_id = prf_id

    def process(self):
        try:
            compxprog = self._get_competencias_x_programa()
            if compxprog is not None:
                print("ingresando competencias")
                self._iterate_on_records(compxprog)
        except Exception as e:
            logging.error("exceptionCO %s", e)
            insert_into_histories = InsertIntoHistories(self.pg_connection)
            insert_into_histories.insert(
                (
                    f"Ocurrio una excepción al realizar operaciones en Competencia  {e} {traceback.format_exc()}",
                    "excepciónCO",
                    "error",
                )
            )

    def _iterate_on_records(self, compxpro):
        for cxp in compxpro:
            self._validate_and_update_or_create_record(cxp)

    def _validate_and_update_or_create_record(self, cxp):
        cmp_id = cxp[2]
        cpr_id = cxp[0]
        if not self._exist_in_db(queries.query_competenciaxprograma_post(), cpr_id):
            self._validate_competencia_or_create(cmp_id)
            self._create_record(queries.insert_competenciaxprograma(), cxp)
        self._run_rea_creation_process(cpr_id)

    def _run_rea_creation_process(self, cpr_id):
        resultados_aprendizaje = self._get_resultados_aprendizaje(cpr_id)
        if resultados_aprendizaje is not None:
            print("ingresando Resultados de aprendizaje")
            for rea in resultados_aprendizaje:
                self._validate_rea_or_create(rea)

    def _validate_rea_or_create(self, rea):
        if not self._exist_in_db(queries.query_resultado_aprendizaje_post(), rea[0]):
            self._create_record(queries.insert_resultado_aprendizaje(), rea)
            # self._validate_ixfrj_or_create(rea[0])

    def _validate_ixfrj_or_create(self, rea_id):
        instructor_resp_juicio = self._get_instructor_resp_juicio(rea_id)
        if instructor_resp_juicio is not None:
            print("ingresando Instructor Resp. Juicio")
            print(len(instructor_resp_juicio))
            for irj in instructor_resp_juicio:
                self._validate_irj_or_create(irj)

    def _validate_irj_or_create(self, irj):
        if not self._exist_in_db(queries.query_instructor_res_juicio_post(), irj[0]):
            print(f"52- {irj}")
            nis = irj[4]
            instructor_record = self._get_record_by_id(
                queries.query_funcionario_ora(), nis
            )
            if instructor_record is not None:
                print("ingresando funcionario resp juicio")
                instructor_list = list(instructor_record)
                instructor_list.append(self.LMS_STATES["procesado"])
                self._verify_or_create_record(
                    queries.query_funcionario_post(),
                    queries.insert_funcionario(),
                    nis,
                    tuple(instructor_list),
                )
                self._create_record(queries.insert_instructor_res_juicio(), irj)

    def _get_instructor_resp_juicio(self, rea_id):
        records = self.select_oc(
            queries.query_instructor_res_juicio_ora(), {"id": rea_id}, False
        )
        return records

    def _get_resultados_aprendizaje(self, cpr_id):
        records = self.select_oc(
            queries.query_resultado_aprendizaje_ora(), {"id": cpr_id}, False
        )
        return records

    def _validate_competencia_or_create(self, cmp_id):
        if not self._exist_in_db(queries.query_competencia_post(), cmp_id):
            competencia = self._get_record_by_id(
                queries.query_competencia_ora(), cmp_id
            )
            ltc_id = competencia[3]
            self._validate_linea_tecnologica_or_create(ltc_id)
            self._create_record(queries.insert_competencia(), competencia)

    def _validate_linea_tecnologica_or_create(self, ltc_id):
        if not self._exist_in_db(queries.query_linea_tecnologica_post(), ltc_id):
            linea_tecnologica = self._get_record_by_id(
                queries.query_linea_tecnologica_ora(), ltc_id
            )
            self._create_record(queries.insert_linea_tecnologica(), linea_tecnologica)

    def _get_competencias_x_programa(self):
        records = self.select_oc(
            queries.query_competenciaxprograma_ora(), {"id": self.prf_id}, False
        )
        return records
