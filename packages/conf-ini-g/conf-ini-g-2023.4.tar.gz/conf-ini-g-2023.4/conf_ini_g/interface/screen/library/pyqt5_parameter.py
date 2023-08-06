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

from typing import Callable

import PyQt5.QtWidgets as wdgt

from conf_ini_g.interface.screen.library.pyqt5_generic import (
    CreateClassesWithCapitalizedMethods,
    SetCapitalizedMethods,
    library_wgt_t,
)


_CLASSES = (
    ("label_wgt_t", wdgt.QLabel),
    ("simple_entry_wgt_t", wdgt.QLineEdit),
    ("group_wgt_t", wdgt.QGroupBox),
    ("stack_wgt_t", wdgt.QStackedWidget),
    ("tabs_wgt_t", wdgt.QTabWidget),
)


class button_wgt_t(wdgt.QPushButton):
    """"""

    def __init__(self, text: str, parent: library_wgt_t = None):
        """"""
        super().__init__(text=text, parent=parent)
        SetCapitalizedMethods(self)

    def SetFunction(self, function: Callable) -> None:
        self.clicked.connect(function)


class choices_dots_wgt_t(wdgt.QRadioButton):
    """"""

    def __init__(self, text: str, parent: library_wgt_t = None):
        """"""
        super().__init__(text=text, parent=parent)
        SetCapitalizedMethods(self)

    def SetFunction(self, function: Callable) -> None:
        self.clicked.connect(function)


class choices_list_wgt_t(wdgt.QComboBox):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        SetCapitalizedMethods(self)

    def Selection(self) -> str:
        return self.currentText()

    def SelectionIndex(self) -> int:
        return self.currentIndex()

    def ItemAt(self, index: int) -> str:
        return self.itemText(index)

    def SetFunction(self, function: Callable) -> None:
        self.activated.connect(function)
        # OR: self.currentTextChanged.connect(function)


class scroll_container_t(wdgt.QScrollArea):
    """"""

    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        SetCapitalizedMethods(self)

    @classmethod
    def NewForWidget(cls, widget: library_wgt_t) -> scroll_container_t:
        """"""
        instance = cls()
        instance.setWidget(widget)
        instance.setWidgetResizable(True)
        # instance.setBackgroundRole(qg_.QPalette.Dark)

        return instance


CreateClassesWithCapitalizedMethods(_CLASSES, globals())
