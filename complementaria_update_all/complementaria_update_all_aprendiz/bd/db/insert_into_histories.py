import psycopg2


class InsertIntoHistories:
    def __init__(self, pg_connection):
        self.pg_connection = pg_connection

    def insert(self, data):
        print(data)
        try:
            cursor = self.pg_connection.connection.cursor()
            query = """INSERT INTO "LOG"."HISTORIES" ("USER_ID","EVENT","PREVIOUS_STATE","NEW_STATE") VALUES (1,%s,%s,%s)"""
            cursor.execute(query, data)
            self.pg_connection.connection.commit()
            cursor.close()
            # print("Datos insertados en la tabla 'histories' correctamente")
        except psycopg2.Error as e:
            self.pg_connection.connection.rollback()
            print("Error al insertar datos en la tabla 'histories':", e)
