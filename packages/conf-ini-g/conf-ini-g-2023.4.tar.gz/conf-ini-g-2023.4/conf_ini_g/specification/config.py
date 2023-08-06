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
import textwrap as text
from typing import Any, Sequence

import conf_ini_g.specification.unit as unit
from conf_ini_g.specification.constant import UNIT_SECTION, UNIT_SEPARATOR
from conf_ini_g.specification.section import section_t


@dtcl.dataclass(init=False, repr=False, eq=False)
class config_t(list[section_t]):

    updater: Any = None
    has_default_value: Sequence[int] | None = None

    def __init__(self, sections: Sequence[section_t], /) -> None:
        """
        Raising exceptions is adapted here since execution cannot proceed without a valid specification
        """
        if sections.__len__() == 0:
            raise ValueError(
                f"{self.__class__.__name__}: Must be instantiated from a non-empty iterable"
            )
        super().__init__(sections)

        issues = self.Issues()
        if issues is not None:
            print("\n".join(issues))
            raise ValueError("Invalid config specification")

        self.AddUnitSection()

    def AddUnitSection(self) -> None:
        """"""
        section = section_t(
            name=UNIT_SECTION,
            definition="Unit definitions",
            description=f"Units defined in this section can be use in any other section "
            f"to specify a parameter value as follows: "
            f"numeric_value{UNIT_SEPARATOR}unit, e.g., 1.5'mm",
            basic=True,
            optional=True,
            category=UNIT_SECTION,
            accept_unknown_parameters=True,
        )
        self.append(section)

    @property
    def valid_section_names(self) -> Sequence[str]:
        """"""
        return tuple(_sct.name for _sct in self)

    def Issues(self, /, *, pre_units: bool = True) -> Sequence[str] | None:
        """
        To be called before adding the automatically-added unit section
        """
        output = []

        valid_names = self.valid_section_names
        if valid_names.__len__() > set(valid_names).__len__():
            output.append("Specification with repeated section names")

        for section in self:
            if pre_units and unit.IsUnitSection(section.name, possibly_fuzzy=True):
                output.append(
                    f"{UNIT_SECTION}: Reserved section name; "
                    f"Implicitly added to all configurations; "
                    f"Must not be used in specification (in any case combination)"
                )
            else:
                output.extend(section.Issues())
            if section.controller is not None:
                if section.controller.section not in self:
                    output.append(
                        f"{section.controller.section}: "
                        f'Unknown section declared as controller of section "{section.name}"'
                    )
                else:
                    controller_section = self[section.controller.section]
                    if controller_section.controller is not None:
                        output.append(
                            f"{section.controller.section}: "
                            f'Section controlling "{section.name}" is itself controlled'
                        )
                    if section.controller.parameter not in controller_section:
                        output.append(
                            f"{section.controller.section}.{section.controller.parameter}: "
                            f'Unknown parameter declared as controller of section "{section.name}"'
                        )
                    else:
                        controller_parameter = controller_section[
                            section.controller.parameter
                        ]
                        if controller_parameter.optional:
                            output.append(
                                f"{section.controller.section}.{section.controller.parameter}: "
                                f'Optional parameter declared as controller of section "{section.name}"'
                            )
                        if controller_parameter.type_options.__len__() > 1:
                            output.append(
                                f"{section.controller.section}.{section.controller.parameter}: "
                                f'Multi-type parameter declared as controller of section "{section.name}"'
                            )

        if output.__len__() == 0:
            output = None

        return output

    def __contains__(self, key: str) -> bool:
        """"""
        for section in self:
            if key == section.name:
                return True

        return False

    def __getitem__(self, key: int | str) -> section_t:
        """"""
        if isinstance(key, int):
            raise KeyError(
                f"{self.__class__.__name__}: Not meant to be accessed as a list"
            )

        for section in self:
            if key == section.name:
                return section

        raise KeyError(f"{key}: Not an existing section")

    def __str__(self) -> str:
        """"""
        sections = (str(_sct) for _sct in self)
        sections = "\n".join(sections)
        sections = text.indent(sections, "    ")

        return f"{self.__class__.__name__[:-2].upper()}:\n{sections}"
