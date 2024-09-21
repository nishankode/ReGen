# app.py

import streamlit as st
import sys
import pandas as pd
from io import StringIO

# Add these paths to sys.path if needed
sys.path.append('../src')
sys.path.append('../scripts')

# Import required modules (you may need to adjust these imports based on your project structure)
from jobDescriptionScraper import LinkedInDescriptionScraper
from jobListingScraper import LinkedInJobListingScraper
from resumeRestructre import save_restructured_resume
from pdfLoader import loadPdfContent
from resumeRelevancyScore import RelevanceScorer
from reGenerate import regen_resume

class ResumeApp:
    def __init__(self):
        self.jobs = None
        self.restructured_resume_path = None
        self.restructured_resume_json = None

    def upload_resume(self):
        uploaded_file = st.file_uploader("Choose your resume PDF", type="pdf")
        if uploaded_file is not None:
            with open("temp_resume.pdf", "wb") as f:
                f.write(uploaded_file.getvalue())
            
            self.restructured_resume_path, self.restructured_resume_json = save_restructured_resume("temp_resume.pdf", 1)
            st.success("Resume uploaded and restructured successfully!")
            return True
        return False

    def get_job_search_params(self):
        job_title = st.text_input("Enter job title to search for:", "Machine Learning Engineer")
        location = st.text_input("Enter location:", "India")
        num_jobs = st.number_input("Number of jobs to scrape:", min_value=1, max_value=20, value=5)
        username = st.text_input("LinkedIn username:")
        password = st.text_input("LinkedIn password:", type="password")
        return job_title, location, num_jobs, username, password

    def scrape_and_analyze_jobs(self, job_title, location, num_jobs, username, password):
        job_listing_scraper = LinkedInJobListingScraper()
        self.jobs = job_listing_scraper.scrape_linkedin_jobs(job_title, location, num_jobs, username, password)

        job_description_scraper = LinkedInDescriptionScraper()
        self.jobs['Job Descriptions'] = self.jobs['Job ID'].apply(lambda x: job_description_scraper.getDescription(job_id=x))

        old_resume_content = loadPdfContent(self.restructured_resume_path)
        resume_relevance_scorer = RelevanceScorer()
        self.jobs['Old Resume Score'] = self.jobs['Job Descriptions'].apply(lambda x: resume_relevance_scorer.calculate_relevance_score(old_resume_content, x))

        self.jobs[['ReGen JSON', 'ReGen FilePath']] = self.jobs.apply(self.apply_regen_resume, axis=1)

        self.jobs['New Resume Score'] = self.jobs[['Job Descriptions', 'Job ID']].apply(lambda x: resume_relevance_scorer.calculate_relevance_score_new(x[1], x[0]), axis=1)

    def apply_regen_resume(self, row):
        regen_json, output_filepath = regen_resume(row['Job Descriptions'], self.restructured_resume_json, row['Job ID'])
        return pd.Series({'ReGen JSON': regen_json, 'ReGen FilePath': output_filepath})

    def display_results(self):
        st.subheader("Job Analysis Results")
        for _, row in self.jobs.iterrows():
            st.write(f"Job Title: {row['Job Title']}")
            st.write(f"Company: {row['Company Name']}")
            st.write(f"Location: {row['Location']}")
            st.write(f"Old Resume Score: {row['Old Resume Score']:.2f}")
            st.write(f"New Resume Score: {row['New Resume Score']:.2f}")
            if st.button(f"View Job Description for {row['Job Title']}"):
                st.text_area("Job Description", row['Job Descriptions'], height=200)
            if st.button(f"Download Tailored Resume for {row['Job Title']}"):
                st.download_button(
                    label="Download PDF",
                    data=open(row['ReGen FilePath'], "rb").read(),
                    file_name=f"tailored_resume_{row['Job ID']}.pdf",
                    mime="application/pdf"
                )
            st.write("---")

        if st.checkbox("Show full job data"):
            st.dataframe(self.jobs)

def main():
    st.title("Resume Tailoring and Job Application System")

    app = ResumeApp()

    if app.upload_resume():
        job_title, location, num_jobs, username, password = app.get_job_search_params()

        if st.button("Search and Analyze Jobs"):
            app.scrape_and_analyze_jobs(job_title, location, num_jobs, username, password)
            app.display_results()
    else:
        st.warning("Please upload a resume to get started.")

if __name__ == "__main__":
    main()