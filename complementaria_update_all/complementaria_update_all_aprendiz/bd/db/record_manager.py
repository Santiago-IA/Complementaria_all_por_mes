from db.querys_db import QuerysDB
from psycopg2 import sql
import db.queries as queries


class RecordManager(QuerysDB):
    LMS_STATES = {
        "procesado": 1,
        "migrado": 2,
        "implementado": 3,
        "sincronizado": 4,
        "finalizado": 5,
        "error": 6,
    }

    USER_TYPE = {"instructor": 3, "aprendiz": 5}

    SCHEMA_INTEGRACION = "INTEGRACION"
    SCHEMA_TEMPORAL = "TEMPORAL"

    def __init__(self, oc_connection, pg_connection):
        super().__init__(oc_connection, pg_connection)
        self.oc_connection = oc_connection
        self.pg_connection = pg_connection

    def _verify_or_create_record(self, query_select, query_insert, id, record):
        if record is not None and not self._exist_in_db(query_select, id):
            self._create_record(query_insert, record)

    def _create_record(self, query_insert, values):
        self.insert_or_update(query_insert, values)

    def _exist_in_db(self, query, id):
        result = self.select_pg(query, (id,))
        return False if result is None else True

    def _get_record_by_id(self, query_select, id):
        return self.select_oc(query_select, {"id": id})

    def _get_record_by_id_pg(self, query_select, id):
        return self.select_pg(query_select, (id,))

    def _get_info_from_record(self, eca_record):
        ica_id = eca_record[2]
        column_name = eca_record[3]
        new_value = eca_record[5]
        return ica_id, column_name, new_value

    def _get_enrollment_by_nis_and_fic_id(self, query, nis, fic_id):
        return self.select_pg(query, (nis, fic_id))

    def _update_column(
        self, table, columns_and_values, name_id, id, schema="INTEGRACION"
    ):
        set_pairs = []
        values = []
        for column, value in columns_and_values.items():
            set_pairs.append(sql.SQL("{} = %s").format(sql.Identifier(column)))
            values.append(value)
        set_clause = sql.SQL(", ").join(set_pairs)
        values.append(id)
        query = sql.SQL(queries.update_columns_and_values()).format(
            sql.Identifier(schema),
            sql.Identifier(table),
            set_clause,
            sql.Identifier(name_id),
        )
        self.insert_or_update(query, tuple(values))
