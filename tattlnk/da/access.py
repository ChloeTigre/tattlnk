"""Data access classes"""
from __future__ import annotations

from ..utils.database import DBAdapter
import json

import logging


logger = logging.getLogger(__name__)

conn = DBAdapter.factory()

class Datum(object):
    @classmethod
    def load(cls, key) -> Datum:
        return cls.load_item(key)


class Code(Datum):
    def __init__(self, code=None):
        self.code = code
        self.data = None

    def load(self):
        self.data = json.loads([a for a in conn.dql(""
            "SELECT data from code_table WHERE code = ? "
            "AND archived = FALSE ORDER BY version DESC LIMIT 1", (self.code))][0])

    def save(self):
        json_data = json.dumps(self.data)
        if self.code is None:
            rowid = conn.dml("INSERT INTO code_table(data, version, archived) VALUES(?, 1, FALSE)", (json_data), True)
            self.code = rowid
            self.load()
        else:
            res = conn.dml("INSERT INTO code_table(code, data, version, archived) VALUES(?, ?, ?, FALSE)", (self.code, json_data, self.version + 1), False)
            if res == 0:
                raise RuntimeError("Tried to update non-existing data with code %s", self.code)
            self.load()
            
    @classmethod
    def load_item(cls, code) -> Code:
        c = cls(code)
        c.load()
        return c

