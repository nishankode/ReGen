from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from io import BytesIO
import os

def is_content_empty(content):
    """
    Check if the content is effectively empty.
    """
    if isinstance(content, str):
        return not content.strip()
    elif isinstance(content, (list, dict)):
        return not content
    return True

def generate_resume_from_json(json_data, jobid):
    """
    Generate a PDF resume from JSON data.

    This function takes a JSON object containing personal and professional information
    and creates a formatted PDF resume. The resume includes sections such as contact
    information, professional summary, skills, experience, projects, education,
    certifications, and more.

    Args:
        json_data (dict): A dictionary containing the resume information.
        jobid (str): A unique identifier for the job application.

    Returns:
        str: The file path of the generated PDF resume.

    Note:
        The function saves the generated PDF in a '../generatedResumes' directory
        with the filename format '{jobid}.pdf'.
    """

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=LETTER)
    styles = getSampleStyleSheet()
    
    content = []
    
    # Add Name
    if 'name' in json_data and not is_content_empty(json_data['name']):
        content.append(Paragraph(f"<b>{json_data['name']}</b>", styles['Title']))
    
    # Add Contact Info
    if 'contact' in json_data and not is_content_empty(json_data['contact']):
        contact = json_data['contact']
        contact_info = []
        for field in ['email', 'phone', 'linkedin', 'github', 'location']:
            if field in contact and not is_content_empty(contact[field]):
                contact_info.append(f"{field.capitalize()}: {contact[field]}")
        if contact_info:
            content.append(Paragraph(" | ".join(contact_info), styles['Normal']))
            content.append(Spacer(1, 12))

    # Add Summary
    if 'summary' in json_data and not is_content_empty(json_data['summary']):
        content.append(Paragraph("<b>Professional Summary</b>", styles['Heading2']))
        content.append(Paragraph(json_data['summary'], styles['Normal']))
        content.append(Spacer(1, 12))
    
    # Add Skills
    if 'skills' in json_data and not is_content_empty(json_data['skills']):
        content.append(Paragraph("<b>Skills</b>", styles['Heading2']))
        for skill_category, skill_list in json_data['skills'].items():
            if not is_content_empty(skill_list):
                content.append(Paragraph(f"<b>{skill_category}:</b>", styles['Normal']))
                content.append(Paragraph(", ".join(skill_list), styles['Normal']))
        content.append(Spacer(1, 12))

    # Add Experience
    if 'experience' in json_data and not is_content_empty(json_data['experience']):
        content.append(Paragraph("<b>Professional Experience</b>", styles['Heading2']))
        for job in json_data['experience']:
            if not is_content_empty(job):
                content.append(Paragraph(f"<b>{job.get('title', '')}</b>", styles['Heading3']))
                content.append(Paragraph(f"{job.get('company', '')} – {job.get('location', '')}", styles['Normal']))
                content.append(Paragraph(f"{job.get('duration', '')}", styles['Normal']))
                responsibilities = job.get('responsibilities', [])
                if not is_content_empty(responsibilities):
                    for responsibility in responsibilities:
                        content.append(Paragraph(f"• {responsibility}", styles['Normal']))
                content.append(Spacer(1, 12))

    # Add Projects
    if 'projects' in json_data and not is_content_empty(json_data['projects']):
        content.append(Paragraph("<b>Projects</b>", styles['Heading2']))
        for project in json_data['projects']:
            if not is_content_empty(project):
                content.append(Paragraph(f"<b>{project.get('name', '')}</b>", styles['Heading3']))
                content.append(Paragraph(project.get('company', ''), styles['Normal']))
                content.append(Paragraph(project.get('description', ''), styles['Normal']))
                content.append(Spacer(1, 12))

    # Add Open Source Contributions
    if 'open_source_contributions' in json_data and not is_content_empty(json_data['open_source_contributions']):
        content.append(Paragraph("<b>Open Source Contributions</b>", styles['Heading2']))
        for contrib in json_data['open_source_contributions']:
            if not is_content_empty(contrib):
                content.append(Paragraph(f"<b>{contrib.get('project', '')}</b>", styles['Heading3']))
                content.append(Paragraph(contrib.get('contribution', ''), styles['Normal']))
                content.append(Spacer(1, 12))

    # Add Education
    if 'education' in json_data and not is_content_empty(json_data['education']):
        content.append(Paragraph("<b>Education</b>", styles['Heading2']))
        for edu in json_data['education']:
            if not is_content_empty(edu):
                content.append(Paragraph(edu.get('degree', ''), styles['Heading3']))
                content.append(Paragraph(edu.get('institution', ''), styles['Normal']))
                if 'graduation_year' in edu and not is_content_empty(edu['graduation_year']):
                    content.append(Paragraph(f"Graduation Year: {edu['graduation_year']}", styles['Normal']))
                if 'relevant_courses' in edu and not is_content_empty(edu['relevant_courses']):
                    content.append(Paragraph(f"Relevant Courses: {', '.join(edu['relevant_courses'])}", styles['Normal']))
                content.append(Spacer(1, 12))

    # Add Certifications
    if 'certifications' in json_data and not is_content_empty(json_data['certifications']):
        content.append(Paragraph("<b>Certifications</b>", styles['Heading2']))
        for cert in json_data['certifications']:
            if not is_content_empty(cert):
                content.append(Paragraph(f"{cert.get('name', '')}, Issued: {cert.get('issued', '')}", styles['Normal']))
        content.append(Spacer(1, 12))

    # Add Technical Proficiencies
    if 'technical_proficiencies' in json_data and not is_content_empty(json_data['technical_proficiencies']):
        content.append(Paragraph("<b>Technical Proficiencies</b>", styles['Heading2']))
        for category, profs in json_data['technical_proficiencies'].items():
            if not is_content_empty(profs):
                content.append(Paragraph(f"{category.capitalize()}: {', '.join(profs)}", styles['Normal']))
        content.append(Spacer(1, 12))

    # Add References
    if 'references' in json_data and not is_content_empty(json_data['references']):
        content.append(Paragraph("<b>References</b>", styles['Heading2']))
        content.append(Paragraph(json_data['references'], styles['Normal']))

    # Build PDF
    pdf.build(content)
    
    buffer.seek(0)

    # Save PDF to file
    output_filename = f"{jobid}.pdf"
    output_filepath = os.path.join('../generatedResumes', output_filename)
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, "wb") as f:
        f.write(buffer.getvalue())

    return output_filepath