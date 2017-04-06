#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               &  Loreto Notarantonio 2015, October
# ######################################################################################

import pyudev           # sudo pip3.4 --proxy=localhost:60080 install pyudev
import os, sys
# ##########################################################################
# # setupRS485(usbDevice)
# ##########################################################################
def isUsbDevice(usbDevName):
    usbDevPath = None



    if usbDevName:
        usbDevName = usbDevName.split('/')[-1]   # nel caso fosse stato passato anche il path lo togliamo
        usbDevPath = '/dev/' + usbDevName
        # print (usbDevPath)
        if os.path.islink(usbDevPath):
            usbDevName = os.readlink(usbDevPath)  # ritorna solo il nome
            print (usbDevPath, 'is link -->', usbDevName)
        usbDevPath = '/dev/' + usbDevName
        # print (usbDevPath)

        context = pyudev.Context()

        try:
            isVaildDevice = pyudev.Device.from_device_file(context, usbDevPath) == (pyudev.Device.from_name(context, 'tty', usbDevName))
        except:
            isVaildDevice = False
            usbDevPath = None
            # print('{0} - is not a valid USB device'.format(usbDevPath))
            # sys.exit()

        # print (isVaildDevice)
    # sys.exit()
    return usbDevPath

