"""The module that defines the ``RenameGroupGroupData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class RenameGroupGroupData:
    """Input data required for the `Group::RenameGroup` operation."""

    #: The new name of the group
    name: "str"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc="The new name of the group",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["RenameGroupGroupData"], d: t.Dict[str, t.Any]
    ) -> "RenameGroupGroupData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
        )
        res.raw_data = d
        return res
