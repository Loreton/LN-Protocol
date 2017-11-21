
from . MyHelp import myHELP


#######################################################
# DEBUG options
#######################################################
def debugParameters(myParser, required=False):
    myParser.add_argument('---------------debug-options ----',
                                required=False,
                                action='store_true',
                                help=myHELP('', None))


    myParser.add_argument('--execute',
                                required=False,
                                action='store_true',
                                help=myHELP('Specifies if program must be started', default=False))

    myParser.add_argument('--debug',
                                required=False,
                                action='store_true',
                                help=myHELP('Specifies if program must be started', default=False))

    myParser.add_argument('--parameters',
                                required=False,
                                action='store_true',
                                help=myHELP('Display input paramenters..', default=False))


