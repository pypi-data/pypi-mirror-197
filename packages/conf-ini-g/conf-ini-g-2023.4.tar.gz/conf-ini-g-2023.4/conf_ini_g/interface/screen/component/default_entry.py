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

from typing import Any

from conf_ini_g.interface.screen.library.pyqt5_parameter import simple_entry_wgt_t
from conf_ini_g.specification.constrained_type import constrained_type_t
from conf_ini_g.specification.default import missing_required_value_t
from conf_ini_g.specification.parameter import parameter_t


class default_entry_wgt_t(simple_entry_wgt_t):
    """"""

    @classmethod
    def NewWithDetails(
        cls,
        value: Any | None | missing_required_value_t,
        _: constrained_type_t,
        __: parameter_t,
    ) -> default_entry_wgt_t:
        """"""
        instance = cls()

        if (value is None) or isinstance(value, missing_required_value_t):
            value = ""
        else:
            value = str(value)
        instance.SetText(value)

        return instance

    def Value(self) -> str:
        """
        Cannot be done using: class.Value = class.Text since the Text method is added to instances, not to the class
        """
        return self.Text()
