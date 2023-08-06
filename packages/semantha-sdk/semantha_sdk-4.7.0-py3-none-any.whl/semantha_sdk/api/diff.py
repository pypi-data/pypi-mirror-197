from __future__ import annotations

from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.diff import Diff as DiffDTO, DiffSchema


class DiffEndpoint(SemanthaAPIEndpoint):
    """ Create diffs between two texts. """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/diff"

    def post(self, left_text: str, right_text: str) -> list[DiffDTO]:
        """ Create a diff between two given texts.

        Args:
            left_text (object): One of the two texts for the diff.
            right_text (object): The other text for the diff.
        """

        return self._session.post(
            url=self._endpoint,
            body={
                "left": left_text,
                "right": right_text
            }
        ).execute().to(DiffSchema)
