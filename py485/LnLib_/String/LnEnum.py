#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:
# ######################################################################################
from  collections import OrderedDict

class myEnumClass():
    pass
    def __str__(self):
        _str_ = []
        for key,val in self.__dict__.items():
            _str_.append('{:<15}: {}'.format(key, val))

        return '\n'.join(_str_)



def LnEnum(data, myDictType=myEnumClass, weighted=False):
    if not myDictType:
        myDictType = myEnumClass

    ENUM = myDictType()
    for index, name in enumerate(data):
        itemName = name.strip().replace(' ', '_')
        if weighted:
                # - ritorna il nome con una sequenza binaria
            try:
                ENUM[itemName] = 2**index
            except (TypeError):
                setattr(ENUM, itemName, 2**index)
        else:
                # - ritorna il nome con una sequenza unitaria
            try:
                ENUM[itemName] = index
            except (TypeError):
                setattr(ENUM, itemName, index)

    return ENUM




######################################################################
# -    M  A  I  N
######################################################################
if __name__ == '__main__':
    data = ['', 'CIAO', 'DUE', 'TRE', 'QUATTRO', ]
    val = LnEnum(data, OrderedDict)
    print (val)
    print (val['TRE'])


    val = LnEnum(data, myDictType=myEnumClass)
    print (val)
    print (val.TRE)
    # for key in val.__dict__.keys():
    #     print (key)