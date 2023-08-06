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

# Necessary since library_wgt_t is not defined until after the call to CreateClassesWithCapitalizedMethods
from __future__ import annotations

from types import BuiltinMethodType, MethodType
from typing import Sequence

import PyQt5.QtCore as core
import PyQt5.QtWidgets as wdgt


# SetCapitalizedMethods does not "see" the methods of the base classes. So for example, calling it on QHBoxLayout has no
# effect on the methods of QLayout. Therefore, it might be necessary to call it also on QLayout even if QLayout is not
# use explicitly.
_CLASSES = (
    ("library_wgt_t", wdgt.QWidget),
    ("layout_t", wdgt.QLayout),
    ("hbox_lyt_t", wdgt.QHBoxLayout),
    ("vbox_lyt_t", wdgt.QVBoxLayout),
    ("grid_lyt_t", wdgt.QGridLayout),
)


def SetCapitalizedMethods(widget: wdgt.QLayout | library_wgt_t) -> None:
    """
    AMethod = wdgt.QSomeWidgetClass.aMethod does not work because the call then misses self
    """
    for name in dir(widget):
        first_letter = name[0]
        # hasattr test: necessary since this function is called early in the initialization process, so some fields
        # might not have been set yet.
        if (
            (first_letter != "_")
            and (first_letter == first_letter.lower())
            and hasattr(widget, name)
        ):
            attribute = getattr(widget, name)
            if isinstance(attribute, (BuiltinMethodType, MethodType)):
                capitalized = first_letter.upper() + name[1:]
                if not hasattr(widget, capitalized):
                    setattr(widget, first_letter.upper() + name[1:], attribute)


def CreateClassesWithCapitalizedMethods(
    classes: Sequence[tuple[str, type]], scope: dict
) -> None:
    """"""
    for new_class, base_class in classes:

        def InitWithMethodCapitalization(self, *args, **kwargs) -> None:
            """"""
            base_class.__init__(self, *args, **kwargs)
            SetCapitalizedMethods(self)

        cls = type(new_class, (base_class,), {})
        setattr(cls, "__init__", InitWithMethodCapitalization)
        scope[new_class] = cls


CreateClassesWithCapitalizedMethods(_CLASSES, globals())


class file_selection_wgt_t(wdgt.QFileDialog):
    """"""

    def __init__(self, caption: str, extension_filter: str = None):
        """"""
        if extension_filter is None:
            extension_filter = "Any files (*)"
        super().__init__(caption=caption, filter=extension_filter)
        SetCapitalizedMethods(self)

    def SelectedFile(self) -> str:
        return self.selectedFiles()[0]

    def RunAndGetClosingStatus(self) -> int:
        return self.exec_()


class widget_event_loop_t(wdgt.QApplication):
    """"""

    @staticmethod
    def GetInstance() -> core.QCoreApplication:
        return widget_event_loop_t.instance()

    @staticmethod
    def Run() -> int:
        return wdgt.QApplication.exec_()


def ShowErrorMessage(message: str, parent: library_wgt_t = None) -> None:
    """"""
    wdgt.QMessageBox.critical(parent, "Error", message)
