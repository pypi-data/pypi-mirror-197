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

from typing import Any

import colorama as clrm

from conf_ini_g.standard.str_extension import Flattened


# Straight from the INI document, without value interpretation
ini_config_h = dict[str, dict[str, str]]
raw_config_h = dict[str, dict[str, Any]]  # With interpreted values
any_raw_config_h = ini_config_h | raw_config_h


def AsStr(config: any_raw_config_h, /, *, in_html_format: bool = False) -> str:
    """"""
    output = []

    if in_html_format:
        section_color = '<span style="color:green">'
        parameter_color = '<span style="color:blue">'
        color_reset = "</span>"
        newline = "<br/>"
        indentation = "&nbsp;"
    else:
        section_color = clrm.Fore.GREEN
        parameter_color = clrm.Fore.BLUE
        color_reset = clrm.Fore.RESET
        newline = "\n"
        indentation = " "

    longest = 0
    for section, parameters in config.items():
        if parameters.__len__() == 0:
            continue

        inner_output = []
        lengths = []
        for name, value in parameters.items():
            length = name.__len__()
            lengths.append(length)
            longest = max(longest, length)

            flattened = Flattened(str(value))
            inner_output.append(f"{parameter_color}{name}{color_reset}@= {flattened}")

        output.append(
            (f"{section_color}[{section}]{color_reset}", inner_output, lengths)
        )

    output = (
        f"{_sct}{newline}"
        + newline.join(
            _lne.replace("@", (longest - _lgt + 1) * indentation, 1)
            for _lne, _lgt in zip(_prm, _lgs)
        )
        for _sct, _prm, _lgs in output
    )

    return f"{newline}{newline}".join(output)
