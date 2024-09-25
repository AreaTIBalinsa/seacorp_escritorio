from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow
import sys
import serial
import time
import socket
from datetime import datetime
import sys
import cv2
from pyzbar.pyzbar import decode

from View.Ui_Principal import Ui_MainWindow
import pulsosArduino
from View.Ui_modal_alerta import Ui_modalAlerta as Modal_Alerta

# Importación de Base de Datos
import DataBase.database_conexion # El archivo database_conexion.py

# Puertos COM
COMARDUINO = ""
COMINDICADOR = ""

seleccionarTalloSolo = False
seleccionarTalloCoral = False
seleccionarMediaValvaTs = False
seleccionarMediaValvaTc = False
seleccionarOtros = False

lblReestablecer = False
lblApagar = False
lblIniciarProceso = False

seleccionarTalloSolo = False
seleccionarTalloCoral = False
seleccionarMediaValvaTs = False
seleccionarMediaValvaTc = False
seleccionarOtros = False

lblReestablecer = False
lblApagar = False
lblIniciarProceso = False

captaCodigo = False
pesoMaximo = 0
pesoTara = 0
pesoExcedido = 0
presentacion = ""
fechaPeso = ""
horaPeso = datetime.now().strftime('%H:%M:%S')

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
frmEditarPesadaAlerta = False
frmDescuentoAlerta = False
frmFinalizarAlerta = False

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
                # print("WT IN: " + str(e))
                time.sleep(1)
                # Cerrar la conexión serial si hay una excepción
                if serialIndicador is not None and serialIndicador.is_open:
                    serialIndicador.close()
    
    def stop(self):
        print("Thread Stopped")
        self.terminate()
        
""" Creamos hilo para la ejecución en segundo plano para subir los datos al servidor """

class WorkerThreadSubirDatosBase(QThread):
    # Tarea a ejecutarse cada determinado tiempo.
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
                    # self.conexion.actualizar_datos_servidor_pesadas()
                except Exception as e:
                    print(f"Error al interactuar con la base de datos: {e}")
                    print('ERROR')
                else:
                    s.close()
            time.sleep(240)

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
            # print("Serial Exception: " + str(e))
            time.sleep(1)  # Espera antes de intentar reconectar
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
    # Tarea a ejecutarse cada determinado tiempo.
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

class InicioSistema(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.conexion = DataBase.database_conexion.Conectar()
        self.modal_alerta = Modal_Alerta()
        
        # self.pulsosArduino = pulsosArduino
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 270)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon("Resources/icon.jpg"))
        self.setWindowTitle('SISTEMA INTEGRAL || BALINSA')
        
        self.ui.imgPlataformaBalanza.setPixmap(QPixmap("Resources/plataforma_balanza.png"))
        self.ui.imgPanera.setPixmap(QPixmap("Resources/panera.png"))
        self.ui.imgFlechaDerecha.setPixmap(QPixmap("Resources/flecha.png"))
        self.ui.imgFlechaIzquierda.setPixmap(QPixmap("Resources/flecha.png"))
        
        self.workerFechaHora = WorkerThreadFechaHora()
        self.workerFechaHora.start() # Iniciamos el hilo
        self.workerFechaHora.update_fecha.connect(self.mostrar_fecha)
        self.workerFechaHora.update_hora.connect(self.mostrar_hora)
        
        self.worker = WorkerThread() # Hilo de Balanza
        self.worker.start()
        self.worker.update_peso.connect(self.fn_actualizar_peso)
        self.worker.update_estado.connect(self.fn_actualizar_estado)
        
        # self.workerBase = WorkerThreadSubirDatosBase()
        # self.workerBase.start()
        
        self.fn_asignaPesosMaximosYTaras()
        
        self.ui.imgPanera.setHidden(True)
        self.ui.txtCodigoColaborador.setEnabled(False)
        self.ui.txtCodigoColaborador.setFocus(False)
        self.ui.txtCodigoColaborador.setText("")
        self.ui.lblPesoIndicador.setText("-----")
        self.ui.lblIndicadorPlataforma.setText("-----")
        
        self.ui.frmEditarTaraAlerta.setHidden(True)
        self.ui.frmSombra.setHidden(True)
        self.ui.frmAlerta.setHidden(True)
        
        self.fn_modal_alerta()
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            qr_codes = decode(frame)

            for qr_code in qr_codes:
                qr_data = qr_code.data.decode('utf-8')
                
                if(captaCodigo):
                    self.ui.txtCodigoColaborador.setText(qr_data)
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
            
    def closeEvent(self, event):
        self.cap.release()
        event.accept()
        
    def mostrar_hora(self,val):
        self.ui.lblHora.setText(val)
        
    def mostrar_fecha(self,val):
        self.ui.lblFecha.setText(val)
        
    def fn_modal_alerta(self):
        
        self.dialog_modal_alerta = QDialog(self)
        # dialog_modal_alerta.setWindowIcon(QtGui.QIcon(imagen))
        self.dialog_modal_alerta.setWindowIcon(QtGui.QIcon("Resources/icon.jpg"))
        self.modal_alerta.setupUi(self.dialog_modal_alerta)
        self.dialog_modal_alerta.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.modal_alerta.labelFondoSistema.setPixmap(QPixmap("Resources/conchas.png"))
        self.modal_alerta.lblImgTalloSolo.setPixmap(QPixmap("Resources/tallo_solo.png"))
        self.modal_alerta.lblImgTalloCoral.setPixmap(QPixmap("Resources/tallo_coral.png"))
        self.modal_alerta.lblImgMediaValvaTs.setPixmap(QPixmap("Resources/media_valva.png"))
        self.modal_alerta.lblImgMediaValvaTc.setPixmap(QPixmap("Resources/media_valva.png"))
        self.modal_alerta.lblImgOtros.setPixmap(QPixmap("Resources/media_valva.png"))
        self.modal_alerta.lblImgReestablecer.setPixmap(QPixmap("Resources/reestablecer.png"))
        self.modal_alerta.lblImgApagar.setPixmap(QPixmap("Resources/off_ok.png"))
        self.modal_alerta.lblImgIniciarProceso.setPixmap(QPixmap("Resources/iniciar.png"))
        
        # self.modal_alerta.modal_lblAlertaTitulo.setText(titulo)
        
        self.dialog_modal_alerta.keyReleaseEvent = self.keyReleaseEvent
        self.dialog_modal_alerta.exec_()
        
    def fn_actualizar_peso(self, val):
        global captaCodigo
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
                pesoExcedido = 0
            else:
                pesoIndicador = pesoIndicador - pesoTara
                
                if(pesoIndicador > 0):
                    if(captaCodigo == False):
                        self.ui.imgPanera.setHidden(False)
                        self.ui.imgFlechaDerecha.setHidden(True)
                        self.ui.imgFlechaIzquierda.setHidden(True)
                        self.ui.lblColoquePeso.setHidden(True)
                        
                        self.ui.txtCodigoColaborador.setEnabled(True)
                        self.ui.txtCodigoColaborador.setFocus(True)
                        captaCodigo = True
                    
                    if pesoIndicador >= pesoMaximo and pesoMaximo != 0:
                        self.ui.lblPesoIndicador.setText(str(format(pesoMaximo, ".3f")))
                        self.ui.lblIndicadorPlataforma.setText(str(format(pesoMaximo, ".3f")))
                        pesoExcedido = pesoIndicador - pesoMaximo
                        self.ui.txtCodigoColaborador.setFocus(True)
                    else:
                        self.ui.lblPesoIndicador.setText(format(pesoIndicador, ".3f"))
                        self.ui.lblIndicadorPlataforma.setText(format(pesoIndicador, ".3f"))
                        self.ui.txtCodigoColaborador.setFocus(True)
                else:
                    self.ui.imgPanera.setHidden(True)
                    self.ui.imgFlechaDerecha.setHidden(False)
                    self.ui.imgFlechaIzquierda.setHidden(False)
                    self.ui.lblColoquePeso.setHidden(False)
                    
                    self.ui.txtCodigoColaborador.setEnabled(False)
                    self.ui.txtCodigoColaborador.setFocus(False)
                    self.ui.txtCodigoColaborador.setText("")
                    
                    captaCodigo = False
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

    # ======================== Eventos con el Teclado ========================
    
    def condiciones_base(self):
        return (
            not frmEditarTaraAlerta and
            not frmEditarPesadaAlerta and
            not frmDescuentoAlerta and
            not frmFinalizarAlerta
        )
        
    def condiciones_alertas(self):
        return (
            not self.ui.frmEditarTaraAlerta.isVisible() and
            not self.ui.frmSombra.isVisible() and
            not self.ui.frmAlerta.isVisible()
        )
        
    def condiciones_alertas_sombra(self):
        return (
            not self.ui.frmEditarTaraAlerta.isVisible() and
            not self.ui.frmSombra.isVisible()
        )
        
    def fn_alerta(self,titulo,imagen,mensaje,tiempo = 500):
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

        timer = QtCore.QTimer()
        timer.singleShot(tiempo, lambda: self.ui.frmAlerta.setHidden(True))
        
        if self.condiciones_alertas_sombra():
            timer2 = QtCore.QTimer()
            timer2.singleShot(tiempo, lambda: self.ui.frmSombra.setHidden(True))
         
    def keyReleaseEvent(self, event):
        
        global seleccionarTalloSolo
        global seleccionarTalloCoral
        global seleccionarMediaValvaTs
        global seleccionarMediaValvaTc
        global seleccionarOtros
        global seleccionarlblReestablecer
        global seleccionarlblApagar
        global seleccionarlblIniciarProceso
            
        if event.key() == Qt.Key_1:
            if not seleccionarTalloSolo:
                seleccionarTalloSolo = True
                self.modal_alerta.lblTalloSolo.setStyleSheet("background-color: rgb(20, 180, 60);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 40;")
            else:
                seleccionarTalloSolo = False
                self.modal_alerta.lblTalloSolo.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 40;")
            
        if event.key() == Qt.Key_2:
            if not seleccionarTalloCoral:
                seleccionarTalloCoral = True
                self.modal_alerta.lblTalloCoral.setStyleSheet("background-color: rgb(20, 180, 60);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 55;")
            else:
                seleccionarTalloCoral = False
                self.modal_alerta.lblTalloCoral.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 55;")
            
        if event.key() == Qt.Key_3:
            if not seleccionarMediaValvaTs:
                seleccionarMediaValvaTs = True
                self.modal_alerta.lblMediaValvaTs.setStyleSheet("background-color: rgb(20, 180, 60);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
            else:
                seleccionarMediaValvaTs = False
                self.modal_alerta.lblMediaValvaTs.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
            
        if event.key() == Qt.Key_4:
            if not seleccionarMediaValvaTc:
                seleccionarMediaValvaTc = True
                self.modal_alerta.lblMediaValvaTc.setStyleSheet("background-color: rgb(20, 180, 60);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
            else:
                seleccionarMediaValvaTc = False
                self.modal_alerta.lblMediaValvaTc.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
            
        if event.key() == Qt.Key_5:
            if not seleccionarOtros:
                seleccionarOtros = True
                self.modal_alerta.lblOtros.setStyleSheet("background-color: rgb(20, 180, 60);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 30;")
            else:
                seleccionarOtros = False
                self.modal_alerta.lblOtros.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 30;")
            
        if event.key() == Qt.Key_6:
            seleccionarTalloSolo = False
            seleccionarTalloCoral = False
            seleccionarMediaValvaTs = False
            seleccionarMediaValvaTc = False
            seleccionarOtros = False
            
            self.modal_alerta.lblTalloSolo.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 40;")
            self.modal_alerta.lblTalloCoral.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 55;")
            self.modal_alerta.lblMediaValvaTs.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
            self.modal_alerta.lblMediaValvaTc.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
            self.modal_alerta.lblOtros.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 30;")
            
        if event.key() == Qt.Key_7:
            if self.dialog_modal_alerta is not None:
                self.dialog_modal_alerta.close()
        
        if event.key() == Qt.Key_0:
            pass
        
        if not self.ui.txtCodigoColaborador.hasFocus():
            if (event.key() == Qt.Key_1) and self.condiciones_base() and self.condiciones_alertas():
                self.fn_seleccionarEspecie(1)
                
            if (event.key() == Qt.Key_2) and self.condiciones_base() and self.condiciones_alertas():
                self.fn_seleccionarEspecie(2)
            
            if (event.key() == Qt.Key_3) and self.condiciones_base() and self.condiciones_alertas():
                self.fn_seleccionarEspecie(3)
            
            if (event.key() == Qt.Key_4) and self.condiciones_base() and self.condiciones_alertas():
                self.fn_seleccionarEspecie(4)
            
            if (event.key() == Qt.Key_5) and self.condiciones_base() and self.condiciones_alertas():
                self.fn_seleccionarEspecie(5)
                
            # if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and self.condiciones_base() and self.condiciones_alertas():
            #     pass
    
    # ======================== Termina eventos con el Teclado ========================
    
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
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = InicioSistema()
    gui.show()
    sys.exit(app.exec_())
    
# DISEÑADO Y DESARROLLADO POR SANTOS VILCHEZ EDINSON PASCUAL
# LA UNIÓN - PIURA - PERU ; 2024