from __future__ import annotations

from io import IOBase
from typing import List

from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.document import Document, DocumentSchema
from semantha_sdk.model.document_metadata import DocumentMetadata


class ReferencesEndpoint(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/references"

    def post(
            self,
            file: IOBase = None,
            referencedocument: IOBase = None,
            referencedocumentids: list[str] = None,
            tags: list[str] = None,
            documentclassids: list[str] = None,
            similaritythreshold: float = 0.85,
            synonymousthreshold: float = 0.98,
            marknomatch: bool = False,
            withreferencetext: bool = False,
            withareas: bool = False,
            withcontext: bool = True,
            language: str = None,
            mode: str = "fingerprint",
            documenttype: str = None,
            metadata: list[DocumentMetadata] = None,
            considertexttype: bool = False,
            resizeparagraphs: bool = False,
            detectlanguage: bool = False,
            maxreferences: int = 50
    ) -> Document:
        """ Matches one input document to a set of reference documents.

            If you match against internal library the 'tags' parameter can be used to filter the library.

            Args:
                file (IOBase): Input document (left document).
                referencedocument (IOBase): Reference document(s) to be used instead of the documents in the domain's library.
                referencedocumentids (list[str]): To filter for document IDs. The limit here is 1000 IDs.
                    The IDs are passed as a JSON array.
                tags (str): List of tags to filter the reference library.
                    You can combine the tags using a comma (OR) and using a plus sign (AND).
                documentclassids (list[str]): List of documentclass IDs for the target.
                    The limit here is 1000 IDs. The IDs are passed as a JSON array.
                    This does not apply on the GET referencedocuments call. Here the ids are separated with a comma.
                similaritythreshold (float): Threshold for the similarity score.
                    semantha will not deliver results with a sentence score lower than the threshold.
                    In general, the higher the threshold, the more precise the results.
                synonymousthreshold (float): Threshold for good matches.
                marknomatch (bool): Marks the matches that have not matched.
                withreferencetext (bool): Provide the reference text in the result JSON.
                    If set to false, you have to query the library to resolve the references yourself.
                language (str): The language of the input document (only available if configured for the domain).
                mode (str):
                    Determine references:
                        Mode to enable if a semantic search ("fingerprint") or keyword search ("keyword") should be considered.
                    Creating document model:
                        It also defines what structure should be considered for what operator (similarity or extraction).
                    One of "fingerprint", "keyword", "document" or "auto".
                documenttype (str):
                    Specifies the document type that is to be used by semantha when reading the input document.
                metadata (list[DocumentMetadataDTO]): TBD.
                withcontext (bool): Creates and saves the context.
                withareas (bool): Gives back the coordinates of referenced area.
                considertexttype (bool):
                    Use this parameter to ensure that only paragraphs of the same type are compared with each other.
                    The parameter is of type boolean and is set to false by default.
                resizeparagraphs (bool): Automatically resizes paragraphs based on their semantic meaning.
                detectlanguage (bool):
                    Auto-detect the language of the document.
                maxreferences (int): Maximum number of returned references.
        """
        response = self._session.post(
            self._endpoint,
            body={
                "file": file,
                "referencedocument": referencedocument,
                "referencedocumentids": referencedocumentids,
                "tags": ",".join(tags),
                "documentclassids": documentclassids,
                "similaritythreshold": str(similaritythreshold),
                "synonymousthreshold": str(synonymousthreshold),
                "marknomatch": str(marknomatch),
                "withreferencetext": str(withreferencetext),
                "language": language,
                "mode": mode,
                "documenttype": documenttype,
                "metadata": metadata,
                "withcontext": str(withcontext),
                "considertexttype": str(considertexttype),
                "resizeparagraphs": str(resizeparagraphs),
                "withareas": str(withareas)
            },
            q_params={
                "detectlanguage": str(detectlanguage),
                "maxreferences": maxreferences
            }
        ).execute()
        return response.to(DocumentSchema)
