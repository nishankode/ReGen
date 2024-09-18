"""
Resume Generator and Optimization Module.

This module provides functionality to generate and optimize resumes based on job descriptions.
It uses OpenAI's GPT model to refine resume content and generate tailored resumes.
"""

from openai import OpenAI
import json
from resumeGenerator import generate_resume_from_json


def generate_regen_prompt(job_description, resume_json):
    """
    Generate a prompt for resume regeneration.

    This function creates a detailed prompt for the AI model to optimize
    a resume based on a given job description.

    Args:
        job_description (str): The job description to tailor the resume to.
        resume_json (str): The original resume in JSON format.

    Returns:
        str: A formatted prompt for the AI model.
    """
    regen_prompt = f"""
    You are given a resume in JSON format and a job description. Your task is to update the resume to make it as relevant as possible to the job description while strictly preserving the structure of the JSON.

    **Instructions:**
    1. Rephrase, expand, and optimize the content within the JSON to reflect the skills, qualifications, and experiences that align with the job description.
    2. Where appropriate, add details, achievements, and relevant context that would make the candidate stand out for the job.
    3. Ensure the JSON structure remains completely intact. The keys, nested objects, arrays, and their structure must not be changed. Only modify the values where necessary.
    4. Do **not** fabricate any facts. All changes should be based on plausible improvements of the existing information.
    5. Focus on aligning the resume with the job responsibilities, required qualifications, and desired skills as described in the job description.

    **Resume JSON:** {resume_json}

    **Job Description:** {job_description}
    """
    return regen_prompt


def regen_resume_json(job_description, resume_json):
    """
    Regenerate the resume JSON based on the job description.

    This function uses OpenAI's GPT model to optimize the resume content
    for a specific job description.

    Args:
        job_description (str): The job description to tailor the resume to.
        resume_json (str): The original resume in JSON format.

    Returns:
        dict: The regenerated resume as a Python dictionary.
    """
    regen_prompt = generate_regen_prompt(job_description, resume_json)

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": regen_prompt}
        ]
    )
    result = completion.choices[0].message.content

    try:
        parsed_json = json.loads(result)
    except:
        # Remove the leading and trailing backticks and 'json' identifier
        json_string = result.strip().lstrip('```json').rstrip('```')

        # Parse the JSON string
        parsed_json = json.loads(json_string)

    return parsed_json


def regen_resume(job_description, resume_json, job_id):
    """
    Regenerate and save a tailored resume.

    This function regenerates the resume JSON and creates a formatted resume file.

    Args:
        job_description (str): The job description to tailor the resume to.
        resume_json (str): The original resume in JSON format.
        job_id (str): An identifier for the job application.

    Returns:
        tuple: A tuple containing:
            - dict: The regenerated resume as a Python dictionary.
            - str: The file path of the generated resume document.
    """
    regen_json = regen_resume_json(job_description, resume_json)

    output_filepath = generate_resume_from_json(regen_json, job_id)

    return regen_json, output_filepath