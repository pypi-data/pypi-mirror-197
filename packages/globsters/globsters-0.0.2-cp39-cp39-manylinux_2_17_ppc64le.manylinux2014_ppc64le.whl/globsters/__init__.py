from __future__ import annotations

from functools import lru_cache
from typing import Sequence, Union, Tuple

from .globsters import Globster as Globster
from .globsters import Globsters as Globsters
from .globsters import __version_lib__ as __version_lib__
from .globsters import bslash2fslash as bslash2fslash
from .globsters import fslash2bslash as fslash2bslash

__version__ = __version_lib__
__all__ = ("__version__", "Globster", "Globsters", "globster", "globsters")


@lru_cache(maxsize=16)
def _globster(
    pattern: Union[Tuple[str, ...], str], case_insensitive: bool = False
) -> Globster:
    return Globsters(
        (pattern,) if isinstance(pattern, str) else pattern, case_insensitive
    )


def globster(
    patterns: Union[Sequence[str], str],
    case_insensitive: bool = False,
    cache: bool = True,
) -> Globsters:
    """Create a Globster object from a glob pattern(s)"""
    if cache:
        if isinstance(patterns, str):
            return _globster(patterns, case_insensitive)
        return _globster(tuple(set(patterns)), case_insensitive)
    if isinstance(patterns, str):
        return globster((patterns,), case_insensitive)
    return Globsters(tuple(set(patterns)), case_insensitive)


def globsters(
    patterns: Sequence[str],
    case_insensitive: bool = False,
    cache: bool = True,
) -> Globsters:
    """Create a Globster object from a glob pattern(s)"""
    if cache:
        return _globster(tuple(set(patterns)), case_insensitive)
    return Globsters(tuple(set(patterns)), case_insensitive)


__doc__ = globsters.__doc__
if hasattr(globsters, "__all__"):
    __all__ = globsters.__all__
