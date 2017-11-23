
# from . ColoredHelp import coloredHelp
# from . check_file  import check_file
import LnLib as Ln

#######################################################
# DEBUG options
#######################################################
def iniFileOptions(myParser, defaultIniFile):

    myParser.add_argument('-ini', '--ini-file',
                                metavar='',
                                type=Ln.check_file,
                                required=False,
                                default=defaultIniFile,
                                help=Ln.coloredHelp('Specifies ini fileName...', default=defaultIniFile))
