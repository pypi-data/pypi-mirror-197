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

from typing import ClassVar, Iterator, Sequence

from conf_ini_g.interface.screen.generic import FormattedName
from conf_ini_g.interface.screen.library.pyqt5_constant import (
    ALIGNED_RIGHT,
    ALIGNED_TOP,
)
from conf_ini_g.interface.screen.library.pyqt5_generic import (
    grid_lyt_t,
    hbox_lyt_t,
    library_wgt_t,
)
from conf_ini_g.interface.screen.library.pyqt5_parameter import (
    group_wgt_t,
    label_wgt_t,
    stack_wgt_t,
)
from conf_ini_g.interface.screen.parameter import parameter_t
from conf_ini_g.specification.parameter import parameter_t as parameter_spec_t
from conf_ini_g.specification.section import section_t as section_spec_t


class base_section_t(group_wgt_t):

    HEADER_NAMES: ClassVar[tuple[str]] = (
        "Parameter",
        "Type(s)",
        "Value",
        "Unit",
    )
    HEADER_STYLE: ClassVar[str] = "background-color: darkgray; padding-left: 5px;"

    @classmethod
    def NewWithName(cls, name: str, /) -> base_section_t:
        """"""
        instance = cls()

        instance.setTitle(FormattedName(name, " "))

        return instance

    @classmethod
    def Headers(cls) -> Sequence[label_wgt_t]:
        """"""
        output = []

        for text in cls.HEADER_NAMES:
            header = label_wgt_t(f'<font color="blue">{text}</font>')
            header.SetStyleSheet(cls.HEADER_STYLE)
            output.append(header)

        return output

    @property
    def active_parameters(self) -> Sequence[parameter_t]:
        """"""
        raise NotImplementedError(
            f"{base_section_t.active_parameters.__name__}: Must be overridden by subclasses"
        )

    def __getitem__(self, key: int | str) -> parameter_t:
        """"""
        if isinstance(key, int):
            for parameter in self.active_parameters:
                if key == parameter.uid:
                    return parameter
        else:
            raise KeyError(
                f"{self.__class__.__name__}: Not meant to be accessed by parameter name"
            )

        raise KeyError(f"{key}: Not a parameter of section {self.name}")


class section_t(base_section_t):

    __slots__ = ("parameters",)
    parameters: Sequence[parameter_t]

    @classmethod
    def NewForSection(cls, section: section_spec_t, /) -> section_t | None:
        #
        instance = cls.NewWithName(section.name)

        parameters, layout = _ParametersFromSection(section)
        if parameters.__len__() == 0:
            return None

        for h_idx, header in enumerate(cls.Headers()):
            layout.AddWidget(header, 0, h_idx)

        instance.parameters = parameters
        instance.SetLayout(layout)

        return instance

    @property
    def active_parameters(self) -> Sequence[parameter_t]:
        """
        Mimics controlled_section_t version
        """
        return self.parameters


class controlled_section_t(base_section_t):

    __slots__ = ("parameter_sets", "page_stack")
    parameter_sets: Sequence[Sequence[parameter_t]]
    page_stack: stack_wgt_t

    @classmethod
    def NewForSection(
        cls,
        section: section_spec_t,
        /,
    ) -> controlled_section_t | None:
        """"""
        instance = cls.NewWithName(section.name)

        parameter_sets = []
        max_parameter_set_length = 0
        page_stack = stack_wgt_t()
        for parameter_specs in (section, *section.alternatives.values()):
            parameters, layout = _ParametersFromSpecifications(parameter_specs)
            if (n_parameters := parameters.__len__()) > 0:
                for h_idx, header in enumerate(cls.Headers()):
                    layout.AddWidget(header, 0, h_idx)

            parameter_sets.append(parameters)
            max_parameter_set_length = max(max_parameter_set_length, n_parameters)

            page = library_wgt_t()
            page.SetLayout(layout)
            page_stack.AddWidget(page)

        if max_parameter_set_length == 0:
            return None

        controlling_values = section.controlling_values
        page_stack.SetCurrentIndex(controlling_values.index(section.controller_value))

        instance.parameter_sets = parameter_sets
        instance.page_stack = page_stack

        # Curiously, the stacked widget cannot be simply declared as child of instance; This must be specified through
        # a layout.
        layout = hbox_lyt_t()
        layout.AddWidget(page_stack)
        layout.SetContentsMargins(0, 0, 0, 0)
        instance.SetLayout(layout)

        return instance

    @property
    def active_parameters(self) -> Sequence[parameter_t]:
        """"""
        return self.parameter_sets[self.page_stack.CurrentIndex()]


def _ParametersFromSection(
    section: section_spec_t, /
) -> tuple[Sequence[parameter_t], grid_lyt_t]:
    """"""
    return _ParametersFromSpecifications(section.active_parameters)


def _ParametersFromSpecifications(
    specifications: Sequence[parameter_spec_t] | Iterator[parameter_spec_t], /
) -> tuple[Sequence[parameter_t], grid_lyt_t]:
    """"""
    parameters = []

    layout = grid_lyt_t()
    layout.SetAlignment(ALIGNED_TOP)
    layout.SetColumnStretch(0, 4)
    layout.SetColumnStretch(1, 4)
    layout.SetColumnStretch(2, 8)
    layout.SetColumnStretch(3, 1)
    layout.SetContentsMargins(0, 0, 0, 0)

    for row, parameter_spec in enumerate(specifications, start=1):
        parameter = parameter_t.NewForParameter(parameter_spec)
        parameters.append(parameter)

        has_unit = parameter.unit is not None
        layout.AddWidget(parameter.name, row, 0, alignment=ALIGNED_RIGHT)
        layout.AddWidget(parameter.type_selector, row, 1)
        layout.AddWidget(parameter.value_stack, row, 2, 1, 2 - 1)  # - int(has_unit))
        if has_unit:
            layout.AddWidget(parameter.unit, row, 3)

    return parameters, layout
