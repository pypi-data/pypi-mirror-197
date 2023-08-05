# This file is placed in the Public Domain.


'storage'


import json
import os
import pathlib
import _thread


from .decoder import ObjectDecoder
from .encoder import ObjectEncoder
from .objects import Object, items, oid, otype, search, update
from .utility import fnclass, fntime, locked


def __dir__():
    return (
            'Storage',
            'dump',
            'find',
            'last',
            'load',
            'save'
           )


disklock = _thread.allocate_lock()


def cdir(path):
    pth = pathlib.Path(path)
    if path.split('/')[-1].count(':') == 2:
        pth = pth.parent
    os.makedirs(pth, exist_ok=True)


class NoClass(Exception):

    pass


class Storage:

    cls = Object()
    workdir = '.operbot'

    @staticmethod
    def add(clz):
        setattr(Storage.cls, '%s.%s' % (clz.__module__, clz.__name__), clz)

    @staticmethod
    def files(oname=None):
        res = []
        path = Storage.path('')
        if not os.path.exists(path):
            return res
        for fnm in os.listdir(path):
            if oname and oname.lower() not in fnm.split('.')[-1].lower():
                continue
            if fnm not in res:
                res.append(fnm)
        return res

    @staticmethod
    def fns(otp):
        assert Storage.workdir
        path = Storage.path(otp)
        dname = ''
        for rootdir, dirs, _files in os.walk(path, topdown=False):
            if dirs:
                dname = sorted(dirs)[-1]
                if dname.count('-') == 2:
                    ddd = os.path.join(rootdir, dname)
                    fls = sorted(os.listdir(ddd))
                    if fls:
                        path2 = os.path.join(ddd, fls[-1])
                        yield path2

    @staticmethod
    def hook(otp):
        fqn = fnclass(otp)
        cls = getattr(Storage.cls, fqn, None)
        if not cls:
            raise NoClass(fqn)
        obj = cls()
        with open(otp, 'r', encoding='utf-8') as ofile:
            dct = load(ofile)
            update(obj, dct)
        return obj

    @staticmethod
    def path(path=''):
        return os.path.join(Storage.workdir, 'store', path)

    @staticmethod
    def types(oname=None):
        for name, _typ in items(Storage.cls):
            if oname and oname in name.split('.')[-1].lower():
                yield name

    @staticmethod
    def strip(path):
        return path.split('store')[-1][1:]


Storage.add(Object)


@locked(disklock)
def dump(
         obj,
         fnm,
         *args,
         skipkeys=False,
         ensure_ascii=True,
         check_circular=True,
         allow_nan=True,
         cls=None,
         indent=None,
         separators=None,
         default=None,
         sort_keys=False,
         **kw
        ):
    return json.dump(
                     obj,
                     fnm,
                     *args,
                     skipkeys=skipkeys,
                     ensure_ascii=ensure_ascii,
                     check_circular=check_circular,
                     allow_nan=allow_nan,
                     cls=cls or ObjectEncoder,
                     indent=indent,
                     separators=separators,
                     default=default,
                     sort_keys=sort_keys,
                     **kw
                    )


def find(otp, selector=None):
    if selector is None:
        selector = {}
    if '.' in otp:
        tps = [otp]
    else:
        tps = Storage.types(otp)
    for typ in tps:
        for fnm in Storage.fns(typ):
            obj = Storage.hook(fnm)
            if '__deleted__' in obj and obj.__deleted__:
                continue
            if selector and not search(obj, selector):
                continue
            yield fnm, obj


def last(obj, selector=None):
    if selector is None:
        selector = {}
    result = sorted(find(otype(obj), selector), key=lambda x: fntime(x[0]))
    if result:
        _fn, ooo = result[-1]
        if ooo:
            update(obj, ooo)


@locked(disklock)
def load(
         fnm,
         *args,
         cls=None,
         object_hook=None,
         parse_float=None,
         parse_int=None,
         parse_constant=None,
         object_pairs_hook=None,
         **kw
        ):
    return json.load(
                     fnm,
                     *args,
                     cls=cls or ObjectDecoder,
                     parse_float=parse_float,
                     parse_int=parse_int,
                     parse_constant=parse_constant,
                     object_pairs_hook=object_pairs_hook,
                     **kw
                    )


def save(obj, opath=None):
    if not opath:
        opath = Storage.path(oid(obj))
    cdir(opath)
    with open(opath, 'w', encoding='utf-8') as ofile:
        dump(obj, ofile)
    return os.path.abspath(opath)
