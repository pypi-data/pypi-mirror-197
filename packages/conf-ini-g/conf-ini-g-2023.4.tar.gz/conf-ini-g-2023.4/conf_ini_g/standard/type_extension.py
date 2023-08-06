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

from types import GenericAlias
from typing import Annotated, Any, Sequence, get_args, get_origin

from conf_ini_g.standard.path_extension import PathFromComponents, path_t


none_t = type(None)
annotated_type_t = type(Annotated[object, None])
any_type_h = type | annotated_type_t
any_type_and_none_h = any_type_h | None


FAKE_TYPE_ANNOTATION = None
UNIVERSAL_ANNOTATED_TYPE = Annotated[object, FAKE_TYPE_ANNOTATION]
UNIVERSAL_ANNOTATED_TYPES = (None, UNIVERSAL_ANNOTATED_TYPE)


def Unaliased(alias: GenericAlias | type, /) -> type:
    """"""
    type_ = get_origin(alias)
    if type_ is None:
        return alias

    return type_(Unaliased(_elm) for _elm in get_args(alias))


def PythonTypeOfAnnotated(annotated_type: annotated_type_t) -> type:
    """"""
    return annotated_type.__args__[0]


def AnnotationsOfType(annotated_type: annotated_type_t) -> Sequence[Any]:
    """"""
    return tuple(
        _nnt for _nnt in annotated_type.__metadata__ if _nnt is not FAKE_TYPE_ANNOTATION
    )


def EducatedValue(
    value: Any, expected_type: Any, base_for_relative_paths: path_t | None, /
) -> Any:
    """
    Mostly checks that the value has the expected type, "slightly" converting it along the way. The slight conversions
    are:
    - str | list[str] | tuple[str, ...] -> path
    - Any -> tuple of appropriate elements if tuple expected

    See EducatedString.
    """
    # TODO: The parenthesis management might need a rethinking in EducatedValue or wherever appropriate
    if value is None:
        return None

    if isinstance(expected_type, type):
        expects_path = issubclass(expected_type, path_t)
        if expects_path and isinstance(value, str):
            output = expected_type(value)
        elif expects_path and isinstance(value, list | tuple):
            output = expected_type(PathFromComponents(*value))
        elif isinstance(value, expected_type):
            output = value
        else:
            raise TypeError(
                f'{value}: Value of type "{type(value).__name__}". Expected={expected_type}.'
            )

        if expects_path and not output.is_absolute():
            output = (base_for_relative_paths / output).resolve(strict=True)

        return output

    if isinstance(expected_type, Sequence):
        if isinstance(expected_type, tuple):
            if value.__len__() != expected_type.__len__():
                raise TypeError(
                    f"{value}: Invalid length of {value.__len__()}. Expected={expected_type.__len__()}."
                )

            output = tuple(
                EducatedValue(_elm, _typ, base_for_relative_paths)
                for _elm, _typ in zip(value, expected_type)
            )
        elif isinstance(expected_type, list) and (expected_type.__len__() == 1):
            if (
                isinstance(value, str)
                or not isinstance(value, Sequence)
                or _ValueMatchesExpectedItems(value, expected_type[0])
            ):
                value = [value]
            output = tuple(
                EducatedValue(_elm, expected_type[0], base_for_relative_paths)
                for _elm in value
            )
        else:
            raise TypeError(f"{expected_type}: Invalid sequence type of expected type")

        return output

    raise TypeError(f"{expected_type}: Invalid value of expected type")


def _ValueMatchesExpectedItems(value: Sequence, expected_type: Any, /) -> bool:
    """"""
    if isinstance(expected_type, type):
        return isinstance(value, expected_type)

    if isinstance(expected_type, Sequence):
        if isinstance(expected_type, tuple):
            if value.__len__() != expected_type.__len__():
                return False

            return all(
                _ValueMatchesExpectedItems(_elm, _typ)
                for _elm, _typ in zip(value, expected_type)
            )
        elif isinstance(expected_type, list) and (expected_type.__len__() == 1):
            # TODO: not sure if the following call accounts for all cases, but it worked so far
            return _ValueMatchesExpectedItems(value, expected_type[0])
        else:
            raise TypeError(f"{expected_type}: Invalid sequence type of expected type")
    else:
        raise TypeError(f"{expected_type}: Invalid value of expected type")


def EducatedString(value: Any, /, *, level: int = 0) -> str:
    """
    See EducatedValue.
    """
    # Test this first since strings are also sequences
    if isinstance(value, str):
        return value

    if isinstance(value, Sequence):
        output = ", ".join(EducatedString(_elm, level=level + 1) for _elm in value)
        if level > 0:
            return f"({output})"
        else:
            return output

    if isinstance(value, path_t):
        return ", ".join(value.parts)

    return str(value)
