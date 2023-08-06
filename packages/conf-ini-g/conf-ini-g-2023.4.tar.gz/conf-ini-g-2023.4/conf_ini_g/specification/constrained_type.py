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

import dataclasses as dtcl
from conf_ini_g.standard.path_extension import path_t as pl_path_t
from typing import Annotated, Any, Sequence

import colorama as clrm

from conf_ini_g.specification.constraint import (
    boolean_t,
    choices_t,
    constraint_t,
    number_t,
    path_t,
    sequence_t,
)
from conf_ini_g.standard.str_extension import EvaluatedValue
from conf_ini_g.standard.type_extension import (
    FAKE_TYPE_ANNOTATION,
    AnnotationsOfType,
    PythonTypeOfAnnotated,
    annotated_type_t,
    any_type_and_none_h,
    none_t,
)


any_annotation_h = constraint_t | Any


# Do not use _invalid_value_t = object, for example, otherwise isinstance returns True for anything
class _invalid_value_t:
    """"""

    def __str__(self) -> str:
        """"""
        return f"{clrm.Fore.RED}INVALID VALUE{clrm.Fore.RESET}"


INVALID_VALUE = _invalid_value_t()


@dtcl.dataclass(repr=False, eq=False)
class constrained_type_t:

    py_type: type = None
    annotations: Sequence[any_annotation_h] = None

    @classmethod
    def NewFromType(cls, type_: any_type_and_none_h, /) -> constrained_type_t:
        """"""
        if isinstance(type_, (type, none_t)):
            type_ = Annotated[type_, FAKE_TYPE_ANNOTATION]
        # else: must be annotated_type_t

        return cls.NewFromAnnotatedType(type_)

    @classmethod
    def NewFromAnnotatedType(
        cls, annotated_type: annotated_type_t, /
    ) -> constrained_type_t:
        """"""
        instance = cls()

        instance.py_type = PythonTypeOfAnnotated(annotated_type)
        instance.annotations = AnnotationsOfType(annotated_type)

        return instance

    def Issues(self, name: str, section: str, /) -> Sequence[str]:
        """"""
        output = []

        # self.annotations.__len__() == 0 is OK. It means that there was only a fake annotation, which has been
        # discarded by AnnotationsOfType.
        py_type = self.py_type
        for annotation in self.annotations:
            if hasattr(annotation, "Issues"):
                output.extend(annotation.Issues(py_type, name, section))
            # This was once considered an issue, but it probably isn't
            # else:
            #     output.append(f'{annotation}: Annotation has no "Issues" method')

        return output

    def ContainsOrMatches(
        self,
        expected_annotation: any_annotation_h | Sequence[any_annotation_h],
        /,
        *,
        py_type: type = None,
        full: bool = False,
    ) -> bool:
        """"""
        if (py_type is not None) and (self.py_type is not py_type):
            return False

        ref_types = tuple(type(_nnt) for _nnt in self.annotations)
        if isinstance(expected_annotation, Sequence):
            expected_annotations = expected_annotation
        else:
            expected_annotations = (expected_annotation,)

        if full:
            # Comparing the iterators returns False, hence the conversions to lists (through sorted, which is necessary)
            type_name = lambda _elm: _elm.__name__
            ref_types = sorted(ref_types, key=type_name)
            expected_types = sorted(
                (type(_nnt) for _nnt in expected_annotations), key=type_name
            )

            return ref_types == expected_types
        else:
            n_founds = 0
            for annotation in expected_annotations:
                if isinstance(annotation, ref_types):
                    n_founds += 1

            return n_founds == expected_annotations.__len__()

    def FirstConstraintWithAttribute(
        self, attribute: str | Sequence[str], /
    ) -> any_annotation_h | None:
        """"""
        # Do not test isinstance(attribute, Sequence) since str is a sequence
        if isinstance(attribute, str):
            attributes = (attribute,)
        else:
            attributes = attribute

        for annotation in self.annotations:
            if all(hasattr(annotation, _ttr) for _ttr in attributes):
                return annotation

        return None

    def TypedValue(self, value: Any, /) -> tuple[Any | None, bool]:
        """"""
        failed_conversion = None, False

        if isinstance(value, self.py_type):
            typed_value, success = value, True
        elif isinstance(value, str):
            typed_value, success = EvaluatedValue(value, expected_type=self.py_type)
        else:
            return failed_conversion

        if success:
            for annotation in self.annotations:
                if hasattr(annotation, "ValueIsValid") and not annotation.ValueIsValid(
                    typed_value
                ):
                    return failed_conversion

            return typed_value, True

        return failed_conversion

    def __str__(self) -> str:
        """"""
        if self.py_type is none_t:
            type_name = "None"
        else:
            type_name = self.py_type.__name__
        output = [f"{clrm.Fore.CYAN}{type_name}{clrm.Fore.RESET}"]

        for annotation in self.annotations:
            output.append(str(annotation))

        return " ->\n".join(output)


@dtcl.dataclass(init=False, repr=False, eq=False)
class constrained_types_t(list):
    """"""

    @classmethod
    def NewFromTypes(
        cls, types: Sequence[any_type_and_none_h], /
    ) -> constrained_types_t:
        """"""
        instance = cls()

        idx_o_none = 0
        for t_idx, type_ in enumerate(types):
            cstd_type = constrained_type_t.NewFromType(type_)
            instance.append(cstd_type)
            if cstd_type.py_type is none_t:
                idx_o_none = t_idx

        if idx_o_none > 0:
            keep = instance[idx_o_none]
            del instance[idx_o_none]
            instance.insert(0, keep)

        return instance

    @property
    def n_types(self) -> int:
        """"""
        return self.__len__()

    def Issues(self, name: str, section: str, /) -> Sequence[str]:
        """"""
        output = []

        if self.n_types == 0:
            output.append(f"{section}/{name}: Empty list of allowed types")
        else:
            if (self.n_types == 1) and self.AllowsNone():
                output.append(
                    f'{self}: None cannot be the only allowed type of the optional parameter "{section}/{name}"'
                )
            n_nones = 0
            for cstd_type in self:
                if cstd_type.py_type is none_t:
                    n_nones += 1
                else:
                    output.extend(cstd_type.Issues(name, section))
            if n_nones > 1:
                output.append(
                    f'{self}: None cannot be mentioned more than once for parameter "{section}/{name}"'
                )

        return output

    def AllowsNone(self) -> bool:
        """"""
        return self[0].py_type is none_t

    def MatchingTypeOf(self, py_type: type, /) -> constrained_type_t:
        """"""
        output = None

        for cstd_type in self:
            if cstd_type.py_type is py_type:
                output = cstd_type
                break

        return output

    def TypedValue(self, value: str, /) -> tuple[Any, constrained_type_t | None]:
        """"""
        typed_value = None
        type_spec = None

        success = False
        for cstd_type in self:
            typed_value, success = cstd_type.TypedValue(value)
            if success:
                type_spec = cstd_type
                break

        if not success:
            typed_value = INVALID_VALUE

        return typed_value, type_spec

    def __str__(self) -> str:
        """"""
        output = (str(_typ) for _typ in self)

        return " +\n".join(output)


SIMPLE_ATT_TYPES: dict[str, constrained_type_t] = {
    "boolean": constrained_type_t.NewFromAnnotatedType(Annotated[bool, boolean_t()]),
    "float": constrained_type_t.NewFromAnnotatedType(Annotated[float, number_t()]),
    "int": constrained_type_t.NewFromAnnotatedType(Annotated[int, number_t()]),
    "choices": constrained_type_t.NewFromAnnotatedType(Annotated[str, choices_t()]),
    "path": constrained_type_t.NewFromAnnotatedType(Annotated[pl_path_t, path_t()]),
    "sequence": constrained_type_t.NewFromAnnotatedType(Annotated[tuple, sequence_t()]),
    "None": constrained_type_t.NewFromAnnotatedType(
        Annotated[None, FAKE_TYPE_ANNOTATION]
    ),
}
