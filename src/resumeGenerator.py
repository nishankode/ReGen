from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from io import BytesIO
import os


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
    content.append(Paragraph(f"<b>{json_data.get('name', 'Your Name')}</b>", styles['Title']))
    
    # Add Contact Info
    contact = json_data.get("contact", {})
    contact_info = f"Email: {contact.get('email', '')} | Phone: {contact.get('phone', '')} | LinkedIn: {contact.get('linkedin', '')} | GitHub: {contact.get('github', '')} | Location: {contact.get('location', '')}"
    content.append(Paragraph(contact_info, styles['Normal']))
    content.append(Spacer(1, 12))

    # Add Summary
    content.append(Paragraph("<b>Professional Summary</b>", styles['Heading2']))
    content.append(Paragraph(json_data.get('summary', 'Summary not provided'), styles['Normal']))
    content.append(Spacer(1, 12))
    
    # Add Skills
    content.append(Paragraph("<b>Skills</b>", styles['Heading2']))
    skills = json_data.get('skills', {})
    for skill_category, skill_list in skills.items():
        content.append(Paragraph(f"<b>{skill_category.replace('_', ' ').capitalize()}:</b>", styles['Normal']))
        content.append(Paragraph(", ".join(skill_list), styles['Normal']))
    content.append(Spacer(1, 12))

    # Add Experience
    content.append(Paragraph("<b>Professional Experience</b>", styles['Heading2']))
    experience = json_data.get('experience', [])
    for job in experience:
        content.append(Paragraph(f"<b>{job.get('title', '')}</b>", styles['Heading3']))
        content.append(Paragraph(f"{job.get('company', '')} – {job.get('location', '')}", styles['Normal']))
        content.append(Paragraph(f"{job.get('duration', '')}", styles['Normal']))
        for responsibility in job.get('responsibilities', []):
            content.append(Paragraph(f"• {responsibility}", styles['Normal']))
        content.append(Spacer(1, 12))

    # Add Projects
    content.append(Paragraph("<b>Projects</b>", styles['Heading2']))
    projects = json_data.get('projects', [])
    for project in projects:
        content.append(Paragraph(f"<b>{project.get('name', '')}</b>", styles['Heading3']))
        content.append(Paragraph(project.get('company', ''), styles['Normal']))
        content.append(Paragraph(project.get('description', ''), styles['Normal']))
        content.append(Spacer(1, 12))

    # Add Open Source Contributions
    content.append(Paragraph("<b>Open Source Contributions</b>", styles['Heading2']))
    contributions = json_data.get('open_source_contributions', [])
    for contrib in contributions:
        content.append(Paragraph(f"<b>{contrib.get('project', '')}</b>", styles['Heading3']))
        content.append(Paragraph(contrib.get('contribution', ''), styles['Normal']))
        content.append(Spacer(1, 12))

    # Add Education
    content.append(Paragraph("<b>Education</b>", styles['Heading2']))
    education = json_data.get('education', {})
    content.append(Paragraph(education.get('degree', 'Degree not provided'), styles['Heading3']))
    content.append(Paragraph(education.get('institution', 'Institution not provided'), styles['Normal']))
    content.append(Paragraph(f"Graduation Year: {education.get('graduation_year', '')}", styles['Normal']))
    content.append(Paragraph(f"Relevant Courses: {', '.join(education.get('relevant_courses', []))}", styles['Normal']))
    content.append(Spacer(1, 12))

    # Add Certifications
    content.append(Paragraph("<b>Certifications</b>", styles['Heading2']))
    certifications = json_data.get('certifications', [])
    for cert in certifications:
        content.append(Paragraph(f"{cert.get('name', '')}, Issued: {cert.get('issued', '')}", styles['Normal']))
    content.append(Spacer(1, 12))

    # Add Technical Proficiencies
    content.append(Paragraph("<b>Technical Proficiencies</b>", styles['Heading2']))
    technical_proficiencies = json_data.get('technical_proficiencies', {})
    for category, profs in technical_proficiencies.items():
        content.append(Paragraph(f"{category.capitalize()}: {', '.join(profs)}", styles['Normal']))
    content.append(Spacer(1, 12))

    # Add Publications & Talks
    content.append(Paragraph("<b>Publications & Talks</b>", styles['Heading2']))
    publications = json_data.get('publications_talks', [])
    for pub in publications:
        content.append(Paragraph(f"{pub.get('title', '')}, {pub.get('event', '')} ({pub.get('year', '')})", styles['Normal']))
    content.append(Spacer(1, 12))

    # Add Volunteer Experience
    content.append(Paragraph("<b>Volunteer Experience</b>", styles['Heading2']))
    volunteer_experience = json_data.get('volunteer_experience', [])
    for exp in volunteer_experience:
        content.append(Paragraph(f"{exp.get('organization', '')} - {exp.get('role', '')}", styles['Normal']))
        content.append(Paragraph(exp.get('description', ''), styles['Normal']))
    content.append(Spacer(1, 12))

    # Add References
    references = json_data.get('references', 'Available upon request.')
    content.append(Paragraph("<b>References</b>", styles['Heading2']))
    content.append(Paragraph(references, styles['Normal']))

    # Build PDF
    pdf.build(content)
    
    buffer.seek(0)

    # Save PDF to file
    output_filename = f"{jobid}.pdf"
    output_filepath = os.path.join('../generatedResumes', output_filename)
    with open(output_filepath, "wb") as f:
        f.write(buffer.getvalue())

    return output_filepath