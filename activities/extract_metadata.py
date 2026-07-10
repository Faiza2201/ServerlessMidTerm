from pypdf import PdfReader
from azure.storage.blob import BlobClient
import os
import tempfile


def extract_metadata(input):

    blob = BlobClient.from_connection_string(
        os.environ["AzureWebJobsStorage"],
        container_name=input["container"],
        blob_name = input["blob_name"].split("/",1)[1]
    )

    data = blob.download_blob().readall()

    file = tempfile.NamedTemporaryFile(delete=False)
    file.write(data)
    file.close()

    reader = PdfReader(file.name)

    metadata = reader.metadata

    return {
        "title": metadata.title if metadata else None,
        "author": metadata.author if metadata else None,
        "creator": metadata.creator if metadata else None,
        "creation_date": str(metadata.creation_date) if metadata else None
    }