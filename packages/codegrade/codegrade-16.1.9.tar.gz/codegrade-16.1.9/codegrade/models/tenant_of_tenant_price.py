"""The module that defines the ``TenantOfTenantPrice`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class TenantOfTenantPrice:
    """The data you will receive for a tenant of a tenant price."""

    #: The id of the tenant that is connected to this price.
    id: "str"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.str,
                doc="The id of the tenant that is connected to this price.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "id": to_dict(self.id),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["TenantOfTenantPrice"], d: t.Dict[str, t.Any]
    ) -> "TenantOfTenantPrice":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
        )
        res.raw_data = d
        return res
