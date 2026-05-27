#!  INSERT NIVEL_FORMACION ---------------------------------------------------------------


def insert_nivel_formacion():
    return """
INSERT INTO "INTEGRACION"."NIVEL_FORMACION" ("NFS_ID", "NFS_NOMBRE", "NFS_TIPO_FORMACION", "NFS_ESTADO", "NFS_DURACION_MAXIMA", "NFS_DURACION_MAX_ETAPA_PROD", "NFS_ORDEN", "NFS_OCULTAR_NIA", "NFS_OCULTAR_GRADO", "NFS_REQUISITO_ADICIONAL", "NFS_NIVEL", "NFS_INSCR_POSIBLES") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """


# *  INSERT  LINEA_TECNOLOGIA---------------------------------------------------------------
def insert_linea_tecnologica():
    return """
    INSERT INTO "INTEGRACION"."LINEA_TECNOLOGICA" ("LTC_ID", "LTC_NOMBRE", "LTC_DESCRIPCION")VALUES (%s,%s,%s)
            """


# *  INSERT  TECNOLOGIA_RED---------------------------------------------------------------
def insert_tecnologia_red():
    return """
    INSERT INTO "INTEGRACION"."TECNOLOGIA_RED"("TRD_ID", "TRD_NOMBRE", "TRD_FCH_CREACION", "LTC_ID") VALUES (%s,%s,%s,%s)
           """


# ?  INSERT  PROGRAMA_FORMACION---------------------------------------------------------------
def insert_programa_formacion():
    return """
    INSERT INTO "INTEGRACION"."V_PROGRAMA_FORMACION_B" ("PRF_ID", "PRF_CODIGO", "PRF_TIPO_PROGRAMA", "TIS_ID_OFRECIDO", "NFS_ID_OFRECIDO", "PRF_VERSION", "PRF_DENOMINACION", "LTC_ID", "TRD_ID", "PRF_DURACION_MAXIMA", "PRF_ALAMEDIDA", "PRF_EDAD_MIN_REQUERIDA", "NIA_ID_MIN_REQUERIDO", "PRF_GRADO_MIN_REQUERIDO", "PRF_ESTADO", "PRF_FCH_REGISTRO", "PRF_FCH_ACTIVO", "RGN_ID", "SED_ID", "PRF_FCH_CANCELACION", "PRF_MOTIVO_CANCELACION", "ARD_ID", "PRF_DUR_ETAPA_LECTIVA", "PRF_DUR_ETAPA_PROD", "PRF_RESOLUCION", "PRF_URL_MATERIAL", "ETF_ID", "PRF_REQUISITO_CERTIFICACION", "PRF_COMPETENCIA_MIN_INST", "PRF_CERTIFICA_TP")
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """


def insert_competencia():
    return """
    INSERT INTO "INTEGRACION"."COMPETENCIA"("CMP_ID", "CMP_NOMBRE", "CMP_ACTIVO", "LTC_ID","CMP_DURACION_MAXIMA","CMP_FCH_REGISTRO", "CMP_BASICA", "CMP_VERSION", "CMP_CODIGO","CMP_TIPO_COMPETENCIA", "CMP_GRUPO")
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """


def insert_competenciaxprograma():
    return """
        INSERT INTO "INTEGRACION"."COMPETENCIAXPROGRAMA"("CPR_ID", "PRF_ID", "CMP_ID", "CPR_ACTIVO", "MOD_ID", "CPR_FCH_REGISTRO")VALUES(%s,%s,%s,%s,%s,%s)
    """


def insert_resultado_aprendizaje():
    return """
   INSERT INTO "INTEGRACION"."RESULTADO_APRENDIZAJE"("REA_ID", "CPR_ID", "REA_ETAPA", "REA_NOMBRE", "REA_ESTADO") VALUES(%s,%s,%s,%s,%s)
    """


def insert_ficha_caracterizacion():
    return """
    INSERT INTO "INTEGRACION"."V_FICHA_CARACTERIZACION_B" ("FIC_ID", "FIC_CUPO", "RGN_ID", "SED_ID", "SSD_ID", "PRF_ID", "NIS_FUN_REGISTRO", "MPO_ID", "FIC_FCH_INICIALIZACION", "FIC_FCH_FINALIZACION", "FIC_RESPONSABLE", "LTC_ID", "TRD_ID", "NFS_ID_OFRECIDO", "FIC_MOD_FORMACION", "JOR_ID", "NIS_EMP", "FIC_ESTADO", "FIC_FCH_REGISTRO", "FIC_FCH_CANCELACION", "FIC_MOTIVO_CANCELACION","SEM_ID", "FIC_CUPO_MINIMO", "FIC_VECES_CUPO_PRUEBA", "NIS_FUN_GESTOR", "FIC_PROGRAMACION_APROBADA", "FIC_FCH_PROG_APROBADA", "POF_ID", "PRE_ID", "PRE_NOMBRE", "LMS_ESTADO", "PRF_CODIGO", "PRA_ID", "PRA_NOMBRE","PRF_DENOMINACION")  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """


def insert_instructorxficha():
    return """
    INSERT INTO "INTEGRACION"."V_INSTRUCTORXFICHA_B"("INF_ID", "NIS_FUN_INSTRUCTOR", "FIC_ID", "INF_ESTADO","NUM_DOC_CONCAT")VALUES(%s,%s,%s,%s,%s)
    """


def insert_funcionario():
    return """
    INSERT INTO "INTEGRACION"."V_FUNCIONARIO_B"("NIS", "TIPO_DOCUMENTO", "NUM_DOC_IDENTIDAD", "PER_NOMBRE", "PER_PRIMER_APELLIDO", "PER_SEGUNDO_APELLIDO", "PER_CORREO_E","RGN_ID","RGN_NOMBRE", "SED_ID", "SED_NOMBRE", "FUN_RESPON_FUNCIONAL","FUN_INSTRUCTOR", "NIS_JEFE_INMEDIATO", "FUN_ESTADO","LMS_ESTADO","NUM_DOC_CONCAT")VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """


def insert_instructor_res_juicio():
    return """
    INSERT INTO "INTEGRACION"."V_INSTRUCTOR_RESP_JUICIO_B" ("IRJ_ID", "AIR_ID", "INF_ID", "REA_ID", "NIS_FUN_INSTRUCTOR", "FIC_ID") VALUES(%s,%s,%s,%s,%s,%s)
    """


def insert_registro_academico():
    return """
    INSERT INTO "INTEGRACION"."V_REGISTRO_ACADEMICO_B" ("RGA_ID", "RGA_PERIODO", "NIS", "TIPO_DOCUMENTO", "NUM_DOC_IDENTIDAD", "ING_ID", "FIC_ID", "PRF_ID", "RTA_ID", "RGA_ETAPA_RUTA", "RGA_ESTADO", "RGA_FCH_REGISTRO", "RGA_FCH_ULTIMO_ESTADO", "NIS_EMP", "RGA_FCH_PASO_A_PRO", "RGA_FCH_FIN_FORMACION","NUM_DOC_CONCAT") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """


def insert_persona():
    return """
    INSERT INTO  "INTEGRACION"."V_PERSONA_B" ("NIS", "TIPO_DOCUMENTO", "NUM_DOC_IDENTIDAD", "PER_NOMBRE", "PER_PRIMER_APELLIDO", "PER_SEGUNDO_APELLIDO","PER_CORREO_E","LMS_ESTADO","NUM_DOC_CONCAT")VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """


def insert_proyxregistro_academico():
    return """
   INSERT INTO "INTEGRACION"."V_PROYXREGISTRO_ACADEMICO_B" ("PRG_ID", "RGA_ID", "PRA_ID", "PRG ESTADO", "PRG_FCH_INICIO", "PRG_FCH_FIN", "GRT_ID", "FIC_ID", "RGA_ESTADO", "NIS", "LMS_ID") 
   VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """


def insert_instructor_lms():
    return """ 
    INSERT INTO "INTEGRACION"."USUARIO_LMS" ("USR_NIS", "INF_ID", "USR_NOMBRE", "USR_APELLIDO", "USR_CORREO", "FIC_ID", "USR_TIPO", "LMS_ESTADO", "USR_TIPO_DOC", "USR_NUM_DOC","USR_NUM_DOC_CONCAT") VALUES(%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)
    """


def insert_aprendiz_lms():
    return """ 
    INSERT INTO "INTEGRACION"."USUARIO_LMS" ("USR_NIS", "RGA_ID", "USR_NOMBRE", "USR_APELLIDO", "USR_CORREO", "FIC_ID", "USR_TIPO", "LMS_ESTADO", "USR_TIPO_DOC", "USR_NUM_DOC","USR_NUM_DOC_CONCAT") VALUES(%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)
    """


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# *---------------------------------------------------------------SELECTS---------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


def query_usuario_lms():
    return """
    SELECT *
    FROM "INTEGRACION"."USUARIO_LMS" WHERE "USR_NIS" = %s
    """


# *------------------------------------------------------------------------------------------------------------
# ? LISTO


def query_linea_tecnologica_ora():
    return """
        SELECT LTC_ID,
        LTC_NOMBRE,
        LTC_DESCRIPCION
        FROM CATALOGO.LINEA_TECNOLOGICA
        WHERE LTC_ID = :id 
    """


def query_linea_tecnologica_post():
    return """
    SELECT 
    "LTC_ID",
    "LTC_NOMBRE","LTC_DESCRIPCION"
    FROM "INTEGRACION"."LINEA_TECNOLOGICA"
    WHERE "LTC_ID" = %s 
    """


# *-----------------------------------------------------------------------------------------------------------
# ? LISTO
def query_tecnologia_red_ora():
    return """
   select TRD_ID,
       TRD_NOMBRE,
       TRD_FCH_CREACION,
       LTC_ID FROM CATALOGO.TECNOLOGIA_RED WHERE TRD_ID = :id
    """


def query_tecnologia_red_post():
    return """
    SELECT "TRD_ID",
       "TRD_NOMBRE",
       "TRD_FCH_CREACION",
       "LTC_ID" FROM "INTEGRACION"."TECNOLOGIA_RED" WHERE "TRD_ID" = %s
    """


# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# Jerarquia de ejecucion de extraccion e insercion de datos
# --------------------------------------------------------------------------------------------------
# Se traen todos los registros que hayan en tabla CATALOGO.LINEA_TECNOLOGICA de la base de datos de SOFIA.


# --------------------------------------------------------------------------------------------------
# Se traen los registros de la tabla CATALOGO.NIVEL_FORMACION  que tengan NFS_

# ? LISTO


def query_nivel_formacion_ora():
    return """

    SELECT  
    NFS_ID,
	NFS_NOMBRE,
	NFS_TIPO_FORMACION,
	NFS_ESTADO,
	NFS_DURACION_MAXIMA,
	NFS_DURACION_MAX_ETAPA_PROD,
	NFS_ORDEN,
	NFS_OCULTAR_NIA,
	NFS_OCULTAR_GRADO,
	NFS_REQUISITO_ADICIONAL,
	NFS_NIVEL,
	NFS_INSCR_POSIBLES
    FROM CATALOGO.NIVEL_FORMACION
    WHERE NFS_ID = :id
    """


def query_nivel_formacion_post():
    return """

    SELECT  
    "NFS_ID",
	"NFS_NOMBRE",
	"NFS_TIPO_FORMACION",
	"NFS_ESTADO",
	"NFS_DURACION_MAXIMA",
	"NFS_DURACION_MAX_ETAPA_PROD",
	"NFS_ORDEN",
	"NFS_OCULTAR_NIA",
	"NFS_OCULTAR_GRADO",
	"NFS_REQUISITO_ADICIONAL",
	"NFS_NIVEL",
	"NFS_INSCR_POSIBLES"
    FROM "INTEGRACION"."NIVEL_FORMACION"
    WHERE "NFS_ID" = %s
    """


# --------------------------------------------------------------------------------------------------
# verificar el estado 3= vigente si se incluye en el where// RITA CONFIRMÓ QUE  ES EL ESTADO 3 "vigente" el que se debe filtrar.
# Se inserta los registros  de la tabla INTEGRACION.V_PROGRAMA_FORMACION_B y solo se traen los registros que tengan PRF_ESTADO= 3 (Vigente).


# ? LISTO DIANA
def query_programa_formacion_ora():
    return """
    SELECT
        PRF_ID, PRF_CODIGO, PRF_TIPO_PROGRAMA, TIS_ID_OFRECIDO, NFS_ID_OFRECIDO, PRF_VERSION, PRF_DENOMINACION, LTC_ID, TRD_ID, PRF_DURACION_MAXIMA, PRF_ALAMEDIDA, PRF_EDAD_MIN_REQUERIDA, NIA_ID_MIN_REQUERIDO, PRF_GRADO_MIN_REQUERIDO, PRF_ESTADO, PRF_FCH_REGISTRO, PRF_FCH_ACTIVO, RGN_ID, SED_ID, PRF_FCH_CANCELACION, PRF_MOTIVO_CANCELACION, ARD_ID, PRF_DUR_ETAPA_LECTIVA, PRF_DUR_ETAPA_PROD, PRF_RESOLUCION, PRF_URL_MATERIAL, ETF_ID, PRF_REQUISITO_CERTIFICACION, PRF_COMPETENCIA_MIN_INST, PRF_CERTIFICA_TP
        FROM INTEGRACION.V_PROGRAMA_FORMACION_B WHERE PRF_ID = :id AND PRF_ESTADO IN (1,3)
    """


def query_programa_formacion_post():
    return """
  SELECT
       "PRF_ID",
        "PRF_CODIGO",
        "PRF_TIPO_PROGRAMA",
        "TIS_ID_OFRECIDO",
        "NFS_ID_OFRECIDO",
        "PRF_VERSION",
        "PRF_DENOMINACION",
        "LTC_ID",
        "TRD_ID",
        "PRF_DURACION_MAXIMA",
        "PRF_ALAMEDIDA",
        "PRF_EDAD_MIN_REQUERIDA",
        "NIA_ID_MIN_REQUERIDO",
        "PRF_GRADO_MIN_REQUERIDO",
        "PRF_ESTADO",
        "PRF_FCH_REGISTRO",
        "PRF_FCH_ACTIVO",
        "RGN_ID",
        "SED_ID",
        "PRF_FCH_CANCELACION",
        "PRF_MOTIVO_CANCELACION",
        "ARD_ID",
        "PRF_DUR_ETAPA_LECTIVA",
        "PRF_DUR_ETAPA_PROD",
        "PRF_RESOLUCION",
        "PRF_URL_MATERIAL",
        "ETF_ID",
        "PRF_REQUISITO_CERTIFICACION",
        "PRF_COMPETENCIA_MIN_INST",
        "PRF_CERTIFICA_TP"
        FROM "INTEGRACION"."V_PROGRAMA_FORMACION_B" WHERE "PRF_ID" = %s
    """


# --------------------------------------------------------------------------------------------------
# Se insertan los registros de la tabla DISENIOCUR.COMPETENCIA que tengan el CPM_ACTIVO en 1 (activo).
# ? LISTO
def query_competencia_ora():
    return """
   SELECT  CMP.CMP_ID,
	CMP.CMP_NOMBRE,
        CMP.CMP_ACTIVO,
        CMP.LTC_ID,
        CMP.CMP_DURACION_MAXIMA,
        CMP.CMP_FCH_REGISTRO,
        CMP.CMP_BASICA,
        CMP.CMP_VERSION,
        CMP.CMP_CODIGO,
        CMP.CMP_TIPO_COMPETENCIA,
        CMP.CMP_GRUPO
        FROM DISENIOCUR.COMPETENCIA CMP WHERE CMP_ID = :id
"""


def query_competencia_post():
    return """
SELECT "CMP_ID", "CMP_NOMBRE", "CMP_ACTIVO", "LTC_ID", "CMP_DURACION_MAXIMA","CMP_FCH_REGISTRO","CMP_BASICA", "CMP_VERSION","CMP_CODIGO", "CMP_TIPO_COMPETENCIA", "CMP_GRUPO"
FROM "INTEGRACION"."COMPETENCIA" WHERE "CMP_ID" = %s
"""


# --------------------------------------------------------------------------------------------------
# la query trae los registros de la tabla DISENIOCUR.COMPETENCIAXPROGRAMA según los CMP_ID que estén descargados en la tabla DISENIOCUR.COMPETENCIA y adicional a esto , solo trae los registros del campo CPR_ACTIVO que esté en estado "Activo".
# Nota: se debe verificar la descripción del campo CPR_ACTIVO.


# ? LISTO
def query_competenciaxprograma_ora():
    return """
    SELECT CPR.CPR_ID,
       CPR.PRF_ID,
       CPR.CMP_ID,
       CPR.CPR_ACTIVO,
       CPR.MOD_ID,
       CPR.CPR_FCH_REGISTRO
       FROM DISENIOCUR.COMPETENCIAXPROGRAMA CPR WHERE CPR.PRF_ID = :id
    """


def query_competenciaxprograma_post():
    return """
        SELECT "CPR_ID", "PRF_ID", "CMP_ID", "CPR_ACTIVO", "MOD_ID", "CPR_FCH_REGISTRO"
        FROM "INTEGRACION"."COMPETENCIAXPROGRAMA" WHERE "CPR_ID" = %s
"""


# --------------------------------------------------------------------------------------------------
# Se traen los registros  a la tabla DISENIOCUR.RESULTADO_APRENDIZAJE según los CPR_ID traidos anteriormente en la tabla  DISENIOCUR.COMPETENCIAXPROGRAMA y se verifica que el campo REA_ESTADO sea  igual a 1(activo)- solo se traen los registros con el campo REA_ESTADO =1
# VALIDAR CONSULTA
# ? LISTO: JUAN
def query_resultado_aprendizaje_ora():
    return """
    SELECT  REA_ID,
	        CPR_ID,
            REA_ETAPA,
            REA_NOMBRE,
            REA_ESTADO
    FROM DISENIOCUR.RESULTADO_APRENDIZAJE 
    WHERE CPR_ID = :id
    """


def query_resultado_aprendizaje_post():
    return """
    SELECT *
    FROM "INTEGRACION"."RESULTADO_APRENDIZAJE" 
    WHERE "REA_ID" = %s
    """


# --------------------------------------------------------------------------------------------------
# Se traen las fichas de caracterización que estén en estado 7 "En ejecución" del campo FIC_ESTADO
# --------------------QUERY PARA TRAER LOS REGISTROS DE LA TABLA FICHA_CARACTERIZACION--------------------


# ? LISTO: JUAN
# * Query consulta Oracle
def query_ficha_caracterizacion_ora():
    return """
    SELECT FIC.FIC_ID,FIC.FIC_CUPO,FIC.RGN_ID,FIC.SED_ID,FIC.SSD_ID,FIC.PRF_ID,FIC.NIS_FUN_REGISTRO,FIC.MPO_ID,FIC.FIC_FCH_INICIALIZACION,FIC.FIC_FCH_FINALIZACION,FIC.FIC_RESPONSABLE, FIC.LTC_ID, FIC.TRD_ID, FIC.NFS_ID_OFRECIDO,FIC.FIC_MOD_FORMACION,FIC.JOR_ID,FIC.NIS_EMP,FIC.FIC_ESTADO,FIC.FIC_FCH_REGISTRO,FIC.FIC_FCH_CANCELACION,FIC.FIC_MOTIVO_CANCELACION,FIC.SEM_ID, FIC.FIC_CUPO_MINIMO, FIC.FIC_VECES_CUPO_PRUEBA, FIC.NIS_FUN_GESTOR, FIC.FIC_PROGRAMACION_APROBADA, FIC.FIC_FCH_PROG_APROBADA, FIC.POF_ID, FIC.PRE_ID, FIC.PRE_NOMBRE
    FROM INTEGRACION.V_FICHA_CARACTERIZACION_B FIC
    WHERE FIC.FIC_ID = :id
    """


# * Query consulta Postgres
def query_ficha_caracterizacion_post():
    return """
    SELECT "FIC_ID", "FIC_CUPO", "RGN_ID", "SED_ID", "SSD_ID", "PRF_ID", "NIS_FUN_REGISTRO", "MPO_ID", "FIC_FCH_INICIALIZACION", "FIC_FCH_FINALIZACION", "FIC_RESPONSABLE", "LTC_ID", "TRD_ID", "NFS_ID_OFRECIDO", "FIC_MOD_FORMACION", "JOR_ID", "NIS_EMP", "FIC_ESTADO", "FIC_FCH_REGISTRO", "FIC_FCH_CANCELACION", "FIC_MOTIVO_CANCELACION", "LMS_ID", "SEM_ID", "FIC_CUPO_MINIMO", "FIC_VECES_CUPO_PRUEBA", "NIS_FUN_GESTOR", "FIC_PROGRAMACION_APROBADA", "FIC_FCH_PROG_APROBADA", "POF_ID", "PRE_ID", "PRE_NOMBRE", "LMS_ESTADO", "PRF_CODIGO", "PRA_ID", "PRA_NOMBRE", "PRF_DENOMINACION"
    FROM "INTEGRACION"."V_FICHA_CARACTERIZACION_B"
    WHERE "FIC_ID" = %s
    """


# --------------------------------------------------------------------------------------------------
# se crea la query que llene los registros de la tabla INSTRUCTORXFICHA y que traiga solo los registros de los FIC_ID insertados en la tabla FICHA_CARACTERIZACION  y se valida que solo traiga los registros con campo INF_ESTADO=1 (Vigente)
# --------------------QUERY PARA  INSERTAR LA TABLA INSTRUCTORXFICHA--------------------
# ? LISTO: JU
def query_instructorxficha_ora():
    return """
    SELECT INF_ID,
           NIS_FUN_INSTRUCTOR,
           FIC_ID,
           INF_ESTADO
    FROM INTEGRACION.V_INSTRUCTORXFICHA_B
    WHERE FIC_ID = :id
    """


def query_instructorxficha_by_inf_id_ora():
    return """
    SELECT INF_ID,
           NIS_FUN_INSTRUCTOR,
           FIC_ID,
           INF_ESTADO
    FROM INTEGRACION.V_INSTRUCTORXFICHA_B
    WHERE INF_ID = :id
    """


def query_instructorxficha_post():
    return """
    SELECT *
    FROM "INTEGRACION"."V_INSTRUCTORXFICHA_B"
    WHERE "INF_ID" = %s
    """


# --------------------------------------------------------------------------------------------------
# Se traen los registros para insertarlos en la tabla V_FUNCIONARIO_B teniendo en cuenta todos los registros que existan asociados al campo NIS_FUN_INSTRUCTOR y a su ves que el campo FUN_ESTADO sea igual a 1(activo) -OSEA QUE EL FUNCIONARIO TENGA CONTRATO VIGENTE.
# --------------------QUERY PARA INSERTAR LOS REGISTROS DE LA TABLA INTEGRACION.V_FUNCIONARIO_B--------------------
# VALIDAR CONSULTA
# ? LISTO
def query_funcionario_ora():
    return """
    SELECT FUN.NIS,
       FUN.TIPO_DOCUMENTO,
       FUN.NUM_DOC_IDENTIDAD,
       FUN.PER_NOMBRE,
       FUN.PER_PRIMER_APELLIDO,
       FUN.PER_SEGUNDO_APELLIDO,
       FUN.PER_CORREO_E,
       FUN.RGN_ID,
       FUN.RGN_NOMBRE,
       FUN.SED_ID,
       FUN.SED_NOMBRE,
       FUN.FUN_RESPON_FUNCIONAL,
       FUN.FUN_INSTRUCTOR,
       FUN.NIS_JEFE_INMEDIATO,
       FUN.FUN_ESTADO
    FROM INTEGRACION.V_FUNCIONARIO_B FUN WHERE FUN.NIS = :id
    """


def query_funcionario_post():
    return """
    SELECT "NIS", "TIPO_DOCUMENTO", "NUM_DOC_IDENTIDAD", "PER_NOMBRE", "PER_PRIMER_APELLIDO", "PER_SEGUNDO_APELLIDO", "RGN_ID", "RGN_NOMBRE", "SED_ID", "SED_NOMBRE", "FUN_RESPON_FUNCIONAL", "FUN_INSTRUCTOR", "NIS_JEFE_INMEDIATO", "FUN_ESTADO", "LMS_ESTADO", "LMS_ID", "PER_CORREO_E"
    FROM "INTEGRACION"."V_FUNCIONARIO_B" WHERE "NIS" = %s
"""


# --------------------------------------------------------------------------------------------------
# Se insertan los registros a la tabla INSTRUCTOR_RESP_JUICIO asociados a los INF_ID registrados anteriormente en la tabla V_INSTRUCTORXFICHA_B ,teniendo en cuenta solo los que tengan el campo INF_ESTADO igual a 1(vigente)// solo se trae los registros de los Instructores que esten   en estado vigente en el campo INF_ESTADO.
# --------------------QUERY PARA INSERTAR LOS REGISTOS DE LA TABLA INSTRUCTOR_RESP_JUICIO--------------------
# VALIDAR CONSULTA
# ? LISTO: JUAN
def query_instructor_res_juicio_ora():
    return """
    SELECT IRJ_ID,AIR_ID, INF_ID,REA_ID,NIS_FUN_INSTRUCTOR,FIC_ID
    FROM INTEGRACION.V_INSTRUCTOR_RESP_JUICIO_B IRJ
    WHERE REA_ID = :id
    """


def query_instructor_res_juicio_post():
    return """
    SELECT *
    FROM "INTEGRACION"."V_INSTRUCTOR_RESP_JUICIO_B"
    WHERE "IRJ_ID" = %s
    """


# --------------------------------------------------------------------------------------------------
# -------------------QUERY PARA CREAR LA TABLA INTEGRACION.V_REGISTRO_ACADEMICO_B-------------------
# Se trae los registros asociados a todos los registros de la tabla FICHA_CARACTERIZACION insertados anteriormente y se pone la condición de que solo traiga los registros con el campo RGA_ESTADO= 7 (Formación)
# ? LISTO: JUAN
def query_registros_academicos_ora():
    return """
    SELECT 
       RGA_ID,
       RGA_PERIODO,
       NIS,
       TIPO_DOCUMENTO,
       NUM_DOC_IDENTIDAD,
       ING_ID,
       FIC_ID,
       PRF_ID,
       RTA_ID,
       RGA_ETAPA_RUTA,
       RGA_ESTADO,
       RGA_FCH_REGISTRO,
       RGA_FCH_ULTIMO_ESTADO,
       NIS_EMP,
       RGA_FCH_PASO_A_PRO,
       RGA_FCH_FIN_FORMACION
     FROM INTEGRACION.V_REGISTRO_ACADEMICO_B RGA
    WHERE FIC_ID = :id
    """


def query_registro_academico_ora():
    return """
    SELECT 
       RGA_ID,
       RGA_PERIODO,
       NIS,
       TIPO_DOCUMENTO,
       NUM_DOC_IDENTIDAD,
       ING_ID,
       FIC_ID,
       PRF_ID,
       RTA_ID,
       RGA_ETAPA_RUTA,
       RGA_ESTADO,
       RGA_FCH_REGISTRO,
       RGA_FCH_ULTIMO_ESTADO,
       NIS_EMP,
       RGA_FCH_PASO_A_PRO,
       RGA_FCH_FIN_FORMACION
     FROM INTEGRACION.V_REGISTRO_ACADEMICO_B RGA
    WHERE RGA_ID = :id 
    """


def query_registro_academico_post():
    return """
    SELECT 
       "RGA_ID", "RGA_PERIODO", "NIS", "TIPO_DOCUMENTO", "NUM_DOC_IDENTIDAD", "ING_ID", "FIC_ID", "PRF_ID", "RTA_ID", "RGA_ETAPA_RUTA", "RGA_ESTADO", "RGA_FCH_REGISTRO", "RGA_FCH_ULTIMO_ESTADO", "NIS_EMP", "RGA_FCH_PASO_A_PRO", "RGA_FCH_FIN_FORMACION"
    FROM "INTEGRACION"."V_REGISTRO_ACADEMICO_B" WHERE "RGA_ID" = %s
    """


# ------------------------------------------------------------------------------------------------------
# -------------------------QUERY NOTAS ESTUDIANTE-----------------------------------------------
# ---------------------------------------------------------------
def query_aprendiz_x_detalle_ruta_adr_ora():
    return """
    SELECT ADR_ID, ACA_ID, ACA_ID_ACT_VIRTUAL, ADR_ESTADO, ADR_EVALUACION_COMPETENCIA, ADR_EVALUACION_RESULTADO, ADR_FCH_EVALUO, ADR_FCH_FIN, ADR_FCH_INICIO, ADR_HORAS_DEDICADAS, ADR_PLAN_MEJORA, CMP_ID, NIS_FUN_EVALUO, PRG_ID, REA_ID,RGA_ID, FIC_ID
    FROM INTEGRACION.V_APRENDIZXDETALLERUTA_B WHERE ADR_ID = :id
    """


def query_aprendiz_x_detalle_ruta_fic_ora():
    return """
    SELECT ADR_ID, ACA_ID, ACA_ID_ACT_VIRTUAL, ADR_ESTADO, ADR_EVALUACION_COMPETENCIA, ADR_EVALUACION_RESULTADO, ADR_FCH_EVALUO, ADR_FCH_FIN, ADR_FCH_INICIO, ADR_HORAS_DEDICADAS, ADR_PLAN_MEJORA, CMP_ID, NIS_FUN_EVALUO, PRG_ID, REA_ID,RGA_ID, FIC_ID
    FROM INTEGRACION.V_APRENDIZXDETALLERUTA_B WHERE FIC_ID = :id
    """


def query_aprendiz_x_detalle_ruta_post():
    return """
    SELECT * FROM "INTEGRACION"."V_APRENDIZXDETALLE_RUTA_B" WHERE "ADR_ID" = %s
    """


def insert_aprendiz_x_detalle_ruta():
    return """
    INSERT INTO "INTEGRACION"."V_APRENDIZXDETALLE_RUTA_B"
("ADR_ID", "ACA_ID", "ACA_ID_ACT_VIRTUAL", "ADR_ESTADO", "ADR_EVALUACION_COMPETENCIA", "ADR_EVALUACION_RESULTADO", "ADR_FCH_EVALUO", "ADR_FCH_FIN", "ADR_FCH_INICIO", "ADR_HORAS_DEDICADAS", "ADR_PLAN_MEJORA", "CMP_ID", "NIS_FUN_EVALUO", "PRG_ID", "REA_ID","RGA_ID", "FIC_ID") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
    """


# --------------------------------------------------------------------------------------------------
# -------------------QUERY PARA TRAER LOS REGISTRO DE INTEGRACION.V_PERSONA_B-------------------
# Se traen todos los registros asociados al nis de la tabla REGISTRO_ACADEMICO y se insertan en la tabla INTEGRACION.V_PERSONA_B
# VALIDAR CONSULTA
# ? LISTO: JUAN
def query_persona_ora():
    return """
    SELECT
       NIS,
       TIPO_DOCUMENTO,
       NUM_DOC_IDENTIDAD,
       PER_NOMBRE,
       PER_PRIMER_APELLIDO,
       PER_SEGUNDO_APELLIDO,
       PER_CORREO_E
    FROM INTEGRACION.V_PERSONA_B
    WHERE NIS = :id
    """


def query_persona_post():
    return """
    SELECT
       "NIS", "TIPO_DOCUMENTO", "NUM_DOC_IDENTIDAD", "PER_NOMBRE", "PER_PRIMER_APELLIDO", "PER_SEGUNDO_APELLIDO", "LMS_ID", "LMS_ESTADO", "PER_CORREO_E"
    FROM "INTEGRACION"."V_PERSONA_B"
    WHERE "NIS" = %s
    """

def query_persona_document_post():
    return """
    SELECT "ID_USUARIO_LMS", "USR_NIS", "INF_ID", "RGA_ID", "USR_NOMBRE", "USR_APELLIDO", "USR_CORREO", "FIC_ID", "USR_TIPO", "LMS_ID", "LMS_ESTADO", "USR_TIPO_DOC", "USR_NUM_DOC", created_at, updated_at, "OPERATION"
    FROM "INTEGRACION"."USUARIO_LMS"
    WHERE "USR_NUM_DOC" = %s
    """


# --------------------------------------------------------------------------------------------------
# -------------------QUERY PARA LLENAR LOS REGISTROS DE LA TABLA PROYXREGISTRO_ACADEMMICO-------------------
# Se traen los registros  asociados al RGA_ID de la tabla REGISTRO_ACADEMICO y solo se insertan los registros que esten con el campo PRG_ESTADO = 1(En ejecución)
# ?listo
def query_proyxregistro_academico_ora():
    return """
        SELECT DISTINCT PRA_ID FROM INTEGRACION.V_PROYXREGISTRO_ACADEMICO_B WHERE FIC_ID = :id
    """


def query_proyecto_aprendizaje_ora():
    return """
    SELECT PRA_ID, PRA_NOMBRE FROM INTEGRACION.V_PROYECTO_APRENDIZAJE_B WHERE PRA_ID = :id
    """


# ------------------------------------------------------------------------------------------------------------
# *-----------------------------------------DATOS REGISTRO ACADEMICO Y USUARIOS -----------------------------------------------------
def update_registro_academico_row():
    return """
    UPDATE "INTEGRACION"."V_REGISTRO_ACADEMICO_B" 
    SET "RGA_FCH_FIN_FORMACION"=%s, "RGA_PERIODO"=%s, "NIS"=%s, "TIPO_DOCUMENTO"=%s, "NUM_DOC_IDENTIDAD"=%s, "ING_ID"=%s, "FIC_ID"=%s, "PRF_ID"=%s, "RTA_ID"=%s, "RGA_ETAPA_RUTA"=%s, "RGA_ESTADO"=%s, "RGA_FCH_REGISTRO"=%s, "RGA_FCH_ULTIMO_ESTADO"=%s, "NIS_EMP"=%s, "RGA_FCH_PASO_A_PRO"=%s 
    WHERE "RGA_ID"=%s
    """


def update_instructorxficha_row():
    return """
    UPDATE "INTEGRACION"."V_INSTRUCTORXFICHA_B" SET "INF_ESTADO"=%s,"NIS_FUN_INSTRUCTOR"=%s, "FIC_ID"=%s  WHERE "INF_ID"=%s
"""


def update_fichacaracterizacion_row():
    return """
    UPDATE "INTEGRACION"."V_FICHA_CARACTERIZACION_B" SET "FIC_CUPO=%s", "RGN_ID=%s", "SED_ID=%s", "SSD_ID=%s", "PRF_ID=%s", "NIS_FUN_REGISTRO=%s", "MPO_ID=%s", "FIC_FCH_INICIALIZACION=%s", 
    "FIC_FCH_FINALIZACION=%s", "FIC_RESPONSABLE=%s", "LTC_ID=%s", "TRD_ID=%s", "NFS_ID_OFRECIDO=%s", "FIC_MOD_FORMACION=%s", "JOR_ID=%s", "NIS_EMP=%s", 
    "FIC_ESTADO=%s","FIC_FCH_REGISTRO=%s", "FIC_FCH_CANCELACION=%s", "FIC_MOTIVO_CANCELACION=%s","SEM_ID=%s", "FIC_CUPO_MINIMO=%s", "FIC_VECES_CUPO_PRUEBA=%s", "NIS_FUN_GESTOR=%s", 
    "FIC_PROGRAMACION_APROBADA=%s", "FIC_FCH_PROG_APROBADA=%s", "POF_ID=%s", "PRE_ID=%s", "PRE_NOMBRE=%s", "LMS_ESTADO=%s", "NOMBRE_CURSO=%s","CODIGO_PROGRAMA=%s" WHERE "FIC_ID"=%s
"""

def get_last_row_processed():
    return """
        SELECT "ICA_ID" FROM "INTEGRACION"."INDICE_CAMBIO_PROCESADO_C" WHERE "ENI_ID" = %s  ORDER BY "ICAP_ID" DESC LIMIT 1
    """


def get_enrollment_c_user():
    return """
    SELECT "ID_USUARIO_LMS_ENROLL", "FIC_ID", courseid, roleid, userid, "LMS_ESTADO", "NIS", created_at, updated_at, enroll_state, "RGA_ESTADO"
    FROM "INTEGRACION"."USUARIO_LMS_ENROLL_C" WHERE "NIS" = %s AND "FIC_ID" = %s
    """


def get_temporary_user_enrollment_c():
    return """
        SELECT "F"."FIC_ID", "F"."LMS_ID" AS courseid, 5  AS roleid, "U"."LMS_ID" AS userid, "U"."USR_NIS", CASE 
        WHEN "RGA"."RGA_ESTADO" IN (4, 7, 8) THEN 0
        ELSE 1
	    END AS enroll_state,
	    "RGA"."RGA_ESTADO"
        FROM "INTEGRACION"."USUARIO_LMS" AS "U"
        INNER JOIN "INTEGRACION"."V_REGISTRO_ACADEMICO_B" AS "RGA" ON "RGA"."NIS" = "U"."USR_NIS"
        INNER JOIN "INTEGRACION"."V_FICHA_CARACTERIZACION_B" AS "F" ON "RGA"."FIC_ID" = "F"."FIC_ID"
         INNER JOIN "INTEGRACION"."V_PROGRAMA_FORMACION_B" AS "PRF" ON "PRF"."PRF_ID" = "F"."PRF_ID" AND "PRF"."PRF_TIPO_PROGRAMA" = 'C'
        WHERE "U"."LMS_ESTADO" = 2 AND "F"."LMS_ID" IS NOT NULL AND "F"."FIC_ID" = %s AND "U"."USR_NIS" = %s
    """


def get_temporary_user_enrollment_ixf_c():
    return """
        SELECT "F"."FIC_ID", "F"."LMS_ID" AS courseid, 3 AS roleid, "U"."LMS_ID" AS userid, "U"."USR_NIS",CASE "IXF"."INF_ESTADO"
        WHEN 'V' THEN 0
        ELSE 1
    	END AS enroll_state,
    	CASE "IXF"."INF_ESTADO"
        WHEN 'V' THEN 0
        ELSE 1
    	END AS "INF_ESTADO"
        FROM "INTEGRACION"."USUARIO_LMS" AS "U"
        INNER JOIN "INTEGRACION"."V_INSTRUCTORXFICHA_B" AS "IXF" ON "IXF"."NIS_FUN_INSTRUCTOR" = "U"."USR_NIS"
        INNER JOIN "INTEGRACION"."V_FICHA_CARACTERIZACION_B" AS "F" ON "IXF"."FIC_ID" = "F"."FIC_ID"
        INNER JOIN "INTEGRACION"."V_PROGRAMA_FORMACION_B" AS "PRF" ON "PRF"."PRF_ID" = "F"."PRF_ID" AND "PRF"."PRF_TIPO_PROGRAMA" = 'C'
        WHERE "U"."LMS_ESTADO" = 2 AND "F"."LMS_ID" IS NOT NULL AND "F"."FIC_ID" = %s AND "U"."USR_NIS" = %s
    """


def insert_enroll_c():
    return """
    INSERT INTO "INTEGRACION"."USUARIO_LMS_ENROLL_C"
    ("FIC_ID", courseid, roleid, userid, "NIS", enroll_state, "RGA_ESTADO")
    VALUES(%s, %s, %s, %s, %s, %s,%s)
    """


def get_enrollments_c():
    return """
    SELECT "ID_USUARIO_LMS_ENROLL", "FIC_ID", courseid, roleid, userid, "LMS_ESTADO", "NIS", created_at, updated_at, enroll_state, "RGA_ESTADO"
    FROM "INTEGRACION"."USUARIO_LMS_ENROLL_C" WHERE "FIC_ID" = %s
    """


def insert_newness_course_c():
    return """ 
    INSERT INTO "INTEGRACION"."NOVEDAD_FICHA_C"
    ("FIC_ID", courseid, "LMS_ESTADO","FIC_ESTADO", visible,"OPERATION")
    VALUES(%s, %s, %s, %s, %s,%s)
    """


def query_newness_course_c():
    return """
    SELECT NFC.*
    FROM "INTEGRACION"."NOVEDAD_FICHA_C" NFC
    WHERE NFC."FIC_ID" = %s
    """


def insert_newness_enroll_c():
    return """ 
    INSERT INTO "INTEGRACION"."NOVEDAD_ENROLL_C"
    ("RGA_ID", "RGA_ESTADO", "LMS_ESTADO", "NIS", userid, suspend,"OPERATION")
    VALUES(%s, %s, %s, %s, %s, %s,%s)
    """


def query_newness_enroll_c():
    return """
    SELECT *
    FROM "INTEGRACION"."NOVEDAD_ENROLL_C" WHERE "RGA_ID" = %s
    """


def get_courseid_and_fic_id_by_inf_id():
    return """
    SELECT "FIC"."FIC_ID", "FIC"."LMS_ID"  FROM "INTEGRACION"."V_FICHA_CARACTERIZACION_B" "FIC" INNER JOIN "INTEGRACION"."V_INSTRUCTORXFICHA_B" "INF" ON
    "FIC"."FIC_ID" = "INF"."FIC_ID" AND "INF"."INF_ID" = %s
    """


def get_courseid_and_fic_id_by_rga_id():
    return """
    SELECT "FIC"."FIC_ID", "FIC"."LMS_ID"  FROM "INTEGRACION"."V_FICHA_CARACTERIZACION_B" "FIC" INNER JOIN "INTEGRACION"."V_REGISTRO_ACADEMICO_B" "RGA" ON
    "FIC"."FIC_ID" = "RGA"."FIC_ID" AND "RGA"."RGA_ID" = %s
    """


def insert_newness_rga_enroll_c():
    return """ 
    INSERT INTO "INTEGRACION"."NOVEDAD_ENROLL_C"
    ("RGA_ID", "RGA_ESTADO", "LMS_ESTADO", "NIS", userid, suspend,"OPERATION","FIC_ID",courseid,roleid)
    VALUES(%s, %s, %s, %s, %s, %s,%s,%s,%s,%s)
    """


def query_newness_enroll_rga_c():
    return """
    SELECT *
    FROM "INTEGRACION"."NOVEDAD_ENROLL_C" WHERE "RGA_ID" = %s
    """


def insert_newness_ixf_enroll_c():
    return """ 
    INSERT INTO "INTEGRACION"."NOVEDAD_ENROLL_C"
    ("INF_ID", "INF_ESTADO", "LMS_ESTADO", "NIS", userid, suspend,"OPERATION","FIC_ID",courseid,roleid)
    VALUES(%s, %s, %s, %s, %s, %s,%s,%s,%s,%s)
    """


def query_newness_enroll_ixf_c():
    return """
    SELECT *
    FROM "INTEGRACION"."NOVEDAD_ENROLL_C" WHERE "INF_ID" = %s
    """

def get_max_id_from_ica():
    return """
    SELECT MAX(ICA_ID) FROM INTEGRACION.INDICE_CAMBIO
    """
    

def query_count_fichas():
    return """
    select count(*) from  "INTEGRACION"."V_FICHA_CARACTERIZACION_B" fic inner join "INTEGRACION"."V_PROGRAMA_FORMACION_B" prf on fic."PRF_ID" = prf."PRF_ID" 
    where "LMS_ID" is null and "LMS_ESTADO" =1 
   	and prf."PRF_TIPO_PROGRAMA" = 'C' 
  	and fic."FIC_MOD_FORMACION" in ('V','A') 
 	and fic.created_at between %s and %s
    """

def  query_count_aprendiz_formacion_c():
    return """ 
      SELECT count(*)
        FROM "INTEGRACION"."USUARIO_LMS" ul
        INNER JOIN "INTEGRACION"."V_REGISTRO_ACADEMICO_B" rga ON ul."USR_NIS" = rga."NIS"
        INNER JOIN "INTEGRACION"."V_FICHA_CARACTERIZACION_B" fic ON rga."FIC_ID" = fic."FIC_ID"
        INNER JOIN "INTEGRACION"."V_PROGRAMA_FORMACION_B" prf ON fic."PRF_ID" = prf."PRF_ID"
        WHERE ul."LMS_ID" IS NULL
          AND ul."LMS_ESTADO" = 1
          AND prf."PRF_TIPO_PROGRAMA" = 'C'
          AND fic."FIC_MOD_FORMACION" IN ('V', 'A')
          AND ul.created_at BETWEEN %s AND %s
    """
def  query_count_instructor_formacion_c():
    return """ 
      SELECT count(*)
        FROM "INTEGRACION"."USUARIO_LMS" ul
        INNER JOIN "INTEGRACION"."V_INSTRUCTORXFICHA_B" ixf ON ul."USR_NIS" = ixf."NIS_FUN_INSTRUCTOR"
        INNER JOIN "INTEGRACION"."V_FICHA_CARACTERIZACION_B" fic ON ixf."FIC_ID" = fic."FIC_ID"
        INNER JOIN "INTEGRACION"."V_PROGRAMA_FORMACION_B" prf ON fic."PRF_ID" = prf."PRF_ID"
        WHERE ul."LMS_ID" IS NULL
          AND ul."LMS_ESTADO" = 1
          AND prf."PRF_TIPO_PROGRAMA" = 'C'
          AND fic."FIC_MOD_FORMACION" IN ('V', 'A')
          AND ul.created_at BETWEEN %s AND %s
    """
    
def insert_execution_report():
    return """
    INSERT INTO "LOG"."EXECUTION_REPORT"
    ("FICHAS_C","APRENDICES_CREADOS", "INSTRUCTORES_CREADOS", "START_EXECUTION", "END_EXECUTION")
    VALUES(%s, %s, %s, %s, %s);
    """
    
    
##------ Migrate from Temporal -------------------

def query_person_temporal():
    return """
    SELECT "NIS", "TIPO_DOCUMENTO", "NUM_DOC_IDENTIDAD", "PER_NOMBRE", "PER_PRIMER_APELLIDO", "PER_SEGUNDO_APELLIDO", "LMS_ID", "LMS_ESTADO", "PER_CORREO_E", "DBU_FCH_NACIMIENTO"
    FROM "TEMPORAL"."V_PERSONA_B" WHERE "NIS" = %s
    """
    
def query_usuario_lms_enroll_c_temporal():
    return """
    SELECT "FIC_ID", courseid, roleid, userid, "LMS_ESTADO", "NIS", created_at, updated_at, enroll_state, "RGA_ESTADO"
    FROM "TEMPORAL"."USUARIO_LMS_ENROLL_C" WHERe "FIC_ID" = %s AND "NIS" = %s 
    """
    
def insert_usuario_lms_enroll_c():
    return """
    INSERT INTO "INTEGRACION"."USUARIO_LMS_ENROLL_C"
    ("FIC_ID", courseid, roleid, userid, "LMS_ESTADO", "NIS", created_at, updated_at, enroll_state, "RGA_ESTADO")
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
def query_usuario_lms_temporal():
    return """
    SELECT "USR_NIS", "INF_ID", "RGA_ID", "USR_NOMBRE", "USR_APELLIDO", "USR_CORREO", "FIC_ID", "USR_TIPO", "LMS_ID", "LMS_ESTADO", "USR_TIPO_DOC", "USR_NUM_DOC", created_at, updated_at, "OPERATION"
    FROM "TEMPORAL"."USUARIO_LMS" WHERE "USR_NIS" = %s
    """
    

def query_registro_academico_post_temp():
    return """
    SELECT 
    "RGA_ID", "RGA_PERIODO", "NIS", "TIPO_DOCUMENTO", "NUM_DOC_IDENTIDAD", "ING_ID", "FIC_ID", "PRF_ID", "RTA_ID", "RGA_ETAPA_RUTA", "RGA_ESTADO", "RGA_FCH_REGISTRO", "RGA_FCH_ULTIMO_ESTADO", "NIS_EMP", "RGA_FCH_PASO_A_PRO", "RGA_FCH_FIN_FORMACION"
    FROM "TEMPORAL"."V_REGISTRO_ACADEMICO_B" WHERE "RGA_ID" = %s
    """

def insert_persona_from_temporal():
    return """
    INSERT INTO  "INTEGRACION"."V_PERSONA_B" ("NIS", "TIPO_DOCUMENTO", "NUM_DOC_IDENTIDAD", "PER_NOMBRE", "PER_PRIMER_APELLIDO", "PER_SEGUNDO_APELLIDO", "LMS_ID", "LMS_ESTADO", "PER_CORREO_E", "DBU_FCH_NACIMIENTO")VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    
def insert_usuario_lms_from_temporal():
    return """
    INSERT INTO "INTEGRACION"."USUARIO_LMS" ("USR_NIS", "INF_ID", "RGA_ID", "USR_NOMBRE", "USR_APELLIDO", "USR_CORREO", "FIC_ID", "USR_TIPO", "LMS_ID", "LMS_ESTADO", "USR_TIPO_DOC", "USR_NUM_DOC", created_at, updated_at, "OPERATION") VALUES(%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    
    