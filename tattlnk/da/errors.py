"""Models for tattlnk"""
from __future__ import annotations

import plyvel

class AccessError(Exception):
    pass


class NonExistentError(Exception):
    pass

