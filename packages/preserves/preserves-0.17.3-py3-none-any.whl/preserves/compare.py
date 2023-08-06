"""TODO"""

import numbers
from enum import Enum
from functools import cmp_to_key

from .values import preserve, Float, Embedded, Record, Symbol, cmp_floats, _unwrap
from .compat import basestring_

class TypeNumber(Enum):
    BOOL = 0
    FLOAT = 1
    DOUBLE = 2
    SIGNED_INTEGER = 3
    STRING = 4
    BYTE_STRING = 5
    SYMBOL = 6

    RECORD = 7
    SEQUENCE = 8
    SET = 9
    DICTIONARY = 10

    EMBEDDED = 11

def type_number(v):
    if hasattr(v, '__preserve__'):
        raise ValueError('type_number expects Preserves value; use preserve()')

    if isinstance(v, bool): return TypeNumber.BOOL
    if isinstance(v, Float): return TypeNumber.FLOAT
    if isinstance(v, float): return TypeNumber.DOUBLE
    if isinstance(v, numbers.Number): return TypeNumber.SIGNED_INTEGER
    if isinstance(v, basestring_): return TypeNumber.STRING
    if isinstance(v, bytes): return TypeNumber.BYTE_STRING
    if isinstance(v, Symbol): return TypeNumber.SYMBOL

    if isinstance(v, Record): return TypeNumber.RECORD
    if isinstance(v, list) or isinstance(v, tuple): return TypeNumber.SEQUENCE
    if isinstance(v, set) or isinstance(v, frozenset): return TypeNumber.SET
    if isinstance(v, dict): return TypeNumber.DICTIONARY

    if isinstance(v, Embedded): return TypeNumber.EMBEDDED

    try:
        i = iter(v)
    except TypeError:
        i = None
    if i is None:
        raise ValueError('Invalid Preserves value in type_number')
    else:
        return TypeNumber.SEQUENCE

def cmp(a, b):
    """TODO"""
    return _cmp(preserve(a), preserve(b))

def lt(a, b):
    """TODO"""
    return cmp(a, b) < 0

def le(a, b):
    """TODO"""
    return cmp(a, b) <= 0

def eq(a, b):
    """TODO"""
    return _eq(preserve(a), preserve(b))

key = cmp_to_key(cmp)
_key = key

_sorted = sorted
def sorted(iterable, *, key=lambda x: x, reverse=False):
    """TODO"""
    return _sorted(iterable, key=lambda x: _key(key(x)), reverse=reverse)

def sorted_items(d):
    """TODO"""
    return sorted(d.items(), key=_item_key)

def _eq_sequences(aa, bb):
    aa = list(aa)
    bb = list(bb)
    n = len(aa)
    if len(bb) != n: return False
    for i in range(n):
        if not _eq(aa[i], bb[i]): return False
    return True

def _item_key(item):
    return item[0]

def _eq(a, b):
    a = _unwrap(a)
    b = _unwrap(b)
    ta = type_number(a)
    tb = type_number(b)
    if ta != tb: return False

    if ta == TypeNumber.DOUBLE:
        return cmp_floats(a, b) == 0

    if ta == TypeNumber.EMBEDDED:
        return _eq(a.embeddedValue, b.embeddedValue)

    if ta == TypeNumber.RECORD:
        return _eq(a.key, b.key) and _eq_sequences(a.fields, b.fields)

    if ta == TypeNumber.SEQUENCE:
        return _eq_sequences(a, b)

    if ta == TypeNumber.SET:
        return _eq_sequences(sorted(a), sorted(b))

    if ta == TypeNumber.DICTIONARY:
        return _eq_sequences(sorted_items(a), sorted_items(b))

    return a == b

def _simplecmp(a, b):
    return (a > b) - (a < b)

def _cmp_sequences(aa, bb):
    aa = list(aa)
    bb = list(bb)
    n = min(len(aa), len(bb))
    for i in range(n):
        v = _cmp(aa[i], bb[i])
        if v != 0: return v
    return len(aa) - len(bb)

def _cmp(a, b):
    a = _unwrap(a)
    b = _unwrap(b)
    ta = type_number(a)
    tb = type_number(b)
    if ta.value < tb.value: return -1
    if tb.value < ta.value: return 1

    if ta == TypeNumber.DOUBLE:
        return cmp_floats(a, b)

    if ta == TypeNumber.EMBEDDED:
        return _cmp(a.embeddedValue, b.embeddedValue)

    if ta == TypeNumber.RECORD:
        v = _cmp(a.key, b.key)
        if v != 0: return v
        return _cmp_sequences(a.fields, b.fields)

    if ta == TypeNumber.SEQUENCE:
        return _cmp_sequences(a, b)

    if ta == TypeNumber.SET:
        return _cmp_sequences(sorted(a), sorted(b))

    if ta == TypeNumber.DICTIONARY:
        return _cmp_sequences(sorted_items(a), sorted_items(b))

    return _simplecmp(a, b)
