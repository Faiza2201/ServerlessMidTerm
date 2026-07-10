from azure.data.tables import TableServiceClient
import os


def store_results(report):

    print("Saving report to Table Storage")


    connection_string = os.environ[
        "AzureWebJobsStorage"
    ]


    table_service = TableServiceClient.from_connection_string(
        connection_string
    )


    table_name = "PDFReports"


    try:
        table_service.create_table(
            table_name
        )
    except Exception:
        pass


    table_client = table_service.get_table_client(
        table_name
    )


    entity = {

        "PartitionKey": "PDFAnalysis",

        "RowKey": report["report_id"],

        "Document": report["document"],

        "Status": report["status"],

        "CreatedAt": report["created_at"],

        "SensitiveDataDetected":
            str(
                report["analysis"]
                ["sensitive_data"]
                .get(
                    "sensitiveDataDetected",
                    False
                )
            )
    }


    table_client.create_entity(
        entity
    )


    print("Report stored successfully")


    return {
        "message": "Report saved",
        "document": report["document"]
    }