#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# updated by Loreto: 23-10-2017 17.51.47
# -----------------------------------------------


import LnLib as Ln
C=Ln.Color()

################################################
# formatting help message
################################################
def coloredHelp(text, default=None, required=False):
    mandatory = C.getColored(color=C.yellowH, text='MANDATORY') if required else C.getColored(color=C.green, text='OPTIONAL')

    if not text:
        myHelp = ''
    else:
        myHelp   = '''{MANDATORY} - {TEXT}
        [DEFAULT: {DEFAULT}]
            '''.format(MANDATORY=mandatory, TEXT=C.getColored(color=C.yellow, text=text), DEFAULT=default)


    return myHelp