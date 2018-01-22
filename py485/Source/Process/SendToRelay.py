#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 22-01-2018 16.15.20
#
# ######################################################################################


import    Source as Prj


########################################################
# - SendToRelay()
########################################################
def SendToRelay(myPort, payload):
    global logger, serialPort
    assert type(payload) == bytearray
    serialPort = myPort
    Ln     = Prj.LnLib
    logger  = Ln.SetLogger(package=__package__)



        # ---------------------------------------------------------------------
        # - invio del messaggio al Relay ed attesa dello stesso come echo
        # - Se non lo riceviamo vuol diche che c'è un problema
        # ---------------------------------------------------------------------
    LOOP = 10
    while LOOP:
        # logger.info('waiting for idle state')
        # _waitForIdleState()
        try:
                # - invio messaggio (torna il dict dei dati nella seriale232)
            xmittedData = serialPort.write485(payload)
            logger.info('xmittedData: {}'.format(xmittedData))
            print('xmittedData: {}'.format(xmittedData))
            Prj.monitorRaw(serialPort, MAX_LOOP=3, dHex=True, dText=True, dChar=False)
            LOOP -= 1
            Ln.KeyboardInput('pausing...', validKeys='ENTER', exitKey='X')

            '''

                # - attesa echo
            rcvdData    = serialPort.read232(timeoutValue=4000) # return dict.raw dict.hexd dict.hexm dict.text dict.char
            logger.info('rcvdData   : {}'.format(rcvdData))
            print('rcvdData   : {}'.format(rcvdData))
            if  rcvdData == xmittedData:

            # data232 = serialPort.fmtData(data, Ln.Dict)
            # if  data232.raw == xmittedData.raw:
                print ('    echo has been received from Arduino Relay...')
                break
            else:
                LOOP -= 1
            '''


        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            serialPort.Close()
            Ln.Exit(0)



    if LOOP < 1:
        Ln.Exit(1, "    Il relay non risponde...")

    logger = Ln.SetLogger(__name__, exiting=True)


def _waitForIdleState():
    '''
    Relay device send a dummy record with RCODE==LN_WAITING_FOR_CMD==6
    to indicate that it's in idle state.
    '''

    while True:
        try:
                # read serial data
            dict232, dict485 = serialPort.read485(timeoutValue=2000)
                # - ricevuto il messaggio di waiting for command da parte del Relay
            if dict485.raw and dict485.fld.f05_RCODE==6:
                logger.info(dict485.fld, dictTitle='RS485 received data')
                if dict485.fld.f05_RCODE == 6:
                    print('Idle message received from...: ', dict485.fld.f01_sourceAddr)
                continue

        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            serialPort.Close()
            Ln.Exit(9999)

    Ln.Exit(9999)



def _monitorDebug():

    while True:
        try:
            dict232, dict485 = serialPort.read485(timeoutValue=5000)
                # - ricevuto il messaggio di waiting for command da parte del Relay
            if dict485.raw:
                logger.info(dict485.fld, dictTitle='RS485 received data')

                if dict485.fld.f05_RCODE == 6:
                    print('Idle message received from...: ', dict485.fld.f01_sourceAddr)
                else:
                    dict485.printTree(fPAUSE=True)

            else:
                print('nothing received...')
            return


        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            sys.exit()
