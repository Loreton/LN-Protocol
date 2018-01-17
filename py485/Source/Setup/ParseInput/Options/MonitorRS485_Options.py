#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 17-01-2018 15.04.03
#
import    Source as Prj

#######################################################
# monitorRs485
#######################################################
def monitorRs485(myParser):
    commonRs485(myParser)
    # no optional flags

def monitorRaw(myParser):
    # ----- common part into the Prj modules --------
    # import    Source as Prj
    Ln     = Prj.LnLib
    # C      = Ln.Color()
    # logger = Ln.SetLogger(__package__)
    # -----

    myGroup = myParser.add_mutually_exclusive_group(required=True)  # True indica obbligatorietà di almeno uno del gruppo

    myGroup.add_argument( "--text",
                                # required=True,
                                action='store_true',
                                help=Ln.coloredHelp("display text format.", required=False))
    myGroup.add_argument( "--hex",
                                # required=False,
                                action='store_true',
                                help=Ln.coloredHelp("display HEX format.", required=False))
    myGroup.add_argument( "--char",
                                # required=False,
                                action='store_true',
                                help=Ln.coloredHelp("display CHAR format.", required=False))

    commonRs485(myParser)


def commonRs485(myParser):
    # ----- common part into the Prj modules --------
    # import    Source as Prj
    Ln     = Prj.LnLib
    # C      = Ln.Color()
    # logger = Ln.SetLogger(__package__)
    # -----
    myParser.add_argument('-p', '--port',
                                metavar='',
                                type=str,
                                required=True,
                                default=None,
                                help=Ln.coloredHelp('usb port to be monitored...', default=None, required=True))