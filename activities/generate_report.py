import datetime


def generate_report(results):

    print("Generating final PDF report")

    report = {
        "report_id": datetime.datetime.utcnow().isoformat(),

        "document": results[0].get(
            "document",
            "unknown"
        ),

        "analysis": {
            "text": results[0],
            "metadata": results[1],
            "statistics": results[2],
            "sensitive_data": results[3]
        },

        "status": "completed",

        "created_at": datetime.datetime.utcnow().isoformat()
    }


    print("Report generation completed")

    return report