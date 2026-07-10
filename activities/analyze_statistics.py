from pypdf import PdfReader
from azure.storage.blob import BlobClient
import os
import tempfile


def analyze_statistics(input):

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

    pages = len(reader.pages)
    words = 0

    for page in reader.pages:
        text = page.extract_text() or ""
        words += len(text.split())

    return {
        "page_count": pages,
        "word_count": words,
        "avg_words_per_page": round(words/pages,2) if pages else 0,
        "reading_time_minutes": round(words/200,2)
    }