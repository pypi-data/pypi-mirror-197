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

from conf_ini_g.interface.screen.library.pyqt5_generic import hbox_lyt_t, library_wgt_t
from conf_ini_g.interface.screen.library.pyqt5_parameter import choices_dots_wgt_t
from conf_ini_g.specification.constrained_type import constrained_type_t
from conf_ini_g.specification.default import missing_required_value_t
from conf_ini_g.specification.parameter import parameter_t


class boolean_wgt_t(library_wgt_t):

    __slots__ = ("true_btn",)
    true_btn: choices_dots_wgt_t

    def __init__(self, parent: library_wgt_t = None) -> None:
        """"""
        super().__init__(parent=parent)
        # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
        for slot in boolean_wgt_t.__slots__:
            setattr(self, slot, None)

    @classmethod
    def NewWithDetails(
        cls,
        value: bool | None | missing_required_value_t,
        att_type: constrained_type_t,
        _: parameter_t | None,
    ) -> boolean_wgt_t:
        """
        If att_type does not contain the necessary details, an exclamation point is added to the default values.
        """
        instance = cls()

        # TODO: can be None: see interface.screen.parameter.NewForParameter. But can it be missing_required_value_t?
        #     If yes, comment how.
        if (value is None) or isinstance(value, missing_required_value_t):
            value = True

        annotation = att_type.FirstConstraintWithAttribute("mode")
        if annotation is None:
            labels = ("True!", "False!")
        else:
            labels = getattr(annotation.mode, "value", None)
            if labels is None:
                labels = ("True!", "False!")

        true_btn = choices_dots_wgt_t(labels[0], parent=instance)
        false_btn = choices_dots_wgt_t(labels[1], parent=instance)
        true_btn.SetChecked(value)
        false_btn.SetChecked(not value)

        instance.true_btn = true_btn

        layout = hbox_lyt_t()
        layout.SetContentsMargins(0, 0, 0, 0)
        layout.addWidget(true_btn)
        layout.addWidget(false_btn)
        instance.setLayout(layout)

        return instance

    def Text(self) -> str:
        return str(self.Value())

    def Value(self) -> bool:
        return self.true_btn.isChecked()
