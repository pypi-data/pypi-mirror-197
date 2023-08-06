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

from __future__ import annotations

import dataclasses as dtcl
from typing import Any, Sequence

from conf_ini_g.specification.constant import UNIT_SEPARATOR
from conf_ini_g.specification.constrained_type import (
    INVALID_VALUE,
    constrained_type_t,
    constrained_types_t,
)
from conf_ini_g.specification.default import missing_required_value_t
from conf_ini_g.specification.parameter import parameter_t
from conf_ini_g.standard.dtcl_extension import AsStr


@dtcl.dataclass(repr=False, eq=False)
class actual_t:

    uid: int = None
    type: constrained_type_t = None
    value: Any = None
    unit: str = None
    comment: str = None

    @classmethod
    def _New(cls) -> actual_t:
        """"""
        instance = cls()
        instance.uid = id(instance)

        return instance

    @classmethod
    def NewWithDefaultValue(
        cls,
        parameter: parameter_t,
    ) -> actual_t:
        """"""
        instance = cls._New()
        instance._SetDefaultTypesAndValue(parameter)

        return instance

    @classmethod
    def NewForProgrammaticEntry(
        cls,
        value: str,
        type_options: constrained_types_t,
    ) -> actual_t:
        """"""
        instance = cls._New()
        instance.SetTypesAndValueFromString(value, type_options)

        return instance

    @classmethod
    def NewFromINIEntry(
        cls,
        value_w_comment: str,
        comment_marker: str,
        type_options: constrained_types_t,
    ) -> actual_t:
        """"""
        value, comment = _SplittedValueAndComment(value_w_comment, comment_marker)

        instance = cls.NewForProgrammaticEntry(value, type_options)
        instance.comment = comment

        return instance

    def _SetDefaultTypesAndValue(self, parameter: parameter_t, /) -> None:
        """"""
        value = parameter.default
        if isinstance(value, missing_required_value_t):
            att_type = value.main_type
        else:
            att_type = parameter.type_options.MatchingTypeOf(type(value))

        # TODO: give the meaning of "att"
        self.type = att_type
        self.value = value

    def SetTypesAndValueFromString(
        self, value_w_unit: Any, type_options: constrained_types_t, /
    ) -> None:
        """"""
        if isinstance(value_w_unit, str):
            value_as_str, unit = _SplittedValueAndUnit(value_w_unit)
        else:
            value_as_str, unit = value_w_unit, None
        value, att_type = type_options.TypedValue(value_as_str)

        self.type = att_type
        self.value = value
        self.unit = unit

    def Issues(self, name: str, section: str, /) -> Sequence[str]:
        """"""
        if self.value is INVALID_VALUE:
            return (
                f"{section}/{name}: No matching type in specification or invalid value",
            )

        return ()

    def __str__(self) -> str:
        """"""
        output = AsStr(self)
        intro_length = output.find(":") + 2

        return output[intro_length:]


def _SplittedValueAndComment(
    value_w_comment: str,
    comment_marker: str,
    /,
) -> tuple[str, str| None]:
    """"""
    value, comment = _SplittedElements(value_w_comment, comment_marker)
    if (comment is not None) and (comment.__len__() == 0):
        comment = None

    return value, comment


def _SplittedValueAndUnit(value_w_unit: str, /) -> tuple[str, str | None]:
    """"""
    # if unit.__len__() == 0, do not make it None so that an invalid unit error is noticed later on
    return _SplittedElements(value_w_unit, UNIT_SEPARATOR, from_left=False)


def _SplittedElements(
    combined: str, separator: str, /, *, from_left: bool = True
) -> tuple[str, str | None]:
    """"""
    if from_left:
        where_separator = combined.find(separator)
    else:
        where_separator = combined.rfind(separator)

    if where_separator != -1:
        left = combined[:where_separator].strip()
        right = combined[(where_separator + 1) :].strip()
    else:
        left = combined
        right = None

    return left, right
