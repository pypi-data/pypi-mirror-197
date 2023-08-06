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

from typing import Annotated, Callable, Iterator, Sequence

import conf_ini_g.activated.config as actv
import conf_ini_g.interface.screen.component.file_dialogs as fd_
import conf_ini_g.interface.storage.config as iocf
from conf_ini_g.interface.screen.component.boolean import boolean_wgt_t
from conf_ini_g.interface.screen.library.pyqt5_constant import (
    ALIGNED_HCENTER,
    SELECTABLE_TEXT,
)
from conf_ini_g.interface.screen.library.pyqt5_generic import (
    ShowErrorMessage,
    grid_lyt_t,
    hbox_lyt_t,
    library_wgt_t,
    vbox_lyt_t,
)
from conf_ini_g.interface.screen.library.pyqt5_parameter import (
    button_wgt_t,
    label_wgt_t,
    scroll_container_t,
    tabs_wgt_t,
)
from conf_ini_g.interface.screen.section import controlled_section_t, section_t
from conf_ini_g.raw.config import AsStr, ini_config_h, raw_config_h
from conf_ini_g.specification.config import config_t as config_spec_t
from conf_ini_g.specification.constrained_type import constrained_type_t
from conf_ini_g.specification.constraint import boolean_t, path_t
from conf_ini_g.specification.section import section_t as section_spec_t
from conf_ini_g.standard.path_extension import any_path_h
from conf_ini_g.standard.path_extension import path_t as pl_path_t


class config_t(library_wgt_t):
    __slots__ = (
        "ini_document",
        "target",
        "sections",
    )
    ini_document: pl_path_t | None
    target: config_spec_t
    sections: list[section_t]

    def __init__(self, title: str | None, /) -> None:
        """"""
        super().__init__()
        if title is not None:
            self.SetWindowTitle(title)

        # Do not use self.__class__.__slots__ because it will be the parent slots in case of inheritance
        for slot in config_t.__slots__:
            setattr(self, slot, None)

    @classmethod
    def NewFromConfig(
        cls,
        title: str | None,
        config: config_spec_t,
        /,
        *,
        advanced_mode: bool = False,
        ini_document: any_path_h = None,
        action: tuple[str, Callable[[raw_config_h], None]] = None,
    ) -> config_t:
        """"""
        instance = cls(title)
        if is_linked_to_ini := (ini_document is not None):
            instance.ini_document = pl_path_t(ini_document)
        instance.target = config

        # --- Top-level widgets
        if title is None:
            title_wgt = None
        else:
            title_wgt = label_wgt_t("<b>" + title + "</b>")
            title_wgt.SetAlignment(ALIGNED_HCENTER)
        advanced_mode_lyt = _AdvancedModeLayout(advanced_mode, instance)
        button_lyt = _ActionButtonsLayout(is_linked_to_ini, instance, action)

        # --- Sections
        categories = {}
        sections = []
        controlled_sections = []

        for section in config:
            if section.controller is None:
                visual_section = section_t.NewForSection(section)
            else:
                visual_section = controlled_section_t.NewForSection(section)
                if visual_section is not None:
                    controlled_sections.append((visual_section, section))
            if visual_section is None:
                continue

            sections.append(visual_section)

            if (category_name := section.category) not in categories:
                contents = library_wgt_t(parent=None)
                layout = vbox_lyt_t()
                contents.SetLayout(layout)
                scroll_area = scroll_container_t.NewForWidget(contents)
                categories[category_name] = (layout, scroll_area)

            layout = categories[category_name][0]
            layout.AddWidget(visual_section)

        instance.sections = sections

        if categories.__len__() > 1:
            category_selector = tabs_wgt_t()
            for category_name, (_, scroll_area) in categories.items():
                category_selector.AddTab(scroll_area, category_name)
        else:
            category_name = tuple(categories.keys())[0]
            category_selector = categories[category_name][1]

        for visual_section, section_spec in controlled_sections:
            section_name, uid = actv.ControllerSectionAndUid(section_spec, config)
            parameter = instance[section_name][uid]
            widget = parameter.active_value
            if hasattr(widget, "SetFunction"):
                widget.SetFunction(visual_section.page_stack.SetCurrentIndex)
            else:
                controller = section_spec.controller
                ShowErrorMessage(
                    f'{controller.section}.{controller.parameter}: Controller has no "SetFunction" method; Disabling control'
                )

        # --- Layout...
        layout = grid_lyt_t()
        if title_wgt is None:
            first_available_row = 0
        else:
            layout.AddWidget(title_wgt, 0, 0, 1, 1)
            first_available_row = 1
        layout.AddWidget(category_selector, first_available_row, 0, 1, 1)
        layout.addLayout(advanced_mode_lyt, first_available_row + 1, 0, 1, 1)
        layout.AddLayout(button_lyt, first_available_row + 2, 0, 1, 1)

        instance.SetLayout(layout)
        # --- ...Layout

        instance.ToogleAdvancedMode(advanced_mode)

        return instance

    def UpdateControlOfSection(self, section: section_spec_t, /) -> None:
        """"""
        section_name, uid = actv.ControllerSectionAndUid(section, self.target)
        parameter = self[section_name][uid]
        value = parameter.Value()

        section.controller_value = value

    def ToogleAdvancedMode(self, advanced_mode: bool, /) -> None:
        """"""
        for section_spec, section in zip(self.target, self.sections):
            if section_spec.basic:
                should_check_parameters = True
            elif advanced_mode:
                section.SetVisible(True)
                should_check_parameters = True
            else:
                section.SetVisible(False)
                should_check_parameters = False

            if should_check_parameters:
                active_parameters = section.active_parameters
                active_uids = (_prm.uid for _prm in active_parameters)
                parameter_specs = (section_spec[_uid] for _uid in active_uids)
                for parameter_spec, parameter in zip(
                    parameter_specs, active_parameters
                ):
                    if not parameter_spec.basic:
                        if advanced_mode:
                            parameter.SetVisible(True)
                        else:
                            parameter.SetVisible(False)

    def AsINIConfig(self) -> ini_config_h:
        """"""
        output = {}

        for section_spec, section in zip(self.target, self):
            section_name = section_spec.name
            section_as_dict = {}

            for parameter in section.active_parameters:
                name = self.target[section_name][parameter.uid].name
                section_as_dict[name] = parameter.Text()

            output[section_name] = section_as_dict

        return output

    def ShowInINIFormat(self) -> None:
        """"""
        config = self.AsINIConfig()
        config = AsStr(config, in_html_format=True)
        label = label_wgt_t("<tt>" + config + "<tt/>")
        label.SetStyleSheet("font-weight:bold; padding:20px;")
        label.SetTextInteractionFlags(SELECTABLE_TEXT)
        label.show()

    def SaveToTarget(self) -> Sequence[str] | None:
        """"""
        for section_spec, section in zip(self.target, self):
            if section_spec.controller is not None:
                self.UpdateControlOfSection(section_spec)

            for parameter in section.active_parameters:
                value = parameter.Value()
                parameter_spec = section_spec[parameter.uid]
                parameter_spec.actual.SetTypesAndValueFromString(
                    value, parameter_spec.type_options
                )

        return self.target.Issues(pre_units=False)

    def SaveConfig(self, new_ini: bool, /) -> None:
        #
        do_save = True

        if new_ini:
            doc_name = fd_.SelectedOutputFile(
                "Save Config As",
                "Save Config As",
                mode=path_t.TARGET_TYPE.document,
                valid_types={"Config files": ("ini", "INI")},
            )
            if doc_name is None:
                do_save = False
            else:
                self.ini_document = doc_name
        else:
            pass  # Will overwrite self.ini_document

        if do_save:
            config = self.AsINIConfig()
            error = iocf.SaveRawConfigToINIDocument(config, self.ini_document)
            if error is not None:
                ShowErrorMessage(error, self)

    def __getitem__(
        self, key: str | int
    ) -> section_t | controlled_section_t:
        """"""
        if isinstance(key, str):
            for section, section_spec in zip(self.sections, self.target):
                if key == section_spec.name:
                    return section
        else:
            raise KeyError(
                f"{self.__class__.__name__}: Not meant to be accessed as a list"
            )

        raise KeyError(f"{key}: Not an existing section")

    def __iter__(self) -> Iterator[section_t]:
        """"""
        return iter(self.sections)


def _AdvancedModeLayout(advanced_mode: bool, parent: config_t, /) -> hbox_lyt_t:
    """"""
    output = hbox_lyt_t()

    annotated_type = Annotated[bool, boolean_t(mode=boolean_t.MODE.on_off)]
    att_type = constrained_type_t.NewFromAnnotatedType(annotated_type)
    boolean = boolean_wgt_t.NewWithDetails(
        advanced_mode,
        att_type,
        None,
    )
    boolean.true_btn.toggled.connect(parent.ToogleAdvancedMode)

    output.addWidget(label_wgt_t("<i>Advanced Mode</i>"))
    output.addWidget(boolean)

    return output


def _ActionButtonsLayout(
    has_ini_document: bool,
    parent: config_t,
    action: tuple[str, Callable[[raw_config_h], None]] | None,
    /,
) -> grid_lyt_t:
    #
    buttons = []
    geometries = []

    button = button_wgt_t("Show in INI format")
    button.SetFunction(parent.ShowInINIFormat)
    buttons.append(button)
    geometries.append((0, 0, 1, 2))

    button = button_wgt_t("Save Config As")
    button.SetFunction(lambda: parent.SaveConfig(True))
    buttons.append(button)
    if has_ini_document:
        geometries.append((1, 0, 1, 1))

        button = button_wgt_t("Save Config (Overwriting)")
        button.SetFunction(lambda: parent.SaveConfig(False))
        buttons.append(button)
        geometries.append((1, 1, 1, 1))
    else:
        geometries.append((1, 0, 1, 2))

    if action is None:
        label = "Close"
    else:
        label = action[0]
    button = button_wgt_t(label)
    if action is None:
        function = parent.Close
    else:

        def function():
            issues = parent.SaveToTarget()
            if issues is None:
                config, issues = actv.RawConfigWithConsumedUnits(parent.target)
                if issues is None:
                    button.SetEnabled(False)
                    try:
                        action[1](config)
                    except Exception as exception:
                        ShowErrorMessage(str(exception), parent)
                    button.SetEnabled(True)
                else:
                    ShowErrorMessage("\n".join(issues), parent)
            else:
                ShowErrorMessage("\n".join(issues), parent)

    button.SetFunction(function)
    buttons.append(button)
    geometries.append((2, 0, 1, 2))

    layout = grid_lyt_t()
    for button, geometry in zip(buttons, geometries):
        layout.AddWidget(button, *geometry)
    layout.setContentsMargins(0, 0, 0, 0)

    return layout
