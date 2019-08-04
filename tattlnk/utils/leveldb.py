from __future__ import annotations

from typing import Generator
import logging
from ..config import Config
import plyvel

logger = logging.getLogger(__name__)

_db = None

class Factory(object):
    @staticmethod
    def get_driver():
        global _db
        if _db is not None and not _db.closed:
            return _db
        if Config.get('DBDriver', 'leveldb') == 'leveldb':
            db_path = Config.get('DBPath', 'data/db')
            _db = plyvel.DB(db_path, create_if_missing=True)
            return _db
        logger.error("Bad config in app, please check DBDriver")
        raise RuntimeError("Config error")



__all__ = ['Factory']
