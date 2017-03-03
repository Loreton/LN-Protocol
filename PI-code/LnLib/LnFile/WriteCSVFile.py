#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per ...........
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

# unicode tips https://www.safaribooksonline.com/library/view/fluent-python/9781491946237/ch04.html

# import os, sys

from ..LnCommon.LnLogger import SetLogger


##############################################################
# - data deve essere una LIST di LIST
# - Se è una list allora scrive le righe così come sono
##############################################################
def WriteCSVFile(csvFile, data=[], dquote=True, sepChar=';', encoding='utf-8', newline = '\n'):
    logger = SetLogger(package=__name__)
    logger.debug('writing file:             {0}'.format(csvFile))
    logger.debug('number of lines to write: {0}'.format(len(data)))

        # -----------------------------------------------------------------------
        # - Per ogni canzone prendiamo gli attributi e salviamola.
        # -----------------------------------------------------------------------

    nLines = 0
    f = open(csvFile, "w", encoding=encoding, newline=newline)
    for line in data:
        if isinstance(line, list):
            # converte all items to string perché...
            # ...potrebbe dare errore se qualche item non è stringa
            if dquote:
                lineStr = ['"' + str(item) + '"' for item in line]
            else:
                lineStr = [str(item) for item in line]

            f.write('{0}{1}'.format(sepChar.join(lineStr), newline))
        else:
            f.write('{0}{1}'.format(line, newline))

        nLines += 1

    f.close()
    return nLines