import InicioSistema

def fn_encenderPulsoVerde():
    if InicioSistema.workerAR.serialArduino and InicioSistema.workerAR.serialArduino.is_open:
        InicioSistema.workerAR.serialArduino.write(str("a").encode('utf8'))