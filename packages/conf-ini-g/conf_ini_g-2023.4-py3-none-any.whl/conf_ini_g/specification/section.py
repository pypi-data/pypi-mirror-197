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
import itertools as ittl
import textwrap as text
from typing import Any
from typing import NamedTuple as named_tuple_t
from typing import Sequence

from conf_ini_g.specification.generic import generic_t
from conf_ini_g.specification.parameter import parameter_t


@dtcl.dataclass(init=False, repr=False, eq=False)
class controller_t(named_tuple_t):
    section: str = None
    parameter: str = None
    # All controller values are equal in role. However, this one is called primary because it refers to the parameters
    # of the section, as opposed to the parameters in the alternatives.
    primary_value: Any = None


@dtcl.dataclass(init=False, repr=False, eq=False)
class section_t(generic_t, list[parameter_t]):

    category: str = "Main"
    optional: bool = False
    accept_unknown_parameters: bool = False
    controller: controller_t = None
    alternatives: dict[Any, list[parameter_t]] = None
    # Cannot be None as Python prohibits indexing by None
    controller_value: Any = None

    def __init__(self, *_, **kwargs) -> None:
        """"""
        list.__init__(self, kwargs.get("parameters", []))

        attributes = tuple(_fld.name for _fld in dtcl.fields(section_t))
        arguments = {_key: _val for _key, _val in kwargs.items() if _key in attributes}
        for name, value in arguments.items():
            setattr(self, name, value)

    @property
    def all_parameters(self) -> Sequence[parameter_t]:
        """"""
        if self.alternatives is None:
            return self
        else:
            return tuple(ittl.chain(self, *self.alternatives.values()))

    @property
    def active_parameters(self) -> list[parameter_t]:
        """"""
        # The test self.controller_value is None avoids querying self.alternatives with None, which is forbidden by
        # Python. This could happen if the config has not been fully activated, which should be avoided, but do happen
        # when instantiating a command-line parser for example (other cases?)
        if (
            (self.controller is None)
            or (self.controller_value == self.controller.primary_value)
            or (self.controller_value is None)
        ):
            return self
        else:
            return self.alternatives[self.controller_value]

    @property
    def controlling_values(self) -> Sequence[Any]:
        """
        Call only on controlled sections
        """
        return (self.controller.primary_value,) + tuple(self.alternatives.keys())

    def Issues(self, /, *, context: str = None) -> Sequence[str]:
        """"""
        output = super().Issues()

        valid_name_sets = [tuple(_prm.name for _prm in super().__iter__())]
        if self.alternatives is not None:
            for parameters in self.alternatives.values():
                valid_name_sets.append(tuple(_prm.name for _prm in parameters))
        for valid_name_set in valid_name_sets:
            if valid_name_set.__len__() > set(valid_name_set).__len__():
                output.append(
                    f"{self.name}: Section with repeated parameter names (possibly in alternatives)"
                )

        basic = self.basic
        optional = self.optional

        if not (basic or optional):
            output.append(f"{self.name}: Section is not basic but not optional")

        if (self.controller is None) and (not optional) and (self.__len__() == 0):
            output.append(f"{self.name}: Empty mandatory section")

        n_parameters = 0
        n_basic_prms = 0
        for parameter in self.all_parameters:
            output.extend(parameter.Issues(section=self.name))

            n_parameters += 1
            if parameter.basic:
                n_basic_prms += 1

            if parameter.basic and not basic:
                output.append(
                    f"{parameter.name}: Basic parameter in advanced section {self.name}"
                )
            if optional and not parameter.optional:
                output.append(
                    f"{parameter.name}: Mandatory parameter in optional section {self.name}"
                )

        if (n_parameters == 0) and not self.accept_unknown_parameters:
            output.append(
                f"{self.name}: Section without specified parameters which does not accept unknown parameters"
            )
        if basic and (n_parameters > 0) and (n_basic_prms == 0):
            output.append(f"{self.name}: Basic section without any basic parameters")

        control = (self.controller, self.alternatives)
        if any(_elm is None for _elm in control) and any(
            _elm is not None for _elm in control
        ):
            output.append(
                f"{self.name}: Controlled section must have both a controller and alternative parameters"
            )
        elif self.controller is not None:
            if self.controller.section == self.name:
                output.append(f"{self.name}: Section cannot be controlled by itself")
            controlling_values = self.controlling_values
            if controlling_values.__len__() > set(controlling_values).__len__():
                output.append(
                    f"{self.name}: Controlled section has duplicated controller values"
                )
            for parameter in self.all_parameters:
                if not parameter.optional:
                    output.append(
                        f'{parameter.name}: Mandatory parameter in controlled section "{self.name}"'
                    )

        return output

    def AddParameter(self, parameter: parameter_t) -> None:
        """
        For programmatic use
        """
        self.active_parameters.append(parameter)

    def _Item(self, key: str | int) -> parameter_t | None:
        """"""
        if isinstance(key, str):
            for parameter in self.active_parameters:
                if key == parameter.name:
                    return parameter
        else:
            for parameter in self.active_parameters:
                if ((actual := parameter.actual) is not None) and (key == actual.uid):
                    return parameter

        return None

    def __contains__(self, key: str | int) -> bool:
        """"""
        return self._Item(key) is not None

    def __getitem__(self, key: str | int) -> parameter_t:
        """"""
        item = self._Item(key)
        if item is None:
            raise KeyError(f"{key}: Not a parameter of section {self.name}")

        return item

    def __str__(self) -> str:
        """"""
        parameters = (str(_prm) for _prm in self)
        parameters = "\n".join(parameters)
        parameters = text.indent(parameters, "    ")

        return f"{super().__str__()}\n{parameters}"
