#!/usr/bin/env python3
#


# ##########################################################################
# # RS485_sendMSG()
# ##########################################################################
def RS485_sendMSG(gv, slaveADDR):
    data = bytearray()
    data.append(slaveADDR)   # Address
    data.append(0x11)
    data.append(0x12)
    data = Master.writeData(data, fDEBUG=True)
    return


