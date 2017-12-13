#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 13-12-2017 16.29.40
#
# ######################################################################################
import  sys
import  collections
import  inspect, os
from    pathlib import WindowsPath, PosixPath
from    LnLib.Common.LnColor  import LnColor; C=LnColor()

class myPrint():
    def __init__(self):
        self._lastLine = ''
        self._myList = []

    def add(self, color='', tab=0, text='', end='\n'):
        thisTAB = ' '*tab
        if color:
            endColor = C.RESET
        else:
            endColor = ''

        outText = '{0}{1}{2}{3}'.format(thisTAB, color, text, endColor)

        if end == '\n':
            self._myList.append(self._lastLine + outText)
            self._lastLine = ''
        else:
            self._lastLine += outText

    def get(self):
        return self._myList

    @property
    def Print(self):
        for line in self._myList:
            print (line)


# #######################################################
# #  ''' RECURSIVE '''
# # Ritorna una lista che contiene
# # l'alberatura delle key di un dictionary
# #    [level - keyName ]
# #######################################################
def PrintDictionary(myDict, myDictTYPES=[], level=0, whatPrint='LTKV', fPRINT=False, fEXIT=False, fPAUSE=False, maxDepth=10, header=None, stackLevel=2):
    global myPRINT
    if level == 0:
        myPRINT = myPrint()
        PrintHeader('START - ', header, stackLevel=stackLevel+1)

    if level > maxDepth:
        print('MAXLevel reached.....')
        return

    # per evitare LOOP
    if level > 100:
        print('MAXLevel 100 reached.....')
        sys.exit()

    myTAB=' '*4*level   # Indent del dictionary
    for key, val in sorted(myDict.items()):                  # per tutte le chiavi del dict

            # - Se è un DICT iteriamo
        if type(val) in myDictTYPES:
            thisTYPE = str(type(val)).split("'")[1]
            if "DotMap" in thisTYPE:
                thisTYPE = 'LnDict'
            elif "OrderedDict" in thisTYPE:
                thisTYPE = 'oDict'
            else:
                thisTYPE = thisTYPE[-6:]

            line0 = ''
            if 'L' in whatPrint: line0 = '[{LVL:2}]'.format(LVL=level)
            if 'T' in whatPrint: line0 = '{LINE0} {TYPE:<8}'.format(LINE0=line0, TYPE=thisTYPE)
            if 'K' in whatPrint: line0 = '{LINE0} {TAB}{KEY}'.format(LINE0=line0, TAB=myTAB, KEY=key)
            myPRINT.add(color=C.cyanH, text=line0, tab=4)

            # ---- recursive iteration
            PrintDictionary(val, myDictTYPES=myDictTYPES, level=level+1, whatPrint=whatPrint, fPRINT=fPRINT, maxDepth=maxDepth)    # in questo caso il return value non mi interessa

        else:
            getDictValue(key, val, level, myDictTYPES, whatPrint=whatPrint, fPRINT=True)



    if level == 0:
        if fEXIT:
            PrintHeader('END - ', header, stackLevel=stackLevel+1)
            myPRINT.Print
            sys.exit()


        elif fPAUSE:
            PrintHeader('END - ', header, stackLevel=stackLevel+1)
            myPRINT.Print
            print()
            exitKeyLIST = ["x", "q"]
            msg = "...press: [{0}] to continue - {1} to exit ==> ".format("ENTER", exitKeyLIST)
            while True:
                choice = input(msg).strip()
                if choice == '':    # diamo priorità alla exit
                    break

                elif choice.lower() in exitKeyLIST:
                    sys.exit()

                else:
                    C.printColored(color=C.cyan, text='\n... try again\n')

            return

        else:
            myPRINT.Print
            return

        myPRINT.Print
    else:
        print()
        return


# #######################################################
# #
# #######################################################
def PrintHeader(prefix, header, stackLevel=3):
    try:
        caller = inspect.stack()[stackLevel]
        dummy, fileName, funcLineNO, funcName, lineCode, rest = caller

        # --------------------------------------------------------------
        # da errore quando racchiudo il file all'interno di uno ZIP - NON so il perche
        #   stat = os.stat(fullname)
        #   NotADirectoryError: [Errno 20] Not a directory: '/home/pi/GIT-REPO/LnProtocol/py485/bin/LnLib_20171123.zip/LnLib/Dict/PrintDictionaryTree.py'
        # --------------------------------------------------------------

    except:
        fileName    = sys._getFrame(stackLevel).f_code.co_filename
        funcLineNO  = sys._getFrame(stackLevel).f_lineno
        funcName    = sys._getFrame(stackLevel).f_code.co_name
        lineCode    = ['']

    finally:
        fName       = os.path.basename( fileName.split('.')[0])
        if funcName == '<module>': funcName = '__main__'
        caller = "Called by: [{FNAME}.{FUNC}:{LINEO}]".format(FNAME=fName, FUNC=funcName, LINEO=funcLineNO)
        caller2 = "by: [{FNAME}.{FUNC}:{LINEO}]".format(FNAME=fName, FUNC=funcName, LINEO=funcLineNO)


        # -------------------------------------------------------
        # - Cerchiamo di catturare il dictionary richiamato
        # - da verificare con attenzione
        # -------------------------------------------------------
    if not header:
        if '.printTree' in lineCode[0]:
            dictionaryName = (lineCode[0].split('.printTree')[0].split()[-1])
            header = "dictionary: {0}".format(dictionaryName)

        elif '.printDict' in lineCode[0]:
            dictionaryName = (lineCode[0].split('.printDict')[0].split()[-1])
            header = "dictionary: {0}".format(dictionaryName)

        else:
            header = "lineCode: {0}...".format(lineCode[0].strip()[:40])


    # print()
    myPRINT.add(color=C.cyan, text="*"*60, tab=8)

    myPRINT.add(color=C.cyan, text="*     {0}{1}".format(prefix, caller), tab=8)

    if header:
        myPRINT.add(color=C.cyan, text="*     {0}".format(header), tab=8)

    myPRINT.add(color=C.cyan, text="*"*60, tab=8)




# #######################################################
# # Stampa i soli valori contenuti in un ramo, indicato
# #  da dotQualifers, partendo dal dict myDictRoot
# #######################################################
def getDictValue(key, value, level, myDictTYPES, whatPrint='LT', fPRINT=True):

    # level = 0
    myTAB=' '*4*level

        # - dict forzato nell'ordine di immissione
    retValue  = collections.OrderedDict()
    if isinstance(value, (WindowsPath)):
        valueTYPE = 'WinPath'
        value = str(value)
    elif isinstance(value, (PosixPath)):
        valueTYPE = 'PosixPath'
        value = str(value)
    else:
        valueTYPE = str(type(value)).split("'")[1]


    listOfValue = []

    # ------------------------------
    # - valutazione del valore
    # ------------------------------
    if valueTYPE == 'str':
        s = value
        if s.find('\n') >= 0:
            listOfValue.extend(s.split('\n'))
        elif s.find(';') >= 0:
            listOfValue.extend(s.split(';'))
        else:
            STEP = 60
            while s:
                listOfValue.append(s[:STEP])
                s = s[STEP:]

    elif valueTYPE == 'list':
        listOfValue.append('[')
        """
            quanto segue NON va sempre bene in quanto potrebbe esserci una lista di liste...
            x = ['  ' + item for item in value]
            listOfValue.extend(x)
        """
            # indentiamo leggermete i valori
        for item in value:
            listOfValue.append(C.printColored(color=C.magenta, text=('   {0}'.format(item))))

        listOfValue.append(']')


    else:
        listOfValue.append(value)


    # =========================================
    # = P R I N T
    # =========================================
        # - print della riga con la key a lunghezza fissa baseStartValue
    baseStartValue = 52
    # line0 = '[{LVL:2}] {TYPE:<8} {TAB}{KEY}'.format(LVL=level, TAB=myTAB*level, TYPE=valueTYPE, KEY=key)
    line0 = ''
    if 'L' in whatPrint: line0 = '[{LVL:2}]'.format(LVL=level)
    if 'T' in whatPrint: line0 = '{LINE0} {TYPE:<10}'.format(LINE0=line0, TYPE=valueTYPE[:10])
    if 'K' in whatPrint: line0 = '{LINE0} {TAB}{KEY}'.format(LINE0=line0, TAB=myTAB, KEY=key)

    line0 = line0.ljust(baseStartValue)
    if not 'V' in whatPrint:
        myPRINT.add(color=C.cyan, text=line0, tab=4)
        return


    myPRINT.add(color=C.cyan, text=line0, tab=4, end='')
    myLISTline = '{}{}'.format(' '*4, line0)

    myPRINT.add(color=C.greenH, text=': ', end='')
    myLISTline += ': '


        # - print del valore della prima entry della lista
    if len(listOfValue) == 0:
        line  = ''
        myPRINT.add(color=C.greenH, text=line)

    else:
        line  = '{VAL}'.format(VAL=listOfValue[0])
        myPRINT.add(color=C.greenH, text=line)


            # - print delle altre righe se presenti
        for line in listOfValue[1:]:
            line  = '{LINE:<{LUN}}  {VAL}'.format(LINE=' ', LUN=baseStartValue, VAL=line)
            myPRINT.add(color=C.greenH, text=line, tab=4)
        else:
            retValue[key] = value




if __name__ == '__main__':

    example_dict = { 'key1' : 'value1',
                     'key2' : 'value2',
                     'key3' : { 'key3a': 'value3a' },
                     'key4' : {
                                'key4b': 'value4b',

                                'key4a':    {
                                                'key4aa': 'value4aa',
                                                'key4ab': 'value4ab',
                                                'key4ac': 'value4ac'
                                            },

                                'key4c' :   {
                                                'key4ca': 'value4ca'
                                            },
                            }
                    }


