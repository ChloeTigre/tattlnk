"""Data access classes"""
from __future__ import annotations

from ..utils.database import DBAdapter
import json

import logging


logger = logging.getLogger(__name__)

conn = DBAdapter.factory()

class Datum(object):
    def __init__(self):
        self.public_attrs = []
    @classmethod
    def load(cls, key) -> Datum:
        return cls.load_item(key)

    def __str__(self):
        return json.dumps(self.as_dict(), indent=4)

    def as_dict(self):
        return {a: getattr(self, a) for a in self.public_attrs}


class Code(Datum):
    def __init__(self, code=None):
        super(Code, self).__init__()
        self.public_attrs += 'code data version archived'.split()
        self.code = code
        self.data = None
        self.version = 0
        self.archived = False

    def load(self, include_archived=False):
        if include_archived:
            query = "" \
                "SELECT data, version, archived from code_table WHERE code = ? " \
                "ORDER BY version DESC LIMIT 1"
        else:
            query = "" \
                "SELECT data, version, archived from code_table WHERE code = ? " \
                "AND archived = FALSE ORDER BY version DESC LIMIT 1"
        out = next(conn.dql(query, (self.code,)))
        self.data, self.version, self.archived = json.loads(out[0]), out[1], out[2]

    def save(self):
        json_data = json.dumps(self.data)
        print(json_data)
        if self.code is None:
            rowid = conn.dml("INSERT INTO code_index(code) VALUES(NULL)", (), True)
            conn.dml("INSERT INTO code_table(code, data, version, archived) VALUES(?, ?, 1, FALSE)", (rowid, json_data))
            self.code = rowid
            self.load()
        else:
            res = conn.dml("INSERT INTO code_table(code, data, version, archived) VALUES(?, ?, ?, FALSE)", (self.code, json_data, self.version + 1), False)
            if res == 0:
                raise RuntimeError("Tried to update non-existing data with code %s", self.code)
            self.load()

    def unpublish_latest(self):
        if self.code is None or self.archived == True:
            return
        conn.dml("UPDATE code_table SET archived = TRUE WHERE code = ? AND version = ?", (self.code, self.version))
        self.archived = True

    def purge_code(self):
        conn.dml("DELETE FROM code_table WHERE code = ?", (self.code,))
        conn.dml("DELETE FROM code_index WHERE code = ?", (self.code,))

    @classmethod
    def load_item(cls, code) -> Code:
        c = cls(code)
        c.load()
        return c

