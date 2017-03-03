#!/usr/bin/env python3
#

# ##########################################################################
# # VW_getMSG()
# # se attivato subi dopo un invio, rilegge il messaggio inviato da se stesso.
# ##########################################################################
def checkMsgValidity(gv, data):

    gv.rcvedMSG.STX         = data[BYTE_STX]
    gv.rcvedMSG.msgNO       = data[BYTE_MsgNO_HIGH:BYTE_MsgNO_LOW]
    gv.rcvedMSG.destAddr    = data[BYTE_DestADDR]
    gv.rcvedMSG.srcAddr     = data[BYTE_SourceADDR]
    gv.rcvedMSG.data        = data[BYTE_StartOfMsg:-1]
    gv.rcvedMSG.ETX         = data[-1]

    if gv.rcvedMSG.STX !=  gv.prot.STX:
        print('Il byte di STX non è valido {0:02X} '.format(data[0]))
        data = ''

    elif gv.rcvedMSG.ETX !=  gv.prot.ETX:
        print('Il byte di ETX non è valido {0:02X} '.format(data[-1]))
        data = ''

    elif gv.rcvedMSG.srcAddr ==  gv.prot.MASTER_ADDRESS:
        print('ECHO received - Ricevuto messaggio inviato da me stesso.')
        data = ''

    elif gv.rcvedMSG.destAddr !=  gv.prot.MASTER_ADDRESS:
        print('Destination Address is not Master Address {0:02X} '.format(gv.rcvedMSG.destAddr))
        data = ''

    else:
        pass
        # fullMSG     = ' '.join('{:02X}'.format(c) for c in data)
        # TextOfMsg   = ' '.join('{:02X}'.format(c) for c in data[MSG_START:-1])

    return data