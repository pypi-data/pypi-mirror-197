import enum
import dataclasses
import pathlib
from typing import List, Union

import numpy as np
import numpy.typing as npt


FloatArray = npt.NDArray[np.float_]


class Shape(enum.Enum):
    CIRCLE = "circle"
    BOX = "box"


@dataclasses.dataclass
class RegSet:
    X: FloatArray
    Y: FloatArray
    shape: Shape = Shape.CIRCLE
    size: int = 10
    color: str = "green"
    width: int = 1
    comment: str = ""

    def __eq__(self, other: "RegSet") -> bool:  # type: ignore
        return (
            (self.X == other.X).all()
            and (self.Y == other.Y).all()
            and self.shape == other.shape
            and self.size == other.size
            and self.color == other.color
            and self.width == other.width
            and self.comment == other.comment
        )


class RegionsError(Exception):
    "Exception class"


def apex_xy_to_ds9_xy(xa: FloatArray, ya: FloatArray, size_y: int):
    """
    Convert Apex position (xa, ya) to DS9 position (x9, y9) as follows:
        x9 = xa + 1
        y9 = size_y - ya
    kev 2022-02: The correctness was visually checked in DS9 using manually generated FITS
    file (with single gauss profile point), passed through the following pipeline:
    target_pos markup -> apex_geo.py processing -> this correction -> ds9 checkup
    """
    return xa + 1, size_y - ya


def from_apex(size_y: int, *regsets: RegSet) -> List[RegSet]:
    result: List[RegSet] = []
    for r in regsets:
        X, Y = apex_xy_to_ds9_xy(r.X, r.Y, size_y)
        converted = RegSet(**dataclasses.asdict(r))
        converted.X = X
        converted.Y = Y
        result.append(converted)
    return result


def save_as(
    filename: Union[str, pathlib.Path],
    *regsets: RegSet,
    precision: int = 1,
):
    lines: List[str] = []
    lines.append("# Region file format: DS9 version 4.1")
    lines.append(
        'global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman"'
        " select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1"
    )
    lines.append("image")

    p = precision
    for r in regsets:
        if r.comment:
            lines.append(f"# {r.comment}")
        for x, y in zip(r.X, r.Y):
            if r.shape == Shape.CIRCLE:
                lines.append(
                    f"circle({x:.{p}f},{y:.{p}f},{r.size:.{p}f}) # color={r.color} width={r.width}"
                )
            elif r.shape == Shape.BOX:
                lines.append(
                    f"box({x:.{p}f},{y:.{p}f},{r.size:.{p}f},{r.size:.{p}f}) # color={r.color} width={r.width}"
                )
            else:
                raise RegionsError(f"save_as: unsupported shape: {r.shape}")

    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(s + "\n" for s in lines)
