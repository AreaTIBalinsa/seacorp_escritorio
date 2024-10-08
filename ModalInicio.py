from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow
import sys
import os
from View.Ui_modal_inicio import Ui_Modal_Inicio
import InicioSistema
import pulsosArduino

class ModalPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Modal_Inicio()
        self.ui.setupUi(self)
        self.pulsosArduino = pulsosArduino
        
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon("Resources/icon.jpg"))
        self.setWindowTitle('SISTEMA INTEGRAL || BALINSA')
        
        self.ui.labelFondoSistema.setPixmap(QPixmap("Resources/conchas.png"))
        self.ui.lblImgTalloSolo.setPixmap(QPixmap("Resources/tallo_solo.png"))
        self.ui.lblImgTalloCoral.setPixmap(QPixmap("Resources/tallo_coral.png"))
        self.ui.lblImgMediaValvaTs.setPixmap(QPixmap("Resources/media_valva.png"))
        self.ui.lblImgMediaValvaTc.setPixmap(QPixmap("Resources/media_valva.png"))
        self.ui.lblImgOtros.setPixmap(QPixmap("Resources/media_valva.png"))
        self.ui.lblImgReestablecer.setPixmap(QPixmap("Resources/reestablecer.png"))
        self.ui.lblImgApagar.setPixmap(QPixmap("Resources/off_ok.png"))
        self.ui.lblImgIniciarProceso.setPixmap(QPixmap("Resources/iniciar.png"))
        self.ui.imgFinalizar.setPixmap(QPixmap("Resources/error.png"))
        
        self.ui.frmSombra.setHidden(True)
        
    def keyReleaseEvent(self, event):
            
        if (event.key() == Qt.Key_1) and not self.ui.frmSombra.isVisible():
            if not InicioSistema.seleccionarTalloSolo:
                InicioSistema.seleccionarTalloSolo = True
                self.ui.lblTalloSolo.setStyleSheet("background-color: rgb(20, 180, 60);""border-top-left-radius: 10px;""border-top-right-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 40;")
            else:
                InicioSistema.seleccionarTalloSolo = False
                self.ui.lblTalloSolo.setStyleSheet("background-color: rgb(255, 207, 11);""border-top-left-radius: 10px;""border-top-right-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 40;")
            
        if (event.key() == Qt.Key_2) and not self.ui.frmSombra.isVisible():
            if not InicioSistema.seleccionarTalloCoral:
                InicioSistema.seleccionarTalloCoral = True
                self.ui.lblTalloCoral.setStyleSheet("background-color: rgb(20, 180, 60);""border-top-left-radius: 10px;""border-top-right-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 55;")
            else:
                InicioSistema.seleccionarTalloCoral = False
                self.ui.lblTalloCoral.setStyleSheet("background-color: rgb(255, 207, 11);""border-top-left-radius: 10px;""border-top-right-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 55;")
            
        if (event.key() == Qt.Key_3) and not self.ui.frmSombra.isVisible():
            if not InicioSistema.seleccionarMediaValvaTs:
                InicioSistema.seleccionarMediaValvaTs = True
                self.ui.lblMediaValvaTs.setStyleSheet("background-color: rgb(20, 180, 60);""border-top-left-radius: 10px;""border-top-right-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
            else:
                InicioSistema.seleccionarMediaValvaTs = False
                self.ui.lblMediaValvaTs.setStyleSheet("background-color: rgb(255, 207, 11);""border-top-left-radius: 10px;""border-top-right-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
            
        if (event.key() == Qt.Key_4) and not self.ui.frmSombra.isVisible():
            if not InicioSistema.seleccionarMediaValvaTc:
                InicioSistema.seleccionarMediaValvaTc = True
                self.ui.lblMediaValvaTc.setStyleSheet("background-color: rgb(20, 180, 60);""border-top-left-radius: 10px;""border-top-right-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
            else:
                InicioSistema.seleccionarMediaValvaTc = False
                self.ui.lblMediaValvaTc.setStyleSheet("background-color: rgb(255, 207, 11);""border-top-left-radius: 10px;""border-top-right-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
            
        if (event.key() == Qt.Key_5) and not self.ui.frmSombra.isVisible():
            if not InicioSistema.seleccionarOtros:
                InicioSistema.seleccionarOtros = True
                self.ui.lblOtros.setStyleSheet("background-color: rgb(20, 180, 60);""border-top-left-radius: 10px;""border-top-right-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 30;")
            else:
                InicioSistema.seleccionarOtros = False
                self.ui.lblOtros.setStyleSheet("background-color: rgb(255, 207, 11);""border-top-left-radius: 10px;""border-top-right-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 30;")
            
        if (event.key() == Qt.Key_Minus) and not self.ui.frmSombra.isVisible():
            self.fn_resetearSeleccion()
            
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and not self.ui.frmSombra.isVisible():      
            self.aplicacion_Principal = InicioSistema.AplicacionPrincipal()
            
            frames = [
                (self.aplicacion_Principal.ui.frmTalloSolo, InicioSistema.seleccionarTalloSolo),
                (self.aplicacion_Principal.ui.frmTalloCoral, InicioSistema.seleccionarTalloCoral),
                (self.aplicacion_Principal.ui.frmMediaValvaTalloSolo, InicioSistema.seleccionarMediaValvaTs),
                (self.aplicacion_Principal.ui.frmMediaValvaTalloCoral, InicioSistema.seleccionarMediaValvaTc),
                (self.aplicacion_Principal.ui.frmOtros, InicioSistema.seleccionarOtros)
            ]
            
            x_start = 20
            y_position = 500
            frame_width = 232
            frame_height = 90
            spacing = 20
            
            current_x = x_start
            for frame, is_visible in frames:
                if is_visible:
                    frame.setGeometry(current_x, y_position, frame_width, frame_height)
                    frame.setHidden(False)
                    current_x += frame_width + spacing
                else:
                    frame.setHidden(True)
            
            if not self.aplicacion_Principal.isVisible():
                self.aplicacion_Principal.show()
            else:
                self.aplicacion_Principal.showNormal()
                self.aplicacion_Principal.activateWindow()
                
            self.aplicacion_Principal.fn_verificarProceso()
            self.aplicacion_Principal.fn_listarPesadas()
            self.close()
            
        if (event.key() == Qt.Key_1) and self.ui.frmSombra.isVisible():
            self.pulsosArduino.fn_apagarIndicador()
            # os.system("shutdown -s")
        
        if (event.key() == Qt.Key_2) and self.ui.frmSombra.isVisible():
            self.pulsosArduino.fn_apagarIndicador()
            # os.system("shutdown -r")
            
        if (event.key() == Qt.Key_3) and self.ui.frmSombra.isVisible():
            self.ui.frmSombra.setHidden(True)
            
        if (event.key() == Qt.Key_0) and not self.ui.frmSombra.isVisible():
            self.ui.frmSombra.setHidden(False)
            
    def fn_resetearSeleccion(self):
        InicioSistema.seleccionarTalloSolo = False
        InicioSistema.seleccionarTalloCoral = False
        InicioSistema.seleccionarMediaValvaTs = False
        InicioSistema.seleccionarMediaValvaTc = False
        InicioSistema.seleccionarOtros = False
        
        self.ui.lblTalloSolo.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 40;")
        self.ui.lblTalloCoral.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 55;")
        self.ui.lblMediaValvaTs.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
        self.ui.lblMediaValvaTc.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 50;")
        self.ui.lblOtros.setStyleSheet("background-color: rgb(255, 207, 11);""border-radius: 10px;""border: none;""color: rgb(255, 255, 255);""padding-left: 30;")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ModalPrincipal()
    gui.show()
    sys.exit(app.exec_())