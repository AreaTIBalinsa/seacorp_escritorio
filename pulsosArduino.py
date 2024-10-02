import InicioSistema
from datetime import time

def fn_registroCorrecto():
    if InicioSistema.workerAR.serialArduino and InicioSistema.workerAR.serialArduino.is_open:
        InicioSistema.workerAR.serialArduino.write(str("ac").encode('utf8'))
        time.sleep(0.5)
        InicioSistema.workerAR.serialArduino.write(str("df").encode('utf8'))
        
def fn_registroExcesoPeso():
    if InicioSistema.workerAR.serialArduino and InicioSistema.workerAR.serialArduino.is_open:
        InicioSistema.workerAR.serialArduino.write(str("bc").encode('utf8'))
        time.sleep(0.5)
        InicioSistema.workerAR.serialArduino.write(str("ef").encode('utf8'))
        time.sleep(0.5)
        InicioSistema.workerAR.serialArduino.write(str("ac").encode('utf8'))
        time.sleep(0.5)
        InicioSistema.workerAR.serialArduino.write(str("df").encode('utf8'))
        
def fn_apagarIndicador():
    if InicioSistema.workerAR.serialArduino and InicioSistema.workerAR.serialArduino.is_open:
        InicioSistema.workerAR.serialArduino.write(str("y").encode('utf8'))
        time.sleep(1)
        InicioSistema.workerAR.serialArduino.write(str("z").encode('utf8'))