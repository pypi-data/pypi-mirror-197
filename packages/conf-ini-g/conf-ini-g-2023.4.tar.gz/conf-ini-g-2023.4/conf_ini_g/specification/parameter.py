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

from conf_ini_g.specification.constrained_type import constrained_types_t
from conf_ini_g.specification.default import missing_required_value_t
from conf_ini_g.specification.generic import generic_t
from conf_ini_g.standard.type_extension import any_type_h


@dtcl.dataclass(repr=False, eq=False)
class parameter_t(generic_t):
    """
    Since optionality is determined by whether default is of instance missing_required_value_t or not, and since it is
    not possible to give a default value of instance missing_required_value_t without knowing the allowed types, then
    parameters are optional by default (contrary to sections).

    If a parameter is mandatory (default is an instance of missing_required_value_t), _type_options must be None and the
    allowed types must be given through missing_required_value_t.types.

    The parameter specification does not contain a value. When talking about value below, it refers to the value a
    functional parameter instance (instance of a subclass of actual_t) could have.

    types:
        Used at instantiation time: parameter_t(types=...). It is set to None in __post_init__.
    _type_options:
        Used internally after conversion to constrained_type_t
    default:
        Can be None only if types contains None at instantiation time
    """

    types: any_type_h | Sequence[any_type_h] = None
    default: Any = None
    _type_options: constrained_types_t | None = dtcl.field(init=False)
    actual: Any = dtcl.field(init=False)

    def __post_init__(self) -> None:
        """"""
        # Incoherence in the processing below will be caught later on by Issues
        if isinstance(self.types, Sequence):
            types = self.types
        elif self.optional:
            types = (self.types,)
        else:
            types = None

        if types is None:
            self._type_options = None
        else:
            self._type_options = constrained_types_t.NewFromTypes(types)
        self.types = None
        self.actual = None

    def DefaultIsValid(self) -> bool:
        """"""
        output = False

        default_value = self.default
        for type_ in self._type_options:
            if isinstance(default_value, type_.py_type):
                n_tests = 0
                n_valids = 0
                for annotation in type_.annotations:
                    if hasattr(annotation, "ValueIsValid"):
                        n_tests += 1
                        if annotation.ValueIsValid(default_value):
                            n_valids += 1
                if n_valids == n_tests:
                    output = True
                    break

        return output

    def Issues(self, /, *, section: str = None) -> Sequence[str]:
        """
        section: should not be optional here, but the base method signature (also used by section_t which does not
                 need a context) must be respected.
        """
        output = super().Issues(context=section)

        if self.optional:
            output.extend(self._type_options.Issues(self.name, section))
            if isinstance(self.default, missing_required_value_t):
                output.append(
                    f"{section}/{self.name}: Default value of optional parameter cannot be of type "
                    f'"{missing_required_value_t.__name__}"'
                )
            elif not self.DefaultIsValid():
                output.append(
                    f'{self.default}: Invalid default value for parameter "{section}/{self.name}"'
                )
        else:
            if not self.basic:
                output.append(
                    f"{section}/{self.name}: Parameter is not basic but not optional"
                )
            if self._type_options is not None:
                output.append(
                    f"{section}/{self.name}: Mandatory parameter with explicit allowed types; "
                    f'Specify them through the "missing_required_value_t" instance of "default"'
                )
            if isinstance(self.default, missing_required_value_t):
                output.extend(self.default.Issues(self.name, section))
            else:
                output.append(
                    f"{section}/{self.name}: Default value of mandatory parameter must be of type "
                    f'"{missing_required_value_t.__name__}"'
                )

        if self.actual is not None:
            output.extend(self.actual.Issues(self.name, section))

        return output

    @property
    def optional(self) -> bool:
        """"""
        return not isinstance(self.default, missing_required_value_t)

    @property
    def type_options(self) -> constrained_types_t:
        """"""
        if self.optional:
            return self._type_options
        else:
            return self.default.type_options
