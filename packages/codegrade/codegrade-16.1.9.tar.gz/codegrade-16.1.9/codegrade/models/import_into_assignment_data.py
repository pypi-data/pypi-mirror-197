"""The module that defines the ``ImportIntoAssignmentData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class ImportIntoAssignmentData:
    """Input data required for the `Assignment::ImportInto` operation."""

    #: The id of the assignment from which you want to import the assignment.
    from_assignment_id: "int"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "from_assignment_id",
                rqa.SimpleValue.int,
                doc=(
                    "The id of the assignment from which you want to import"
                    " the assignment."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "from_assignment_id": to_dict(self.from_assignment_id),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["ImportIntoAssignmentData"], d: t.Dict[str, t.Any]
    ) -> "ImportIntoAssignmentData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            from_assignment_id=parsed.from_assignment_id,
        )
        res.raw_data = d
        return res
