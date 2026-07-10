from azure.storage.blob import BlobClient
import fitz


def extract_text(input):

    blob_name = input["blob_name"].split("/",1)[1]

    blob = BlobClient.from_connection_string(
        "UseDevelopmentStorage=true",
        container_name="pdfs",
        blob_name=blob_name
    )

    data = blob.download_blob().readall()

    pdf = fitz.open(stream=data, filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    return {
        "text": text
    }