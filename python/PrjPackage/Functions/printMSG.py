#!/usr/bin/env python3
#

# ##########################################################################
# #
# ##########################################################################


def printHexMsg(data, prefix=''):

    if data:
        print("\n{0:<10}".format(prefix), end='' )
        print (' '.join('{:02X}'.format(c) for c in data))
        # print( )

        TextOfMsg = ' '.join('{:02X}'.format(c) for c in data[BYTE_StartOfMsg:-1])

        print("      STX           : {0:02X}".format(data[0]))
        print("      MSG_NO        : {0:02X} {1:02X}".format(data[BYTE_MsgNO_LOW], data[BYTE_MsgNO_HIGH]))
        print("      from --> to   : {0:02X} {1:02X}".format(data[BYTE_SourceADDR], data[BYTE_DestADDR]))
        print("      Messaggio     : {0}".format(TextOfMsg))
        print("      ETX           : {0:02X}".format(data[-1]))

        print()


