"""The endpoints for webhook objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import os
import typing as t

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from .. import parsers, utils

if t.TYPE_CHECKING or os.getenv("CG_EAGERIMPORT", False):
    import codegrade


_ClientT = t.TypeVar("_ClientT", bound="codegrade.client._BaseClient")


class WebhookService(t.Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: _ClientT) -> None:
        self.__client = client

    def delete_webhook(
        self: "WebhookService[codegrade.client.AuthenticatedClient]",
        *,
        webhook_id: "str",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "None":
        """Deletes a specific webhook given its uuid.

        :param webhook_id: The id of the webhook to delete.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """

        url = "/api/v1/webhooks/{webhookId}".format(webhookId=webhook_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.delete(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 204):
            # fmt: off
            # fmt: on
            return parsers.ConstantlyParser(None).try_parse(resp)

        from ..models.any_error import AnyError

        raise utils.get_error(
            resp,
            (
                (
                    (400, 409, 401, 403, 404, "5XX"),
                    utils.unpack_union(AnyError),
                ),
            ),
        )
