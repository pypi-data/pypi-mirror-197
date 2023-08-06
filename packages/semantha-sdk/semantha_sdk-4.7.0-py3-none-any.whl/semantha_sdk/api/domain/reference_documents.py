from __future__ import annotations

from io import IOBase
from typing import List

from semantha_sdk import RestClient
from semantha_sdk.api.domain.cluster import DocumentClusterEndpoint
from semantha_sdk.api.model.named_entities import NamedEntitiesEndpoint
from semantha_sdk.api.domain.statistics import StatisticsEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model import Paragraph
from semantha_sdk.model.document import DocumentSchema, Document
from semantha_sdk.model.paragraph import ParagraphSchema, PatchParagraph
from semantha_sdk.model.reference_document import DocumentInformationSchema, ReferenceDocuments, \
    ReferenceDocumentsSchema, DocumentInformation
from semantha_sdk.model.sentence import Sentence, SentenceSchema


class ReferenceDocumentEndpoint(SemanthaAPIEndpoint):
    class ReferenceDocumentParagraphs(SemanthaAPIEndpoint):

        @property
        def _endpoint(self):
            return self._parent_endpoint + "/paragraphs"

        def __call__(self, id: str):
            return ReferenceDocumentEndpoint.ReferenceDocumentParagraphs.ReferenceDocumentParagraph(self._session, self._endpoint, id)

        class ReferenceDocumentParagraph(SemanthaAPIEndpoint):

            def __init__(self, session: RestClient, parent_endpoint: str, id: str):
                super().__init__(session, parent_endpoint)
                self._id = id

            @property
            def _endpoint(self):
                return self._parent_endpoint + f"/{self._id}"

            def get(self) -> Paragraph:
                """ Get the paragraph of the reference document """
                return self._session.get(self._endpoint).execute().to(ParagraphSchema)

            def delete(self):
                """ Delete the paragraph of the reference document """
                self._session.delete(self._endpoint).execute()

            def patch(self, update: PatchParagraph) -> Paragraph:
                """Update the paragraph of the reference document
                Args:
                    update (Paragraph): (partial) paragraph information that should be updated. Please provide an
                                        instance of Paragraph (semantha_sdk.model.Paragraphs.Paragraph). E.g. to alter
                                        (only) the text of the paragraph you can use something like
                                        Paragraph({"text": "updated text"}).
                """
                return self._session.patch(
                    url=self._endpoint,
                    json=ParagraphSchema().dump(update)
                ).execute().to(ParagraphSchema)

    class ReferenceDocumentSentences(SemanthaAPIEndpoint):

        @property
        def _endpoint(self):
            return self._parent_endpoint + "/sentences"

        def __call__(self, id: str):
            return ReferenceDocumentEndpoint.ReferenceDocumentSentences.ReferenceDocumentSentence(self._session, self._endpoint, id)

        class ReferenceDocumentSentence(SemanthaAPIEndpoint):

            def __init__(self, session: RestClient, parent_endpoint: str, id: str):
                super().__init__(session, parent_endpoint)
                self._id = id

            @property
            def _endpoint(self):
                return self._parent_endpoint + f"/{self._id}"

            def get(self) -> Sentence:
                """ Get the paragraph of the reference document """
                return self._session.get(self._endpoint).execute().to(SentenceSchema)

    def __init__(self, session: RestClient, parent_endpoint: str, id: str):
        super().__init__(session, parent_endpoint)
        self._id = id
        self.__child_reference_document_paragraphs = ReferenceDocumentEndpoint.ReferenceDocumentParagraphs(session, self._endpoint)
        self.__child_reference_document_sentences = ReferenceDocumentEndpoint.ReferenceDocumentSentences(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + f"/{self._id}"

    @property
    def paragraphs(self):
        return self.__child_reference_document_paragraphs

    @property
    def sentences(self):
        return self.__child_reference_document_sentences

    def get(self) -> Document:
        """ Get the reference document """
        return self._session.get(self._endpoint).execute().to(DocumentSchema)

    def delete(self):
        """ Delete the reference document """
        self._session.delete(self._endpoint).execute()

    def patch(
            self,
            update: DocumentInformation,
    ) -> DocumentInformation:
        """ Update the document information of the reference document

        Args:
            update (DocumentInformation): (partial) document information that should be updated. Please provide an
                                          instance of DocumentInformation (semantha_sdk.model.ReferenceDocuments.
                                          DocumentInformation). E.g. to alter (only) the name of the document you can
                                          use something like Document({"name": "new name"}).
        """
        return self._session.patch(
            url=self._endpoint,
            json=DocumentSchema().dump(update)
        ).execute().to(DocumentInformationSchema)


class ReferenceDocumentsEndpoint(SemanthaAPIEndpoint):

    def __init__(self, session: RestClient, parent_endpoint: str):
        super().__init__(session, parent_endpoint)
        self.__statistics = StatisticsEndpoint(session, self._endpoint)
        self.__named_entities = NamedEntitiesEndpoint(session, self._endpoint)
        self.__document_clusters = DocumentClusterEndpoint(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/referencedocuments"

    @property
    def statistic(self):
        return self.__statistics

    @property
    def namedentities(self):
        return self.__named_entities

    @property
    def clusters(self):
        return self.__document_clusters

    def get(self,
            offset: int = None,
            limit: int = None,
            filter_documentids: List[str] = None,
            filter_tags: List[str] = None,
            filter_documentclassids: List[str] = None,
            filter_name: str = None,
            filter_createdbefore: int = None,
            filter_createdafter: int = None,
            filter_metadata: str = None,
            filter_comment: str = None,
            sort_by: str = None,
            return_fields: str = None) -> ReferenceDocuments:
        """ Get reference documents (library documents)

        If no parameters are set all reference documents are returned.
        However, the result set can be filtered (filter_*), sorted (sort_by), sliced (offset AND limit) and the returned
        attributes/fields can be manipulated (return_fields) to reduce the size of the response.
        Note that some filters and sorting can only be used iff slicing is used (offset and limit).

        Args:
            offset (int): the start index (inclusive) of the returned slice of reference documents
            limit (int): the end index (exclusive) of the returned slice of reference documents
            filter_documentids: str: the document ids to filter by. Filtering by doc ids can be done without slicing.
            filter_tags (str): the tags to filter by: comma separated lists are interpreted as OR and + is interpreted
                               as AND. E.g. 'a+b,c+d' means a AND b OR c AND d. The tag filter can be used without
                               slicing.
            filter_documentclassids (str): the class ids to filter by. Filtering by class ids can be done without
                                             slicing.
            filter_name (str): filter by (document) name. Can only be used with slicing (offset and limit).
            filter_createdbefore (int): filter by creation date before. Can only be used with slicing (offset and
                                         limit).
            filter_createdafter (int): filter by creation date after. Can only be used with slicing (offset and
                                        limit).
            filter_metadata (str): filter by metadata. Can only be used with slicing (offset and limit).
            filter_comment (str): filter by comment. Can only be used with slicing (offset and limit).
            sort_by (str): (lexically) sort the result by one or more criteria: "name", "filename", "metadata",
                           "created", "updated", "color", "comment", "derivedcolor", "derivedcomment", "documentclass".
                           If a value is prefixed by a '-', the sorting is inverted. Can only be used with slicing
                           (offset and limit). Note that sorting is performed before slicing.
            return_fields (str): limit the returned fields to the defined (instead of a full response): "id", "name",
                                 "tags", "derivedtags", "metadata", "filename", "created", "processed", "lang",
                                 "updated", "color", "derivedcolor", "comment", "derivedcomment", "documentclass",
                                 "contentpreview"
        """
        if (offset is None and limit is not None) or (limit is None and offset is not None):
            raise ValueError("'limit' and 'offset' must be set together.")
        if offset is None and limit is None:
            if filter_documentids is not None:
                raise ValueError("filter by document id can only be used if 'limit' and 'offset' are set")
            if filter_name is not None:
                raise ValueError("filter by name can only be used if 'limit' and 'offset' are set")
            if filter_createdbefore is not None:
                raise ValueError("filter by 'created before' can only be used if 'limit' and 'offset' are set")
            if filter_createdafter is not None:
                raise ValueError("filter by 'created after' can only be used if 'limit' and 'offset' are set")
            if filter_metadata is not None:
                raise ValueError("filter by metadata can only be used if 'limit' and 'offset' are set")
            if filter_comment is not None:
                raise ValueError("filter by comment can only be used if 'limit' and 'offset' are set")
            if sort_by is not None:
                raise ValueError("sorting can only activated if 'limit' and 'offset' are set")

        q_params = {}
        if filter_tags is not None:
            q_params["tags"] = ",".join(filter_tags)
        if filter_documentclassids is not None:
            q_params["documentclassids"] = ",".join(filter_documentclassids)
        if return_fields is not None:
            q_params["fields"] = return_fields
        if offset is not None and limit is not None:
            q_params["offset"] = offset
            q_params["limit"] = limit
            if filter_documentids is not None:
                q_params["documentids"] = ",".join(filter_documentids)
            if filter_name is not None:
                q_params["name"] = filter_name
            if filter_createdbefore is not None:
                q_params["createdbefore"] = filter_createdbefore
            if filter_createdafter is not None:
                q_params["createdafter"] = filter_createdafter
            if filter_metadata is not None:
                q_params["metadata"] = filter_metadata
            if filter_comment is not None:
                q_params["comment"] = filter_comment
            if sort_by is not None:
                q_params["sort"] = sort_by

        return self._session.get(self._endpoint, q_params=q_params).execute().to(ReferenceDocumentsSchema)

    def delete(self):
        """ Delete all reference documents """
        self._session.delete(self._endpoint).execute()

    def post(
            self,
            name: str = None,
            tags: str = None,
            metadata: str = None,
            file: IOBase = None,
            documenttype: str = None,
            color: str = None,
            comment: str = None,
            detectlanguage: bool = False,
            addparagraphsasdocuments: bool = False
    ) -> list[DocumentInformation]:
        """ Upload a reference document

        Args:
            name (str): The document name in your library (in contrast to the file name being used during upload).
            tags (str): List of tags to filter the reference library.
                You can combine the tags using a comma (OR) and using a plus sign (AND).
            metadata (str): Use this parameter to add a meta data to your library item.
            file (IOBase): Input document as file like object.
            documenttype (str): Specifies the document type that is to be used when processing the document.
            color (str): Use this parameter to specify the color for your reference document.
                Possible values are RED, MAGENTA, AQUA, ORANGE, GREY, or LAVENDER.
            comment (str): Use this parameter to add a comment to your library item.
            detectlanguage (bool): Auto-detect the language of the document and add it to library if 'domain language'=='document language'.
            addparagraphsasdocuments (bool): If true a library item for every paragraph in this document is added.
        """
        return self._session.post(
            self._endpoint,
            body={
                "name": name,
                "tags": tags,
                "metadata": metadata,
                "file": file,
                "documenttype": documenttype,
                "color": color,
                "comment": comment,
                "addparagraphsasdocuments": addparagraphsasdocuments
            },
            q_params={
                "detectlanguage": str(detectlanguage)
            }
        ).execute().to(DocumentInformationSchema)

    def __call__(self, id: str):
        return ReferenceDocumentEndpoint(self._session, self._endpoint, id)
