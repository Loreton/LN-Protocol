#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
from .. import colorama

'''
    C = gv.Ln.Colors()
    C.printRed('loreto', tab=5)
    C.printERROR('loreto', tab=20)
'''
class LnColor:
    colorama.init(autoreset=True)
    # for i in dir('LnColors'): print (i)
    '''
        devo mantenere i valori seguenti perché a volte
        devo mandare una stringa pronta con il colore e non posso usare il printColor(msg) oppure il getColor()
        in quanto ho una stringa multicolor
        usageMsg = " {COLOR}   {TEXT} {COLRESET}[options]".format(COLOR=C.YEL, TEXE='Loreto', COLRESET=C.RESET)

    '''
    FG         = colorama.Fore
    BG         = colorama.Back
    HI         = colorama.Style

    CRITICAL   = FG.BLUE
    ERROR      = FG.RED
    WARNING    = FG.MAGENTA
    INFO       = FG.GREEN

    BLACK      = FG.BLACK
    RED        = FG.RED
    GREEN      = colorama.Fore.GREEN
    YELLOW     = FG.YELLOW
    BLUE       = FG.BLUE
    MAGENTA    = FG.MAGENTA
    # FUCSIA     = FG.MAGENTA + HI.BRIGHT
    CYAN       = FG.CYAN
    WHITE      = FG.WHITE

    REDH       = FG.RED     + HI.BRIGHT
    GREENH     = FG.GREEN   + HI.BRIGHT
    YELLOWH    = FG.YELLOW  + HI.BRIGHT
    CYANH      = FG.CYAN    + HI.BRIGHT
    MAGENTAH   = FG.MAGENTA + HI.BRIGHT
    # FUCSIAH    = FG.FUCSIA  + HI.BRIGHT

    RESET      = HI.RESET_ALL

    BW         = FG.BLACK + BG.WHITE
    BWH        = FG.BLACK + BG.WHITE + HI.BRIGHT
    YelloOnBlack        = FG.BLACK + BG.YELLOW


    callerFunc = sys._getframe(1).f_code.co_name


        # -----------------------------------------------
        # - Y E L L O W
        # -----------------------------------------------
    def yellowRev(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print (' '*tab + self.YelloOnBlack, msg, end, reset)

    def printYellow(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( ' '*tab + self.YELLOW, msg, end, reset)

    def printYellowH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( ' '*tab + self.YELLOWH, msg, end, reset)

    def getYellow(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( ' '*tab + self.YELLOW, msg, end, reset)

    def getYellowH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( ' '*tab + self.YELLOWH, msg, end, reset)




        # -----------------------------------------------
        # - G R E E N
        # -----------------------------------------------
    def printGreen(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( ' '*tab + self.GREEN, msg, end, reset)

    def printGreenH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( ' '*tab + self.GREENH, msg, end, reset)

    def getGreen(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( ' '*tab + self.GREEN, msg, end, reset)

    def getGreenH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( ' '*tab + self.GREENH, msg, end, reset)





        # -----------------------------------------------
        # - B L U E
        # -----------------------------------------------
    def printBlue(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( ' '*tab + self.BLUE, msg, end, reset)

    def getBlue(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( ' '*tab + self.BLUE, msg, end, reset)




        # -----------------------------------------------
        # - M A G E N T A
        # -----------------------------------------------
    def printMagenta(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( ' '*tab + self.MAGENTA, msg, end, reset)

    def printMagentaH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( ' '*tab + self.MAGENTAH, msg, end, reset)


    def getMagenta(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( ' '*tab + self.MAGENTA, msg, end, reset)

    def getMagentaH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( ' '*tab + self.MAGENTAH, msg, end, reset)


        # -----------------------------------------------
        # - C Y A N
        # -----------------------------------------------
    def printCyan(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( ' '*tab + self.CYAN, msg, end, reset)

    def printCyanH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( ' '*tab + self.CYANH, msg, end, reset)


    def getCyan(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( ' '*tab + self.CYAN, msg, end, reset)

    def getCyanH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( ' '*tab + self.CYANH, msg, end, reset)





        # -----------------------------------------------
        # - W H I T E
        # -----------------------------------------------
    def printWhite(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( ' '*tab + self.WHITE, msg, end, reset)

    def getWhite(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( ' '*tab + self.WHITE, msg, end, reset)





        # -----------------------------------------------
        # - R E D
        # -----------------------------------------------
    def printRed(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( ' '*tab + self.RED, msg, end, reset)

    def printRedH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        self._print ( ' '*tab + self.REDH, msg, end, reset)


    def getRed(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( ' '*tab + self.RED, msg, end, reset)

    def getRedH(self, msg, tab=0, end='\n', reset=True, string_encode='latin-1'):
        return self._print ( ' '*tab + self.REDH, msg, end, reset)









        #  aliases
    YEL         = YELLOW

    printERROR  = printRedH
    # getREDH     = printRedH
    # getYellow   = printYellow
    # getGreen    = printGreen
    # getFucsia   = printFucsia
    # getWhite    = printWhite
    # getMagenta  = printMagenta
    # getCyan     = printCyan


        # common

    def _print(self, color, msg, end, reset=True, string_encode='latin-1'):
        endColor = self.RESET if reset else ''

        outText = '{0}{1}{2}'.format(color, msg, endColor)

        callerFunc = sys._getframe(1).f_code.co_name
        # print ('....2', callerFunc)
        if callerFunc.startswith('get'):
            return outText

        else:
            try:
                print (outText, end=end )

            except (UnicodeEncodeError):
                print (color, msg.encode(string_encode), endColor, end=end )

            finally:
                return None


