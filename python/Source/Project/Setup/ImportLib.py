#!/opt/python3.4/bin/python3.4

#!/usr/bin/python3.4

# sudo update-alternatives --config python
# /opt/python3.4/bin/pip3.4 install netifaces

import sys
import os



import importlib # per importare un modulo come variabile
################################################################################
# - importLnLib()
# - cerchiamo la libName prima come directory e poi come zipFile
################################################################################
def ImportLib(libName, fDEBUG=False):
    mainFile = os.path.abspath(sys.argv[0])
    if fDEBUG:
        print('')
        print('mainFile...: {0}'.format(mainFile))
        print('')

    filename, extension     = os.path.splitext(os.path.basename(mainFile))
    SourceDir               = os.path.abspath(os.path.dirname(mainFile))
    ProjectDir              = os.path.dirname(SourceDir)
    binDir                  = os.path.join(ProjectDir, 'bin')
    zipFile                 = '{0}.zip'.format(libName)



        # --------------------------------------------------------------
        # aggiungiamo le nostre path
        # visto l'odine di inserimento delle path dovremmo trovare
        # prima la directory e poi lo zip
        # --------------------------------------------------------------
    if not ProjectDir in sys.path: sys.path.append(ProjectDir)
    if not binDir     in sys.path: sys.path.append(binDir)

    for path in sys.path:
        zipFullName = os.path.abspath(os.path.join(path, zipFile))
        if os.path.isfile(zipFullName):
            if not zipFullName in sys.path:
                sys.path.append(zipFullName)


    if fDEBUG:
        for path in sys.path:
            print ('{0:<90}'.format(path), end='')
            zipFullName = os.path.abspath(os.path.join(path, zipFile))
            if os.path.isdir(os.path.join(path, 'LnLib')):
                print('    - {0} directory'.format(libName) )
            elif os.path.isfile(zipFullName):
                print('    - {0} FOUND'.format(zipFile) )
            else:
                print()
                # print('    - NOT FOUND')


    # Ln = importlib.import_module(libName)

    try:
        Ln = importlib.import_module(libName)
    except ImportError as why:
        sys.stderr.write("\n")
        sys.stderr.write("      ERROR loading python module: " + libName + "\n")
        sys.stderr.write("      REASON: " + str(why) + "\n")
        sys.exit(1)
    # import LnLib  as Ln
    return Ln

