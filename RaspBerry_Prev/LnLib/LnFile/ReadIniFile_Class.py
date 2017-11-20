#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import os

import collections
import configparser
import codecs

from ..LnCommon.LnLogger import SetLogger
from ..LnCommon.LnColor  import LnColor

class ReadIniFile(object):
    """docstring for ClassName"""
    def __init__(self, fileName, RAW=False, returnOrderedDict=False, extraSections=[], exitOnError=False, strict=True, subSectionChar=None):
        self._filename                = fileName
        self._delimiters              = ('=', ':')
        self._comment_prefixes        = ('#',';')
        self._inline_comment_prefixes = (';',)
        self._strict                  = strict # True: impone unique key/session
        self._empty_lines_in_values   = True
        self._default_section         = 'DEFAULT'
        self._interpolation           = configparser.ExtendedInterpolation()
        self._RAW                     = RAW
        self._returnOrderedDict       = returnOrderedDict
        self._extraSections           = extraSections
        self._subSectionChar          = subSectionChar
        self._allow_no_value          = False

        self._SetParser()



    def _SetParser(self):
            # Setting del parser
        self._configMain = configparser.ConfigParser(
                allow_no_value          = self._allow_no_value,
                delimiters              = self._delimiters,
                comment_prefixes        = self._comment_prefixes,
                inline_comment_prefixes = self._inline_comment_prefixes,
                strict                  = self._strict,
                empty_lines_in_values   = self._empty_lines_in_values,
                default_section         = self._default_section,
                interpolation           = self._interpolation
        )
        self._configMain.optionxform = str        # mantiene il case nei nomi delle section e delle Keys (Assicurarsi che i riferimenti a vars interne siano case-sensitive)


    def Delimiters(self, delimiters):
        self._delimiters = delimiters
        self._SetParser()

    def CommentPrefix(self, comment_prefixes):
        self._comment_prefixes = comment_prefixes
        self._SetParser()



    # ######################################################
    # # https://docs.python.org/3/library/configparser.html
    # ######################################################
    def read(self, onlySection=None, returnOrderedDict=False, extraSections=[]):
        logger  = SetLogger(package=__name__)
        self._returnOrderedDict = returnOrderedDict
        self._extraSections = extraSections
        self._onlySection = onlySection

        configMain = self._configMain

        try:
            data = codecs.open(self._filename, "r", "utf8")
            self._configMain.readfp(data)

        except (Exception) as why:
            print("Errore nella lettura del file: {FILE} - {WHY}".format(FILE=self._filename, WHY=str(why)))
            sys.exit(-1)

            # ------------------------------------------------------------------
            # - per tutte le sezioni che sono extra facciamo il merge.
            # - Se Key-Val esistono esse sono rimpiazzate
            # ------------------------------------------------------------------
        for sectionName in extraSections:
            logger.info('adding Section: {SECTION}'.format(SECTION=sectionName))
            logger.info('          data: {EXTRA}'.format(EXTRA=extraSections[sectionName]))
            extraSection = extraSections[sectionName]

            if not self._configMain.has_section(sectionName):
                logger.debug('creating Section: {0}'.format(sectionName))
                self._configMain.add_section(sectionName)

            for key, val in extraSection.items():
                logger.debug('adding on Section {0}:'.format(sectionName))
                logger.debug('   key: {0}'.format(key))
                logger.debug('   val: {0}'.format(val))
                self._configMain.set(sectionName, key, val)



            # Parsing del file
        if type(self._configMain) in [configparser.ConfigParser]:
            self.dict = self._iniConfigAsDict()
        else:
            self.dict = self._configMain



    ############################################################
    # subSectionChar:  carattere da individuare nel nome della section per
    #                  interpretare la stessa come section+subsection
    ############################################################
    def _iniConfigAsDict(self):
        """
        Converts a ConfigParser object into a dictionary.

        The resulting dictionary has sections as keys which point to a dict of the
        sections options as key => value pairs.
        """

        the_dict = collections.OrderedDict({}) if self._returnOrderedDict else {}
        fDEBUG = False
        try:
            for section in self._configMain.sections():
                # -----------------------------------------------------------------------
                # - questo blocco serve per splittare eventauli section in cui il nome
                # - contiene un separatore (es. '.') ed interpretarli come subSections
                # -----------------------------------------------------------------------
                if self._subSectionChar:
                    subSection = section.split(self._subSectionChar)
                else:
                    subSection = [section]  # una sola section

                currSECT = the_dict  # top
                for sect in subSection:
                    if not sect in currSECT:
                        currSECT[sect] = collections.OrderedDict({}) if self._returnOrderedDict else {}
                    currSECT = currSECT[sect] #  aggiorna pointer

                if fDEBUG: print ()
                if fDEBUG: print ('[{SECT}]'.format(SECT=section))
                for key, val in self._configMain.items(section, raw=self._RAW):
                    currSECT[key] = val
                    if fDEBUG: print ('    {KEY:<30} : {VAL}'.format(KEY=key, VAL=val))

        except (configparser.InterpolationMissingOptionError) as why:
            print("\n"*2)
            print("="*60)
            print("ERRORE nella validazione del file")
            print("-"*60)
            print(str(why))
            print("="*60)
            sys.exit(-2)

        if self._onlySection:
            return the_dict[self._onlySection]
        else:
            return the_dict

