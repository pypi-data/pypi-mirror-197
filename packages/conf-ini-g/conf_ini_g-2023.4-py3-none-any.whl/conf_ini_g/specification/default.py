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
from typing import Sequence

import colorama as clrm

from conf_ini_g.specification.constrained_type import (
    constrained_type_t,
    constrained_types_t,
)
from conf_ini_g.standard.type_extension import any_type_h


@dtcl.dataclass(repr=False, eq=False)
class missing_required_value_t:
    """
    types:
        Used at instantiation time: missing_required_value_t(types=...) (types= can be omitted). It is set to None in
        __post_init__.
    type_options:
        Used internally after conversion to constrained_type_t
    """

    types: any_type_h | Sequence[any_type_h] = None
    type_options: constrained_types_t = dtcl.field(init=False)

    def __post_init__(self):
        """"""
        if isinstance(self.types, Sequence):
            types = self.types
        else:
            types = (self.types,)

        self.types = None
        self.type_options = constrained_types_t.NewFromTypes(types)

    @classmethod
    def NewFromConstrainedType(
        cls, cstd_type: constrained_type_t | Sequence[constrained_type_t], /
    ):
        """"""
        instance = cls()

        while instance.type_options.__len__() > 0:
            del instance.type_options[0]
        if isinstance(cstd_type, Sequence):
            instance.type_options.extend(cstd_type)
        else:
            instance.type_options.append(cstd_type)

        return instance

    @property
    def main_type(self) -> constrained_type_t:
        """"""
        return self.type_options[0]

    def Issues(self, name: str, section: str, /) -> Sequence[str]:
        """"""
        output = []

        if self.type_options.__len__() == 0:
            output.append(
                f"{section}/{name}: No types specified for mandatory parameter"
            )
        else:
            if self.type_options.AllowsNone():
                output.append(
                    f'{self.type_options}: None among types of mandatory parameter "{section}/{name}"'
                )
            output.extend(self.type_options.Issues(name, section))

        return output

    def __str__(self) -> str:
        """"""
        types = [str(_typ) for _typ in self.type_options]
        if types.__len__() > 1:
            among = " among"
            types_as_str = ", ".join(types)
        else:
            among = ""
            types_as_str = types[0]

        return f"{clrm.Fore.RED}REQUIRED VALUE{clrm.Fore.RESET} with TYPE{among}: {types_as_str}"
