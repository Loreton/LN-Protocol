#!/usr/bin/python3.4
# -*- coding: iso-8859-15 -*-
#
#!/usr/bin/python -O
# -O Optimize e non scrive il __debug__
#
# ####################################################################################################################
import sys, subprocess, os

from ..LnCommon.LnLogger import SetLogger
# from ..LnCommon.LnColor  import LnColor
# from ..LnCommon.Exit     import Exit

##########################################################
# - timeout solo dalla Versione 3.3
##########################################################
def ExecGetOut(command, timeout=5, EXECUTE=True, shell=False):
    logger = SetLogger(package=__name__)


        # converto in LIST
    if isinstance(command, list):
        cmdLIST = command
    elif isinstance(command, str):
        cmdLIST = [x.strip() for x in command.split()]

    if shell:
        cmdLIST = ' '.join(cmdLIST)                      # Join command
        # rCode = os.system(cmdLIST)
        # return

    rCode   = 0
    output  = ''
    error   = ''



    logger.debug('[dry-run: {DRYRUN}] - executing command "{0}"'.format(command, DRYRUN=not EXECUTE))
    if EXECUTE:
        try:
            output = subprocess.check_output(cmdLIST, shell=shell, stderr=subprocess.STDOUT, timeout=timeout) # ritorna <class 'bytes'>

        except subprocess.CalledProcessError as why:
            error  = '{0} - {1}'.format('CalledProcessError', str(why))
            rCode = 1

        except subprocess.TimeoutExpired as why:
            error  = '{0} - {1}'.format('TimeoutExpired', str(why))
            rCode = 1

        except subprocess.TypeError as why:
            error  = '{0} - {1}'.format('TypeError', str(why))
            rCode = 1

        except (Exception) as why:
            error  = '{0} - {1}'.format('Exception', str(why))
            rCode = 1

    else:
        rCode = 0
        error = ''
        output = 'run in dry-run mode'



    logger.debug('rCode: {0}'.format(rCode))
    # print('output: {0}'.format(output))

    if rCode:
        for line in error.split('\n'):
            logger.error('   {0}'.format(line))

    elif rCode == 0 and output and EXECUTE:
        output = output.decode('utf-8')           # converti in STRing
        for line in output.split('\n'):
            logger.debug('   {0}'.format(line))

    return rCode, output, error

