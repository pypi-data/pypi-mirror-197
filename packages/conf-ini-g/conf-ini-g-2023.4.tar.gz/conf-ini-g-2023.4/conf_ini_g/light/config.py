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

import inspect as nspt
from typing import Any, Callable, Sequence

from conf_ini_g.standard.path_extension import any_path_h, path_t
from conf_ini_g.standard.str_extension import AlignedNameAndValue
from conf_ini_g.standard.type_extension import EducatedValue, Unaliased


config_as_dict_h = dict[str, dict[str, Any]]


class config_t:
    path: path_t
    base_for_relative_paths: path_t
    _annotations: dict[str, Any]

    @classmethod
    def NewFromDictionary(
        cls, as_dict: config_as_dict_h, /, *, path: any_path_h = None
    ) -> config_t:
        """
        The dictionary values are already properly typed
        """
        instance = cls()

        if (path is not None) and isinstance(path, str):
            path = path_t(path)

        instance.path = path
        if path is None:
            instance.base_for_relative_paths = path_t.home()
        else:
            instance.base_for_relative_paths = path.parent
        instance._annotations = nspt.get_annotations(cls)

        for s_name, section in as_dict.items():
            for p_name, value in section.items():
                instance.Set(_FullName(s_name, p_name), value)

        return instance

    def Set(self, name: str, value: Any, /) -> None:
        """"""
        expected_type = Unaliased(self._annotations[name])
        educated = EducatedValue(value, expected_type, self.base_for_relative_paths)

        setattr(self, name, educated)

    def __str__(self) -> str:
        """"""
        output = []

        max_name_length = 0
        AllButCallable = lambda _elm: not isinstance(_elm, Callable)
        for name, value in nspt.getmembers(self, AllButCallable):
            if name[0] != "_":
                if (current_length := name.__len__()) > max_name_length:
                    max_name_length = current_length
                output.append(_FormattedNameAndValue(name, value))
        output = map(
            lambda _elm: AlignedNameAndValue(_elm, max_name_length + 1), output
        )

        return "\n".join(output)


def _FullName(section: str, parameter: str, /) -> str:
    """"""
    return f"{section.strip().lower().replace(' ', '_')}_{parameter.strip().lower()}"


def _FormattedNameAndValue(name: str, value: Any, /) -> str:
    """"""
    if value is None:
        as_str = "None"
    elif isinstance(value, bool):
        as_str = str(value)
    elif isinstance(value, str):
        as_str = f'"{value}"'
    elif isinstance(value, path_t):
        as_str = f"💻{value}"
    else:
        as_str = _FormattedValue(value)

    return f"{name} = {as_str}"


def _FormattedValue(value: Any, /, *, level: int = 0) -> str:
    """"""
    if value is None:
        output = "None"
    elif isinstance(value, bool):
        output = str(value)
    elif isinstance(value, str):
        output = f'"{value}"'
    elif isinstance(value, path_t):
        output = f"💻{value}"
    elif isinstance(value, Sequence):
        output = ", ".join(_FormattedValue(_vle, level=level + 1) for _vle in value)
        if level > 0:
            output = f"({output})"
    else:
        output = f"{value}:{type(value).__name__}"

    return output
