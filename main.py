import json
import yaml
from openai import OpenAI

from response_model import ResponseModel


def main():
    with open("data/data.json", "r") as f:
        job_postings = json.load(f)

    total_words = 0
    total_job_postings = len(job_postings)

    for posting in job_postings.values():
        posting_string = json.dumps(posting)
        total_words += len(posting_string.split())

    print(f"Total words in job postings: {total_words}")
    print(f"Total job postings: {total_job_postings}")
    print(f"Average words per job posting: {total_words / total_job_postings}")

    with open("data/resume.yaml", "r") as f:
        resume = yaml.safe_load(f)

    resume_string = yaml.dump(resume)

    print(f"Total words in resume: {len(resume_string.split())}")

    total_words += len(resume_string.split())

    print(f"Average words per query: {total_words / total_job_postings}")

    print(f"Estimated tokens per query: {(total_words / total_job_postings) * 1.33}")

    print(f"Total estimated tokens: {total_words * 1.33}")

    print()
    print("Sending requests...")

    results = []
    for index, job_posting in enumerate(job_postings.values()):
        print(f"Request {index + 1}/{total_job_postings}")
        job_posting_string = json.dumps(job_posting)

        try:
            score = get_alignment_score(job_posting_string, resume_string)
        except Exception as e:
            print(
                f"Error - unable to get alignment score for company: {job_posting['employer_name']} with position: {job_posting['position_title']}. Error: {e}"
            )
            continue

        result = {
            "job_posting": job_posting,
            "score": {
                "rating": score.rating,
                "reasoning": score.reasoning,
            },
        }

        results.append(result)

        print(f"Comapny: {job_posting['employer_name']}")
        print(f"Position: {job_posting['position_title']}")
        print(f"Score: {score.rating}")
        print(f"Reasoning: {score.reasoning}")
        print()

    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)


def get_alignment_score(job_posting_string, resume_string):
    client = OpenAI()

    prompt = f"""
    Given the following job application and resume, please assess the candidate's fit for the role on a scale of 0-100:
    
    Job Application:
    {job_posting_string}
    
    Resume:
    {resume_string}
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that assesses the fit of a candidate for a job based on their resume and job application. Your task is to rate the candidate's fit on a scale of 0-100, where 0 indicates a complete mismatch and 100 indicates a perfect match. Make sure to provide a single integer. Do not provide a range. Have a bias towards companies that are more likely to pay well. Also provide a short one sentence reasoning for your rating.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        timeout=20,
        response_format=ResponseModel,
    )

    response = completion.choices[0].message.parsed

    return response


if __name__ == "__main__":
    main()
