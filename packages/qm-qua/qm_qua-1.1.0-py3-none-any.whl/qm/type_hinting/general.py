import pathlib
from typing import TypeVar, Union

PathLike = TypeVar("PathLike", str, pathlib.Path)
Number = Union[int, float]
Value = Union[Number, bool]
