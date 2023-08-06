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

from typing import Sequence

from conf_ini_g.interface.screen.library.pyqt5_generic import library_wgt_t
from conf_ini_g.interface.screen.library.pyqt5_parameter import (
    choices_list_wgt_t,
    label_wgt_t,
)
from conf_ini_g.specification.constrained_type import constrained_type_t
from conf_ini_g.standard.type_extension import none_t


single_type_wgt_t = label_wgt_t


class multiple_types_wgt_t(choices_list_wgt_t):
    """"""

    def __init__(
        self,
        types: Sequence[constrained_type_t],
        selected_type: constrained_type_t,
        parent: library_wgt_t = None,
    ) -> None:
        """"""
        super().__init__(parent=parent)

        for type_ in types:
            if type_.py_type is none_t:
                self.AddItem("None")
            else:
                self.AddItem(type_.py_type.__name__)
        self.SetCurrentText(selected_type.py_type.__name__)

    def Value(self) -> str:
        """
        Cannot be done using: class.Value = class.Text since the Text method is added to instances, not to the class
        """
        return self.Text()
