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
from typing import Any, Type

from conf_ini_g.interface.screen.component.boolean import boolean_wgt_t
from conf_ini_g.interface.screen.component.choices import choices_wgt_t
from conf_ini_g.interface.screen.component.default_entry import default_entry_wgt_t
from conf_ini_g.interface.screen.component.none import none_wgt_t
from conf_ini_g.interface.screen.component.path import path_wgt_t
from conf_ini_g.interface.screen.component.sequence import sequence_wgt_t
from conf_ini_g.interface.screen.component.type_options import (
    multiple_types_wgt_t,
    single_type_wgt_t,
)
from conf_ini_g.interface.screen.generic import FormattedName
from conf_ini_g.interface.screen.library.pyqt5_constant import (
    SIZE_EXPANDING,
    SIZE_FIXED,
)
from conf_ini_g.interface.screen.library.pyqt5_generic import library_wgt_t
from conf_ini_g.interface.screen.library.pyqt5_parameter import (
    label_wgt_t,
    simple_entry_wgt_t,
    stack_wgt_t,
)
from conf_ini_g.specification.constant import UNIT_SEPARATOR
from conf_ini_g.specification.constrained_type import (
    SIMPLE_ATT_TYPES,
    constrained_type_t,
)
from conf_ini_g.specification.parameter import parameter_t as parameter_spec_t
from conf_ini_g.standard.type_extension import any_type_h


_TYPE_WIDGET_TRANSLATOR: dict[constrained_type_t, Type[library_wgt_t]] = {
    SIMPLE_ATT_TYPES["boolean"]: boolean_wgt_t,
    SIMPLE_ATT_TYPES["float"]: default_entry_wgt_t,
    SIMPLE_ATT_TYPES["int"]: default_entry_wgt_t,
    SIMPLE_ATT_TYPES["choices"]: choices_wgt_t,
    SIMPLE_ATT_TYPES["path"]: path_wgt_t,
    SIMPLE_ATT_TYPES["sequence"]: sequence_wgt_t,
    SIMPLE_ATT_TYPES["None"]: none_wgt_t,
}


@dtcl.dataclass(repr=False, eq=False)
class parameter_t:
    """
    In order to leave the section widget put the name, type, and input widgets of each parameter in columns,
    actual_t is not a container widget. Instead, it just store its component widgets for later addition to a layout.
    """

    uid: int  # Allows to retrieve the parameter specification
    name: label_wgt_t = None  # Visual version, not functional one
    type_selector: single_type_wgt_t | multiple_types_wgt_t = None
    value_stack: stack_wgt_t = None
    unit: simple_entry_wgt_t = None
    comment: str = None

    @classmethod
    def NewForParameter(cls, parameter: parameter_spec_t, /) -> parameter_t:
        """"""
        instance = cls(uid=parameter.actual.uid)

        formatted_name = FormattedName(parameter.name, " ")
        comment = (
            f"{formatted_name}\n{parameter.definition}.\n\n{parameter.description}."
        )
        if parameter.actual.comment is not None:
            comment += f"\n\n{parameter.actual.comment}."

        instance.name = label_wgt_t(formatted_name)
        instance.comment = comment
        instance.name.SetToolTip(comment)

        type_options = parameter.type_options
        if type_options.__len__() > 1:
            initial_type = parameter.actual.type
            type_selector = multiple_types_wgt_t(type_options, initial_type)
        else:
            type_selector = single_type_wgt_t(type_options[0].py_type.__name__)
        instance.type_selector = type_selector

        value_stack = stack_wgt_t()
        initial_index = 0
        for t_idx, att_type in enumerate(type_options):
            if att_type is parameter.actual.type:
                initial_value = parameter.actual.value
                initial_index = t_idx
            else:
                initial_value = None
            widget_type = _WidgetTypeForType(att_type)
            value = widget_type.NewWithDetails(
                initial_value,
                att_type,
                parameter,
            )
            value_stack.AddWidget(value)
        value_stack.SetCurrentIndex(initial_index)
        value_stack.SetSizePolicy(SIZE_EXPANDING, SIZE_FIXED)
        instance.value_stack = value_stack

        if parameter.actual.unit is not None:
            instance.unit = simple_entry_wgt_t(parameter.actual.unit)

        name_style = "padding-right: 5px;"
        if parameter.optional:
            name_style += "color: gray;"
        instance.name.SetStyleSheet(name_style)
        instance.type_selector.SetStyleSheet(name_style)

        if isinstance(type_selector, multiple_types_wgt_t):
            type_selector.activated.connect(instance.value_stack.SetCurrentIndex)

        return instance

    @property
    def active_value(self) -> library_wgt_t:
        """"""
        return self.value_stack.CurrentWidget()

    def SetVisible(self, visible: bool, /) -> None:
        """"""
        self.name.SetVisible(visible)
        self.type_selector.SetVisible(visible)
        self.value_stack.SetVisible(visible)
        if self.unit is not None:
            self.unit.SetVisible(visible)

    def Text(self) -> str:
        #
        output = self.active_value.Text()

        if self.unit is None:
            unit = None
        else:
            unit = self.unit.Text().strip()

        if (unit is not None) and (unit.__len__() > 0):
            output += UNIT_SEPARATOR + unit

        return output

    def Value(self) -> Any:
        """"""
        if self.unit is None:
            unit = None
        else:
            unit = self.unit.Text().strip()

        if (unit is not None) and (unit.__len__() > 0):
            output = self.active_value.Text() + UNIT_SEPARATOR + unit
        else:
            output = self.active_value.Value()

        return output


def RegisterNewTranslation(
    new_type: any_type_h, widget_type: Type[library_wgt_t], /
) -> None:
    """"""
    att_type = constrained_type_t.NewFromType(new_type)
    if att_type in _TYPE_WIDGET_TRANSLATOR:
        # Raising an exception is adapted here since it is a developer-oriented function
        raise ValueError(
            f"{att_type}: Type already registered in type-to-widget translations"
        )

    _TYPE_WIDGET_TRANSLATOR[att_type] = widget_type


def _WidgetTypeForType(att_type: constrained_type_t, /) -> Type[library_wgt_t]:
    """"""
    for registered_type, widget_type in _TYPE_WIDGET_TRANSLATOR.items():
        if att_type.ContainsOrMatches(
            registered_type.annotations, py_type=registered_type.py_type
        ):
            return widget_type

    return default_entry_wgt_t
