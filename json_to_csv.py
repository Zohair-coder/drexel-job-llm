import json
import csv

with open("results.json", "r") as f:
    results = json.load(f)

with open("results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Job ID", "ChatGPT Score", "Company", "Position", "Reasoning"])
    for result in results:
        writer.writerow(
            [
                result["job_posting"]["position_id"],
                result["score"]["rating"],
                result["job_posting"]["employer_name"],
                result["job_posting"]["position_title"],
                result["score"]["reasoning"],
            ]
        )
