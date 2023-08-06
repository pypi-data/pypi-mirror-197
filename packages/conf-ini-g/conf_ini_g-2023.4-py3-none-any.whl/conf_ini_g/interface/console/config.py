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

import re as rgex
from argparse import ArgumentParser as argument_parser_t
from typing import Any, Iterator, Sequence

import colorama as clrm

from conf_ini_g.interface.console.generic import DisplayErrorAndQuit
from conf_ini_g.raw.config import ini_config_h, raw_config_h
from conf_ini_g.specification.config import config_t
from conf_ini_g.specification.default import missing_required_value_t
from conf_ini_g.standard.str_extension import Flattened


parsed_arguments_h = dict[str, str]


# Specified INI document file is stored in INI_DOCUMENT_VARIABLE
INI_DOCUMENT_VARIABLE = "ini_document"

ADVANCED_MODE_OPTION = "advanced-mode"
ADVANCED_MODE_VARIABLE = "advanced_mode"

# Usage: {section_name}{SECTION_PARAMETER_SEPARATOR}{parameter_name}
SECTION_PARAMETER_SEPARATOR = "-"


def CommandLineParser(
    description: str | None, specification: config_t, /
) -> argument_parser_t:
    """"""
    output = argument_parser_t(description=description, allow_abbrev=False)
    output.add_argument(
        dest=INI_DOCUMENT_VARIABLE,
        help="Path to INI configuration file",
        default=None,
        nargs="?",
        metavar="INI_config_file",
    )

    for section in specification:
        for parameter in section.all_parameters:
            option = f"{section.name}{SECTION_PARAMETER_SEPARATOR}{parameter.name}"
            if option == ADVANCED_MODE_OPTION:
                # Raising an exception is adapted here since execution has been launched from command line
                DisplayErrorAndQuit(
                    f"{option}: Configuration section and parameter colliding with advanced mode option"
                )

            attribute = f"{section.name}{SECTION_PARAMETER_SEPARATOR}{parameter.name}"

            # Default is a missing_required_value_t instance to avoid overwriting if in INI but not passed
            type_options = parameter.type_options
            default = missing_required_value_t.NewFromConstrainedType(type_options)

            if parameter.optional:
                if isinstance(parameter.default, str):
                    delimiter = '"'
                else:
                    delimiter = ""
                types_and_value = (
                    f"Options: {type_options}. "
                    f"Default: {clrm.Fore.GREEN}{delimiter}{parameter.default}{delimiter}{clrm.Fore.RESET}"
                )
            else:
                types_and_value = str(default)
            flattened = Flattened(types_and_value)
            definition = f"{parameter.definition}. {flattened}"

            # Type could be PythonTypeOfAnnotated(cmd_line_type). However, to allow passing any of the allowed types,
            # deferring type validation to functional config instantiation, this parameter is not passed.
            output.add_argument(
                f"--{option}",
                dest=attribute,
                help=definition,
                default=default,
                metavar=attribute,
            )

    output.add_argument(
        f"--{ADVANCED_MODE_OPTION}",
        dest=ADVANCED_MODE_VARIABLE,
        help="Toggle display of advanced sections and parameters",
        action="store_true",
    )

    return output


def ParsedArguments(
    parser: argument_parser_t, /, *, arguments: Sequence[str] = None
) -> tuple[str | None, bool, raw_config_h]:
    """"""
    parsed, unknowns = parser.parse_known_args(args=arguments)
    parsed = vars(parsed)

    advanced_mode = parsed[ADVANCED_MODE_VARIABLE]
    del parsed[ADVANCED_MODE_VARIABLE]

    ini_document = parsed[INI_DOCUMENT_VARIABLE]
    del parsed[INI_DOCUMENT_VARIABLE]

    pattern = rgex.compile(
        r"--(\w+)" + SECTION_PARAMETER_SEPARATOR + r"(\w+)=(.+)", flags=rgex.ASCII
    )
    for unknown in unknowns:
        match = pattern.fullmatch(unknown)
        if match is None:
            # Raising an exception is adapted here since execution has been launched from command line
            DisplayErrorAndQuit(
                f"{unknown}: Invalid option syntax; Expected=--SECTION-PARAMETER=VALUE"
            )

        section, parameter, value = match.groups()
        parsed[f"{section}{SECTION_PARAMETER_SEPARATOR}{parameter}"] = value

    parsed_as_ini = {}
    for sct_name, prm_name, value in _SectionParameterValueIterator(parsed):
        if sct_name in parsed_as_ini:
            parsed_as_ini[sct_name][prm_name] = value
        else:
            parsed_as_ini[sct_name] = {prm_name: value}

    return ini_document, advanced_mode, parsed_as_ini


def TransferArgumentsToINIConfig(
    arguments: raw_config_h, config: ini_config_h, specification: config_t
) -> None:
    """
    Raising an exception is adapted here since execution has been launched from command line
    """
    for sct_name, parameters in arguments.items():
        if sct_name not in specification:
            DisplayErrorAndQuit(
                f"{sct_name}: Invalid section; Expected={specification.valid_section_names}"
            )
        section = specification[sct_name]

        for prm_name, value in parameters.items():
            if (prm_name in section) or section.accept_unknown_parameters:
                if sct_name not in config:
                    config[sct_name] = {}
                config[sct_name][prm_name] = value
            else:
                DisplayErrorAndQuit(
                    f"{sct_name}.{prm_name}: Attempt to add an unknown parameter to a section accepting none"
                )


def _SectionParameterValueIterator(
    arguments: parsed_arguments_h,
) -> Iterator[tuple[str, str, Any]]:
    """"""
    for prm_uid, value in arguments.items():
        # See CommandLineParser for why this can happen
        if isinstance(value, missing_required_value_t):
            continue

        section, parameter = prm_uid.split(SECTION_PARAMETER_SEPARATOR)
        yield section, parameter, value
