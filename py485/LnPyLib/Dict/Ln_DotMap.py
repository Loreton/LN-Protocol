#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# updated by ...: Loreto Notarantonio
# Version ......: 02-01-2018 08.34.51
#
# ######################################################################################


from __future__ import print_function
from collections import OrderedDict
from pprint import pprint
from inspect import ismethod

from . DictToList          import KeyTree as LnKeyTree, KeyList as LnKeyList, getValue as LnGetValue
from . PrintDictionaryTree import PrintDictionary as LnPrintDictionary
LORETO = True

class DotMap(OrderedDict):
    ''' creazione di un dictionary di tipo DotMap() '''
    def __init__(self, *args, **kwargs):

        self._map = OrderedDict()
        self._dynamic = True    # mettendo False non funzionano più i test di default. E' normale in quanto si aspettano la creazione dinamica dei figli

            # ===================================
        if LORETO:
            global MY_DICT_TYPES  # global var per la classe
            self._dynamic = False    # mettendo False non funzionano più i test di default. E' normale in quanto si aspettano la creazione dinamica dei figli
            MY_DICT_TYPES = [dict, DotMap, OrderedDict] # by Loreto (DEFAULT dictionary)
            # ===================================

        if kwargs:
            if '_dynamic' in kwargs:
                self._dynamic = kwargs['_dynamic']
        if args:
            d = args[0]
            if isinstance(d, dict):
                for k,v in self.__call_items(d):
                    if type(v) is dict:
                        v = DotMap(v, _dynamic=self._dynamic)
                    if type(v) is list:
                        l = []
                        for i in v:
                            n = i
                            if type(i) is dict:
                                n = DotMap(i, _dynamic=self._dynamic)
                            l.append(n)
                        v = l
                    self._map[k] = v
        if kwargs:
            for k,v in self.__call_items(kwargs):
                if k is not '_dynamic':
                    self._map[k] = v

    def __call_items(self, obj):
        if hasattr(obj, 'iteritems') and ismethod(getattr(obj, 'iteritems')):
            return obj.iteritems()
        else:
            return obj.items()

    def items(self):
        return self.iteritems()

    def iteritems(self):
        return self.__call_items(self._map)

    def __iter__(self):
        return self._map.__iter__()

    def next(self):
        return self._map.next()

    def __setitem__(self, k, v):
        self._map[k] = v
    def __getitem__(self, k):
        if k not in self._map and self._dynamic and k != '_ipython_canary_method_should_not_exist_':
            # automatically extend to new DotMap
            self[k] = DotMap()
        return self._map[k]

    def __setattr__(self, k, v):
        if k in {'_map','_dynamic', '_ipython_canary_method_should_not_exist_'}:
            super(DotMap, self).__setattr__(k,v)
        else:
            self[k] = v

    def __getattr__(self, k):
        if k == {'_map','_dynamic','_ipython_canary_method_should_not_exist_'}:
            super(DotMap, self).__getattr__(k)
        else:
            return self[k]

    def __delattr__(self, key):
        return self._map.__delitem__(key)

    def __contains__(self, k):
        return self._map.__contains__(k)

    def __str__(self):
        items = []
        for k,v in self.__call_items(self._map):
            # bizarre recursive assignment situation (why someone would do this is beyond me)
            if id(v) == id(self):
                items.append('{0}=DotMap(...)'.format(k))
            else:
                items.append('{0}={1}'.format(k, repr(v)))
        out = 'DotMap({0})'.format(', '.join(items))
        return out

    def __repr__(self):
        return str(self)

    def toDict(self):
        d = {}
        for k,v in self.items():
            if type(v) is DotMap:
                # bizarre recursive assignment support
                if id(v) == id(self):
                    v = d
                else:
                    v = v.toDict()
            elif type(v) is list:
                l = []
                for i in v:
                    n = i
                    if type(i) is DotMap:
                        n = i.toDict()
                    l.append(n)
                v = l
            d[k] = v
        return d

    def pprint(self):
        pprint(self.toDict())

        # ===================================
    if LORETO:
        # MY_DICT_TYPES = [dict, DotMap]
        def Ptr(self, listOfQualifiers, create=False):
            ptr = self
            for item in listOfQualifiers:
                if item in ptr:
                    ptr = ptr[item]
                else:
                    if create:
                        ptr[item] = DotMap()
                        ptr = ptr[item]
                    else:
                        return None

            return ptr

        def KeyTree(self, fPRINT=False):
            return LnKeyTree(self, myDictTYPES=MY_DICT_TYPES, fPRINT=fPRINT)

        def KeyList(self):
            return LnKeyList(self, myDictTYPES=MY_DICT_TYPES)


        def PrintTree(self, fEXIT=False, fPAUSE=False, maxDepth=10, header=None, whatPrint='LTKV', stackLevel=1):
            LnPrintDictionary(self, myDictTYPES=MY_DICT_TYPES, whatPrint=whatPrint, fEXIT=fEXIT, fPAUSE=fPAUSE, maxDepth=maxDepth, header=header, stackLevel=stackLevel+1)

        printDict = PrintTree
        printTree = PrintTree

        def GetValue(self, listOfQualifiers=[], fPRINT=False):
            return LnGetValue(self, listOfQualifiers=listOfQualifiers, myDictTYPES=MY_DICT_TYPES, fPRINT=fPRINT)
        # ===================================

    def empty(self):
        return (not any(self))

    # proper dict subclassing
    def values(self):
        return self._map.values()

    # ipython support
    def __dir__(self):
        return self.keys()

    @classmethod
    def parseOther(self, other):
        if type(other) is DotMap:
            return other._map
        else:
            return other
    def __cmp__(self, other):
        other = DotMap.parseOther(other)
        return self._map.__cmp__(other)
    def __eq__(self, other):
        other = DotMap.parseOther(other)
        if not isinstance(other, dict):
            return False
        return self._map.__eq__(other)
    def __ge__(self, other):
        other = DotMap.parseOther(other)
        return self._map.__ge__(other)
    def __gt__(self, other):
        other = DotMap.parseOther(other)
        return self._map.__gt__(other)
    def __le__(self, other):
        other = DotMap.parseOther(other)
        return self._map.__le__(other)
    def __lt__(self, other):
        other = DotMap.parseOther(other)
        return self._map.__lt__(other)
    def __ne__(self, other):
        other = DotMap.parseOther(other)
        return self._map.__ne__(other)

    def __delitem__(self, key):
        return self._map.__delitem__(key)
    def __len__(self):
        return self._map.__len__()
    def clear(self):
        self._map.clear()
    def copy(self):
        return DotMap(self.toDict())
    def get(self, key, default=None):
        return self._map.get(key, default)
    def has_key(self, key):
        return key in self._map
    def iterkeys(self):
        return self._map.iterkeys()
    def itervalues(self):
        return self._map.itervalues()
    def keys(self):
        return self._map.keys()
    def pop(self, key, default=None):
        return self._map.pop(key, default)
    def popitem(self):
        return self._map.popitem()
    def setdefault(self, key, default=None):
        self._map.setdefault(key, default)
    def update(self, *args, **kwargs):
        if len(args) != 0:
            self._map.update(*args)
        self._map.update(kwargs)
    def viewitems(self):
        return self._map.viewitems()
    def viewkeys(self):
        return self._map.viewkeys()
    def viewvalues(self):
        return self._map.viewvalues()
    @classmethod
    def fromkeys(cls, seq, value=None):
        d = DotMap()
        d._map = OrderedDict.fromkeys(seq, value)
        return d
    def __getstate__(self): return self.__dict__
    def __setstate__(self, d): self.__dict__.update(d)

if __name__ == '__main__':
    d = {
        'a':1,
        'b':2,
        'subD': {'c':3, 'd':4}
    }
    dd = DotMap(d)
    print(dd)
    print(len(dd))
    print(dd.copy())
    print(dd)
    print(OrderedDict.fromkeys([1,2,3]))
    print(DotMap.fromkeys([1,2,3], 'a'))
    print(dd.get('a'))
    print(dd.get('f',33))
    print(dd.get('f'))
    print(dd.has_key('a'))
    dd.update([('rat',5),('bum',4)], dog=7,cat=9)
    dd.update({'lol':1,'ba':2})
    print(dd)
    print
    for k in dd:
        print(k)
    print('a' in dd)
    print('c' in dd)
    dd.c.a = 1
    print(dd.toDict())
    dd.pprint()
    print
    print(dd.values())
    dm = DotMap(name='Steve', job='programmer')
    print(dm)
    print(issubclass(dm.__class__, dict))
    am = DotMap()
    am.some.deep.path.cuz.we = 'can'
    print(am)
    del am.some.deep
    print(am)
    parentDict = {
        'name': 'Father1',
        'children': [
            {'name': 'Child1'},
            {'name': 'Child2'},
            {'name': 'Child3'},
        ]
    }
    parent = DotMap(parentDict)
    print([x.name for x in parent.children])

    # pickle
    print('\n== pickle ==')
    import pickle
    s = pickle.dumps(parent)
    d = pickle.loads(s)
    print(d)

    # init from DotMap
    print('\n== init from DotMap ==')
    e = DotMap(d)
    print(e)

    # empty
    print('\n== empty() ==')
    d = DotMap()
    print(d.empty())
    d.a = 1
    print(d.empty())
    print()
    x = DotMap({'a': 'b'})
    print(x.b.empty()) # True (and creates empty DotMap)
    print(x.b) # DotMap()
    print(x.b.empty()) # also True

    # _dynamic
    print('\n== _dynamic ==')
    d = DotMap()
    d.still.works
    print(d)
    d = DotMap(_dynamic=False)
    try:
        d.no.creation
        print(d)
    except KeyError:
        print('KeyError caught')
    d = {'sub':{'a':1}}
    dm = DotMap(d)
    print(dm)
    dm.still.works
    dm.sub.still.works
    print(dm)
    dm2 = DotMap(d,_dynamic=False)
    try:
        dm.sub.yes.creation
        print(dm)
        dm2.sub.no.creation
        print(dm)
    except KeyError:
        print('KeyError caught')

    # _dynamic
    print('\n== toDict() ==')
    conf = DotMap()
    conf.dep = DotMap(facts=DotMap(operating_systems=DotMap(os_CentOS_7=True), virtual_data_centers=[DotMap(name='vdc1', members=['sp1'], options=DotMap(secret_key='badsecret', description='My First VDC')), DotMap(name='vdc2', members=['sp2'], options=DotMap(secret_key='badsecret', description='My Second VDC'))], install_node='192.168.2.200', replication_group_defaults=DotMap(full_replication=False, enable_rebalancing=False, description='Default replication group description', allow_all_namespaces=False), node_defaults=DotMap(ntp_servers=['192.168.2.2'], ecs_root_user='root', dns_servers=['192.168.2.2'], dns_domain='local', ecs_root_pass='badpassword'), storage_pools=[DotMap(name='sp1', members=['192.168.2.220'], options=DotMap(ecs_block_devices=['/dev/vdb'], description='My First SP')), DotMap(name='sp2', members=['192.168.2.221'], options=DotMap(protected=False, ecs_block_devices=['/dev/vdb'], description='My Second SP'))], storage_pool_defaults=DotMap(cold_storage_enabled=False, protected=False, ecs_block_devices=['/dev/vdc'], description='Default storage pool description'), virtual_data_center_defaults=DotMap(secret_key='badsecret', description='Default virtual data center description'), management_clients=['192.168.2.0/24'], replication_groups=[DotMap(name='rg1', members=['vdc1', 'vdc2'], options=DotMap(description='My RG'))]), lawyers=DotMap(license_accepted=True))
    print(conf.dep.toDict()['facts']['replication_groups'])

    # recursive assignment
    print('\n== recursive assignment ==')
    # dict
    d = dict()
    d['a'] = 5
    print(id(d))
    d['recursive'] = d
    print(d)
    print(d['recursive']['recursive']['recursive'])
    # DotMap
    m = DotMap()
    m.a = 5
    print(id(m))
    m.recursive = m
    print(m.recursive.recursive.recursive)
    print(m)
    print(m.toDict())
