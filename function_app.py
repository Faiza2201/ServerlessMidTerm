import azure.functions as func
import azure.durable_functions as df
import logging
import json


app = df.DFApp()


@app.blob_trigger(
    arg_name="myblob",
    path="pdfs/{name}",
    connection="AzureWebJobsStorage"
)
@app.durable_client_input(
    client_name="client"
)
async def process_pdf(myblob: func.InputStream, client):
    logging.info(
        f"PDF detected: {myblob.name}"
    )

    instance_id = await client.start_new(
        "pdf_orchestrator",
        None,
        {
            "blob_name": myblob.name
        }
    )

    logging.info(
        f"Started orchestration {instance_id}"
    )


@app.orchestration_trigger(
    context_name="context"
)
def pdf_orchestrator(context):

    input_data = {
    "container": "pdfs",
    "blob_name": context.get_input()["blob_name"]
}

    tasks = [
        context.call_activity(
            "extract_text",
            input_data
        ),

        context.call_activity(
            "extract_metadata",
            input_data
        ),

        context.call_activity(
            "analyze_statistics",
            input_data
        ),

        context.call_activity(
            "detect_sensitive_data",
            input_data
        )
    ]

    results = yield context.task_all(tasks)


    report = yield context.call_activity(
        "generate_report",
        results
    )


    yield context.call_activity(
        "store_results",
        report
    )

    return report

@app.activity_trigger(input_name="input")
def extract_text(input):
    from activities.extract_text import extract_text
    return extract_text(input)


@app.activity_trigger(input_name="input")
def extract_metadata(input):
    from activities.extract_metadata import extract_metadata
    return extract_metadata(input)


@app.activity_trigger(input_name="input")
def analyze_statistics(input):
    from activities.analyze_statistics import analyze_statistics
    return analyze_statistics(input)


@app.activity_trigger(input_name="input")
def detect_sensitive_data(input):
    from activities.detect_sensitive_data import detect_sensitive_data
    return detect_sensitive_data(input)

@app.activity_trigger(input_name="input")
def generate_report(input):
    from activities.generate_report import generate_report
    return generate_report(input)

@app.activity_trigger(input_name="input")
def store_results(input):
    from activities.store_results import store_results
    return store_results(input)

