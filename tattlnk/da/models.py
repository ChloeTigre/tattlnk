"""Models for tattlnk"""
from __future__ import annotations

from collections import namedtuple
from collections.abc import Iterable
from functools import wraps

from .errors import AccessError, NonExistentError
from ..utils.leveldb import Factory as KVFactory




from datetime import datetime
import json
import logging
import uuid


logger = logging.getLogger(__name__)

CodeEntry = namedtuple("CodeEntry", "code json_data".split())


# some junk decorator
def needs_pk(f):
    @wraps(f)
    def _f(self, *args, **kwargs):
        if not hasattr(self, 'pk') or self.pk is None:
            logger.error("Tried to act on persistence of item without setting its PK first")
            raise Exception("Tried to act on persistence of PK-less item")
        return f(self, *args, **kwargs)
    return _f

def bytesify(stuff):
    if isinstance(stuff, Iterable):
        return bytes(stuff)
    elif isinstance(stuff, int):
        return stuff.to_bytes(64, 'big')
    raise RuntimeError("tried to bytesify unsupported thing: {} of type {}".format(stuff, type(stuff)))


class Datum(object):

    db_prefix = b'changeme'

    @classmethod
    def get_db(cls):
        db = KVFactory.get_driver()
        pdb = db.prefixed_db(cls.db_prefix)
        return pdb
    
    @classmethod
    def get(cls, pk):
        glass = cls()
        glass.pk = pk
        glass.load()
        return glass

    @property
    def pk(self):
        try:
            return self._pk
        except AttributeError:
            return None

    @pk.setter
    def pk(self, value):
        if hasattr(self, 'pk') and getattr(self, 'pk') is not None and value is not None:
            logger.error("tried to override item with pk %s with new value %s", str(self.pk), str(value))
            raise AccessError("Cannot change PK of an entry once set")
        self._pk = value

    def __str__(self):
        return json.dumps(self.as_dict(), indent=4)

    def as_dict(self):
        return {a: getattr(self, a) for a in self.business_attrs}

    def from_dict(self, h):
        for k, v in h.items():
            if k not in self.business_attrs:
                logger.warning("ignored attribute %s when running from_dict", k)
                continue
            setattr(self, k, v)

    def gen_pk(self):
        # override this please please please
        return datetime.now().strptime("%Y%m%d%H%M%S").encode('utf-8')

    def save(self):
        if self.pk is None:
            # generate a public key
            self.pk = self.gen_pk()
        data = json.dumps(self.as_dict()).encode('utf-8')
        pdb = self.get_db()
        # here force pk to be bytes
        pk = bytesify(self.pk)
        pdb.put(pk, data)

    @needs_pk
    def load(self):
        pk = bytesify(self.pk)
        db = KVFactory.get_driver()
        pdb = self.get_db()
        data = pdb.get(pk)
        if data is None:
            logger.error("Tried to load non-existent or empty item with PK: %s", self.pk)
            raise NonExistentError("Item with given PK is not existent")
        self.from_dict(json.loads(data.decode('utf-8')))

    @needs_pk
    def delete(self):
        pk = bytesify(self.pk)
        db = KVFactory.get_driver()
        pdb = self.get_db()
        pdb.delete(pk)
        

class Code(Datum):
    db_prefix = b'code_'
    business_attrs = 'data'.split()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def gen_pk(self):
        return uuid.uuid4().int & (1<<64)-1
    
