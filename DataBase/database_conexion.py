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
        try:
            cursor = self.conexionsql.cursor()
            cursor.execute("SELECT puertoIndicador, puertoArduino FROM tb_puertos")
            resultados = cursor.fetchall()
            return resultados
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            return None
    
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
    
    def db_buscaCliente(self, codigo):
        try:
            cursor = self.conexionsql.cursor()
            sql = "SELECT IFNULL(CONCAT_WS(' ', nombresEmpleado, apellidoPaternoEmple, apellidoMaternoEmple), '') AS nombre_completo, codigo FROM tb_empleados WHERE codigo = %s"
            cursor.execute(sql, (codigo,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            return None
        
    def db_verificarProceso(self):
        try:
            cursor = self.conexionsql.cursor()
            cursor.execute("SELECT idProceso, fechaInicio, horainicio, finProceso FROM tb_procesos ORDER BY idProceso DESC LIMIT 1")
            resultado = cursor.fetchall()
            return resultado[0] if resultado else None
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            return None
    
    def db_verificarLote(self, numeroProceso):
        try:
            cursor = self.conexionsql.cursor()
            sql = "SELECT numeroLote, finLote, horaInicio FROM tb_lotes WHERE idProceso = %s ORDER BY numeroLote DESC LIMIT 1"
            cursor.execute(sql, (numeroProceso,))
            resultado = cursor.fetchall()
            return resultado[0] if resultado else None
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            return None
        
    def db_crearNuevoProceso(self, numeroProceso,fechaInicioProceso, horaInicioProceso):
        try:
            cursor = self.conexionsql.cursor()
            sql = "INSERT INTO tb_procesos (idProceso ,fechaInicio, horainicio, acumulado, finProceso) VALUES (%s, %s, %s, 0, 0)"
            cursor.execute(sql,(numeroProceso,fechaInicioProceso, horaInicioProceso))
            self.conexionsql.commit()
            cursor.close()
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            self.conexionsql.rollback()
            
    def db_crearNuevoLote(self, numeroLote, numeroProceso, horaInicioLote):
        try:
            cursor = self.conexionsql.cursor()
            sql = "INSERT INTO tb_lotes (numeroLote ,idProceso, horaInicio, acumulado, finLote) VALUES (%s, %s, %s, 0, 0)"
            cursor.execute(sql,(numeroLote, numeroProceso, horaInicioLote))
            self.conexionsql.commit()
            cursor.close()
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            self.conexionsql.rollback()
            
    def db_traerAcumuladoProceso(self, numeroProceso):
        try:
            cursor = self.conexionsql.cursor()
            sql = "SELECT SUM(pesoNeto) FROM tb_pesadas WHERE idProceso = %s AND estadoPesada = 1"
            cursor.execute(sql, (numeroProceso,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            return None
    
    def db_traerAcumuladoLote(self, numeroProceso, numeroLote):
        try:
            cursor = self.conexionsql.cursor()
            sql = "SELECT SUM(pesoNeto) FROM tb_pesadas WHERE idProceso = %s AND idLote = %s AND estadoPesada = 1"
            cursor.execute(sql, (numeroProceso,numeroLote))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            return None
        
    def db_guardarPesada(self, numeroProceso, numeroLote, presentacion, pesoIndicador, pesoTara, horaPeso, fechaInicioProceso, codigoColaborador, pesoExcedido):
        try:
            cursor = self.conexionsql.cursor()
            sql = "INSERT INTO tb_pesadas (idProceso ,idLote, especie, pesoNeto, tara, horaPeso, fech_InicioProc, codigoUsuario, pesoExcedido) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,(numeroProceso, numeroLote, presentacion, pesoIndicador, pesoTara, horaPeso, fechaInicioProceso, codigoColaborador, pesoExcedido))
            self.conexionsql.commit()
            cursor.close()
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            self.conexionsql.rollback()
            
    def db_finalizarLote(self, numeroLote, numeroProceso, horaFinLote, acumuladoLote):
        try:
            cursor = self.conexionsql.cursor()
            sql = "UPDATE tb_lotes SET horaFin = %s, acumulado = %s, finLote = 1 WHERE numeroLote = %s AND idProceso = %s"
            cursor.execute(sql, (horaFinLote, acumuladoLote, numeroLote, numeroProceso))
            self.conexionsql.commit()
            cursor.close()
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            self.conexionsql.rollback()
    
    def db_finalizarProceso(self, numeroProceso, fechaFinProceso, horaFinProceso, acumuladoProceso):
        try:
            cursor = self.conexionsql.cursor()
            sql = "UPDATE tb_procesos SET fechaFin = %s, horaFin = %s, acumulado = %s, finProceso = 1 WHERE idProceso = %s"
            cursor.execute(sql, (fechaFinProceso, horaFinProceso, acumuladoProceso, numeroProceso))
            self.conexionsql.commit()
            cursor.close()
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            self.conexionsql.rollback()
            
    def db_listarPesosTabla(self, fechaInicioProceso, numeroProceso, numeroLote):
        try:
            cursor = self.conexionsql.cursor()
            sql = """
                SELECT
                    ROW_NUMBER() OVER (ORDER BY p.idPesada DESC) AS num,
                    IFNULL(CONCAT_WS(' ', nombresEmpleado, apellidoPaternoEmple, apellidoMaternoEmple), '') AS nombreCompleto,
                    especie,
                    pesoNeto,
                    IFNULL((SELECT SUM(pesoNeto) FROM tb_pesadas WHERE especie = "TALLO SOLO" AND fech_InicioProc = %s AND idProceso = %s AND idLote = %s AND p.estadoPesada = 1 AND idPesada <= p.idPesada AND codigoUsuario = p.codigoUsuario), 0) AS acumuladoTalloSolo, 
                    IFNULL((SELECT SUM(pesoNeto) FROM tb_pesadas WHERE especie = "TALLO CORAL" AND fech_InicioProc = %s AND idProceso = %s AND idLote = %s AND p.estadoPesada = 1 AND idPesada <= p.idPesada AND codigoUsuario = p.codigoUsuario), 0) AS acumuladoTalloCoral,
                    IFNULL((SELECT SUM(pesoNeto) FROM tb_pesadas WHERE especie = "MEDIA VALVA T/S" AND fech_InicioProc = %s AND idProceso = %s AND idLote = %s AND p.estadoPesada = 1 AND idPesada <= p.idPesada AND codigoUsuario = p.codigoUsuario), 0) AS acumuladoMediaValvaTalloSolo, 
                    IFNULL((SELECT SUM(pesoNeto) FROM tb_pesadas WHERE especie = "MEDIA VALVA T/C" AND fech_InicioProc = %s AND idProceso = %s AND idLote = %s AND p.estadoPesada = 1 AND idPesada <= p.idPesada AND codigoUsuario = p.codigoUsuario), 0) AS acumuladoMediaValvaTalloCoral, 
                    IFNULL((SELECT SUM(pesoNeto) FROM tb_pesadas WHERE especie = "OTROS" AND fech_InicioProc = %s AND idProceso = %s AND idLote = %s AND p.estadoPesada = 1 AND idPesada <= p.idPesada AND codigoUsuario = p.codigoUsuario), 0) AS acumuladoOtros, 
                    p.horaPeso, 
                    idPesada
                FROM
                    tb_pesadas p
                    INNER JOIN tb_empleados ON p.codigoUsuario = tb_empleados.codigo
                WHERE
                    p.fech_InicioProc = %s AND p.idProceso = %s AND p.idLote = %s AND p.estadoPesada = 1
                ORDER BY
                    p.idPesada DESC
            """
            cursor.execute(sql, (fechaInicioProceso, numeroProceso, numeroLote,
                                fechaInicioProceso, numeroProceso, numeroLote,
                                fechaInicioProceso, numeroProceso, numeroLote,
                                fechaInicioProceso, numeroProceso, numeroLote,
                                fechaInicioProceso, numeroProceso, numeroLote,
                                fechaInicioProceso, numeroProceso, numeroLote))
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            return None
        
    def db_actualizaTaraPresentacion(self, presentacionEditarTara, nuevoValorTara):
        try:
            cursor = self.conexionsql.cursor()
            sql = "UPDATE tb_especies SET tara = %s WHERE idEspecie = %s"
            cursor.execute(sql, (nuevoValorTara, presentacionEditarTara))
            self.conexionsql.commit()
            cursor.close()
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            self.conexionsql.rollback()
            
    def db_eliminarRegistro(self, idPesadaEditarOEliminar):
        try:
            cursor = self.conexionsql.cursor()
            sql = "UPDATE tb_pesadas SET estadoPesada = 0 WHERE idPesada = %s"
            cursor.execute(sql, (idPesadaEditarOEliminar,))
            self.conexionsql.commit()
            cursor.close()
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            self.conexionsql.rollback()
    
    def db_actualizarCodigoColaboradorPesada(self, idPesadaEditarOEliminar, codigoColaboradorNuevo):
        try:
            cursor = self.conexionsql.cursor()
            sql = "UPDATE tb_pesadas SET codigoUsuario = %s WHERE idPesada = %s"
            cursor.execute(sql, (codigoColaboradorNuevo,idPesadaEditarOEliminar))
            self.conexionsql.commit()
            cursor.close()
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            self.conexionsql.rollback()
    
    def db_actualizarEspeciePesada(self, idPesadaEditarOEliminar, codigoNuevaEspecie):
        try:
            cursor = self.conexionsql.cursor()
            sql = "UPDATE tb_pesadas SET especie = %s WHERE idPesada = %s"
            cursor.execute(sql, (codigoNuevaEspecie, idPesadaEditarOEliminar))
            self.conexionsql.commit()
            cursor.close()
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            self.conexionsql.rollback()