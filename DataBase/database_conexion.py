import mysql.connector
from datetime import datetime

class Conectar():
    def __init__(self):
        # Conexion para MySql
        self.conexionsql = mysql.connector.connect(host='localhost',
                                        user='root',
                                        password='',
                                        database='seacorp',
                                        port='3306')
        
    def db_seleccionaPuertoArduino(self):
        cursor = self.conexionsql.cursor()
        cursor.execute("SELECT puertoIndicador, puertoArduino FROM tb_puertos")
        resultados = cursor.fetchall()
        return resultados
    
    def db_traerPesosMaximosYTaras(self):
        try:
            cursor = self.conexionsql.cursor()
            sql = "SELECT pesoLimite, tara FROM tb_especies"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            return None