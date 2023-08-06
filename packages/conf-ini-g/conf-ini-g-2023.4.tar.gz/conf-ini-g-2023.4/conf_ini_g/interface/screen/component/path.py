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

from conf_ini_g.standard.path_extension import path_t as pl_path_t
from typing import Callable

import conf_ini_g.interface.screen.component.file_dialogs as fd_
from conf_ini_g.interface.screen.library.pyqt5_generic import hbox_lyt_t, library_wgt_t
from conf_ini_g.interface.screen.library.pyqt5_parameter import (
    button_wgt_t,
    simple_entry_wgt_t,
)
from conf_ini_g.specification.constrained_type import constrained_type_t
from conf_ini_g.specification.constraint import path_t
from conf_ini_g.specification.default import missing_required_value_t
from conf_ini_g.specification.parameter import parameter_t


class path_wgt_t(library_wgt_t):

    __slots__ = (
        "target_type",
        "path",
        "SelectedFile",
    )
    target_type: path_t.TARGET_TYPE
    path: simple_entry_wgt_t
    SelectedFile: Callable[..., pl_path_t | None]

    def __init__(self, parent: library_wgt_t = None) -> None:
        """"""
        super().__init__(parent=parent)
        # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
        for slot in path_wgt_t.__slots__:
            setattr(self, slot, None)

    @classmethod
    def NewWithDetails(
        cls,
        value: pl_path_t | None | missing_required_value_t,
        att_type: constrained_type_t,
        _: parameter_t,
    ) -> path_wgt_t:
        """
        If att_type does not contain the necessary details, the target type is set to any and considered as input, and
        the selection button label ends with an exclamation point.
        """
        instance = cls()

        if (value is None) or isinstance(value, missing_required_value_t):
            value = ""
        else:
            value = str(value)

        annotation = att_type.FirstConstraintWithAttribute(("target_type", "is_input"))
        if annotation is None:
            target_type = path_t.TARGET_TYPE.any
            is_input = True
            misses_details = True
        else:
            target_type = annotation.target_type
            is_input = annotation.is_input
            misses_details = False

        instance.target_type = target_type
        if is_input:
            instance.SelectedFile = fd_.SelectedInputFile
        else:
            instance.SelectedFile = fd_.SelectedOutputFile

        selector_label = "..."
        if misses_details:
            selector_label += "!"
        path = simple_entry_wgt_t(value, parent=instance)
        path_selector = button_wgt_t(selector_label, parent=instance)
        path_selector.SetFunction(instance.SelectDocument)

        instance.path = path

        path_selector.setFixedWidth(30)

        layout = hbox_lyt_t()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.AddWidget(path)
        layout.AddWidget(path_selector)
        instance.setLayout(layout)

        return instance

    def Text(self) -> str:
        """"""
        return self.path.Text().strip()

    def Value(self) -> pl_path_t | None:
        """"""
        text = self.Text()
        if text.__len__() > 0:
            value = pl_path_t(text)
        else:
            value = None

        return value

    def SelectDocument(self) -> None:
        """"""
        current_path = self.Text()
        current_doc = pl_path_t(current_path).resolve()

        if self.target_type is path_t.TARGET_TYPE.document:
            title = "Select File"
        elif self.target_type is path_t.TARGET_TYPE.folder:
            title = "Select Folder"
        else:
            title = "Select File or Folder"

        selection = self.SelectedFile(
            title,
            title,
            mode=self.target_type,
            start_folder=current_doc.parent,
            initial_selection=current_doc,
        )
        if selection is None:
            return

        self.path.setText(str(selection))
