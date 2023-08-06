from __future__ import annotations

from io import IOBase

from semantha_sdk import RestClient
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.document import DocumentSchema


class DocumentEndpoint(SemanthaAPIEndpoint):

    def __init__(self, session: RestClient, parent_endpoint: str, id: str):
        super().__init__(session, parent_endpoint)
        self._id = id

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/" + self._id

    def get(self):
        return self._session.get(self._endpoint).execute().to(DocumentSchema)


class DocumentsEndpoint(SemanthaAPIEndpoint):
    """ /api/{domainname}/documents endpoint. """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/documents"

    def post(
            self,
            file: IOBase = None,
            type: str = "similarity",
            documenttype: str = None,
            withareas: bool = False,
            withcontext: bool = True,
            mode: str = "sentence",
            withparagraphtype: bool = False
    ) -> list[DocumentEndpoint]:
        """ Create a document model

        Args:

            file (IOBase): Input document (as file)
            type (str): Enum: "similarity" "extraction". Choose the structure of a document
                for similarity or extraction. The type depends on the Use Case you're in.
            documenttype (str): Specifies the document type that is to be used by semantha
                when reading the uploaded PDF document.
            withareas (bool): Gives back the coordinates of referenced area.
            withcontext (bool): Creates and saves the context.
            mode (str): 'paragraph' or 'sentence'
            withparagraphtype (bool): The type of the paragraph, for example heading, text.
        """
        return self._session.post(
            self._endpoint,
            body={
                "file": file,
                "type": type,
                "documenttype": documenttype,
                "withareas": str(withareas),
                "withcontext": str(withcontext),
                "mode": mode,
                "withparagraphtype": str(withparagraphtype)
            }
        ).execute().to(DocumentSchema)

    def __call__(self, id: str):
        return DocumentEndpoint(self._session, self._endpoint, id)
