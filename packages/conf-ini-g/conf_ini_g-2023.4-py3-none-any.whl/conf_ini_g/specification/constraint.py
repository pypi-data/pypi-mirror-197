# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import dataclasses as dtcl
from abc import ABC as abstract_class_t
from abc import abstractmethod
from enum import Enum as enum_t
from conf_ini_g.standard.path_extension import path_t as pl_path_t
from typing import Any, ClassVar, Sequence

import colorama as clrm


py_type_options_h = type | tuple[type, ...]


class constraint_t(abstract_class_t):

    PY_TYPE_OPTIONS: ClassVar[py_type_options_h] = None

    @abstractmethod
    def Issues(self, py_type: type, name: str, section: str, /) -> Sequence[str]:
        """"""
        raise NotImplementedError(
            f"{constraint_t.Issues.__name__}: Abstract method not meant to be called"
        )

    def IssueWithPyType(
        self, py_type: type, expected: py_type_options_h, name: str, section: str, /
    ) -> list[str]:
        """"""
        if (isinstance(expected, Sequence) and (py_type in expected)) or (
            py_type is expected
        ):
            return []

        return [
            f"{py_type}: Invalid Python type for annotation of type {self.__class__.__name__} "
            f'of parameter "{section}/{name}"; Expected={expected}'
        ]

    @abstractmethod
    def ValueIsValid(self, value: Any) -> bool:
        """"""
        raise NotImplementedError(
            f"{constraint_t.ValueIsValid.__name__}: Abstract method not meant to be called"
        )

    def AsStr(self, details: str) -> str:
        """"""
        return (
            f"{constraint_t.__str__(self)}{clrm.Fore.BLUE}[{details}]{clrm.Fore.RESET}"
        )

    def __str__(self) -> str:
        """"""
        return f"{clrm.Fore.MAGENTA}{self.__class__.__name__[:-2].upper()}{clrm.Fore.RESET}"


@dtcl.dataclass(repr=False, eq=False)
class boolean_t(constraint_t):

    PY_TYPE_OPTIONS: ClassVar[py_type_options_h] = bool

    class MODE(enum_t):
        # Always list true value first
        true_false = ("True", "False")
        yes_no = ("Yes", "No")
        on_off = ("On", "Off")

    mode: enum_t = MODE.true_false

    def Issues(self, py_type: type, name: str, section: str, /) -> Sequence[str]:
        """"""
        return self.IssueWithPyType(
            py_type, self.__class__.PY_TYPE_OPTIONS, name, section
        )

    def ValueIsValid(self, value: bool) -> bool:
        """"""
        return True

    def __str__(self) -> str:
        """"""
        mode = str(self.mode.value)[1:-1].replace("'", "")

        return self.AsStr(mode)


number_h = int | float


@dtcl.dataclass(repr=False, eq=False)
class number_t(constraint_t):

    PY_TYPE_OPTIONS: ClassVar[tuple[type, ...]] = number_h.__args__
    INFINITY_NEG: ClassVar[float] = -float("inf")
    INFINITY_POS: ClassVar[float] = float("inf")
    INFINITE_PRECISION: ClassVar[float] = 0.0

    min: number_h = INFINITY_NEG
    max: number_h = INFINITY_POS
    min_inclusive: bool = True
    max_inclusive: bool = True
    precision: number_h = INFINITE_PRECISION

    def Issues(self, py_type: type, name: str, section: str, /) -> Sequence[str]:
        """"""
        output = self.IssueWithPyType(
            py_type, self.__class__.PY_TYPE_OPTIONS, name, section
        )

        if (self.min != self.__class__.INFINITY_NEG) and not isinstance(
            self.min, py_type
        ):
            output.append(
                f"{type(self.min)}: Invalid type for min value {self.min} "
                f'of parameter "{section}/{name}"; Expected={py_type}'
            )
        if (self.max != self.__class__.INFINITY_POS) and not isinstance(
            self.max, py_type
        ):
            output.append(
                f"{type(self.max)}: Invalid type for max value {self.max} "
                f'of parameter "{section}/{name}"; Expected={py_type}'
            )
        if (self.precision != self.__class__.INFINITE_PRECISION) and not isinstance(
            self.precision, py_type
        ):
            output.append(
                f"{type(self.precision)}: Invalid type for precision {self.precision} "
                f'of parameter "{section}/{name}"; Expected={py_type}'
            )
        if self.precision < 0:
            output.append(
                f'{self.precision}: Negative precision for parameter "{section}/{name}"'
            )
        if (self.min > self.max) or (
            (self.min == self.max) and not (self.min_inclusive and self.max_inclusive)
        ):
            if self.min_inclusive:
                opening = "["
            else:
                opening = "]"
            if self.max_inclusive:
                closing = "]"
            else:
                closing = "["
            output.append(
                f'{opening}{self.min},{self.max}{closing}: Empty value interval for parameter "{section}/{name}"'
            )

        return output

    def ValueIsValid(self, value: number_h) -> bool:
        """"""
        if self.min <= value <= self.max:
            if ((value == self.min) and not self.min_inclusive) or (
                (value == self.max) and not self.max_inclusive
            ):
                return False

            if (self.precision != self.__class__.INFINITE_PRECISION) and (
                self.precision * int(value / self.precision) != value
            ):
                return False

            return True
        else:
            return False

    def __str__(self) -> str:
        """"""
        if self.min == self.__class__.INFINITY_NEG:
            min_ = ""
        else:
            if self.min_inclusive:
                inclusiveness = ""
            else:
                inclusiveness = " excluded"
            min_ = f"from {self.min}{inclusiveness}"

        if self.max == self.__class__.INFINITY_POS:
            max_ = ""
        else:
            if self.max_inclusive:
                inclusiveness = ""
            else:
                inclusiveness = " excluded"
            max_ = f"to {self.max}{inclusiveness}"

        if self.precision == self.__class__.INFINITE_PRECISION:
            precision = ""
        else:
            precision = f"w/ precision {self.precision}"

        description = " ".join(" ".join((min_, max_, precision)).split())

        return self.AsStr(description)


@dtcl.dataclass(repr=False, eq=False)
class choices_t(constraint_t):

    PY_TYPE_OPTIONS: ClassVar[tuple[type, ...]] = str

    options: Sequence[str] = None

    def Issues(self, py_type: type, name: str, section: str, /) -> Sequence[str]:
        """"""
        output = self.IssueWithPyType(
            py_type, self.__class__.PY_TYPE_OPTIONS, name, section
        )

        for option in self.options:
            if not isinstance(option, str):
                output.append(
                    f"{type(option).__name__}: Invalid type of option {option} "
                    f'for parameter "{section}/{name}"; Expected=str'
                )

        return output

    def ValueIsValid(self, value: str) -> bool:
        """"""
        return value in self.options

    def __str__(self) -> str:
        """"""
        options = str(self.options)[1:-1].replace("'", '"')

        return self.AsStr(options)


@dtcl.dataclass(repr=False, eq=False)
class path_t(constraint_t):

    PY_TYPE_OPTIONS: ClassVar[tuple[type, ...]] = pl_path_t

    class TARGET_TYPE(enum_t):
        document = 1
        folder = 2
        any = 3

    target_type: enum_t = TARGET_TYPE.document
    is_input: bool = True

    def Issues(self, py_type: type, name: str, section: str, /) -> Sequence[str]:
        """"""
        return self.IssueWithPyType(
            py_type, self.__class__.PY_TYPE_OPTIONS, name, section
        )

    def ValueIsValid(self, value: pl_path_t) -> bool:
        """"""
        # TODO: should type and existence be validated here?
        return True

    def __str__(self) -> str:
        """"""
        if self.is_input:
            direction = "As input"
        else:
            direction = "As output"

        return self.AsStr(f"{self.target_type.name.capitalize()}, {direction}")


@dtcl.dataclass(repr=False, eq=False)
class sequence_t(constraint_t):

    PY_TYPE_OPTIONS: ClassVar[tuple[type, ...]] = tuple
    ANY_LENGTH: ClassVar[tuple[int]] = (0,)

    # Any=Value of any type but None
    items_types: type | tuple[type | None, ...] = (None, Any)
    lengths: tuple[int, ...] = ANY_LENGTH

    def __post_init__(self):
        """"""
        # TODO: convert every type to annotated type (works with Any b.t.w) one day, maybe (but problem of circular
        #     import)
        if (self.items_types is Any) or isinstance(self.items_types, type):
            self.items_types = (self.items_types,)
        if isinstance(self.lengths, int):
            self.lengths = (self.lengths,)
        else:
            self.lengths = tuple(sorted(self.lengths))

    def Issues(self, py_type: type, name: str, section: str, /) -> Sequence[str]:
        """"""
        output = self.IssueWithPyType(
            py_type, self.__class__.PY_TYPE_OPTIONS, name, section
        )

        if all(_typ is None for _typ in self.items_types):
            output.append(
                f'Contents types restricted to "None" for parameter "{section}/{name}"'
            )

        for content_type in self.items_types:
            if not (
                (content_type is None)
                or (content_type is Any)
                or isinstance(content_type, type)
            ):
                output.append(
                    f'{content_type}: Invalid type of parameter "{section}/{name}"; Expected=None, typing.Any, Python types'
                )
        if self.lengths != self.__class__.ANY_LENGTH:
            for length in self.lengths:
                if (not isinstance(length, int)) or (length <= 0):
                    output.append(
                        f'{length}: Invalid length of parameter "{section}/{name}"; Expected=strictly positive integer'
                    )

        return output

    def ValueIsValid(self, value: tuple) -> bool:
        """"""
        if (self.lengths != self.__class__.ANY_LENGTH) and (
            value.__len__() not in self.lengths
        ):
            return False

        none_not_allowed = None not in self.items_types
        any_not_present = Any not in self.items_types
        # If empty, isinstance(element, types_wo_none) returns False; But cannot be empty (see Issues).
        types_wo_none = tuple(_typ for _typ in self.items_types if _typ is not None)
        for element in value:
            if element is None:
                if none_not_allowed:
                    return False
            elif any_not_present and not isinstance(element, types_wo_none):
                return False

        return True

    def __str__(self) -> str:
        """"""
        return self.AsStr(f"Items={self.items_types}, Lengths={self.lengths}")
