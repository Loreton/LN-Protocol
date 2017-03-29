#!/usr/bin/python3.4

# sudo update-alternatives --config python


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
    mainDir                 = os.path.abspath(os.path.dirname(mainFile))

    # ---------------------------------------------------------------------
    # - cerchiamo di individuare la maindir come la directory di base
    # - della seguente struttura:
    # -       mainDir/bin
    # -       mainDir/Source
    # -       mainDir/Conf
    # ---------------------------------------------------------------------
        # dir che devo esistere per cercare la mainDir
    keyDirs = ['bin', 'conf', 'Conf', 'Sourcex']
        # nome dello zipFile della LnLib
    zipFile     = '{0}.zip'.format(libName)
    zipFullName = None

    LOOP = True
    while LOOP:
        if len(mainDir.split(os.sep)) < 2:
            LOOP = False

        if fDEBUG:print('trying mainDir:    ', mainDir)

            # - cerchiamo la zipLnLib
        zipLib = os.path.join(mainDir, zipFile)
        if os.path.isfile(zipLib):
            if fDEBUG:print('FOUND zipLnLib:    ', zipFullName)
            zipFullName = zipLib

            # - trovata mainDir se una delle keyDir esiste
        for keydir in keyDirs:
            if os.path.isdir(os.path.join(mainDir, keydir)):
                if fDEBUG:print('FOUND mainDir:    ', mainDir)
                LOOP = False
                break

            # - se non l'abbiamo trovata saliamo di un livello
        if LOOP:
            mainDir = os.path.dirname(mainDir)

    binDir      = os.path.join(mainDir, 'bin')
    SourceDir   = os.path.join(mainDir, 'Source')


        # --------------------------------------------------------------
        # aggiungiamo le nostre path
        # visto l'odine di inserimento delle path dovremmo trovare
        # prima la directory e poi lo zip
        # --------------------------------------------------------------
    if not binDir    in sys.path: sys.path.append(binDir)
    if not SourceDir in sys.path: sys.path.append(SourceDir)
    if not mainDir   in sys.path: sys.path.append(mainDir)

    for path in sys.path:
        zipFullName = os.path.abspath(os.path.join(path, zipFile))
        if os.path.isfile(zipFullName):
            if not zipFullName in sys.path:
                sys.path.append(zipFullName)



    if fDEBUG:
        print('mainDir      ', mainDir)
        print('SourceDir    ',SourceDir)
        print('binDir       ',binDir)
        print('zipFile      ',zipFullName)
        print ()
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

