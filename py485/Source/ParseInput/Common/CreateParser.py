
from . MyHelp import myHELP
import LnLib as Ln; C=Ln.Color()
import argparse
# ----------------------------------------------
# - creazione del parser
# ----------------------------------------------
def createParser(passedData):
    myParser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,     # indicates that description and epilog are already correctly formatted and should not be line-wrapped:
        description=C.getColored(color=C.yellow, text="{} commands".format(passedData.description)),
        usage='',                                          # non voglio lo usage
        epilog=C.getColored(color=C.yellow, text="default help"),
        conflict_handler='resolve',
    )


    myParser.add_argument('--version',
            action='version',
            version='{PROG}  Version: {VER}'.format (PROG=passedData.prjName, VER=passedData.programVersion ),
            help=myHELP("show program's version number and exit") )

    return myParser