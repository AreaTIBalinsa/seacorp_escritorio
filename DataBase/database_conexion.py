import mysql.connector

hostLocal="localhost"
userLocal="root"
passwordLocal=""
databaseLocal="seacorp"
portLocal="3306"

hostServidor="199.168.*.*"
userServidor="seacorp_admin"
passwordServidor="Seacorp2024#."
databaseServidor="seacorp"

class Conectar():
    def __init__(self):
        # Conexion para MySql
        self.conexionsql = mysql.connector.connect(host = hostLocal,
                                        user = userLocal,
                                        password = passwordLocal,
                                        database = databaseLocal,
                                        port = portLocal)
        
    def db_seleccionaPuertoArduino(self):
        try:
            cursor = self.conexionsql.cursor()
            cursor.execute("SELECT puertoIndicador, puertoArduino FROM tb_puertos")
            resultados = cursor.fetchall()
            return resultados
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            return None
        
    def db_extraerPassword(self):
        try:
            cursor = self.conexionsql.cursor()
            sql = "SELECT passOperador FROM tb_configuracion"
            cursor.execute(sql)
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            return None
    
    def db_extraerUtilizaCamara(self):
        try:
            cursor = self.conexionsql.cursor()
            sql = "SELECT utilizaCamara FROM tb_configuracion"
            cursor.execute(sql)
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
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
        
    def db_buscaServis(self, codigo):
        try:
            cursor = self.conexionsql.cursor()
            sql = "SELECT nombreGrupo, idGrupo FROM tb_grupos WHERE idGrupo = %s"
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
                    idPesada,
                    IFNULL(CONCAT(CONCAT_WS(' ', nombresEmpleado, apellidoPaternoEmple, apellidoMaternoEmple), ' - ', p.codigoUsuario), '') AS nombreCompleto,
                    especie,
                    pesoNeto,
                    acumulados.acumuladoTalloSolo,
                    acumulados.acumuladoTalloCoral,
                    acumulados.acumuladoMediaValvaTalloSolo,
                    acumulados.acumuladoMediaValvaTalloCoral,
                    acumulados.acumuladoOtros,
                    p.horaPeso,
                    p.idPesada
                FROM
                    tb_pesadas p
                    INNER JOIN tb_empleados ON p.codigoUsuario = tb_empleados.codigo
                    LEFT JOIN (
                        SELECT 
                            codigoUsuario,
                            SUM(CASE WHEN especie = "TALLO SOLO" THEN pesoNeto ELSE 0 END) AS acumuladoTalloSolo,
                            SUM(CASE WHEN especie = "TALLO CORAL" THEN pesoNeto ELSE 0 END) AS acumuladoTalloCoral,
                            SUM(CASE WHEN especie = "MEDIA VALVA T/S" THEN pesoNeto ELSE 0 END) AS acumuladoMediaValvaTalloSolo,
                            SUM(CASE WHEN especie = "MEDIA VALVA T/C" THEN pesoNeto ELSE 0 END) AS acumuladoMediaValvaTalloCoral,
                            SUM(CASE WHEN especie = "OTROS" THEN pesoNeto ELSE 0 END) AS acumuladoOtros
                        FROM tb_pesadas
                        WHERE 
                            fech_InicioProc = %s 
                            AND idProceso = %s 
                            AND estadoPesada = 1
                        GROUP BY codigoUsuario
                    ) acumulados ON acumulados.codigoUsuario = p.codigoUsuario
                WHERE
                    p.fech_InicioProc = %s 
                    AND p.idProceso = %s 
                    AND p.idLote = %s 
                    AND p.estadoPesada = 1
                ORDER BY 
                    p.idPesada DESC
            """
            cursor.execute(sql, (fechaInicioProceso, numeroProceso, fechaInicioProceso, numeroProceso, numeroLote))
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            return None
    
    def db_listarPesosTablaEnProceso(self, fechaInicioProceso, numeroProceso, numeroLote):
        try:
            cursor = self.conexionsql.cursor()
            sql = """
                SELECT
                    idPesada,
                    IFNULL(CONCAT(CONCAT_WS(' ', nombresEmpleado, apellidoPaternoEmple, apellidoMaternoEmple), ' - ', p.codigoUsuario), '') AS nombreCompleto,
                    especie,
                    pesoNeto,
                    acumulados.acumuladoTalloSolo,
                    acumulados.acumuladoTalloCoral,
                    acumulados.acumuladoMediaValvaTalloSolo,
                    acumulados.acumuladoMediaValvaTalloCoral,
                    acumulados.acumuladoOtros,
                    p.horaPeso,
                    p.idPesada
                FROM
                    tb_pesadas p
                    INNER JOIN tb_empleados ON p.codigoUsuario = tb_empleados.codigo
                    LEFT JOIN (
                        SELECT 
                            codigoUsuario,
                            SUM(CASE WHEN especie = "TALLO SOLO" THEN pesoNeto ELSE 0 END) AS acumuladoTalloSolo,
                            SUM(CASE WHEN especie = "TALLO CORAL" THEN pesoNeto ELSE 0 END) AS acumuladoTalloCoral,
                            SUM(CASE WHEN especie = "MEDIA VALVA T/S" THEN pesoNeto ELSE 0 END) AS acumuladoMediaValvaTalloSolo,
                            SUM(CASE WHEN especie = "MEDIA VALVA T/C" THEN pesoNeto ELSE 0 END) AS acumuladoMediaValvaTalloCoral,
                            SUM(CASE WHEN especie = "OTROS" THEN pesoNeto ELSE 0 END) AS acumuladoOtros
                        FROM tb_pesadas
                        WHERE 
                            fech_InicioProc = %s 
                            AND idProceso = %s 
                            AND estadoPesada = 1
                        GROUP BY codigoUsuario
                    ) acumulados ON acumulados.codigoUsuario = p.codigoUsuario
                WHERE
                    p.fech_InicioProc = %s 
                    AND p.idProceso = %s 
                    AND p.idLote = %s 
                    AND p.estadoPesada = 1
                ORDER BY 
                    p.idPesada DESC
                LIMIT 1
            """
            cursor.execute(sql, (fechaInicioProceso, numeroProceso, fechaInicioProceso, numeroProceso, numeroLote))
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
            
    def db_aplicarDescuentoPersonal(self, numeroProceso, numeroLote, fechaInicioProceso, horaDescuento, presentacionDescuento, txtIngresarPesoDescuento, codigoColaboradorDescuento):
        try:
            cursor = self.conexionsql.cursor()
            sql = "INSERT INTO tb_descuentos (idProceso , idLote, fecha, hora, especie, pesoDescuento, codigoUsuario) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,(numeroProceso, numeroLote, fechaInicioProceso, horaDescuento, presentacionDescuento, txtIngresarPesoDescuento, codigoColaboradorDescuento))
            self.conexionsql.commit()
            cursor.close()
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            self.conexionsql.rollback()
            
    def db_actualizar_datos_local_colaboradores(self):
        try:
            conexionRemota = mysql.connector.connect(
                host = hostServidor,
                user = userServidor,
                password = passwordServidor,
                database = databaseServidor
            )

            remoto_cursor = conexionRemota.cursor()

            query = "SELECT * FROM tb_empleados"
            remoto_cursor.execute(query)
            remote_data = remoto_cursor.fetchall()

            for data in remote_data:
                try:
                    cursor = self.conexionsql.cursor()
                    query = """INSERT INTO tb_empleados 
                                        (idEmpleado, apellidoPaternoEmple, apellidoMaternoEmple, nombresEmpleado, tipoDocumento, numDocEmple, celularEmple, direccionEmple, estado, fecha_registro, hora_registro, user_registro, codigo, grupo, horaPeso, controlBloq) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        ON DUPLICATE KEY UPDATE
                                        apellidoPaternoEmple = VALUES(apellidoPaternoEmple),
                                        apellidoMaternoEmple = VALUES(apellidoMaternoEmple),
                                        nombresEmpleado = VALUES(nombresEmpleado),
                                        tipoDocumento = VALUES(tipoDocumento),
                                        numDocEmple = VALUES(numDocEmple),
                                        celularEmple = VALUES(celularEmple),
                                        direccionEmple = VALUES(direccionEmple),
                                        estado = VALUES(estado),
                                        fecha_registro = VALUES(fecha_registro),
                                        hora_registro = VALUES(hora_registro),
                                        user_registro = VALUES(user_registro),
                                        codigo = VALUES(codigo),
                                        grupo = VALUES(grupo),
                                        horaPeso = VALUES(horaPeso),
                                        controlBloq = VALUES(controlBloq)
                                        """
                    cursor.execute(query, data)
                    self.conexionsql.commit()
                except mysql.connector.Error as e:
                    print("Error al ejecutar consulta local:", e)
                finally:
                    cursor.close()

        except mysql.connector.Error as error:
            print("Error al conectar a la base de datos remota:", error)
        finally:
            if 'conexionRemota' in locals() and conexionRemota.is_connected():
                conexionRemota.close()
                print("Conexión remota cerrada")
                
    def db_enviar_datos_servidor_procesos(self):
        try:
            local_cursor = self.conexionsql.cursor()

            query = "SELECT * FROM tb_procesos"
            local_cursor.execute(query)
            local_data = local_cursor.fetchall()

            if local_data:
                conexionRemota = mysql.connector.connect(
                    host = hostServidor,
                    user = userServidor,
                    password = passwordServidor,
                    database = databaseServidor
                )

                remoto_cursor = conexionRemota.cursor()

                for data in local_data:
                    try:
                        query = """INSERT INTO tb_procesos 
                                            (idProceso, fechaInicio, horainicio, fechaFin, horaFin, acumulado, finProceso) 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                                            ON DUPLICATE KEY UPDATE
                                            fechaInicio = VALUES(fechaInicio),
                                            horainicio = VALUES(horainicio),
                                            fechaFin = VALUES(fechaFin),
                                            horaFin = VALUES(horaFin),
                                            acumulado = VALUES(acumulado),
                                            finProceso = VALUES(finProceso)
                                            """
                        remoto_cursor.execute(query, data)
                        conexionRemota.commit()
                    except mysql.connector.Error as e:
                        print("Error al ejecutar consulta remota:", e)
                    finally:
                        remoto_cursor.close()

        except mysql.connector.Error as error:
            print("Error al conectar a la base de datos local:", error)
        finally:
            if 'conexionRemota' in locals() and conexionRemota.is_connected():
                conexionRemota.close()
                print("Conexión remota cerrada")
            if 'local_cursor' in locals() and local_cursor:
                local_cursor.close()
                print("Cursor local cerrado")
    
    def db_enviar_datos_servidor_lotes(self):
        try:
            conexionLocal = mysql.connector.connect(
                host = hostLocal,
                user = userLocal,
                password = passwordLocal,
                database = databaseLocal,
                port = portLocal
            )
            
            local_cursor = conexionLocal.cursor()

            query = "SELECT * FROM tb_lotes"
            local_cursor.execute(query)
            local_data = local_cursor.fetchall()

            if local_data:
                conexionRemota = mysql.connector.connect(
                    host = hostServidor,
                    user = userServidor,
                    password = passwordServidor,
                    database = databaseServidor
                )

                remoto_cursor = conexionRemota.cursor()

                for data in local_data:
                    try:
                        query = """INSERT INTO tb_lotes 
                                            (idLote, numeroLote, idProceso, horaInicio, horaFin, acumulado, finLote) 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                                            ON DUPLICATE KEY UPDATE
                                            numeroLote = VALUES(numeroLote),
                                            idProceso = VALUES(idProceso),
                                            horaInicio = VALUES(horaInicio),
                                            horaFin = VALUES(horaFin),
                                            acumulado = VALUES(acumulado),
                                            finLote = VALUES(finLote)
                                            """
                        remoto_cursor.execute(query, data)
                        conexionRemota.commit()
                    except mysql.connector.Error as e:
                        print("Error al ejecutar consulta remota:", e)
                    finally:
                        remoto_cursor.close()

        except mysql.connector.Error as error:
            print("Error al conectar a la base de datos local:", error)
        finally:
            if 'conexionRemota' in locals() and conexionRemota.is_connected():
                conexionRemota.close()
                print("Conexión remota cerrada")
            if 'local_cursor' in locals() and local_cursor:
                local_cursor.close()
                print("Cursor local cerrado")

    
    def db_actualizar_datos_servidor_procesos(self):
        try:
            conexionLocal = mysql.connector.connect(
                host = hostLocal,
                user = userLocal,
                password = passwordLocal,
                database = databaseLocal,
                port = portLocal
            )
            
            local_cursor = conexionLocal.cursor()

            query = "SELECT * FROM tb_procesos"
            local_cursor.execute(query)
            local_data = local_cursor.fetchall()

            if local_data:
                conexionRemota = mysql.connector.connect(
                    host = hostServidor,
                    user = userServidor,
                    password = passwordServidor,
                    database = databaseServidor
                )

                remoto_cursor = conexionRemota.cursor()

                for data in local_data:
                    try:
                        query = """INSERT INTO tb_procesos 
                                            (idProceso, fechaInicio, horainicio, fechaFin, horaFin, acumulado, finProceso) 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                                            ON DUPLICATE KEY UPDATE
                                            fechaInicio = VALUES(fechaInicio),
                                            horainicio = VALUES(horainicio),
                                            fechaFin = VALUES(fechaFin),
                                            horaFin = VALUES(horaFin),
                                            acumulado = VALUES(acumulado),
                                            finProceso = VALUES(finProceso)
                                            """
                        remoto_cursor.execute(query, data)
                        conexionRemota.commit()
                    except mysql.connector.Error as e:
                        print("Error al ejecutar consulta remota:", e)
                    finally:
                        remoto_cursor.close()

        except mysql.connector.Error as error:
            print("Error al conectar a la base de datos local:", error)
        finally:
            if 'conexionRemota' in locals() and conexionRemota.is_connected():
                conexionRemota.close()
                print("Conexión remota cerrada")
            if 'local_cursor' in locals() and local_cursor:
                local_cursor.close()
                print("Cursor local cerrado")
    
    def db_actualizar_datos_servidor_pesadas(self):
        try:
            conexionLocal = mysql.connector.connect(
                host = hostLocal,
                user = userLocal,
                password = passwordLocal,
                database = databaseLocal,
                port = portLocal
            )
            
            local_cursor = conexionLocal.cursor()

            query = "SELECT * FROM tb_pesadas"
            local_cursor.execute(query)
            local_data = local_cursor.fetchall()

            if local_data:
                conexionRemota = mysql.connector.connect(
                    host = hostServidor,
                    user = userServidor,
                    password = passwordServidor,
                    database = databaseServidor
                )

                remoto_cursor = conexionRemota.cursor()

                for data in local_data:
                    try:
                        query = """INSERT INTO tb_pesadas 
                                            (idPesada, idProceso, idLote, especie, pesoNeto, tara, horaPeso, fech_InicioProc, codigoUsuario, pesoExcedido, estadoPesada) 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                            ON DUPLICATE KEY UPDATE
                                            idProceso = VALUES(idProceso),
                                            idLote = VALUES(idLote),
                                            especie = VALUES(especie),
                                            pesoNeto = VALUES(pesoNeto),
                                            tara = VALUES(tara),
                                            horaPeso = VALUES(horaPeso),
                                            fech_InicioProc = VALUES(fech_InicioProc),
                                            codigoUsuario = VALUES(codigoUsuario),
                                            pesoExcedido = VALUES(pesoExcedido),
                                            estadoPesada = VALUES(estadoPesada)
                                            """
                        remoto_cursor.execute(query, data)
                        conexionRemota.commit()
                    except mysql.connector.Error as e:
                        print("Error al ejecutar consulta remota:", e)
                    finally:
                        remoto_cursor.close()

        except mysql.connector.Error as error:
            print("Error al conectar a la base de datos local:", error)
        finally:
            if 'conexionRemota' in locals() and conexionRemota.is_connected():
                conexionRemota.close()
                print("Conexión remota cerrada")
            if 'local_cursor' in locals() and local_cursor:
                local_cursor.close()
                print("Cursor local cerrado")
                
    
    def db_actualizar_datos_servidor_descuentos(self):
        try:
            conexionLocal = mysql.connector.connect(
                host = hostLocal,
                user = userLocal,
                password = passwordLocal,
                database = databaseLocal,
                port = portLocal
            )
            
            local_cursor = conexionLocal.cursor()

            query = "SELECT * FROM tb_descuentos"
            local_cursor.execute(query)
            local_data = local_cursor.fetchall()

            if local_data:
                conexionRemota = mysql.connector.connect(
                    host = hostServidor,
                    user = userServidor,
                    password = passwordServidor,
                    database = databaseServidor
                )

                remoto_cursor = conexionRemota.cursor()

                for data in local_data:
                    try:
                        query = """INSERT INTO tb_descuentos 
                                            (idDescuento, idProceso, idLote, fecha, hora, especie, pesoDescuento, codigoUsuario) 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                            ON DUPLICATE KEY UPDATE
                                            idProceso = VALUES(idProceso),
                                            idLote = VALUES(idLote),
                                            fecha = VALUES(fecha),
                                            hora = VALUES(hora),
                                            especie = VALUES(especie),
                                            pesoDescuento = VALUES(pesoDescuento),
                                            codigoUsuario = VALUES(codigoUsuario)
                                            """
                        remoto_cursor.execute(query, data)
                        conexionRemota.commit()
                    except mysql.connector.Error as e:
                        print("Error al ejecutar consulta remota:", e)
                    finally:
                        remoto_cursor.close()

        except mysql.connector.Error as error:
            print("Error al conectar a la base de datos local:", error)
        finally:
            if 'conexionRemota' in locals() and conexionRemota.is_connected():
                conexionRemota.close()
                print("Conexión remota cerrada")
            if 'local_cursor' in locals() and local_cursor:
                local_cursor.close()
                print("Cursor local cerrado")
                
    def db_traerClientesServis(self, codigoColaboradorDescuentoServis):
        try:
            cursor = self.conexionsql.cursor()
            sql = "SELECT IFNULL(CONCAT_WS(' ', nombresEmpleado, apellidoPaternoEmple, apellidoMaternoEmple), '') AS nombre_completo, codigo FROM tb_empleados WHERE grupo = %s"
            cursor.execute(sql, (codigoColaboradorDescuentoServis,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print("Error al ejecutar la consulta SQL:", e)
            return None
