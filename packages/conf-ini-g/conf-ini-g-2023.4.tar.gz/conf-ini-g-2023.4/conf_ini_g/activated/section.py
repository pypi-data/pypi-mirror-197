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

from conf_ini_g.activated.parameter import actual_t
from conf_ini_g.specification.parameter import parameter_t
from conf_ini_g.specification.section import section_t
from conf_ini_g.standard.type_extension import UNIVERSAL_ANNOTATED_TYPES


def AddUnknownParameter(section: section_t, name: str, value: str, /) -> None:
    """
    Cannot be a method of specification.section.section_t since a value is set
    """
    parameter = parameter_t(
        name=name,
        definition="On-the-fly parameter",
        description="This parameter is not part of the specification. "
        "It was added programmatically because it was found in the INI document or "
        "passed as a command-line argument",
        basic=section.basic,
        types=UNIVERSAL_ANNOTATED_TYPES,
        default=None,
    )
    actual = actual_t.NewForProgrammaticEntry(value, parameter.type_options)
    parameter.actual = actual

    section.AddParameter(parameter)
