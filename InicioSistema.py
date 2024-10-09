from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow
import serial
import time
import socket
from datetime import datetime, timedelta, date
import cv2
from pyzbar.pyzbar import decode
import threading

from View.Ui_Principal import Ui_MainWindow
import ModalInicio
import pulsosArduino

# Importación de Base de Datos
import DataBase.database_conexion # El archivo database_conexion.py

# Puertos COM
COMARDUINO = ""
COMINDICADOR = ""

listoParaAccionar = False
utilizaCamara = ""

captaCodigo = False
captaCodigoQr = False

seleccionarTalloSolo = False
seleccionarTalloCoral = False
seleccionarMediaValvaTs = False
seleccionarMediaValvaTc = False
seleccionarOtros = False

# Variables Base de Datos
pesoMaximo = 0
pesoTara = 0
pesoExcedido = 0
presentacion = ""
fechaInicioProceso = ""
horaInicioProceso = ""
horaInicioLote = ""
numeroProceso = 0
numeroLote = 0
acumuladoProceso = 0
acumuladoLote = 0

pesoMaximoTalloSolo = 0
pesoMaximoTalloCoral = 0
pesoMaximoMediaValvaTalloSolo = 0
pesoMaximoMediaValvaTalloCoral = 0
pesoMaximoOtros = 0

pesoTaraTalloSolo = 0
pesoTaraTalloCoral = 0
pesoTaraMediaValvaTalloSolo = 0
pesoTaraMediaValvaTalloCoral = 0
pesoTaraOtros = 0

frmEditarTaraAlerta = False
frmEditarOEliminarPesadaAlerta = False
frmDescuentoAlerta = False
frmFinalizarAlerta = False

frmIngresarNuevaTara = False
frmSeleccionarEditarPesada = False
frmIngresarPassword = False
frmAlertaEliminar = False
frmAlertaEditarCodigoUsuario = False
frmEditarPresentacion = False
frmAlertaDescuentoCodigoUsuario = False
frmAlertaDescuentoSeleccionaEspecie = False
frmAlertaDescuentoIngresaPeso = False
frmAlertaDescuentoCodigoUsuarioServis = False
frmAlertaDescuentoSeleccionaEspecieServis = False
frmAlertaDescuentoIngresaPesoServis = False

frmIngresarPasswordAdministradorTara = False
frmIngresarPasswordAdministradorEditarPesada = False
frmIngresarPasswordAdministradorDescuento = False

presentacionEditarTara = 0
idPesadaEditarOEliminar = 0
codigoColaboradorNuevo = 0
codigoColaboradorDescuento = 0
codigoColaboradorDescuentoServis = 0

presentacionDescuento = ""
presentacionDescuentoServis = ""

passwordEliminar = ""
numeroDePesada = 0

# Variables de rutas de imagenes para alerta
correcto = "Resources/correcto.png"
error = "Resources/error.png"
loading = "Resources/loading.gif"

""" Creamos hilo para la ejecución en segundo plano del Indicador , de esta forma
evitamos que la aplicación se detenga por la lectura constante """

class WorkerThread(QThread):
    update_peso = pyqtSignal(str)
    update_estado = pyqtSignal(str)
    update_baliza = pyqtSignal(str)
    
    def run(self):
        COMINDICADOR1 = "COM" + COMINDICADOR
        serialIndicador = None

        while True:
            try:
                if serialIndicador is None or not serialIndicador.is_open:
                    serialIndicador = serial.Serial(COMINDICADOR1, baudrate=9600, timeout=1, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
                
                result = serialIndicador.readline().decode('utf-8').strip()
                if not result:
                    self.update_peso.emit("+0.00")
                    self.update_baliza.emit("+0.00")
                    self.update_estado.emit("0")
                else:
                    # self.update_peso.emit(result[6:14]) # Tscale
                    # self.update_baliza.emit(result[6:14]) # Tscale 
                
                    # self.update_peso.emit(result[6:13]) # Weight
                    # self.update_baliza.emit(result[6:13]) # Weight

                    self.update_peso.emit(result[2:10]) # Yaohua 
                    self.update_baliza.emit(result[2:10]) # Yaohua 
                    self.update_estado.emit("1")
            except Exception as e:
                time.sleep(1)
                if serialIndicador is not None and serialIndicador.is_open:
                    serialIndicador.close()
    
    def stop(self):
        print("Thread Stopped")
        self.terminate()
        
""" Creamos hilo para la ejecución en segundo plano para subir los datos al servidor """

class WorkerThreadSubirDatosBase(QThread):
    def run(self):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            try:
                s.connect(("www.google.com", 80))
            except (socket.gaierror, socket.timeout):
                print("Sin conexión a internet")
            else:
                print("Con conexión a internet")
                try:
                    self.conexion = DataBase.database_conexion.Conectar()
                    self.conexion.db_actualizar_datos_servidor_procesos()
                    self.conexion.db_actualizar_datos_servidor_lotes()
                    self.conexion.db_actualizar_datos_servidor_pesadas()
                    self.conexion.db_actualizar_datos_servidor_descuentos()
                except Exception as e:
                    print(f"Error al interactuar con la base de datos: {e}")
                    print('ERROR')
                else:
                    s.close()
            time.sleep(300)

""" Creamos hilo para la ejecución en segundo plano del Arduino, de esta forma
evitamos que la aplicación se detenga por la lectura constante  """
            
class WorkerThreadAR(QThread):
    def __init__(self):
        super().__init__()
        self.serialArduino = None
        self.user_input_arduino = ""
        self.contador = 3

    def run(self):
        try:
            COMARDUINODUINO = "COM" + COMARDUINO
            # Configura los parámetros del puerto serie
            self.serialArduino = serial.Serial()
            self.serialArduino.baudrate = 9600
            self.serialArduino.bytesize = serial.EIGHTBITS
            self.serialArduino.parity = serial.PARITY_NONE
            self.serialArduino.stopbits = serial.STOPBITS_ONE 

            # Reemplaza 'COMX' por el nombre del puerto en tu sistema (p. ej., 'COM3' en Windows, '/dev/ttyUSB0' en Linux)
            self.serialArduino.port = COMARDUINODUINO
            
            while self.contador > 1 and not self.serialArduino.is_open:
                if self.serialArduino is None or not self.serialArduino.is_open:
                    self.serialArduino.open()
                    
                self.contador = self.contador - 1
            
            if self.serialArduino.is_open:
                print("Conectado al puerto Arduino en", self.serialArduino.port)
                time.sleep(2)
                self.serialArduino.write(str("x").encode('utf8'))
            else:
                print("No se pudo abrir el puerto Arduino.")
        except serial.SerialException as e:
            time.sleep(1)
        except Exception as e:
            print("Other Exception: " + str(e))

    def stop(self):
        print("Thread Stopped")
        if self.serialArduino:
            self.serialArduino.close()
        self.terminate()
        
def fn_declararPuertos():
    global COMARDUINO
    global COMINDICADOR
            
    puertos = DataBase.database_conexion.Conectar().db_seleccionaPuertoArduino()
    puertos = puertos[0]
    COMINDICADOR = str(puertos[0])
    COMARDUINO = str(puertos[1])
        
fn_declararPuertos()
        
workerAR = WorkerThreadAR()  # Instancia de WorkerThreadAR
workerAR.start()  # Inicia el hilo

""" Creamos hilo para la ejecución en segundo plano de la Fecha y Hora, de esta forma
evitamos que la aplicación se detenga por la lectura constante """

class WorkerThreadFechaHora(QThread):
    update_fecha = pyqtSignal(str)
    update_hora = pyqtSignal(str)
    def run(self):
        try:
            while True:
                hora_actual = datetime.now().time()
                hora = int(hora_actual.strftime("%H"))
                minutos = hora_actual.strftime("%M")
                segundos = hora_actual.strftime("%S")
                periodo = "AM" if hora < 12 else "PM"
                hora = hora if hora <= 12 else hora - 12
                hora_formateada = "{:02d} : {:02d} : {:02d} {}".format(hora, int(minutos), int(segundos), periodo)
                self.update_hora.emit(hora_formateada)

                fecha_actual = datetime.now().date()
                año = fecha_actual.year
                mes = fecha_actual.month
                dia = fecha_actual.day
                dia_semana = fecha_actual.weekday()
                dia_semana = ["Lunes", 
                            "Martes", 
                            "Miércoles", 
                            "Jueves", 
                            "Viernes", 
                            "Sábado", 
                            "Domingo"][int(dia_semana)]
                meses = {
                    1: "Enero",
                    2: "Febrero",
                    3: "Marzo",
                    4: "Abril",
                    5: "Mayo",
                    6: "Junio",
                    7: "Julio",
                    8: "Agosto",
                    9: "Septiembre",
                    10: "Octubre",
                    11: "Noviembre",
                    12: "Diciembre"
                }
                fecha_formateada = "{} {} de {} del {}".format(dia_semana, dia, meses[mes], año)

                self.update_fecha.emit(fecha_formateada)
                time.sleep(1)
        except Exception as e:
            print("WT FH"+str(e))  
    
    def stop(self):
        print("Thread Stopped")
        self.terminate()

# ===============================
# Creación de la Clase Principal
# ===============================

class AplicacionPrincipal(QMainWindow):
    _instance = None
    primeraVez = True

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AplicacionPrincipal, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self.primeraVez:
            super().__init__()

        if not hasattr(self, 'ui'):
            self.ui = Ui_MainWindow()
            self.conexion = DataBase.database_conexion.Conectar()
            self.modal_Inicio = ModalInicio.ModalPrincipal()
            self.ui.setupUi(self)

            self.initialized = True
            self.primeraVez = False

            self.pulsosArduino = pulsosArduino
            
            self.fn_asignaUtilizaCamara()
            
            if utilizaCamara.upper() == "SI":
                self.cap = cv2.VideoCapture(0)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 270)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)

                self.timer = QTimer()
                self.timer.timeout.connect(self.update_frame)
                self.timer.start(100)
            else:
                self.cap = None
            
            self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.setWindowIcon(QtGui.QIcon("Resources/icon.jpg"))
            self.setWindowTitle('SISTEMA INTEGRAL || BALINSA')
            
            self.ui.imgPlataformaBalanza.setPixmap(QPixmap("Resources/plataforma_balanza.png"))
            self.ui.imgPanera.setPixmap(QPixmap("Resources/panera.png"))
            self.ui.imgFlechaDerecha.setPixmap(QPixmap("Resources/flecha.png"))
            self.ui.imgFlechaIzquierda.setPixmap(QPixmap("Resources/flecha.png"))
            self.ui.imgFinalizar.setPixmap(QPixmap("Resources/error.png"))
            
            self.workerFechaHora = WorkerThreadFechaHora()
            self.workerFechaHora.start() # Iniciamos el hilo
            self.workerFechaHora.update_fecha.connect(self.mostrar_fecha)
            self.workerFechaHora.update_hora.connect(self.mostrar_hora)
            
            self.worker = WorkerThread() # Hilo de Balanza
            self.worker.start()
            self.worker.update_peso.connect(self.fn_actualizar_peso)
            self.worker.update_estado.connect(self.fn_actualizar_estado)
            
            self.fn_asignaPesosMaximosYTaras()
            self.fn_asignarPassword()
            
            self.ui.txtCodigoColaborador.textChanged.connect(self.fn_recepcionaCodigoColaborador)
            self.ui.txtIngresarNuevoCodigoColaborador.textChanged.connect(self.fn_recepcionaCodigoColaboradorNuevo)
            self.ui.txtIngresarCodigoColaboradorDescuento.textChanged.connect(self.fn_recepcionaCodigoColaboradorDescuento)
            self.ui.txtIngresarCodigoServisDescuento.textChanged.connect(self.fn_recepcionaCodigoServisDescuento)
            self.ui.txtIngresarNuevaTara.textChanged.connect(self.fn_validarEntradaNumerica)
            self.ui.txtIngresarPesoDescuento.textChanged.connect(self.fn_validarEntradaNumericaDecimal)
            self.ui.txtIngresarPesoDescuentoServis.textChanged.connect(self.fn_validarEntradaNumericaDecimal)
            self.ui.txtNumeroDePesada.textChanged.connect(self.fn_validarEntradaNumerica)
            
            self.ui.imgPanera.setHidden(True)
            self.ui.txtCodigoColaborador.setEnabled(False)
            self.ui.txtCodigoColaborador.setFocus(False)
            self.ui.txtCodigoColaborador.setText("")
            self.ui.lblPesoIndicador.setText("-----")
            self.ui.lblIndicadorPlataforma.setText("-----")
            
            self.ui.frmEditarTaraAlerta.setHidden(True)
            self.ui.frmFinalizarAlerta.setHidden(True)
            self.ui.frmIngresarNuevaTara.setHidden(True)
            self.ui.frmEditarOEliminarPesadaAlerta.setHidden(True)
            self.ui.frmSeleccionarEditarPesada.setHidden(True)
            self.ui.frmIngresarPassword.setHidden(True)
            self.ui.frmAlertaEliminar.setHidden(True)
            self.ui.frmIngresarPasswordAdministrador.setHidden(True)
            self.ui.frmAlertaEditarCodigoUsuario.setHidden(True)
            self.ui.frmEditarPresentacion.setHidden(True)
            self.ui.frmAlertaDescuentoCodigoUsuario.setHidden(True)
            self.ui.frmAlertaDescuentoServis.setHidden(True)
            self.ui.frmDescuentoAlerta.setHidden(True)
            self.ui.frmSombra.setHidden(True)
            self.ui.frmAlerta.setHidden(True)
            
            self.tablaDePesos = self.ui.tblDetallePesadas
            self.tablaDePesos.setColumnWidth(0, 100)
            self.tablaDePesos.setColumnWidth(1, 250)
            self.tablaDePesos.setColumnWidth(2, 180)
            self.tablaDePesos.setColumnWidth(3, 100)
            self.tablaDePesos.setColumnWidth(4, 100)
            self.tablaDePesos.setColumnWidth(5, 100)
            self.tablaDePesos.setColumnWidth(6, 100)
            self.tablaDePesos.setColumnWidth(7, 100)
            self.tablaDePesos.setColumnWidth(8, 100)
            self.tablaDePesos.setColumnWidth(9, 80)
            self.tablaDePesos.setColumnHidden(10, True)
            
            # self.conexion.db_actualizar_datos_local_colaboradores()
            # self.workerBase = WorkerThreadSubirDatosBase()
            # self.workerBase.start()
        
    def update_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                qr_codes = decode(frame)

                for qr_code in qr_codes:
                    qr_data = qr_code.data.decode('utf-8')
                    
                    if(captaCodigo and captaCodigoQr):
                        self.ui.txtCodigoColaborador.setText(qr_data)
                        self.ui.txtCodigoColaborador.setFocus(True)
                        
                        try:
                            pesoIndicador = float(self.ui.lblPesoIndicador.text())
                            if presentacion != "":
                                if pesoIndicador > 0:
                                    if codigoColaborador != 0:
                                        self.fn_guardarPesada()
                                    else:
                                        self.fn_alerta("¡ERROR AL REGISTRAR!",error,"Debe seleccionar un colaborador.",1000)
                                else:
                                    self.fn_alerta("¡ERROR AL REGISTRAR!",error,"El peso no puede ser 0.",1000)
                            else:
                                self.fn_alerta("¡ERROR AL REGISTRAR!",error,"Debe seleccionar una presentación.",1000)
                        except ValueError:
                            print("El valor del peso no es válido")
                    else:
                        self.ui.txtCodigoColaborador.setText("")
                    
                    (x, y, w, h) = qr_code.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                q_image = q_image.scaled(self.ui.videoCamaraQr.width(), self.ui.videoCamaraQr.height())

                self.ui.videoCamaraQr.setPixmap(QtGui.QPixmap.fromImage(q_image))
        
    def mostrar_hora(self,val):
        self.ui.lblHora.setText(val)
        
    def mostrar_fecha(self,val):
        self.ui.lblFecha.setText(val)
        
    def fn_validarEntradaNumerica(self):
        sender = self.sender()

        if sender is not None and isinstance(sender, QLineEdit):
            texto = sender.text()

            texto_valido = ''.join(filter(str.isdigit, texto))

            sender.setText(texto_valido)
            
    def fn_validarEntradaNumericaDecimal(self):
        sender = self.sender()

        if sender is not None and isinstance(sender, QLineEdit):
            texto = sender.text()

            texto_valido = ''.join(c for i, c in enumerate(texto) if c.isdigit() or (c == '.' and texto.count('.') == 1))

            sender.setText(texto_valido)
            
    def fn_asignarPassword(self):
        global passwordEliminar
        
        resultadoPassword = self.conexion.db_extraerPassword()
        passwordEliminar = resultadoPassword
    
    def fn_asignaUtilizaCamara(self):
        global utilizaCamara
        
        resultadoUtilizaCamara = self.conexion.db_extraerUtilizaCamara()
        utilizaCamara = resultadoUtilizaCamara
        
    def fn_modal_principal(self):
        global pesoMaximo
        global pesoTara
        global presentacion
        global codigoColaborador
        global numeroProceso
        global numeroLote
        global fechaInicioProceso
        global horaInicioProceso
        global horaInicioLote
        global acumuladoProceso
        global acumuladoLote
        global seleccionarTalloSolo
        global seleccionarTalloCoral
        global seleccionarMediaValvaTs
        global seleccionarMediaValvaTc
        global seleccionarOtros
        
        self.fn_seleccionarEspecie(0)
        pesoMaximo = 0
        pesoTara = 0
        presentacion = ""
        codigoColaborador = 0
        numeroProceso = 0
        numeroLote = 0
        fechaInicioProceso = ""
        horaInicioProceso = ""
        horaInicioLote = ""
        acumuladoProceso = 0
        acumuladoLote = 0
        
        seleccionarTalloSolo = False
        seleccionarTalloCoral = False
        seleccionarMediaValvaTs = False
        seleccionarMediaValvaTc = False
        seleccionarOtros = False
        
        if not self.modal_Inicio:
            self.modal_Inicio = ModalInicio.ModalPrincipal()
        elif not self.modal_Inicio.isVisible():
            self.modal_Inicio.show()
        else:
            self.modal_Inicio.showNormal()
            self.modal_Inicio.activateWindow()
            
        self.modal_Inicio.ui.lblTalloSolo.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 40;")
        self.modal_Inicio.ui.lblTalloCoral.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 55;")
        self.modal_Inicio.ui.lblMediaValvaTs.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
        self.modal_Inicio.ui.lblMediaValvaTc.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
        self.modal_Inicio.ui.lblOtros.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 30;")
        
        self.close()
        
    def fn_actualizar_peso(self, val):
        global captaCodigo
        global captaCodigoQr
        global pesoExcedido
        
        try:
            pesoIndicador = val
            signo = pesoIndicador[0:1]
            pesoIndicador = float(pesoIndicador[1:])
            
            if (signo == "-") and pesoIndicador != 0:
                pesoIndicador = pesoIndicador + pesoTara
                self.ui.lblPesoIndicador.setText("-"+str(format(pesoIndicador, ".3f")))
                self.ui.lblIndicadorPlataforma.setText("-"+str(format(pesoIndicador, ".3f")))
                
                self.ui.imgPanera.setHidden(True)
                self.ui.imgFlechaDerecha.setHidden(False)
                self.ui.imgFlechaIzquierda.setHidden(False)
                self.ui.lblColoquePeso.setHidden(False)
                
                self.ui.txtCodigoColaborador.setEnabled(False)
                self.ui.txtCodigoColaborador.setFocus(False)
                self.ui.txtCodigoColaborador.setText("")
                    
                captaCodigo = False
                captaCodigoQr = False
                pesoExcedido = 0
            else:
                pesoIndicador = pesoIndicador - pesoTara
                
                if(pesoIndicador > 0):
                    if(captaCodigo == False and self.condiciones_base() and self.condiciones_alertas()):
                        self.ui.imgPanera.setHidden(False)
                        self.ui.imgFlechaDerecha.setHidden(True)
                        self.ui.imgFlechaIzquierda.setHidden(True)
                        self.ui.lblColoquePeso.setHidden(True)
                        
                        self.ui.txtCodigoColaborador.setEnabled(True)
                        self.ui.txtCodigoColaborador.setFocus(True)
                        captaCodigo = True
                        captaCodigoQr = True
                    
                    if pesoIndicador >= pesoMaximo and pesoMaximo != 0:
                        self.ui.lblPesoIndicador.setText(str(format(pesoMaximo, ".3f")))
                        self.ui.lblIndicadorPlataforma.setText(str(format(pesoMaximo, ".3f")))
                        pesoExcedido = pesoIndicador - pesoMaximo
                    else:
                        self.ui.lblPesoIndicador.setText(format(pesoIndicador, ".3f"))
                        self.ui.lblIndicadorPlataforma.setText(format(pesoIndicador, ".3f"))
                else:
                    self.ui.imgPanera.setHidden(True)
                    self.ui.imgFlechaDerecha.setHidden(False)
                    self.ui.imgFlechaIzquierda.setHidden(False)
                    self.ui.lblColoquePeso.setHidden(False)
                    
                    self.ui.txtCodigoColaborador.setEnabled(False)
                    self.ui.txtCodigoColaborador.setFocus(False)
                    self.ui.txtCodigoColaborador.setText("")
                    
                    captaCodigo = False
                    captaCodigoQr = False
                    pesoExcedido = 0
                    
                    self.ui.lblPesoIndicador.setText(format(pesoIndicador, ".3f"))
                    self.ui.lblIndicadorPlataforma.setText(format(pesoIndicador, ".3f"))
        except ValueError:
            self.ui.lblPesoIndicador.setText("-----")
            self.ui.lblIndicadorPlataforma.setText("-----")
                
    def fn_actualizar_estado(self, val):
        if (val == "0"):
            self.ui.lblPesoIndicador.setText("-----")
            self.ui.lblIndicadorPlataforma.setText("-----")
            self.ui.lblEstadoIndicador.setStyleSheet("background-color: rgb(255, 0, 0); border-radius: 10px;")
        elif (val == "1"):
            self.ui.lblEstadoIndicador.setStyleSheet("background-color: rgb(20, 180, 60); border-radius: 10px;")
            
    def fn_alerta(self,titulo,imagen,mensaje,tiempo = 500, pesado = False):
        if imagen == correcto:
            self.ui.lblAlertaTitulo.setStyleSheet("color: #24D315")
            self.ui.lblAlertaTexto.setStyleSheet("font-size:16pt;")
        elif imagen == error:
            self.ui.lblAlertaTitulo.setStyleSheet("color: #EA1D31")
            self.ui.lblAlertaTexto.setStyleSheet("font-size:16pt;")
        self.ui.frmAlerta.setHidden(False)
        self.ui.frmSombra.setHidden(False)
        self.ui.lblAlertaTitulo.setText(titulo)
        self.ui.imgIconAlerta.setPixmap(QPixmap(imagen))
        self.ui.lblAlertaTexto.setText(mensaje)
        if pesado:
            nombreColaborador = self.ui.txtNombreDelColaborador.text()
            self.ui.lblNombreColaborador.setText(nombreColaborador)
            self.ui.lblAlertaTexto.setGeometry(QtCore.QRect(50, 300, 600, 50))
        else:
            self.ui.lblNombreColaborador.setText("")
            self.ui.lblAlertaTexto.setGeometry(QtCore.QRect(50, 300, 600, 100))

        timer = QtCore.QTimer()
        timer.singleShot(tiempo, lambda: self.ui.frmAlerta.setHidden(True))
        
        if self.condiciones_alertas_sombra():
            timer2 = QtCore.QTimer()
            timer2.singleShot(tiempo, lambda: self.ui.frmSombra.setHidden(True))

    # ======================== Eventos con el Teclado ========================
    
    def condiciones_base(self):
        return (
            not frmEditarTaraAlerta and
            not frmEditarOEliminarPesadaAlerta and
            not frmDescuentoAlerta and
            not frmFinalizarAlerta and
            not frmIngresarNuevaTara and
            not frmSeleccionarEditarPesada and
            not frmIngresarPassword and
            not frmIngresarPasswordAdministradorTara and
            not frmIngresarPasswordAdministradorEditarPesada and
            not frmIngresarPasswordAdministradorDescuento and
            not frmAlertaEditarCodigoUsuario and
            not frmEditarPresentacion and
            not frmAlertaDescuentoCodigoUsuario and
            not frmAlertaDescuentoSeleccionaEspecie and
            not frmAlertaDescuentoIngresaPeso and
            not frmAlertaDescuentoCodigoUsuarioServis and
            not frmAlertaDescuentoSeleccionaEspecieServis and
            not frmAlertaDescuentoIngresaPesoServis and
            not frmAlertaEliminar
        )
        
    def condiciones_alertas(self):
        return (
            not self.ui.frmEditarTaraAlerta.isVisible() and
            not self.ui.frmFinalizarAlerta.isVisible() and
            not self.ui.frmIngresarNuevaTara.isVisible() and
            not self.ui.frmSeleccionarEditarPesada.isVisible() and
            not self.ui.frmEditarOEliminarPesadaAlerta.isVisible() and
            not self.ui.frmIngresarPassword.isVisible() and
            not self.ui.frmIngresarPasswordAdministrador.isVisible() and
            not self.ui.frmAlertaEliminar.isVisible() and
            not self.ui.frmAlertaEditarCodigoUsuario.isVisible() and
            not self.ui.frmEditarPresentacion.isVisible() and
            not self.ui.frmDescuentoAlerta.isVisible() and
            not self.ui.frmAlertaDescuentoCodigoUsuario.isVisible() and
            not self.ui.frmAlertaDescuentoServis.isVisible() and
            not self.ui.frmSombra.isVisible() and
            not self.ui.frmAlerta.isVisible()
        )
        
    def condiciones_alertas_sombra(self):
        return (
            not self.ui.frmEditarTaraAlerta.isVisible() and
            not self.ui.frmFinalizarAlerta.isVisible() and
            not self.ui.frmIngresarNuevaTara.isVisible() and
            not self.ui.frmSeleccionarEditarPesada.isVisible() and
            not self.ui.frmEditarOEliminarPesadaAlerta.isVisible() and
            not self.ui.frmIngresarPassword.isVisible() and
            not self.ui.frmIngresarPasswordAdministrador.isVisible() and
            not self.ui.frmAlertaEditarCodigoUsuario.isVisible() and
            not self.ui.frmEditarPresentacion.isVisible() and
            not self.ui.frmDescuentoAlerta.isVisible() and
            not self.ui.frmAlertaDescuentoCodigoUsuario.isVisible() and
            not self.ui.frmAlertaDescuentoServis.isVisible() and
            not self.ui.frmAlertaEliminar.isVisible()
        )
         
    def keyReleaseEvent(self, event):
        
        global frmEditarTaraAlerta
        global frmEditarOEliminarPesadaAlerta
        global frmDescuentoAlerta
        global frmFinalizarAlerta
        
        global frmIngresarNuevaTara
        global frmSeleccionarEditarPesada
        global frmIngresarPassword
        global frmAlertaEliminar
        global frmAlertaEditarCodigoUsuario
        global frmEditarPresentacion
        global frmAlertaDescuentoCodigoUsuario
        global frmAlertaDescuentoSeleccionaEspecie
        global frmAlertaDescuentoIngresaPeso
        global frmAlertaDescuentoCodigoUsuarioServis
        global frmAlertaDescuentoSeleccionaEspecieServis
        global frmAlertaDescuentoIngresaPesoServis
        
        global frmIngresarPasswordAdministradorTara
        global frmIngresarPasswordAdministradorEditarPesada
        global frmIngresarPasswordAdministradorDescuento
        
        global presentacionEditarTara
        global idPesadaEditarOEliminar
        global codigoColaboradorNuevo
        global codigoColaboradorDescuento
        global presentacionDescuento
        global codigoColaboradorDescuentoServis
        global presentacionDescuentoServis
        
        if (event.key() == Qt.Key_1) and self.ui.frmFinalizarAlerta.isVisible() and frmFinalizarAlerta:
            if acumuladoLote != 0:
                self.fn_finalizarLote()
                self.ui.frmSombra.setHidden(True)
                self.ui.frmFinalizarAlerta.setHidden(True)
                frmFinalizarAlerta = False
                self.fn_alerta("¡LOTE FINALIZADO!",correcto,"Se ha finalizado el lote correctamente.",2000)
            else:
                self.fn_alerta("¡ERROR AL FINALIZAR LOTE!",error,"No se ha acumulado ningún peso en el lote.",2000)
        
        if (event.key() == Qt.Key_2) and self.ui.frmFinalizarAlerta.isVisible() and frmFinalizarAlerta:
            self.fn_finalizarProceso()
            self.ui.frmSombra.setHidden(True)
            self.ui.frmFinalizarAlerta.setHidden(True)
            frmFinalizarAlerta = False
            
        if (event.key() == Qt.Key_3) and self.ui.frmFinalizarAlerta.isVisible() and frmFinalizarAlerta:
            self.ui.frmSombra.setHidden(True)
            self.ui.frmFinalizarAlerta.setHidden(True)
            frmFinalizarAlerta = False
            
        if (event.key() == Qt.Key_1) and self.ui.frmEditarTaraAlerta.isVisible() and frmEditarTaraAlerta:
            self.fn_seleccionaTara(1)
        
        if (event.key() == Qt.Key_2) and self.ui.frmEditarTaraAlerta.isVisible() and frmEditarTaraAlerta:
            self.fn_seleccionaTara(2)
        
        if (event.key() == Qt.Key_3) and self.ui.frmEditarTaraAlerta.isVisible() and frmEditarTaraAlerta:
            self.fn_seleccionaTara(3)
        
        if (event.key() == Qt.Key_4) and self.ui.frmEditarTaraAlerta.isVisible() and frmEditarTaraAlerta:
            self.fn_seleccionaTara(4)
        
        if (event.key() == Qt.Key_5) and self.ui.frmEditarTaraAlerta.isVisible() and frmEditarTaraAlerta:
            self.fn_seleccionaTara(5)
            
        if (event.key() == Qt.Key_1) and self.ui.frmEditarPresentacion.isVisible() and frmEditarPresentacion:
            codigoEspecie = "TALLO SOLO"
            self.fn_actualizaEspeciePesada(codigoEspecie)
        
        if (event.key() == Qt.Key_2) and self.ui.frmEditarPresentacion.isVisible() and frmEditarPresentacion:
            codigoEspecie = "TALLO CORAL"
            self.fn_actualizaEspeciePesada(codigoEspecie)
        
        if (event.key() == Qt.Key_3) and self.ui.frmEditarPresentacion.isVisible() and frmEditarPresentacion:
            codigoEspecie = "MEDIA VALVA T/S"
            self.fn_actualizaEspeciePesada(codigoEspecie)
        
        if (event.key() == Qt.Key_4) and self.ui.frmEditarPresentacion.isVisible() and frmEditarPresentacion:
            codigoEspecie = "MEDIA VALVA T/C"
            self.fn_actualizaEspeciePesada(codigoEspecie)
        
        if (event.key() == Qt.Key_5) and self.ui.frmEditarPresentacion.isVisible() and frmEditarPresentacion:
            codigoEspecie = "OTROS"
            self.fn_actualizaEspeciePesada(codigoEspecie)
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmIngresarNuevaTara.isVisible() and frmIngresarNuevaTara:
            nuevoValorTara = self.ui.txtIngresarNuevaTara.text()
            if nuevoValorTara != "" and nuevoValorTara != 0:
                nuevoValorTara = int(nuevoValorTara)/1000
                self.conexion.db_actualizaTaraPresentacion(presentacionEditarTara, nuevoValorTara)
                self.fn_asignaPesosMaximosYTaras()
                self.ui.frmSombra.setHidden(True)
                self.ui.frmIngresarNuevaTara.setHidden(True)
                frmIngresarNuevaTara = False
                self.fn_alerta("ACTUALIZACIÓN CORRECTA!",correcto,"El registro se ha actualizado correctamente.")
            else:
                self.fn_alerta("¡ERROR AL ACTUALIZAR!",error,"Debe ingresar un valor numérico para la tara.",1000)
                
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmIngresarPassword.isVisible() and frmIngresarPassword:
            passwordExtraido = self.ui.txtPasswordEliminar.text()
            if str(passwordEliminar) == str(passwordExtraido):
                self.conexion.db_eliminarRegistro(idPesadaEditarOEliminar)
                frmIngresarPassword = False
                self.ui.frmSombra.setHidden(True)
                self.ui.frmIngresarPassword.setHidden(True)
                self.fn_listarPesadas()
            else:
                self.fn_alerta("¡CONTRASEÑA INCORRECTA!",error,"La contraseña no coincide con la contraseña declara para eliminar.")
                
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmAlertaEliminar.isVisible() and frmAlertaEliminar:
            frmAlertaEliminar = False
            self.ui.frmAlertaEliminar.setHidden(True)
            frmIngresarPassword = True
            self.ui.frmIngresarPassword.setHidden(False)
            self.ui.txtPasswordEliminar.setFocus(False)
            self.ui.txtPasswordEliminar.setText("")
        
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmAlertaEditarCodigoUsuario.isVisible() and frmAlertaEditarCodigoUsuario:
            if codigoColaboradorNuevo != 0:
                self.conexion.db_actualizarCodigoColaboradorPesada(idPesadaEditarOEliminar, codigoColaboradorNuevo)
                frmAlertaEditarCodigoUsuario = False
                self.ui.frmSombra.setHidden(True)
                self.ui.frmAlertaEditarCodigoUsuario.setHidden(True)
                self.fn_alerta("ACTUALIZACIÓN CORRECTA!",correcto,"El registro se ha actualizado correctamente.")
                nombreColaborador = self.ui.lblNuevoCodigoColaborador.text()
                nuevo_valor_columna_1 = nombreColaborador + " - " + str(codigoColaboradorNuevo)
                self.fn_actualizaColaboradorEnProceso(idPesadaEditarOEliminar, nuevo_valor_columna_1)
                # self.fn_listarPesadas()
            else:
                self.fn_alerta("¡ERROR AL REGISTRAR!",error,"Debe seleccionar un colaborador.",1000)
                
        if (event.key() == Qt.Key_1) and self.ui.frmEditarOEliminarPesadaAlerta.isVisible() and frmEditarOEliminarPesadaAlerta:
            frmEditarOEliminarPesadaAlerta = False
            self.ui.frmEditarOEliminarPesadaAlerta.setHidden(True)
            frmAlertaEditarCodigoUsuario = True
            self.ui.frmAlertaEditarCodigoUsuario.setHidden(False)
            self.ui.txtIngresarNuevoCodigoColaborador.setFocus(False)
            self.ui.txtIngresarNuevoCodigoColaborador.setText("")
            codigoColaboradorNuevo = 0
        
        if (event.key() == Qt.Key_2) and self.ui.frmEditarOEliminarPesadaAlerta.isVisible() and frmEditarOEliminarPesadaAlerta:
            frmEditarOEliminarPesadaAlerta = False
            self.ui.frmEditarOEliminarPesadaAlerta.setHidden(True)
            frmEditarPresentacion = True
            self.ui.frmEditarPresentacion.setHidden(False)
        
        if (event.key() == Qt.Key_3) and self.ui.frmEditarOEliminarPesadaAlerta.isVisible() and frmEditarOEliminarPesadaAlerta:
            frmEditarOEliminarPesadaAlerta = False
            self.ui.frmEditarOEliminarPesadaAlerta.setHidden(True)
            frmAlertaEliminar = True
            self.ui.frmAlertaEliminar.setHidden(False)
            
        if (event.key() == Qt.Key_1) and self.ui.frmAlertaDescuentoCodigoUsuario.isVisible() and frmAlertaDescuentoSeleccionaEspecie:
            self.fn_seleccionarEspecieDescuento(1)
        
        if (event.key() == Qt.Key_2) and self.ui.frmAlertaDescuentoCodigoUsuario.isVisible() and frmAlertaDescuentoSeleccionaEspecie:
            self.fn_seleccionarEspecieDescuento(2)
        
        if (event.key() == Qt.Key_3) and self.ui.frmAlertaDescuentoCodigoUsuario.isVisible() and frmAlertaDescuentoSeleccionaEspecie:
            self.fn_seleccionarEspecieDescuento(3)
        
        if (event.key() == Qt.Key_4) and self.ui.frmAlertaDescuentoCodigoUsuario.isVisible() and frmAlertaDescuentoSeleccionaEspecie:
            self.fn_seleccionarEspecieDescuento(4)
        
        if (event.key() == Qt.Key_5) and self.ui.frmAlertaDescuentoCodigoUsuario.isVisible() and frmAlertaDescuentoSeleccionaEspecie:
            self.fn_seleccionarEspecieDescuento(5)
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmAlertaDescuentoCodigoUsuario.isVisible() and frmAlertaDescuentoIngresaPeso:
            txtIngresarPesoDescuento = self.ui.txtIngresarPesoDescuento.text()
            if txtIngresarPesoDescuento != "":
                txtIngresarPesoDescuento = float(txtIngresarPesoDescuento)
                if txtIngresarPesoDescuento != 0:
                    frmAlertaDescuentoIngresaPeso = False
                    self.ui.frmAlertaDescuentoCodigoUsuario.setHidden(True)
                    self.fn_registrarDescuento()
                else:
                    self.fn_alerta("¡ERROR AL DESCONTAR!",error,"El valor no puede ser 0.",1000)
            else:
                self.fn_alerta("¡ERROR AL DESCONTAR!",error,"Debe ingresar un valor.",1000)
        
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmAlertaDescuentoCodigoUsuario.isVisible() and frmAlertaDescuentoSeleccionaEspecie:
            if presentacionDescuento != "":
                frmAlertaDescuentoSeleccionaEspecie = False
                frmAlertaDescuentoIngresaPeso = True
                self.ui.txtIngresarPesoDescuento.setEnabled(True)
                self.ui.txtIngresarPesoDescuento.setFocus(True)
                self.ui.txtIngresarPesoDescuento.setText("")
            else:
                self.fn_alerta("¡ERROR DE SELECCION!",error,"Debe seleccionar una presentación.",1000)
        
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmAlertaDescuentoCodigoUsuario.isVisible() and frmAlertaDescuentoCodigoUsuario:
            if codigoColaboradorDescuento != 0:
                frmAlertaDescuentoCodigoUsuario = False
                frmAlertaDescuentoSeleccionaEspecie = True
                self.ui.txtIngresarCodigoColaboradorDescuento.setFocus(False)
                self.ui.txtIngresarCodigoColaboradorDescuento.setEnabled(False)
            else:
                self.fn_alerta("¡ERROR DE SELECCION!",error,"Debe seleccionar un colaborador.",1000)
            
        if (event.key() == Qt.Key_1) and self.ui.frmDescuentoAlerta.isVisible() and frmDescuentoAlerta and not frmAlertaDescuentoCodigoUsuario:
            frmDescuentoAlerta = False
            self.ui.frmDescuentoAlerta.setHidden(True)
            frmAlertaDescuentoCodigoUsuario = True
            self.ui.frmAlertaDescuentoCodigoUsuario.setHidden(False)
            
            self.ui.txtIngresarPesoDescuento.setFocus(False)
            self.ui.txtIngresarPesoDescuento.setEnabled(False)
            
            self.ui.txtIngresarCodigoColaboradorDescuento.setEnabled(True)
            self.ui.txtIngresarCodigoColaboradorDescuento.setFocus(True)
            self.ui.txtIngresarCodigoColaboradorDescuento.setText("")
            
            codigoColaboradorDescuento = 0
            presentacionDescuento = ""
            
        if (event.key() == Qt.Key_1) and self.ui.frmAlertaDescuentoServis.isVisible() and frmAlertaDescuentoSeleccionaEspecieServis:
            self.fn_seleccionarEspecieDescuentoServis(1)
        
        if (event.key() == Qt.Key_2) and self.ui.frmAlertaDescuentoServis.isVisible() and frmAlertaDescuentoSeleccionaEspecieServis:
            self.fn_seleccionarEspecieDescuentoServis(2)
        
        if (event.key() == Qt.Key_3) and self.ui.frmAlertaDescuentoServis.isVisible() and frmAlertaDescuentoSeleccionaEspecieServis:
            self.fn_seleccionarEspecieDescuentoServis(3)
        
        if (event.key() == Qt.Key_4) and self.ui.frmAlertaDescuentoServis.isVisible() and frmAlertaDescuentoSeleccionaEspecieServis:
            self.fn_seleccionarEspecieDescuentoServis(4)
        
        if (event.key() == Qt.Key_5) and self.ui.frmAlertaDescuentoServis.isVisible() and frmAlertaDescuentoSeleccionaEspecieServis:
            self.fn_seleccionarEspecieDescuentoServis(5)
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmAlertaDescuentoServis.isVisible() and frmAlertaDescuentoIngresaPesoServis:
            txtIngresarPesoDescuentoServis = self.ui.txtIngresarPesoDescuentoServis.text()
            if txtIngresarPesoDescuentoServis != "":
                txtIngresarPesoDescuentoServis = float(txtIngresarPesoDescuentoServis)
                if txtIngresarPesoDescuentoServis != 0:
                    frmAlertaDescuentoIngresaPesoServis = False
                    self.ui.frmAlertaDescuentoServis.setHidden(True)
                    self.fn_registrarDescuentoServis()
                else:
                    self.fn_alerta("¡ERROR AL DESCONTAR!",error,"El valor no puede ser 0.",1000)
            else:
                self.fn_alerta("¡ERROR AL DESCONTAR!",error,"Debe ingresar un valor.",1000)
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmAlertaDescuentoServis.isVisible() and frmAlertaDescuentoSeleccionaEspecieServis:
            if presentacionDescuentoServis != "":
                frmAlertaDescuentoSeleccionaEspecieServis = False
                frmAlertaDescuentoIngresaPesoServis = True
                self.ui.txtIngresarPesoDescuentoServis.setEnabled(True)
                self.ui.txtIngresarPesoDescuentoServis.setFocus(True)
                self.ui.txtIngresarPesoDescuentoServis.setText("")
            else:
                self.fn_alerta("¡ERROR DE SELECCION!",error,"Debe seleccionar una presentación.",1000)
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmAlertaDescuentoServis.isVisible() and frmAlertaDescuentoCodigoUsuarioServis:
            if codigoColaboradorDescuentoServis != 0:
                frmAlertaDescuentoCodigoUsuarioServis = False
                frmAlertaDescuentoSeleccionaEspecieServis = True
                self.ui.txtIngresarCodigoServisDescuento.setFocus(False)
                self.ui.txtIngresarCodigoServisDescuento.setEnabled(False)
            else:
                self.fn_alerta("¡ERROR DE SELECCION!",error,"Debe seleccionar un servis.",1000)
        
        if (event.key() == Qt.Key_2) and self.ui.frmDescuentoAlerta.isVisible() and frmDescuentoAlerta:
            frmDescuentoAlerta = False
            self.ui.frmDescuentoAlerta.setHidden(True)
            frmAlertaDescuentoCodigoUsuarioServis = True
            self.ui.frmAlertaDescuentoServis.setHidden(False)
            
            self.ui.txtIngresarPesoDescuentoServis.setFocus(False)
            self.ui.txtIngresarPesoDescuentoServis.setEnabled(False)
            
            self.ui.txtIngresarCodigoServisDescuento.setEnabled(True)
            self.ui.txtIngresarCodigoServisDescuento.setFocus(True)
            self.ui.txtIngresarCodigoServisDescuento.setText("")
            
            codigoColaboradorDescuentoServis = 0
            presentacionDescuentoServis = ""
                
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmSeleccionarEditarPesada.isVisible() and frmSeleccionarEditarPesada:
            numeroDePesada = int(self.ui.txtNumeroDePesada.text())
            tablaDePesos = self.ui.tblDetallePesadas
            totalFilas = tablaDePesos.rowCount()

            if numeroDePesada <= totalFilas:
                txtNumeroDePesada = totalFilas - numeroDePesada
                idPesadaEditarOEliminar = tablaDePesos.item(txtNumeroDePesada, 10).text()
                
                frmSeleccionarEditarPesada = False
                self.ui.frmSeleccionarEditarPesada.setHidden(True)
                frmEditarOEliminarPesadaAlerta = True
                self.ui.frmEditarOEliminarPesadaAlerta.setHidden(False)
            else:
                self.fn_alerta("¡ADVERTENCIA!",error,"El registro no existe, intente de nuevo.",1000)
                
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmIngresarPasswordAdministrador.isVisible() and frmIngresarPasswordAdministradorTara:
            passwordExtraido = self.ui.txtPasswordAdministrador.text()
            if str(passwordEliminar) == str(passwordExtraido):
                frmIngresarPasswordAdministradorTara = False
                self.ui.frmIngresarPasswordAdministrador.setHidden(True)
                self.ui.frmSombra.setHidden(False)
                self.ui.frmEditarTaraAlerta.setHidden(False)
                frmEditarTaraAlerta = True
                presentacionEditarTara = 0
                self.ui.txtIngresarNuevaTara.setText("")
            else:
                self.fn_alerta("¡CONTRASEÑA INCORRECTA!",error,"La contraseña es incorrecta.")
                
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmIngresarPasswordAdministrador.isVisible() and frmIngresarPasswordAdministradorEditarPesada:
            passwordExtraido = self.ui.txtPasswordAdministrador.text()
            if str(passwordEliminar) == str(passwordExtraido):
                frmIngresarPasswordAdministradorEditarPesada = False
                self.ui.frmIngresarPasswordAdministrador.setHidden(True)
                self.ui.frmSombra.setHidden(False)
                self.ui.frmSeleccionarEditarPesada.setHidden(False)
                frmSeleccionarEditarPesada = True
                idPesadaEditarOEliminar = 0
                self.ui.txtNumeroDePesada.setText("")
                self.ui.txtNumeroDePesada.setFocus(True)
            else:
                self.fn_alerta("¡CONTRASEÑA INCORRECTA!",error,"La contraseña es incorrecta.")
        
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.ui.frmIngresarPasswordAdministrador.isVisible() and frmIngresarPasswordAdministradorDescuento:
            passwordExtraido = self.ui.txtPasswordAdministrador.text()
            if str(passwordEliminar) == str(passwordExtraido):
                frmIngresarPasswordAdministradorDescuento = False
                self.ui.frmIngresarPasswordAdministrador.setHidden(True)
                self.ui.frmSombra.setHidden(False)
                self.ui.frmDescuentoAlerta.setHidden(False)
                frmDescuentoAlerta = True
            else:
                self.fn_alerta("¡CONTRASEÑA INCORRECTA!",error,"La contraseña es incorrecta.")
        
        if not self.ui.txtCodigoColaborador.hasFocus() and self.condiciones_base() and self.condiciones_alertas():
            self.tablaDePesos.setCurrentCell(0, 1)
            self.setFocus()
            
            if (event.key() == Qt.Key_1) and self.condiciones_base() and self.condiciones_alertas() and seleccionarTalloSolo:
                self.fn_seleccionarEspecie(1)
                
            if (event.key() == Qt.Key_2) and self.condiciones_base() and self.condiciones_alertas() and seleccionarTalloCoral:
                self.fn_seleccionarEspecie(2)
            
            if (event.key() == Qt.Key_3) and self.condiciones_base() and self.condiciones_alertas() and seleccionarMediaValvaTs:
                self.fn_seleccionarEspecie(3)
            
            if (event.key() == Qt.Key_4) and self.condiciones_base() and self.condiciones_alertas() and seleccionarMediaValvaTc:
                self.fn_seleccionarEspecie(4)
            
            if (event.key() == Qt.Key_5) and self.condiciones_base() and self.condiciones_alertas() and seleccionarOtros:
                self.fn_seleccionarEspecie(5)
            
            # ===== Eventos para Abrir los Frame Principales =====
                
            if (event.key() == Qt.Key_9) and self.condiciones_base() and self.condiciones_alertas():
                self.ui.frmSombra.setHidden(False)
                self.ui.frmFinalizarAlerta.setHidden(False)
                frmFinalizarAlerta = True
            
            if (event.key() == Qt.Key_6) and self.condiciones_base() and self.condiciones_alertas():
                frmIngresarPasswordAdministradorTara = True
                self.ui.frmSombra.setHidden(False)
                self.ui.frmIngresarPasswordAdministrador.setHidden(False)
                self.ui.txtPasswordAdministrador.setText("")
                self.ui.txtPasswordAdministrador.setFocus(True)
                
            if (event.key() == Qt.Key_7) and self.condiciones_base() and self.condiciones_alertas():
                frmIngresarPasswordAdministradorEditarPesada = True
                self.ui.frmSombra.setHidden(False)
                self.ui.frmIngresarPasswordAdministrador.setHidden(False)
                self.ui.txtPasswordAdministrador.setText("")
                self.ui.txtPasswordAdministrador.setFocus(True)
            
            if (event.key() == Qt.Key_8) and self.condiciones_base() and self.condiciones_alertas():
                frmIngresarPasswordAdministradorDescuento = True
                self.ui.frmSombra.setHidden(False)
                self.ui.frmIngresarPasswordAdministrador.setHidden(False)
                self.ui.txtPasswordAdministrador.setText("")
                self.ui.txtPasswordAdministrador.setFocus(True)
            
            # ====================================================
                
        if self.ui.txtCodigoColaborador.hasFocus():
            if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.condiciones_base() and self.condiciones_alertas():
                try:
                    pesoIndicador = float(self.ui.lblPesoIndicador.text())
                    if presentacion != "":
                        if pesoIndicador > 0:
                            if codigoColaborador != 0:
                                self.fn_guardarPesada()
                            else:
                                self.fn_alerta("¡ERROR AL REGISTRAR!",error,"Debe seleccionar un colaborador.",1000)
                        else:
                            self.fn_alerta("¡ERROR AL REGISTRAR!",error,"El peso no puede ser 0.",1000)
                    else:
                        self.fn_alerta("¡ERROR AL REGISTRAR!",error,"Debe seleccionar una presentación.",1000)
                except ValueError:
                    print("El valor del peso no es válido")
                    
        if (event.key() == Qt.Key_Minus):
            self.tablaDePesos.setCurrentCell(0, 1)
            self.setFocus()
            if (self.ui.frmEditarTaraAlerta.isVisible()):
                self.ui.frmSombra.setHidden(True)
                self.ui.frmEditarTaraAlerta.setHidden(True)
                frmEditarTaraAlerta = False
            if (self.ui.frmIngresarNuevaTara.isVisible()):
                self.ui.frmSombra.setHidden(True)
                self.ui.frmIngresarNuevaTara.setHidden(True)
                frmIngresarNuevaTara = False
            if (self.ui.frmSeleccionarEditarPesada.isVisible()):
                self.ui.frmSombra.setHidden(True)
                self.ui.frmSeleccionarEditarPesada.setHidden(True)
                frmSeleccionarEditarPesada = False
            if (self.ui.frmEditarOEliminarPesadaAlerta.isVisible()):
                self.ui.frmSombra.setHidden(True)
                self.ui.frmEditarOEliminarPesadaAlerta.setHidden(True)
                frmEditarOEliminarPesadaAlerta = False
            if (self.ui.frmIngresarPassword.isVisible()):
                self.ui.frmSombra.setHidden(True)
                self.ui.frmIngresarPassword.setHidden(True)
                frmIngresarPassword = False
            if (self.ui.frmAlertaEliminar.isVisible()):
                self.ui.frmSombra.setHidden(True)
                self.ui.frmAlertaEliminar.setHidden(True)
                frmAlertaEliminar = False
            if (self.ui.frmAlertaEditarCodigoUsuario.isVisible()):
                self.ui.frmSombra.setHidden(True)
                self.ui.frmAlertaEditarCodigoUsuario.setHidden(True)
                frmAlertaEditarCodigoUsuario = False
            if (self.ui.frmEditarPresentacion.isVisible()):
                self.ui.frmSombra.setHidden(True)
                self.ui.frmEditarPresentacion.setHidden(True)
                frmEditarPresentacion = False
            if (self.ui.frmDescuentoAlerta.isVisible()):
                self.ui.frmSombra.setHidden(True)
                self.ui.frmDescuentoAlerta.setHidden(True)
                frmDescuentoAlerta = False
            if (self.ui.frmAlertaDescuentoCodigoUsuario.isVisible()):
                self.ui.frmSombra.setHidden(True)
                self.ui.frmAlertaDescuentoCodigoUsuario.setHidden(True)
                frmAlertaDescuentoCodigoUsuario = False
                frmAlertaDescuentoSeleccionaEspecie = False
                frmAlertaDescuentoIngresaPeso = False
            if (self.ui.frmAlertaDescuentoServis.isVisible()):
                self.ui.frmSombra.setHidden(True)
                self.ui.frmAlertaDescuentoServis.setHidden(True)
                frmAlertaDescuentoCodigoUsuarioServis = False
                frmAlertaDescuentoSeleccionaEspecieServis = False
                frmAlertaDescuentoIngresaPesoServis = False
            if (self.ui.frmIngresarPasswordAdministrador.isVisible()):
                self.ui.frmSombra.setHidden(True)
                self.ui.frmIngresarPasswordAdministrador.setHidden(True)
                frmIngresarPasswordAdministradorTara = False
                frmIngresarPasswordAdministradorEditarPesada = False
                frmIngresarPasswordAdministradorDescuento = False
    
    # ======================== Termina eventos con el Teclado ========================
    
    def fn_actualizaColaboradorEnProceso(self, idPesadaEditarOEliminar, nuevo_valor_columna_1):
        row_count = self.tablaDePesos.rowCount()

        for fila in range(row_count):
            item_col_10 = self.tablaDePesos.item(fila, 10)

            if item_col_10 is not None and item_col_10.text() == str(idPesadaEditarOEliminar):
                item_col_1 = QTableWidgetItem(str(nuevo_valor_columna_1))

                item_col_1.setTextAlignment(Qt.AlignCenter)

                self.tablaDePesos.setItem(fila, 1, item_col_1)
                break
    
    def fn_actualizaPresentacionEnProceso(self, idPesadaEditarOEliminar, nuevo_valor_columna_1):
        row_count = self.tablaDePesos.rowCount()

        for fila in range(row_count):
            item_col_10 = self.tablaDePesos.item(fila, 10)

            if item_col_10 is not None and item_col_10.text() == str(idPesadaEditarOEliminar):
                item_col_1 = QTableWidgetItem(str(nuevo_valor_columna_1))

                item_col_1.setTextAlignment(Qt.AlignCenter)

                self.tablaDePesos.setItem(fila, 2, item_col_1)
                break
    
    def fn_recepcionaCodigoColaborador(self):
        global codigoColaborador
        
        sender = self.sender()

        if sender is not None and isinstance(sender, QLineEdit):
            texto = sender.text()

            texto_valido = ''.join(filter(str.isdigit, texto))

            sender.setText(texto_valido)
        
        txtCodigoColaborador = self.ui.txtCodigoColaborador.text()

        if (txtCodigoColaborador != "" and len(txtCodigoColaborador) >= 1):

            nombreClienteSeleccionar = self.conexion.db_buscaCliente(txtCodigoColaborador)

            if (len(nombreClienteSeleccionar) > 0):
                self.ui.txtNombreDelColaborador.setText(str(nombreClienteSeleccionar[0][0]))
                codigoColaborador = nombreClienteSeleccionar[0][1]
            else:
                self.ui.txtNombreDelColaborador.setText("COLABORADOR NO ENCONTRADO")
                codigoColaborador = 0
                
        else:
            self.ui.txtNombreDelColaborador.setText("*****")
            codigoColaborador = 0
            
    def fn_recepcionaCodigoColaboradorNuevo(self):
        global codigoColaboradorNuevo
        
        sender = self.sender()

        if sender is not None and isinstance(sender, QLineEdit):
            texto = sender.text()

            texto_valido = ''.join(filter(str.isdigit, texto))

            sender.setText(texto_valido)
        
        txtIngresarNuevoCodigoColaborador = self.ui.txtIngresarNuevoCodigoColaborador.text()

        if (txtIngresarNuevoCodigoColaborador != "" and len(txtIngresarNuevoCodigoColaborador) >= 1):

            nombreClienteSeleccionar = self.conexion.db_buscaCliente(txtIngresarNuevoCodigoColaborador)

            if (len(nombreClienteSeleccionar) > 0):
                self.ui.lblNuevoCodigoColaborador.setText(str(nombreClienteSeleccionar[0][0]))
                codigoColaboradorNuevo = nombreClienteSeleccionar[0][1]
            else:
                self.ui.lblNuevoCodigoColaborador.setText("COLABORADOR NO ENCONTRADO")
                codigoColaboradorNuevo = 0
                
        else:
            self.ui.lblNuevoCodigoColaborador.setText("*****")
            codigoColaboradorNuevo = 0
    
    def fn_recepcionaCodigoColaboradorDescuento(self):
        global codigoColaboradorDescuento
        
        sender = self.sender()

        if sender is not None and isinstance(sender, QLineEdit):
            texto = sender.text()

            texto_valido = ''.join(filter(str.isdigit, texto))

            sender.setText(texto_valido)
        
        txtIngresarCodigoColaboradorDescuento = self.ui.txtIngresarCodigoColaboradorDescuento.text()

        if (txtIngresarCodigoColaboradorDescuento != "" and len(txtIngresarCodigoColaboradorDescuento) >= 1):

            nombreClienteSeleccionar = self.conexion.db_buscaCliente(txtIngresarCodigoColaboradorDescuento)

            if (len(nombreClienteSeleccionar) > 0):
                self.ui.lblCodigoColaboradorDescuento.setText(str(nombreClienteSeleccionar[0][0]))
                codigoColaboradorDescuento = nombreClienteSeleccionar[0][1]
            else:
                self.ui.lblCodigoColaboradorDescuento.setText("COLABORADOR NO ENCONTRADO")
                codigoColaboradorDescuento = 0
                
        else:
            self.ui.lblCodigoColaboradorDescuento.setText("*****")
            codigoColaboradorDescuento = 0
    
    def fn_recepcionaCodigoServisDescuento(self):
        global codigoColaboradorDescuentoServis
        
        sender = self.sender()

        if sender is not None and isinstance(sender, QLineEdit):
            texto = sender.text()

            texto_valido = ''.join(filter(str.isdigit, texto))

            sender.setText(texto_valido)
        
        txtIngresarCodigoServisDescuento = self.ui.txtIngresarCodigoServisDescuento.text()

        if (txtIngresarCodigoServisDescuento != "" and len(txtIngresarCodigoServisDescuento) >= 1):

            nombreServisSeleccionar = self.conexion.db_buscaServis(txtIngresarCodigoServisDescuento)

            if (len(nombreServisSeleccionar) > 0):
                self.ui.lblCodigoServisDescuento.setText(str(nombreServisSeleccionar[0][0]))
                codigoColaboradorDescuentoServis = nombreServisSeleccionar[0][1]
            else:
                self.ui.lblCodigoServisDescuento.setText("SERVIS NO ENCONTRADO")
                codigoColaboradorDescuentoServis = 0
                
        else:
            self.ui.lblCodigoServisDescuento.setText("*****")
            codigoColaboradorDescuentoServis = 0
    
    def fn_asignaPesosMaximosYTaras(self):
        global pesoMaximoTalloSolo
        global pesoMaximoTalloCoral
        global pesoMaximoMediaValvaTalloSolo
        global pesoMaximoMediaValvaTalloCoral
        global pesoMaximoOtros

        global pesoTaraTalloSolo
        global pesoTaraTalloCoral
        global pesoTaraMediaValvaTalloSolo
        global pesoTaraMediaValvaTalloCoral
        global pesoTaraOtros
        
        try:
            pesosPesosMaximosYTaras = self.conexion.db_traerPesosMaximosYTaras()
            
            pesoMaximoTalloSolo = float(pesosPesosMaximosYTaras[0][0])
            pesoTaraTalloSolo = float(pesosPesosMaximosYTaras[0][1])
            
            pesoMaximoTalloCoral = float(pesosPesosMaximosYTaras[1][0])
            pesoTaraTalloCoral = float(pesosPesosMaximosYTaras[1][1])
            
            pesoMaximoMediaValvaTalloSolo = float(pesosPesosMaximosYTaras[2][0])
            pesoTaraMediaValvaTalloSolo = float(pesosPesosMaximosYTaras[2][1])
            
            pesoMaximoMediaValvaTalloCoral = float(pesosPesosMaximosYTaras[3][0])
            pesoTaraMediaValvaTalloCoral = float(pesosPesosMaximosYTaras[3][1])
            
            pesoMaximoOtros = float(pesosPesosMaximosYTaras[4][0])
            pesoTaraOtros = float(pesosPesosMaximosYTaras[4][1])
            
            self.ui.txtPesoMaximoTalloSolo.setText(f"P. Max: {format(pesoMaximoTalloSolo, '.3f')} Kg")
            self.ui.txtPesoMaximoTalloCoral.setText(f"P. Max: {format(pesoMaximoTalloCoral, '.3f')} Kg")
            self.ui.txtPesoMaximoMediaValvaTalloSolo.setText(f"P. Max: {format(pesoMaximoMediaValvaTalloSolo, '.3f')} Kg")
            self.ui.txtPesoMaximoMediaValvaTalloCoral.setText(f"P. Max: {format(pesoMaximoMediaValvaTalloCoral, '.3f')} Kg")
            self.ui.txtPesoMaximoOtros.setText(f"P. Max: {format(pesoMaximoOtros, '.3f')} Kg")
            
            self.ui.txtTaraTalloSolo.setText(f"Tara: {format(pesoTaraTalloSolo*1000, '.0f')} Gr")
            self.ui.txtTaraTalloCoral.setText(f"Tara: {format(pesoTaraTalloCoral*1000, '.0f')} Gr")
            self.ui.txtTaraMediaValvaTalloSolo.setText(f"Tara: {format(pesoTaraMediaValvaTalloSolo*1000, '.0f')} Gr")
            self.ui.txtTaraMediaValvaTalloCoral.setText(f"Tara: {format(pesoTaraMediaValvaTalloCoral*1000, '.0f')} Gr")
            self.ui.txtTaraOtros.setText(f"Tara: {format(pesoTaraOtros*1000, '.0f')} Gr")
            
            especie = 0
            if (presentacion == "TALLO SOLO"):
                especie = 1
            elif (presentacion == "TALLO CORAL"):
                especie = 2
            elif (presentacion == "MEDIA VALVA T/S"):
                especie = 3
            elif (presentacion == "MEDIA VALVA T/C"):
                especie = 4
            elif (presentacion == "OTROS"):
                especie = 5
                
            self.fn_seleccionarEspecie(especie)
        except Exception as e:
            self.fn_alerta("¡ERROR!",error,"No se pudieron obtener los precios del cliente.", 2000)
    
    def fn_seleccionarEspecie(self, especie):
        global presentacion
        global pesoMaximo
        global pesoTara
        
        self.ui.lblTalloSolo.setStyleSheet("background-color: rgb(255, 255, 255); color: #000")
        self.ui.lblTalloCoral.setStyleSheet("background-color: rgb(255, 255, 255); color: #000")
        self.ui.lblMediaValvaTalloSolo.setStyleSheet("background-color: rgb(255, 255, 255); color: #000")
        self.ui.lblMediaValvaTalloCoral.setStyleSheet("background-color: rgb(255, 255, 255); color: #000")
        self.ui.lblOtros.setStyleSheet("background-color: rgb(255, 255, 255); color: #000")
        
        pesoMaximo = 0
        pesoTara = 0
        presentacion = ""
        
        if(especie == 1):
            pesoMaximo = pesoMaximoTalloSolo
            pesoTara = pesoTaraTalloSolo
            presentacion = "TALLO SOLO"
            self.ui.lblTalloSolo.setStyleSheet("background-color: rgb(255, 207, 11); color: #000")
        elif(especie == 2):
            pesoMaximo = pesoMaximoTalloCoral
            pesoTara = pesoTaraTalloCoral
            presentacion = "TALLO CORAL"
            self.ui.lblTalloCoral.setStyleSheet("background-color: rgb(255, 207, 11); color: #000")
        elif(especie == 3):
            pesoMaximo = pesoMaximoMediaValvaTalloSolo
            pesoTara = pesoTaraMediaValvaTalloSolo
            presentacion = "MEDIA VALVA T/S"
            self.ui.lblMediaValvaTalloSolo.setStyleSheet("background-color: rgb(255, 207, 11); color: #000")
        elif(especie == 4):
            pesoMaximo = pesoMaximoMediaValvaTalloCoral
            pesoTara = pesoTaraMediaValvaTalloCoral
            presentacion = "MEDIA VALVA T/C"
            self.ui.lblMediaValvaTalloCoral.setStyleSheet("background-color: rgb(255, 207, 11); color: #000")
        elif(especie == 5):
            pesoMaximo = pesoMaximoOtros
            pesoTara = pesoTaraOtros
            presentacion = "OTROS"
            self.ui.lblOtros.setStyleSheet("background-color: rgb(255, 207, 11); color: #000")

    def fn_verificarProceso(self):
        global numeroProceso
        global numeroLote
        global fechaInicioProceso
        global horaInicioProceso
        global horaInicioLote
        global acumuladoProceso
        global acumuladoLote

        resultadoProceso = self.conexion.db_verificarProceso()

        if resultadoProceso and resultadoProceso[3] == 0:
            numeroProceso = resultadoProceso[0]
            fechaInicioProceso = resultadoProceso[1]
            horaInicioProceso = resultadoProceso[2]

            resultadoAcumuladoProceso = self.conexion.db_traerAcumuladoProceso(numeroProceso)
            acumuladoProceso = resultadoAcumuladoProceso if resultadoAcumuladoProceso is not None else 0

            resultadoLote = self.conexion.db_verificarLote(numeroProceso)

            if resultadoLote is None:
                numeroLote = 1
                acumuladoLote = 0
                horaInicioLote = datetime.now().strftime('%H:%M:%S')
                self.conexion.db_crearNuevoLote(numeroLote, numeroProceso, horaInicioLote)
            else:
                if resultadoLote[1] == 1:
                    numeroLote = resultadoLote[0] + 1
                    acumuladoLote = 0
                    horaInicioLote = datetime.now().strftime('%H:%M:%S')
                    self.conexion.db_crearNuevoLote(numeroLote, numeroProceso, horaInicioLote)
                else:
                    numeroLote = resultadoLote[0]
                    horaInicioLote = resultadoLote[2]
                    resultadoAcumuladoLote = self.conexion.db_traerAcumuladoLote(numeroProceso, numeroLote)
                    acumuladoLote = resultadoAcumuladoLote if resultadoAcumuladoLote is not None else 0
        else:
            if resultadoProceso and resultadoProceso[0]:
                numeroProceso = resultadoProceso[0] + 1
            else:
                numeroProceso = 1
            acumuladoProceso = 0
            fechaInicioProceso = datetime.now().strftime('%Y-%m-%d')
            horaInicioProceso = datetime.now().strftime('%H:%M:%S')
            self.conexion.db_crearNuevoProceso(numeroProceso, fechaInicioProceso, horaInicioProceso)

            numeroLote = 1
            acumuladoLote = 0
            horaInicioLote = datetime.now().strftime('%H:%M:%S')
            self.conexion.db_crearNuevoLote(numeroLote, numeroProceso, horaInicioLote)

        if isinstance(fechaInicioProceso, str):
            fechaInicioProceso_str = datetime.strptime(fechaInicioProceso, '%Y-%m-%d').strftime('%d/%m')
        elif isinstance(fechaInicioProceso, date):
            fechaInicioProceso_str = fechaInicioProceso.strftime('%d/%m')
            
        if isinstance(horaInicioProceso, str):
            horaInicioProceso_str = datetime.strptime(horaInicioProceso, '%H:%M:%S').strftime('%I:%M %p')
        elif isinstance(horaInicioProceso, timedelta):
            horaInicioProceso_str = (datetime.min + horaInicioProceso).strftime('%I:%M %p')

        if isinstance(horaInicioLote, str):
            horaInicioLote_str = datetime.strptime(horaInicioLote, '%H:%M:%S').strftime('%I:%M %p')
        elif isinstance(horaInicioLote, timedelta):
            horaInicioLote_str = (datetime.min + horaInicioLote).strftime('%I:%M %p')

        self.ui.txtNumeroProceso.setText(str(numeroProceso))
        self.ui.txtNumeroLote.setText(str(numeroLote))
        self.ui.lblHoraInicioProceso.setText(f"FECHA {fechaInicioProceso_str} | HORA INICIO: {horaInicioProceso_str}")   
        self.ui.lblHoraInicioLote.setText(f"HORA INICIO: {horaInicioLote_str}")
        self.ui.txtAcumuladoPorProceso.setText(str(acumuladoProceso))
        self.ui.txtAcumuladoPorLote.setText(str(acumuladoLote))
        
    def fn_guardarPesada(self):
        global captaCodigo
        global pesoExcedido
        global captaCodigoQr
        
        pesoIndicador = self.ui.lblPesoIndicador.text()
        horaPeso = datetime.now().strftime('%H:%M:%S')
        
        self.conexion.db_guardarPesada(numeroProceso, numeroLote, presentacion, pesoIndicador, pesoTara, horaPeso, fechaInicioProceso, codigoColaborador, pesoExcedido)
        self.fn_alerta("REGISTRO CORRECTO!",correcto,"El registro se ha guardado correctamente para:", 500, True)
        
        self.ui.txtCodigoColaborador.setEnabled(False)
        self.ui.txtCodigoColaborador.setFocus(False)
        self.ui.txtCodigoColaborador.setText("")
            
        thread = threading.Thread(target=self.fn_accionarPulsos, args=(pesoIndicador, pesoMaximo))
        thread.start()
        
        captaCodigo = True
        captaCodigoQr = False
        pesoExcedido = 0
        # self.fn_listarPesadas()
        self.fn_listarPesadasEnProceso()
        
    def fn_accionarPulsos(self, pesoIndicador, pesoMaximo):
        if float(pesoIndicador) >= pesoMaximo:
            self.pulsosArduino.fn_registroExcesoPeso()
        else:
            self.pulsosArduino.fn_registroCorrecto()
        
    def fn_listarPesadas(self):
        global acumuladoProceso
        global acumuladoLote
        global listoParaAccionar
        global numeroDePesada
        
        resultadoAcumuladoProceso = self.conexion.db_traerAcumuladoProceso(numeroProceso)
        acumuladoProceso = resultadoAcumuladoProceso if resultadoAcumuladoProceso is not None else 0
        
        resultadoAcumuladoLote = self.conexion.db_traerAcumuladoLote(numeroProceso, numeroLote)
        acumuladoLote = resultadoAcumuladoLote if resultadoAcumuladoLote is not None else 0
        
        self.ui.txtAcumuladoPorProceso.setText(str(acumuladoProceso))
        self.ui.txtAcumuladoPorLote.setText(str(acumuladoLote))
        
        self.tablaDePesos.clearContents()
        self.tablaDePesos.setRowCount(0)
        
        pesosListarTabla = self.conexion.db_listarPesosTabla(fechaInicioProceso, numeroProceso, numeroLote)
        
        listoParaAccionar = False
        numeroDePesada = 0
        
        if pesosListarTabla != "" and pesosListarTabla != None:
            if len(pesosListarTabla) > 0:
                
                listoParaAccionar = True
            
                for row_number, row_data in enumerate(pesosListarTabla):
                    
                        self.tablaDePesos.insertRow(row_number)
                        
                        for column_number, data in enumerate(row_data):
                            
                            if column_number == 0:  # Columna de "correlativo"
                                data = (row_number - len(pesosListarTabla))*-1
                                numeroDePesada = len(pesosListarTabla)
                                
                            if column_number == 3:  # Columna de "Peso Neto"
                                data = "{:.3f}".format(data)
                            if column_number == 4:  # Columna de "TALLO SOLO"
                                data = "{:.3f}".format(data)
                            if column_number == 5:  # Columna de "TALLO CORAL"
                                data = "{:.3f}".format(data)
                            if column_number == 6:  # Columna de "MEDIA VALVA TALLO SOLO"
                                data = "{:.3f}".format(data)
                            if column_number == 7:  # Columna de "MEDIA VALVA TALLO CORAL"
                                data = "{:.3f}".format(data)
                            if column_number == 8:  # Columna de "OTROS"
                                data = "{:.3f}".format(data)
                            if column_number == 9 :  # Columna de "Hora Peso"
                                hours, remainder = divmod(data.seconds, 3600)
                                minutes, seconds = divmod(remainder, 60)
                                data = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

                            item = QTableWidgetItem(str(data))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tablaDePesos.setItem(row_number, column_number, item)
                            
    def fn_listarPesadasEnProceso(self):
        global acumuladoProceso
        global acumuladoLote
        global listoParaAccionar
        global numeroDePesada
        
        pesosListarTabla = self.conexion.db_listarPesosTablaEnProceso()
        
        listoParaAccionar = False
        
        if pesosListarTabla != "" and pesosListarTabla != None:
            if len(pesosListarTabla) > 0:
                
                listoParaAccionar = True
            
                for row_number, row_data in enumerate(pesosListarTabla):
                    
                        self.tablaDePesos.insertRow(row_number)
                        
                        for column_number, data in enumerate(row_data):
                            
                            if column_number == 0:  # Columna de "correlativo"
                                numeroDePesada = numeroDePesada + 1
                                data = numeroDePesada
                                
                            if column_number == 3:  # Columna de "Peso Neto"
                                acumuladoProceso += data
                                acumuladoLote += data
                                self.ui.txtAcumuladoPorProceso.setText("{:.3f}".format(acumuladoProceso))
                                self.ui.txtAcumuladoPorLote.setText("{:.3f}".format(acumuladoLote))
                                data = "{:.3f}".format(data)
                                
                            if column_number == 4:  # Columna de "TALLO SOLO"
                                data = "{:.3f}".format(data)
                            if column_number == 5:  # Columna de "TALLO CORAL"
                                data = "{:.3f}".format(data)
                            if column_number == 6:  # Columna de "MEDIA VALVA TALLO SOLO"
                                data = "{:.3f}".format(data)
                            if column_number == 7:  # Columna de "MEDIA VALVA TALLO CORAL"
                                data = "{:.3f}".format(data)
                            if column_number == 8:  # Columna de "OTROS"
                                data = "{:.3f}".format(data)
                            if column_number == 9 :  # Columna de "Hora Peso"
                                hours, remainder = divmod(data.seconds, 3600)
                                minutes, seconds = divmod(remainder, 60)
                                data = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

                            item = QTableWidgetItem(str(data))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.tablaDePesos.setItem(row_number, column_number, item)
        
    def fn_finalizarLote(self):
        horaFinLote = datetime.now().strftime('%H:%M:%S')
        self.conexion.db_finalizarLote(numeroLote, numeroProceso, horaFinLote, acumuladoLote)
        self.fn_verificarProceso()
        self.fn_listarPesadas()
    
    def fn_finalizarProceso(self):
        horaFinProceso = datetime.now().strftime('%H:%M:%S')
        fechaFinProceso = datetime.now().strftime('%Y-%m-%d')
        horaFinProceso = datetime.now().strftime('%H:%M:%S')
        self.conexion.db_finalizarProceso(numeroProceso, fechaFinProceso, horaFinProceso, acumuladoProceso)
        
        horaFinLote = datetime.now().strftime('%H:%M:%S')
        self.conexion.db_finalizarLote(numeroLote, numeroProceso, horaFinLote, acumuladoLote)
        
        self.fn_modal_principal()
        
    def fn_seleccionaTara(self, especie):
        global presentacionEditarTara
        global frmEditarTaraAlerta
        global frmIngresarNuevaTara
        
        presentacionEditarTara = especie
        frmEditarTaraAlerta = False
        self.ui.frmEditarTaraAlerta.setHidden(True)
        frmIngresarNuevaTara = True
        self.ui.frmIngresarNuevaTara.setHidden(False)
        self.ui.txtIngresarNuevaTara.setFocus(True)
        
    def fn_actualizaEspeciePesada(self, codigoEspecie):
        global frmEditarPresentacion
        
        codigoNuevaEspecie = codigoEspecie
        self.conexion.db_actualizarEspeciePesada(idPesadaEditarOEliminar, codigoNuevaEspecie)
        self.ui.frmSombra.setHidden(True)
        self.ui.frmEditarPresentacion.setHidden(True)
        frmEditarPresentacion = False
        # self.fn_listarPesadas()
        self.fn_alerta("ACTUALIZACIÓN CORRECTA!",correcto,"El registro se ha actualizado correctamente.")
        self.fn_actualizaPresentacionEnProceso(idPesadaEditarOEliminar, codigoNuevaEspecie)
        
    def fn_seleccionarEspecieDescuento(self, especie):
        global presentacionDescuento
        
        self.ui.lblDescuentoPresentacionTalloSolo.setStyleSheet("color: rgb(255, 255, 255); border-top-left-radius: 10px; border-top-right-radius: 10px; background-color: rgb(29, 71, 131);")
        self.ui.lblDescuentoPresentacionTalloCoral.setStyleSheet("color: rgb(255, 255, 255); border-top-left-radius: 10px; border-top-right-radius: 10px; background-color: rgb(29, 71, 131);")
        self.ui.lblDescuentoPresentacionMediaValvaTalloSolo.setStyleSheet("color: rgb(255, 255, 255); border-top-left-radius: 10px; border-top-right-radius: 10px; background-color: rgb(29, 71, 131);")
        self.ui.lblDescuentoPresentacionMediaValvaTalloCoral.setStyleSheet("color: rgb(255, 255, 255); border-top-left-radius: 10px; border-top-right-radius: 10px; background-color: rgb(29, 71, 131);")
        self.ui.lblDescuentoPresentacionOtros.setStyleSheet("color: rgb(255, 255, 255); border-top-left-radius: 10px; border-top-right-radius: 10px; background-color: rgb(29, 71, 131);")
        presentacionDescuento = ""
        
        if(especie == 1):
            presentacionDescuento = "TALLO SOLO"
            self.ui.lblDescuentoPresentacionTalloSolo.setStyleSheet("background-color: rgb(255, 207, 11); color: #000; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        elif(especie == 2):
            presentacionDescuento = "TALLO CORAL"
            self.ui.lblDescuentoPresentacionTalloCoral.setStyleSheet("background-color: rgb(255, 207, 11); color: #000; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        elif(especie == 3):
            presentacionDescuento = "MEDIA VALVA T/S"
            self.ui.lblDescuentoPresentacionMediaValvaTalloSolo.setStyleSheet("background-color: rgb(255, 207, 11); color: #000; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        elif(especie == 4):
            presentacionDescuento = "MEDIA VALVA T/C"
            self.ui.lblDescuentoPresentacionMediaValvaTalloCoral.setStyleSheet("background-color: rgb(255, 207, 11); color: #000; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        elif(especie == 5):
            presentacionDescuento = "OTROS"
            self.ui.lblDescuentoPresentacionOtros.setStyleSheet("background-color: rgb(255, 207, 11); color: #000; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        
    def fn_seleccionarEspecieDescuentoServis(self, especie):
        global presentacionDescuentoServis
        
        self.ui.lblDescuentoPresentacionTalloSoloServis.setStyleSheet("color: rgb(255, 255, 255); border-top-left-radius: 10px; border-top-right-radius: 10px; background-color: rgb(29, 71, 131);")
        self.ui.lblDescuentoPresentacionTalloCoralServis.setStyleSheet("color: rgb(255, 255, 255); border-top-left-radius: 10px; border-top-right-radius: 10px; background-color: rgb(29, 71, 131);")
        self.ui.lblDescuentoPresentacionMediaValvaTalloSoloServis.setStyleSheet("color: rgb(255, 255, 255); border-top-left-radius: 10px; border-top-right-radius: 10px; background-color: rgb(29, 71, 131);")
        self.ui.lblDescuentoPresentacionMediaValvaTalloCoralServis.setStyleSheet("color: rgb(255, 255, 255); border-top-left-radius: 10px; border-top-right-radius: 10px; background-color: rgb(29, 71, 131);")
        self.ui.lblDescuentoPresentacionOtros.setStyleSheet("color: rgb(255, 255, 255); border-top-left-radius: 10px; border-top-right-radius: 10px; background-color: rgb(29, 71, 131);")
        presentacionDescuentoServis = ""
        
        if(especie == 1):
            presentacionDescuentoServis = "TALLO SOLO"
            self.ui.lblDescuentoPresentacionTalloSoloServis.setStyleSheet("background-color: rgb(255, 207, 11); color: #000; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        elif(especie == 2):
            presentacionDescuentoServis = "TALLO CORAL"
            self.ui.lblDescuentoPresentacionTalloCoralServis.setStyleSheet("background-color: rgb(255, 207, 11); color: #000; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        elif(especie == 3):
            presentacionDescuentoServis = "MEDIA VALVA T/S"
            self.ui.lblDescuentoPresentacionMediaValvaTalloSoloServis.setStyleSheet("background-color: rgb(255, 207, 11); color: #000; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        elif(especie == 4):
            presentacionDescuentoServis = "MEDIA VALVA T/C"
            self.ui.lblDescuentoPresentacionMediaValvaTalloCoralServis.setStyleSheet("background-color: rgb(255, 207, 11); color: #000; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        elif(especie == 5):
            presentacionDescuentoServis = "OTROS"
            self.ui.lblDescuentoPresentacionOtrosServis.setStyleSheet("background-color: rgb(255, 207, 11); color: #000; border-top-left-radius: 10px; border-top-right-radius: 10px;")
            
    def fn_registrarDescuento(self):
        horaDescuento = datetime.now().strftime('%H:%M:%S')
        txtIngresarPesoDescuento = self.ui.txtIngresarPesoDescuento.text()
        self.conexion.db_aplicarDescuentoPersonal(numeroProceso, numeroLote, fechaInicioProceso, horaDescuento, presentacionDescuento, txtIngresarPesoDescuento, codigoColaboradorDescuento)
        # self.fn_listarPesadas()
        self.fn_alerta("DESCUENTO CORRECTO!",correcto,"El descuento se ha registrado correctamente.")
    
    def fn_registrarDescuentoServis(self):
        txtIngresarPesoDescuentoServis = self.ui.txtIngresarPesoDescuentoServis.text()
        
        respuestaClientesServices = self.conexion.db_traerClientesServis(codigoColaboradorDescuentoServis)
        
        for clienteServis in respuestaClientesServices:
            codigoColaboradorDescuentoBucleServis = clienteServis[1]
            horaDescuento = datetime.now().strftime('%H:%M:%S')
            self.conexion.db_aplicarDescuentoPersonal(numeroProceso, numeroLote, fechaInicioProceso, horaDescuento, presentacionDescuentoServis, txtIngresarPesoDescuentoServis, codigoColaboradorDescuentoBucleServis)
        
        # self.fn_listarPesadas()
        self.fn_alerta("DESCUENTO CORRECTO!",correcto,"El descuento se ha registrado correctamente.")
    
# DISEÑADO Y DESARROLLADO POR SANTOS VILCHEZ EDINSON PASCUAL
# LA UNIÓN - PIURA - PERU ; 2024