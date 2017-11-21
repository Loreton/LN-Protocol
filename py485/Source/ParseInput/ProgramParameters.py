#!/usr/bin/python3.5
#
# Scope:  Programma per ...........
# LnVer_2017-11-05_18.26.32
# -----------------------------------------------
from . Common.MyHelp                import myHELP
from . Common.check_file            import check_file

#######################################################
# PROGRAM options
#######################################################
def programParameters(myParser, gVar, required=False):
    # mandatory = cPrint.getMagentaH('is MANDATORY - ') if required else cPrint.getCyanH('is OPTIONAL - ')
    myParser.add_argument('---------------program-options ----',
                                required=False,
                                action='store_true',
                                help=myHELP('', None))


    myParser.add_argument('--config-file',
                                metavar='',
                                type=check_file,
                                required=False,
                                default=gVar.defaultConfigFile,
                                help=myHELP('Specifies config fileName...', default=gVar.defaultConfigFile))

