import re
from azure.storage.blob import BlobClient
import fitz


def detect_sensitive_data(input):

    print("Starting sensitive data detection")

    # Fix blob path issue: pdfs/test.pdf -> test.pdf
    blob_name = input["blob_name"].split("/",1)[1]

    blob = BlobClient.from_connection_string(
        "UseDevelopmentStorage=true",
        container_name="pdfs",
        blob_name=blob_name
    )

    # Download PDF
    data = blob.download_blob().readall()

    # Extract text from PDF
    pdf = fitz.open(stream=data, filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    # Patterns to detect sensitive information

    emails = re.findall(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text
    )

    phones = re.findall(
        r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b",
        text
    )

    urls = re.findall(
        r"https?://[^\s]+|www\.[^\s]+",
        text
    )

    dates = re.findall(
        r"\b(?:\d{1,2}[/-]){2}\d{2,4}\b",
        text
    )


    result = {
        "emails_found": emails,
        "email_count": len(emails),

        "phones_found": phones,
        "phone_count": len(phones),

        "urls_found": urls,
        "url_count": len(urls),

        "dates_found": dates,
        "date_count": len(dates)
    }


    print("Sensitive data detection completed")

    return result