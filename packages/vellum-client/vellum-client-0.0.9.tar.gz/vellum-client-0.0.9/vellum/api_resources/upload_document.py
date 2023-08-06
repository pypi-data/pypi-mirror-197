from typing import IO, List, Optional

from vellum.api_resources.abstract.documents_api_resource import DocumentsAPIResource
from vellum.api_resources.types import DocumentUploadResult


class UploadDocument(DocumentsAPIResource):
    api_path = "v1/upload-document"

    @classmethod
    def run(  # type: ignore
        cls,
        file: IO,
        label: str,
        index_id: Optional[str] = None,
        index_name: Optional[str] = None,
        external_id: Optional[str] = None,
        keywords: Optional[List[str]] = None,
    ) -> DocumentUploadResult:
        """Upload a document to later search across it.

        Args:
            file: The contents of the file that you'd like to upload
            label: A human-friendly name for the document. Typically the file name.
            index_id: The ID of the document index that you'd like to search across. You must provide either this
                or index_name.
            index_name: The name of the document index that you'd like to search across. You must provide either
                this or index_id.
            external_id: Optionally include a unique ID from your system to this document later.
                Useful if you want to perform updates later.
            keywords: Optionally include keywords to associate with the document that can be used in hybrid search.
        Returns:
            The result of the document upload request.
        """

        if index_id is None and index_name is None:
            raise ValueError("Must provide either index_id or index_name")
        elif index_id is not None and index_name is not None:
            raise ValueError("Must provide only one of index_id or index_name")

        raw_result = super().run(
            file=file,
            label=label,
            index_id=index_id,
            index_name=index_name,
            external_id=external_id,
            keywords=keywords,
        )

        return DocumentUploadResult.from_raw(raw_result)
