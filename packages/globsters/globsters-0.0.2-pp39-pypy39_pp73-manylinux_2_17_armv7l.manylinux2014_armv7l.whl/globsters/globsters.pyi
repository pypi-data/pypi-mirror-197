from typing import Sequence, Union, Callable

__version_lib__: str

bslash2fslash: Callable[[str], str]
fslash2bslash: Callable[[str], str]

class Globster:
    def __init__(
        self, pattern: Union[Sequence[str], str], case_insensitive: bool = False
    ) -> None: ...
    def is_match(self, string: str) -> bool: ...
    def __call__(self, string: str) -> bool: ...

class Globsters:
    def __init__(
        self, patterns: Sequence[str], case_insensitive: bool = False
    ) -> None: ...
    def is_match(self, string: str) -> bool: ...
    def __call__(self, string: str) -> bool: ...
