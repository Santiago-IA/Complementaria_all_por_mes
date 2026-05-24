import importlib
import pdb
from bd.db.querys_db import QuerysDB
from bd.db.insert_into_histories import InsertIntoHistories
from datetime import datetime, timedelta
import traceback
from .shared import get_class_name


class InternalProcess:
    ENTITY = {
        2: "ficha_caracterizacion",
        4: "registro_academico",
        6: "instructor_x_ficha",
    }

    def __init__(self, oc_connection, pg_connection):
        self.oc_connection = oc_connection
        self.pg_connection = pg_connection
        self.type_search = "all"
        self.periodo = None

    def execute(self, entity, type_search, periodo=None):
        try:
            self.type_search = type_search
            self.periodo = periodo
            fichas_c = self._get_fichas_complementaria(entity)
            print(f"Fichas complementarias para procesar {len(fichas_c)}")
            for fic_id in fichas_c:
                print(fic_id)
                self._define_what_process_run(None, entity, fic_id[0])
        except Exception as e:
            print("excepcioni", e,traceback.format_exc())
            insert_into_histories = InsertIntoHistories(self.pg_connection)
            insert_into_histories.insert(
                (
                    "No se encontraron Fichas para procesar en la tabla INDICE_CAMBIO ",
                    "sin datos",
                    "sin datos",
                )
            )

    def _get_fichas_complementaria(self, entity):
        oc_query = QuerysDB(self.oc_connection, self.pg_connection)
        results = oc_query.select_pg(self._query_fichas(entity), None, False)
        return results

    def _define_what_process_run(self, record, entity, fic_id):
        # print(f'40 {record}')
        module_name = f"entity.{self.ENTITY[entity]}"
        module = importlib.import_module(module_name)
        class_name = get_class_name(module_name.replace("_", " "))
        import_class = getattr(module, class_name)
        instance_class = import_class(
            self.oc_connection, self.pg_connection, record, fic_id
        )
        # pdb.set_trace()
        instance_class.process()


    def _query_fichas(self, entity):
        date_condition = ""
        
        start_date, end_date = self._get_date_of_initialization()
        
        if self.type_search == "month":
            date_condition = f""" AND "FIC"."FIC_FCH_INICIALIZACION" >= '{start_date}'::DATE """
        
        elif self.type_search == "year":
            date_condition = f""" AND "FIC"."FIC_FCH_INICIALIZACION" >= '{start_date}'::DATE AND "FIC"."FIC_FCH_INICIALIZACION" <= '{end_date}'::DATE """
        
        elif self.type_search == "all":
            if self.periodo:
                date_condition = f"""
            AND "FIC"."FIC_FCH_INICIALIZACION" >= '{start_date}'::DATE
            AND "FIC"."FIC_FCH_INICIALIZACION" < '{end_date}'::DATE
            """
            else:
                date_condition = f""" AND "FIC"."FIC_FCH_INICIALIZACION" <= '{end_date}'::DATE """
        
        query = f"""
        SELECT DISTINCT "FIC"."FIC_ID" 
        FROM "INTEGRACION"."V_FICHA_CARACTERIZACION_B" "FIC" 
        INNER JOIN "INTEGRACION"."V_PROGRAMA_FORMACION_B" "PRF" 
        ON "FIC"."PRF_ID" = "PRF"."PRF_ID"  
        AND "PRF"."PRF_TIPO_PROGRAMA" = 'C' 
        AND "FIC"."FIC_MOD_FORMACION" IN ('V','A') 
        WHERE 1=1 {date_condition} 
        ORDER BY "FIC"."FIC_ID" DESC
        """
        print(query)
        return query

    def _get_date_of_initialization(self):
        current_time = datetime.now()
        start_date = current_time.date()

        if self.type_search == "month":
            start_date = datetime(start_date.year, start_date.month, 1).date()
            return start_date.strftime("%Y-%m-%d"), None 

        elif self.type_search == "year":
            end_date = (datetime(start_date.year, start_date.month, 1) - timedelta(days=1)).date()
            start_date = datetime(start_date.year, 1, 1).date()
            return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

        elif self.type_search == "all":
            if self.periodo:
                mes, anio = self.periodo.split("_")
                anio = int("20" + anio)
                mes = int(mes)
                fecha_inicio = datetime(anio, mes, 1)
                if mes == 12:
                    fecha_fin = datetime(anio + 1, 1, 1)
                else:
                    fecha_fin = datetime(anio, mes + 1, 1)
                return fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d")

            start_date = datetime(start_date.year - 1, 1, 1).date()
            end_date = datetime(start_date.year, 12, 31).date()
            return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
