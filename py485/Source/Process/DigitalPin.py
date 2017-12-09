#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Master per protocollo Ln-Rs485
#         Invia il comando sul Relay collegato sulla porta seriale
#         Il Relay ritrasmette il comando sul bus Rs485
#
# updated by ...: Loreto Notarantonio
# Version ......: 09-12-2017 18.28.22
#
# ######################################################################################


import  sys
import  time
import  LnLib as Ln; C = Ln.Color()
import  Source as Prj

# gV = Prj.gVars


def digitalRead(LnRs485, iniData, srcAddress, destAddr, pinNO):
    pass

########################################################
# - digitalToggle()
########################################################
def digitalToggle(gv, LnRs485, payload):
    assert type(payload) == bytearray
    logger  = Ln.SetLogger(package=__package__)

        # puntamento ai fieldNames
    _fld     = LnRs485._fld

        # puntamento ai comandi e sottocomandi
    _mainCmd = gv.iniFile.MAIN_COMMAND
    _subCmd  = gv.iniFile.SUB_COMMAND


    C.printColored (color=C.yellowH, text='... press ctrl-c to stop the process.', tab=8)


        # ===================================================
        # = RS-485 preparazione del comando
        # ===================================================
    payload[_fld.DEST_ADDR]                      = int(gv.args.slave_address)
    payload[_fld.CMD]                            = int(_mainCmd.DIGITAL_CMD, 16)     # COMMAND
    payload[_fld.SUB_CMD]                        = int(_subCmd.TOGGLE_PIN,   16)     # SubCOMMAND
    payload[_fld.SEQNO_H], payload[_fld.SEQNO_L] = LnRs485.getSeqCounter()
    payload[_fld.RCODE]                          = 0 # 0 per la TX
    payload[_fld.PIN_NO]                         = gv.args.pin_number     # pinNO




    # xx.printTree(header='invio dati allo slave: {}'.format(payload[LnRs485._fld.DEST_ADDR]))
    # print ('\n'*2)

    # tohex = lambda data: ' '.join('{0:02x}'.format(x) for x in data)


    while True:
        try:

            # xx = LnRs485.PayloadToDict(payload)
            dataSent = LnRs485._rs485Write(payload, fDEBUG=True)
            tohex = ' '.join('{0:02x}'.format(x) for x in dataSent)
            print ('dataSent: {}'.format(tohex))

            time.sleep(2)
            rawData = LnRs485._serialRead(timeoutValue=2000) # return bytearray
            tohex = ' '.join('{0:02x}'.format(x) for x in rawData)
            print ('echo    : {}'.format(tohex))
            if rawData == dataSent:
                print ('data has been received...')
            # if rawData:
            #     print (rawData)
                # fullData = LnRs485.VerifyRs485Data(rawData)
                # payload = fullData.payload
                # raw     = fullData.raw
                # if payload.data:
                #     # print (payload.data)
                #     print (payload.hexd)
                #     # print (payload.hexm)
                #     # print (payload.char)
                #     # print (payload.text)
                #     xx = LnRs485.PayloadToDict(payload.data)
                #     xx.printTree(header='ricezione dati dallo slave: {}'.format(payload.data[LnRs485._fld.SRC_ADDR]))
                #     print ('\n'*2)
                # break




        except (KeyboardInterrupt) as key:
            print (__name__, "Keybord interrupt has been pressed")
            LnRs485.Close()
            sys.exit()