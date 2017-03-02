#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               &  Loreto Notarantonio 2014, July
# ######################################################################################
def testVirtualWire():
    import time
    import pigpio
    import vw

    # RX=11
    # TX=25
    RX=19        # GPIO19 - pin 35
    TX=26        # GPIO26 - pin 37

    BPS=2000

    pi = pigpio.pi() # Connect to local Pi.

    rx = vw.rx(pi, RX, BPS) # Specify Pi, rx gpio, and baud.
    tx = vw.tx(pi, TX, BPS) # Specify Pi, tx gpio, and baud.

    msg = 0

    start = time.time()


    while (time.time()-start) < 300:

      msg += 1

      while not tx.ready():
         time.sleep(0.1)

      time.sleep(0.2)
      tx.put([48, 49, 65, ((msg>>6)&0x3F)+32, (msg&0x3F)+32])

      while not tx.ready():
         time.sleep(0.1)

      time.sleep(0.2)

      tx.put("Hello World #{}!".format(msg))
      '''
      '''

      while rx.ready():
         # print("".join(chr (c) for c in rx.get()))
         for c in rx.get():
            # print("{0:02X}".format(c)),          # python2
            print("{0:02X} ".format(c), end='')    # python3

         print()

    rx.cancel()
    tx.cancel()

    pi.stop()


