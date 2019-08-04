"""Data access classes"""
from __future__ import annotations

from typing import Generator
import sqlite3
import logging
from ..config import Config

logger = logging.getLogger(__name__)

class DBAdapter(object):
    def __init__(self, parameters):
        self._conn = None
        pass

    def dql(self, query, args=None) -> typing.Generator[typing.Tuple]:
        return None

    def dml(self, query, args=None, get_rowid=False) -> int:
        return None

    def ddl(self, query, args=None) -> int:
        return None

    @staticmethod
    def factory():
        if Config.get('DBDriver', 'sqlite3') == 'sqlite3':
            db_fn = Config.get('DBFile', 'data/db.sqlite3')
            return SQLiteAdapter(parameters=dict(file=db_fn))
        raise RuntimeError("No proper DBAdapter")
        


class SQLiteAdapter(DBAdapter):
    def __init__(self, parameters):
        super(SQLiteAdapter, self).__init__(parameters)
        if 'file' not in parameters:
            raise RuntimeError("missing parameter: file")
        f = parameters['file']
        self._conn = sqlite3.connect(f)
        
    def dql(self, query: str, args: tuple = None) -> typing.Generator[typing.Tuple]:
        cur = self._conn.cursor()
        if not args:
            args = ()
        try:
            cur.execute(query, args)
        except sqlite3.Error as e:
            logger.error("Problem with database: %s", e.args[0])
            raise
            
        while True:
            l = cur.fetchone()
            if l is None:
                break
            yield l

    def dml(self, query: str, args: tuple=None, get_rowid: bool=False) -> int:
        cur = self._conn.cursor()
        if not args:
            args = ()
        try:
            cur.execute(query, args)
        except sqlite3.Error as e:
            logger.error("Problem with database: %s", e.args[0])
            raise
        if get_rowid:
            return cur.lastrowid
        return cur.rowcount

    def ddl(self, query: str, args: tuple=None) -> int:
        cur = self._conn.cursor()
        if not args:
            args = ()
        try:
            cur.execute(query, args)
        except sqlite3.Error as e:
            logger.error("Problem with database: %s", e.args[0])
            raise
        return cur.rowcount
