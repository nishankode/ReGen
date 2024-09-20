from pdfLoader import loadPdfContent
from openai import OpenAI
import json
from resumeGenerator import generate_resume_from_json

def get_restructure_prompt(resume_text):
    prompt = f"""
    I have a resume, and I want to extract specific details from it to fill a predefined JSON structure. For each key in the JSON, find the corresponding data in the resume text. If a key does not have relevant information in the resume, leave the value empty and do not generate random or placeholder values. Below is the JSON structure I need to fill:

    {{
    "name": "Full Name",
    "contact": {{
        "email": "email@example.com",
        "linkedin": "linkedin.com/in/username",
        "github": "github.com/username",
        "phone": "(123) 456-7890",
        "location": "Location"
    }},
    "summary": "Professional title with X years of experience in field. Expertise in relevant skills and technologies, with a proven track record in specific outcomes or projects. Skilled in tools such as Tool1, Tool2, and Platform1. Focused on continuous improvement and delivering reliable results.",
    "skills": {{
        "skill_category_name_1": [
        "Skill 1",
        "Skill 2",
        "Skill 3"
        ],
        "skill_category_name_2": [
        "Skill 1",
        "Skill 2"
        ]
        // Add n more skill categories as needed and replace the key name with relavant skill category
    }},
    "experience": [
        {{
        "title": "Job Title 1",
        "company": "Company Name 1",
        "location": "City, Country",
        "duration": "Start Date - End Date",
        "responsibilities": [
            "Responsibility 1",
            "Responsibility 2",
            "Responsibility 3"
        ]
        }},
        {{
        "title": "Job Title 2",
        "company": "Company Name 2",
        "location": "City, Country",
        "duration": "Start Date - End Date",
        "responsibilities": [
            "Responsibility 1",
            "Responsibility 2",
            "Responsibility 3"
        ]
        }}
        // Add n more job experiences similarly
    ],
    "projects": [
        {{
        "name": "Project Name 1",
        "company": "Company Name 1",
        "description": "Project description, including key technologies and outcomes."
        }},
        {{
        "name": "Project Name 2",
        "company": "Company Name 2",
        "description": "Project description, including key technologies and outcomes."
        }}
        // Add n more projects similarly
    ],
    "open_source_contributions": [
        {{
        "project": "Open Source Project Name 1",
        "contribution": "Contribution details."
        }},
        {{
        "project": "Open Source Project Name 2",
        "contribution": "Contribution details."
        }}
        // Add n more contributions similarly
    ],
    "education": [
        {{
        "degree": "Degree Name 1",
        "institution": "Institution Name 1",
        "graduation_year": "Graduation Year",
        "relevant_courses": [
            "Course 1",
            "Course 2",
            "Course 3"
        ]
        }},
        {{
        "degree": "Degree Name 2",
        "institution": "Institution Name 2",
        "graduation_year": "Graduation Year",
        "relevant_courses": [
            "Course 1",
            "Course 2",
            "Course 3"
        ]
        }}
        // Add n more education entries similarly
    ],
    "certifications": [
        {{
        "name": "Certification Name 1",
        "issued": "Issue Date"
        }},
        {{
        "name": "Certification Name 2",
        "issued": "Issue Date"
        }}
        // Add n more certifications similarly
    ],
    "technical_proficiencies": {{
        "parent_technical_proficiency_name_1": [
        "Proficiency 1",
        "Proficiency 2",
        "Proficiency 3"
        ],
        "parent_technical_proficiency_name_2": [
        "Proficiency 1",
        "Proficiency 2"
        ]
        // Add n more technical proficiency categories as needed and parent_technical_proficiency_name with relavant parent technical proficiency name.
    }},
    "references": "Available upon request."
    }}


    Here is the resume text:
    [{resume_text}]

    Important Note: Make sure you dont miss any information or data. Keep as much as you can.

    Please extract relevant data from the resume and fill in the JSON accordingly. If any field is not available in the resume, leave the corresponding value empty.
    Give the output in JSON format only and dont add anything except the json to the output.
    """
    return prompt

def restructure_old_resume(old_resume_path):

    resume_text = loadPdfContent(old_resume_path)

    restructured_prompt = get_restructure_prompt(resume_text)

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": restructured_prompt}
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

def save_restructured_resume(old_resume_path, restructured_resume_id):
    parsed_json = restructure_old_resume(old_resume_path)
    restructured_resume_path = generate_resume_from_json(parsed_json, restructured_resume_id)
    
    return restructured_resume_path, parsed_json