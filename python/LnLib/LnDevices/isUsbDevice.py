#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               &  Loreto Notarantonio 2015, October
# ######################################################################################

import pyudev           # sudo pip3.4 install pyudev

# ##########################################################################
# # setupRS485(usbDevice)
# ##########################################################################
def isUsbDevice(usbDevName):
    usbDevPath = None

    if usbDevName:
        usbDevName = usbDevName.split('/')[-1]   # nel caso fosse stato passato anche il path lo togliamo
        context = pyudev.Context()


        try:
            usbDevPath = '/dev/' + usbDevName
            isVaildDevice = pyudev.Device.from_device_file(context, usbDevPath) == (pyudev.Device.from_name(context, 'tty', usbDevName))
        except:
            isVaildDevice = False
            usbDevPath = None
            # print('{0} - is not a valid USB device'.format(usbDevPath))
            # sys.exit()

        # print (isVaildDevice)
    return usbDevPath

