# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Seacorp_escritorio\View\modal_alerta.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_modalAlerta(object):
    def setupUi(self, modalAlerta):
        modalAlerta.setObjectName("modalAlerta")
        modalAlerta.setWindowModality(QtCore.Qt.NonModal)
        modalAlerta.resize(1600, 900)
        modalAlerta.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.labelFondoSistema = QtWidgets.QLabel(modalAlerta)
        self.labelFondoSistema.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        self.labelFondoSistema.setFocusPolicy(QtCore.Qt.NoFocus)
        self.labelFondoSistema.setText("")
        self.labelFondoSistema.setScaledContents(True)
        self.labelFondoSistema.setObjectName("labelFondoSistema")
        self.frame = QtWidgets.QFrame(modalAlerta)
        self.frame.setGeometry(QtCore.QRect(214, 154, 1171, 591))
        self.frame.setStyleSheet("#frame{\n"
"    background-color: rgba(255, 255, 255, 140);\n"
"    border-radius: 30px;\n"
"    border: none;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frameBtnReestablecer = QtWidgets.QFrame(self.frame)
        self.frameBtnReestablecer.setGeometry(QtCore.QRect(75, 385, 304, 108))
        self.frameBtnReestablecer.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 200);\n"
"border-radius: 10px;\n"
"border: none;")
        self.frameBtnReestablecer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBtnReestablecer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBtnReestablecer.setObjectName("frameBtnReestablecer")
        self.btnReestablecer = QtWidgets.QPushButton(self.frameBtnReestablecer)
        self.btnReestablecer.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnReestablecer.setFont(font)
        self.btnReestablecer.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    color: rgb(255, 255, 255);\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #4683FF;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #0649D1;\n"
"}")
        self.btnReestablecer.setText("")
        self.btnReestablecer.setObjectName("btnReestablecer")
        self.lblPresionarReestablecer = QtWidgets.QLabel(self.frameBtnReestablecer)
        self.lblPresionarReestablecer.setGeometry(QtCore.QRect(0, 75, 301, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblPresionarReestablecer.setFont(font)
        self.lblPresionarReestablecer.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblPresionarReestablecer.setStyleSheet("color: rgb(0, 0, 0);")
        self.lblPresionarReestablecer.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPresionarReestablecer.setObjectName("lblPresionarReestablecer")
        self.lblImgReestablecer = QtWidgets.QLabel(self.frameBtnReestablecer)
        self.lblImgReestablecer.setGeometry(QtCore.QRect(30, 15, 61, 41))
        self.lblImgReestablecer.setStyleSheet("background-color: transparent;")
        self.lblImgReestablecer.setText("")
        self.lblImgReestablecer.setObjectName("lblImgReestablecer")
        self.lblReestablecer = QtWidgets.QLabel(self.frameBtnReestablecer)
        self.lblReestablecer.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblReestablecer.setFont(font)
        self.lblReestablecer.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblReestablecer.setAutoFillBackground(False)
        self.lblReestablecer.setStyleSheet("background-color: #0055FF;\n"
"color: rgb(255, 255, 255);\n"
"border: none;\n"
"border-radius: 10px;\n"
"padding-left: 30px;")
        self.lblReestablecer.setAlignment(QtCore.Qt.AlignCenter)
        self.lblReestablecer.setObjectName("lblReestablecer")
        self.btnReestablecer.raise_()
        self.lblPresionarReestablecer.raise_()
        self.lblReestablecer.raise_()
        self.lblImgReestablecer.raise_()
        self.framebtnIniciarProceso = QtWidgets.QFrame(self.frame)
        self.framebtnIniciarProceso.setGeometry(QtCore.QRect(793, 385, 304, 108))
        self.framebtnIniciarProceso.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 200);\n"
"border-radius: 10px;\n"
"border: none;")
        self.framebtnIniciarProceso.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framebtnIniciarProceso.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framebtnIniciarProceso.setObjectName("framebtnIniciarProceso")
        self.btnIniciarProceso = QtWidgets.QPushButton(self.framebtnIniciarProceso)
        self.btnIniciarProceso.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnIniciarProceso.setFont(font)
        self.btnIniciarProceso.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnIniciarProceso.setAutoFillBackground(False)
        self.btnIniciarProceso.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #4683FF;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #0649D1;\n"
"}")
        self.btnIniciarProceso.setText("")
        self.btnIniciarProceso.setObjectName("btnIniciarProceso")
        self.lblPresionarIniciarProceso = QtWidgets.QLabel(self.framebtnIniciarProceso)
        self.lblPresionarIniciarProceso.setGeometry(QtCore.QRect(0, 75, 301, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblPresionarIniciarProceso.setFont(font)
        self.lblPresionarIniciarProceso.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblPresionarIniciarProceso.setStyleSheet("color: rgb(0, 0, 0);")
        self.lblPresionarIniciarProceso.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPresionarIniciarProceso.setObjectName("lblPresionarIniciarProceso")
        self.lblImgIniciarProceso = QtWidgets.QLabel(self.framebtnIniciarProceso)
        self.lblImgIniciarProceso.setGeometry(QtCore.QRect(10, 16, 61, 41))
        self.lblImgIniciarProceso.setStyleSheet("background-color: transparent;")
        self.lblImgIniciarProceso.setText("")
        self.lblImgIniciarProceso.setObjectName("lblImgIniciarProceso")
        self.lblIniciarProceso = QtWidgets.QLabel(self.framebtnIniciarProceso)
        self.lblIniciarProceso.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblIniciarProceso.setFont(font)
        self.lblIniciarProceso.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblIniciarProceso.setAutoFillBackground(False)
        self.lblIniciarProceso.setStyleSheet("background-color: #0055FF;\n"
"color: rgb(255, 255, 255);\n"
"border: none;\n"
"border-radius: 10px;\n"
"padding-left: 30px;")
        self.lblIniciarProceso.setAlignment(QtCore.Qt.AlignCenter)
        self.lblIniciarProceso.setObjectName("lblIniciarProceso")
        self.btnIniciarProceso.raise_()
        self.lblPresionarIniciarProceso.raise_()
        self.lblIniciarProceso.raise_()
        self.lblImgIniciarProceso.raise_()
        self.framebtnApagarEquipo = QtWidgets.QFrame(self.frame)
        self.framebtnApagarEquipo.setGeometry(QtCore.QRect(441, 447, 304, 108))
        self.framebtnApagarEquipo.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 200);\n"
"border-radius: 10px;\n"
"border: none;")
        self.framebtnApagarEquipo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framebtnApagarEquipo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framebtnApagarEquipo.setObjectName("framebtnApagarEquipo")
        self.btnApagarEquipo = QtWidgets.QPushButton(self.framebtnApagarEquipo)
        self.btnApagarEquipo.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnApagarEquipo.setFont(font)
        self.btnApagarEquipo.setStyleSheet("QPushButton{\n"
"    color: rgb(255, 255, 255);\n"
"    border:none;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: #FF4C4C;\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color: #D90000;\n"
"}")
        self.btnApagarEquipo.setText("")
        self.btnApagarEquipo.setObjectName("btnApagarEquipo")
        self.lblPresionarApagar = QtWidgets.QLabel(self.framebtnApagarEquipo)
        self.lblPresionarApagar.setGeometry(QtCore.QRect(0, 75, 301, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblPresionarApagar.setFont(font)
        self.lblPresionarApagar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblPresionarApagar.setStyleSheet("color: rgb(0, 0, 0);")
        self.lblPresionarApagar.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPresionarApagar.setObjectName("lblPresionarApagar")
        self.lblImgApagar = QtWidgets.QLabel(self.framebtnApagarEquipo)
        self.lblImgApagar.setGeometry(QtCore.QRect(50, 16, 61, 41))
        self.lblImgApagar.setStyleSheet("background-color: transparent;")
        self.lblImgApagar.setText("")
        self.lblImgApagar.setObjectName("lblImgApagar")
        self.lblApagar = QtWidgets.QLabel(self.framebtnApagarEquipo)
        self.lblApagar.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblApagar.setFont(font)
        self.lblApagar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblApagar.setAutoFillBackground(False)
        self.lblApagar.setStyleSheet("background-color: #FF0000;\n"
"color: rgb(255, 255, 255);\n"
"border: none;\n"
"border-radius: 10px;\n"
"padding-left: 30px;")
        self.lblApagar.setAlignment(QtCore.Qt.AlignCenter)
        self.lblApagar.setObjectName("lblApagar")
        self.btnApagarEquipo.raise_()
        self.lblPresionarApagar.raise_()
        self.lblApagar.raise_()
        self.lblImgApagar.raise_()
        self.frameBtnTalloSolo = QtWidgets.QFrame(self.frame)
        self.frameBtnTalloSolo.setGeometry(QtCore.QRect(75, 51, 304, 108))
        self.frameBtnTalloSolo.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 200);\n"
"border-radius: 10px;\n"
"border: none;")
        self.frameBtnTalloSolo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBtnTalloSolo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBtnTalloSolo.setObjectName("frameBtnTalloSolo")
        self.btnTalloSolo = QtWidgets.QPushButton(self.frameBtnTalloSolo)
        self.btnTalloSolo.setGeometry(QtCore.QRect(2, 3, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnTalloSolo.setFont(font)
        self.btnTalloSolo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnTalloSolo.setStyleSheet("background-color: transparent;\n"
"color: rgb(0, 0, 0);\n"
"border: none;")
        self.btnTalloSolo.setText("")
        self.btnTalloSolo.setObjectName("btnTalloSolo")
        self.lblPresionarTalloSolo = QtWidgets.QLabel(self.frameBtnTalloSolo)
        self.lblPresionarTalloSolo.setGeometry(QtCore.QRect(0, 75, 301, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblPresionarTalloSolo.setFont(font)
        self.lblPresionarTalloSolo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblPresionarTalloSolo.setStyleSheet("color: rgb(0, 0, 0);")
        self.lblPresionarTalloSolo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPresionarTalloSolo.setObjectName("lblPresionarTalloSolo")
        self.lblImgTalloSolo = QtWidgets.QLabel(self.frameBtnTalloSolo)
        self.lblImgTalloSolo.setGeometry(QtCore.QRect(25, 17, 61, 41))
        self.lblImgTalloSolo.setStyleSheet("background-color: transparent;")
        self.lblImgTalloSolo.setText("")
        self.lblImgTalloSolo.setObjectName("lblImgTalloSolo")
        self.lblTalloSolo = QtWidgets.QLabel(self.frameBtnTalloSolo)
        self.lblTalloSolo.setGeometry(QtCore.QRect(2, 3, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblTalloSolo.setFont(font)
        self.lblTalloSolo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblTalloSolo.setAutoFillBackground(False)
        self.lblTalloSolo.setStyleSheet("background-color: rgb(255, 207, 11);\n"
"color: rgb(0, 0, 0);\n"
"border: none;\n"
"border-radius: 10px;\n"
"padding-left: 40px;")
        self.lblTalloSolo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblTalloSolo.setObjectName("lblTalloSolo")
        self.btnTalloSolo.raise_()
        self.lblPresionarTalloSolo.raise_()
        self.lblTalloSolo.raise_()
        self.lblImgTalloSolo.raise_()
        self.frameBtnTalloCoral = QtWidgets.QFrame(self.frame)
        self.frameBtnTalloCoral.setGeometry(QtCore.QRect(441, 51, 304, 108))
        self.frameBtnTalloCoral.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 200);\n"
"border-radius: 10px;\n"
"border: none;")
        self.frameBtnTalloCoral.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBtnTalloCoral.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBtnTalloCoral.setObjectName("frameBtnTalloCoral")
        self.btnTalloCoral = QtWidgets.QPushButton(self.frameBtnTalloCoral)
        self.btnTalloCoral.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnTalloCoral.setFont(font)
        self.btnTalloCoral.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    color: rgb(0, 0, 0);\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(255, 207, 11);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(255, 207, 11);\n"
"}")
        self.btnTalloCoral.setText("")
        self.btnTalloCoral.setObjectName("btnTalloCoral")
        self.lblPresionarTalloCoral = QtWidgets.QLabel(self.frameBtnTalloCoral)
        self.lblPresionarTalloCoral.setGeometry(QtCore.QRect(0, 75, 301, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblPresionarTalloCoral.setFont(font)
        self.lblPresionarTalloCoral.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblPresionarTalloCoral.setStyleSheet("color: rgb(0, 0, 0);")
        self.lblPresionarTalloCoral.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPresionarTalloCoral.setObjectName("lblPresionarTalloCoral")
        self.lblImgTalloCoral = QtWidgets.QLabel(self.frameBtnTalloCoral)
        self.lblImgTalloCoral.setGeometry(QtCore.QRect(25, 20, 61, 41))
        self.lblImgTalloCoral.setStyleSheet("background-color: transparent;")
        self.lblImgTalloCoral.setText("")
        self.lblImgTalloCoral.setObjectName("lblImgTalloCoral")
        self.lblTalloCoral = QtWidgets.QLabel(self.frameBtnTalloCoral)
        self.lblTalloCoral.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblTalloCoral.setFont(font)
        self.lblTalloCoral.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblTalloCoral.setAutoFillBackground(False)
        self.lblTalloCoral.setStyleSheet("background-color: rgb(255, 207, 11);\n"
"color: rgb(0, 0, 0);\n"
"border: none;\n"
"border-radius: 10px;\n"
"padding-left: 55px;")
        self.lblTalloCoral.setAlignment(QtCore.Qt.AlignCenter)
        self.lblTalloCoral.setObjectName("lblTalloCoral")
        self.btnTalloCoral.raise_()
        self.lblPresionarTalloCoral.raise_()
        self.lblTalloCoral.raise_()
        self.lblImgTalloCoral.raise_()
        self.frameBtnMediaValvaTS = QtWidgets.QFrame(self.frame)
        self.frameBtnMediaValvaTS.setGeometry(QtCore.QRect(793, 51, 304, 108))
        self.frameBtnMediaValvaTS.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 200);\n"
"border-radius: 10px;\n"
"border: none;")
        self.frameBtnMediaValvaTS.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBtnMediaValvaTS.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBtnMediaValvaTS.setObjectName("frameBtnMediaValvaTS")
        self.btnMediaValvaTs = QtWidgets.QPushButton(self.frameBtnMediaValvaTS)
        self.btnMediaValvaTs.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnMediaValvaTs.setFont(font)
        self.btnMediaValvaTs.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    color: rgb(0, 0, 0);\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(255, 207, 11);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(255, 207, 11);\n"
"}")
        self.btnMediaValvaTs.setText("")
        self.btnMediaValvaTs.setObjectName("btnMediaValvaTs")
        self.lblPresionarMediaValvaTs = QtWidgets.QLabel(self.frameBtnMediaValvaTS)
        self.lblPresionarMediaValvaTs.setGeometry(QtCore.QRect(0, 75, 301, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblPresionarMediaValvaTs.setFont(font)
        self.lblPresionarMediaValvaTs.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblPresionarMediaValvaTs.setStyleSheet("color: rgb(0, 0, 0);")
        self.lblPresionarMediaValvaTs.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPresionarMediaValvaTs.setObjectName("lblPresionarMediaValvaTs")
        self.lblImgMediaValvaTs = QtWidgets.QLabel(self.frameBtnMediaValvaTS)
        self.lblImgMediaValvaTs.setGeometry(QtCore.QRect(25, 18, 61, 41))
        self.lblImgMediaValvaTs.setStyleSheet("background-color: transparent;")
        self.lblImgMediaValvaTs.setText("")
        self.lblImgMediaValvaTs.setObjectName("lblImgMediaValvaTs")
        self.lblMediaValvaTs = QtWidgets.QLabel(self.frameBtnMediaValvaTS)
        self.lblMediaValvaTs.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblMediaValvaTs.setFont(font)
        self.lblMediaValvaTs.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblMediaValvaTs.setAutoFillBackground(False)
        self.lblMediaValvaTs.setStyleSheet("background-color: rgb(255, 207, 11);\n"
"color: rgb(0, 0, 0);\n"
"border: none;\n"
"border-radius: 10px;\n"
"padding-left: 50px;")
        self.lblMediaValvaTs.setAlignment(QtCore.Qt.AlignCenter)
        self.lblMediaValvaTs.setObjectName("lblMediaValvaTs")
        self.btnMediaValvaTs.raise_()
        self.lblPresionarMediaValvaTs.raise_()
        self.lblMediaValvaTs.raise_()
        self.lblImgMediaValvaTs.raise_()
        self.frameBtnMediaValvaTc = QtWidgets.QFrame(self.frame)
        self.frameBtnMediaValvaTc.setGeometry(QtCore.QRect(227, 215, 304, 108))
        self.frameBtnMediaValvaTc.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 200);\n"
"border-radius: 10px;\n"
"border: none;")
        self.frameBtnMediaValvaTc.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBtnMediaValvaTc.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBtnMediaValvaTc.setObjectName("frameBtnMediaValvaTc")
        self.btnMediaValvaTc = QtWidgets.QPushButton(self.frameBtnMediaValvaTc)
        self.btnMediaValvaTc.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnMediaValvaTc.setFont(font)
        self.btnMediaValvaTc.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    color: rgb(0, 0, 0);\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(255, 207, 11);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(255, 207, 11);\n"
"}")
        self.btnMediaValvaTc.setText("")
        self.btnMediaValvaTc.setObjectName("btnMediaValvaTc")
        self.lblPresionarMediaValvaTc = QtWidgets.QLabel(self.frameBtnMediaValvaTc)
        self.lblPresionarMediaValvaTc.setGeometry(QtCore.QRect(0, 75, 301, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblPresionarMediaValvaTc.setFont(font)
        self.lblPresionarMediaValvaTc.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblPresionarMediaValvaTc.setStyleSheet("color: rgb(0, 0, 0);")
        self.lblPresionarMediaValvaTc.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPresionarMediaValvaTc.setObjectName("lblPresionarMediaValvaTc")
        self.lblImgMediaValvaTc = QtWidgets.QLabel(self.frameBtnMediaValvaTc)
        self.lblImgMediaValvaTc.setGeometry(QtCore.QRect(25, 18, 61, 41))
        self.lblImgMediaValvaTc.setStyleSheet("background-color: transparent;")
        self.lblImgMediaValvaTc.setText("")
        self.lblImgMediaValvaTc.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblImgMediaValvaTc.setObjectName("lblImgMediaValvaTc")
        self.lblMediaValvaTc = QtWidgets.QLabel(self.frameBtnMediaValvaTc)
        self.lblMediaValvaTc.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblMediaValvaTc.setFont(font)
        self.lblMediaValvaTc.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblMediaValvaTc.setAutoFillBackground(False)
        self.lblMediaValvaTc.setStyleSheet("background-color: rgb(255, 207, 11);\n"
"color: rgb(0, 0, 0);\n"
"border: none;\n"
"border-radius: 10px;\n"
"padding-left: 50px;")
        self.lblMediaValvaTc.setAlignment(QtCore.Qt.AlignCenter)
        self.lblMediaValvaTc.setObjectName("lblMediaValvaTc")
        self.btnMediaValvaTc.raise_()
        self.lblPresionarMediaValvaTc.raise_()
        self.lblMediaValvaTc.raise_()
        self.lblImgMediaValvaTc.raise_()
        self.frameBtnOtros = QtWidgets.QFrame(self.frame)
        self.frameBtnOtros.setGeometry(QtCore.QRect(641, 215, 304, 108))
        self.frameBtnOtros.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 200);\n"
"border-radius: 10px;\n"
"border: none;")
        self.frameBtnOtros.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBtnOtros.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBtnOtros.setObjectName("frameBtnOtros")
        self.btnOtros = QtWidgets.QPushButton(self.frameBtnOtros)
        self.btnOtros.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnOtros.setFont(font)
        self.btnOtros.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    color: rgb(0, 0, 0);\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(255, 207, 11);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(255, 207, 11);\n"
"}")
        self.btnOtros.setText("")
        self.btnOtros.setObjectName("btnOtros")
        self.lblPresionarOtros = QtWidgets.QLabel(self.frameBtnOtros)
        self.lblPresionarOtros.setGeometry(QtCore.QRect(0, 75, 301, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblPresionarOtros.setFont(font)
        self.lblPresionarOtros.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblPresionarOtros.setStyleSheet("color: rgb(0, 0, 0);")
        self.lblPresionarOtros.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPresionarOtros.setObjectName("lblPresionarOtros")
        self.lblImgOtros = QtWidgets.QLabel(self.frameBtnOtros)
        self.lblImgOtros.setGeometry(QtCore.QRect(60, 18, 61, 41))
        self.lblImgOtros.setStyleSheet("background-color: transparent;")
        self.lblImgOtros.setText("")
        self.lblImgOtros.setObjectName("lblImgOtros")
        self.lblOtros = QtWidgets.QLabel(self.frameBtnOtros)
        self.lblOtros.setGeometry(QtCore.QRect(2, 2, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblOtros.setFont(font)
        self.lblOtros.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblOtros.setAutoFillBackground(False)
        self.lblOtros.setStyleSheet("background-color: rgb(255, 207, 11);\n"
"color: rgb(0, 0, 0);\n"
"border: none;\n"
"border-radius: 10px;\n"
"padding-left: 30px;")
        self.lblOtros.setAlignment(QtCore.Qt.AlignCenter)
        self.lblOtros.setObjectName("lblOtros")
        self.btnOtros.raise_()
        self.lblPresionarOtros.raise_()
        self.lblOtros.raise_()
        self.lblImgOtros.raise_()
        self.frameFondoSistema = QtWidgets.QFrame(modalAlerta)
        self.frameFondoSistema.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        self.frameFondoSistema.setStyleSheet("background-color: rgba(43, 43, 43, 200);\n"
"")
        self.frameFondoSistema.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameFondoSistema.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameFondoSistema.setObjectName("frameFondoSistema")
        self.labelFondoSistema.raise_()
        self.frameFondoSistema.raise_()
        self.frame.raise_()

        self.retranslateUi(modalAlerta)
        QtCore.QMetaObject.connectSlotsByName(modalAlerta)

    def retranslateUi(self, modalAlerta):
        _translate = QtCore.QCoreApplication.translate
        modalAlerta.setWindowTitle(_translate("modalAlerta", "Alerta"))
        self.lblPresionarReestablecer.setText(_translate("modalAlerta", "PRESIONE (6)"))
        self.lblReestablecer.setText(_translate("modalAlerta", "REESTABLECER"))
        self.lblPresionarIniciarProceso.setText(_translate("modalAlerta", "PRESIONE (7)"))
        self.lblIniciarProceso.setText(_translate("modalAlerta", "INICIAR PROCESO"))
        self.lblPresionarApagar.setText(_translate("modalAlerta", "PRESIONE (0)"))
        self.lblApagar.setText(_translate("modalAlerta", "APAGAR"))
        self.lblPresionarTalloSolo.setText(_translate("modalAlerta", "PRESIONE (1)"))
        self.lblTalloSolo.setText(_translate("modalAlerta", "TALLO SOLO"))
        self.lblPresionarTalloCoral.setText(_translate("modalAlerta", "PRESIONE (2)"))
        self.lblTalloCoral.setText(_translate("modalAlerta", "TALLO CORAL"))
        self.lblPresionarMediaValvaTs.setText(_translate("modalAlerta", "PRESIONE (3)"))
        self.lblMediaValvaTs.setText(_translate("modalAlerta", "MEDIA VALVA T/S"))
        self.lblPresionarMediaValvaTc.setText(_translate("modalAlerta", "PRESIONE (4)"))
        self.lblMediaValvaTc.setText(_translate("modalAlerta", "MEDIA VALVA T/C"))
        self.lblPresionarOtros.setText(_translate("modalAlerta", "PRESIONE (5)"))
        self.lblOtros.setText(_translate("modalAlerta", "OTROS"))
