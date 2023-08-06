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

from typing import Sequence

import conf_ini_g.activated.unit as unia
import conf_ini_g.specification.unit as unis
from conf_ini_g.activated.parameter import actual_t
from conf_ini_g.activated.section import AddUnknownParameter
from conf_ini_g.interface.console.config import TransferArgumentsToINIConfig
from conf_ini_g.interface.storage.constant import INI_COMMENT_MARKER
from conf_ini_g.raw.config import ini_config_h, raw_config_h
from conf_ini_g.specification.config import config_t
from conf_ini_g.specification.constant import UNIT_SECTION
from conf_ini_g.specification.section import section_t


STD_UNIT_CONVERSIONS = unis.STD_UNIT_CONVERSIONS


def ActivateFromINIConfig(
    config: config_t,
    ini_config: ini_config_h,
    /,
    *,
    arguments: raw_config_h = None,
) -> tuple[Sequence[str] | None, Sequence[tuple[str, str]]]:
    """"""
    if arguments is not None:
        TransferArgumentsToINIConfig(arguments, ini_config, config)

    issues, for_deferred_check = _SetFromINIConfig(config, ini_config)
    _SetControllerValues(config)
    _AddDefaults(config)

    issues.extend(_Issues(config))
    if issues.__len__() == 0:
        issues = None

    return issues, for_deferred_check


def ControllerSectionAndUid(section: section_t, config: config_t) -> tuple[str, int]:
    """"""
    controller = section.controller
    parameter = config[controller.section][controller.parameter]

    return controller.section, parameter.actual.uid


def RawConfigWithConsumedUnits(
    config: config_t, /
) -> tuple[raw_config_h, Sequence[str] | None]:
    """"""
    raw_config = {}
    issues = []

    if UNIT_SECTION in config:
        unit_conversions = {
            _prm.name: _prm.actual.value for _prm in config[UNIT_SECTION]
        }
    else:
        unit_conversions = {}
    unit_conversions.update(STD_UNIT_CONVERSIONS)

    for section in config:
        section_as_dict = {}

        for parameter in section.active_parameters:
            actual = parameter.actual
            value = actual.value
            unit = actual.unit

            if unit is None:
                converted_value = value
            else:
                conversion_factor = unit_conversions[unit]
                if isinstance(value, Sequence):
                    converted_value = []
                    success = True
                    for element in value:
                        if isinstance(element, (int, float)):
                            converted_value.append(conversion_factor * element)
                        else:
                            success = False
                            issues.append(
                                f"{value}: Value of parameter {parameter.name} does not support unit conversion"
                            )
                            break
                    if success:
                        converted_value = tuple(converted_value)
                    else:
                        converted_value = value
                elif isinstance(value, (int, float)):
                    converted_value = conversion_factor * value
                else:
                    converted_value = value
                    issues.append(
                        f"{value}: Value of parameter {parameter.name} does not support unit conversion"
                    )

            section_as_dict[parameter.name] = converted_value

        raw_config[section.name] = section_as_dict

    if issues.__len__() == 0:
        issues = None

    return raw_config, issues


def _SetFromINIConfig(
    config: config_t, ini_config: ini_config_h, /
) -> tuple[list[str], Sequence[tuple[str, str]]]:
    """"""
    output = []
    for_deferred_check = []

    for section_name, parameters in ini_config.items():
        if section_name in config:
            section = config[section_name]
            if unis.IsUnitSection(section_name):
                unia.AddUnitsToSection(section, parameters)

            for name, value in parameters.items():
                if name in section:
                    actual = actual_t.NewFromINIEntry(
                        value,
                        INI_COMMENT_MARKER,
                        section[name].type_options,
                    )
                    section[name].actual = actual
                elif section.accept_unknown_parameters:
                    AddUnknownParameter(section, name, value)
                    for_deferred_check.append((section_name, name))
                else:
                    output.append(
                        f"{section_name}.{name}: Attempt to add an unknown parameter to a section accepting none"
                    )
        elif unis.IsUnitSection(section_name, possibly_fuzzy=True):
            output.append(
                f'{section_name}: Unit section must respect the following case "{UNIT_SECTION}"'
            )
        else:
            output.append(
                f"{section_name}: Invalid section; Expected={config.valid_section_names}"
            )

    return output, for_deferred_check


def _SetControllerValues(config: config_t) -> None:
    """"""
    for section in config:
        if (controller := section.controller) is not None:
            stc_name, prm_name = controller.section, controller.parameter
            section.controller_value = config[stc_name][prm_name].actual.value


def _AddDefaults(config: config_t, /) -> None:
    #
    has_default_value = []

    for section in config:
        for parameter in section.all_parameters:
            if parameter.optional and (parameter.actual is None):
                actual = actual_t.NewWithDefaultValue(parameter)
                parameter.actual = actual
                has_default_value.append(actual.uid)

    config.has_default_value = tuple(has_default_value)


def _Issues(config: config_t, /) -> Sequence[str]:
    """"""
    output = []

    valid_units = list(STD_UNIT_CONVERSIONS.keys())
    if UNIT_SECTION in config:
        valid_units.extend(_unt.name for _unt in config[UNIT_SECTION])

    for section in config:
        section_name = section.name

        if unis.IsUnitSection(section_name):
            issues = unia.Issues(section)
        else:
            issues = []
            for parameter in section:
                if (actual := parameter.actual) is not None:
                    issues.extend(actual.Issues(parameter.name, section_name))
                    if ((unit := actual.unit) is not None) and (
                        unit not in valid_units
                    ):
                        issues.append(
                            f"{unit}: Invalid unit of parameter {section_name}.{parameter.name}"
                        )

        output.extend(issues)

    return output
