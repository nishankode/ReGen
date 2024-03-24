from langchain_anthropic import ChatAnthropic
from langchain_anthropic.experimental import ChatAnthropicTools
import json
import os
from dotenv import load_dotenv
load_dotenv()

from ScoresExtract import Scores

import warnings
warnings.filterwarnings('ignore')





class ValidateResume:
    """
    Class to validate a resume against a job description and calculate scores.
    """

    def __init__(self):
        """
        Initialize ValidateResume object.

        Retrieves the API key and model name from environment variables.
        """
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.model = "claude-3-opus-20240229"

    def get_resume_scores(self, resume, job_description):
        """
        Get scores for a resume against a job description.

        Args:
            resume (str): The resume to be evaluated.
            job_description (str): The job description against which the resume is evaluated.
            Scores (Scores): Object representing various scores.

        Returns:
            dict: Dictionary containing scores for different aspects.
        """
        # Store input parameters
        self.resume = resume
        self.job_description = job_description
        self.Scores = Scores

        # Initialize ChatAnthropicTools with model and API key
        self.model = ChatAnthropicTools(model=self.model, anthropic_api_key=self.api_key).bind_tools(tools=[self.Scores])

        # Formulate human-readable instructions
        self.human = f"""
            AIM
            ---
            Based on the Below instructions, calculate the score of Candidate's Resume for the Corresponding Job Description.

            INPUTS
            ------
            Candidate's Resume : [{self.resume}]
            Job Description : [{self.job_description}]

            SCORE CALCULATION
            -----------------
            Keyword Matching Score :
            [LLM Identifies the keywords and phrases in the job description that reflect required skills, qualifications, and experiences. Then, count how many of these keywords appear in the candidate's resume and calculate the percentage of matched keywords to calculate the score between 1 and 100, both inclusive.]

            Skills Matching Score :
            [Closely examine the skills and qualifications listed in the job description, Check if the candidate's resume includes evidence of possessing these skills and qualifications. Then, assign weights to skills based on their importance to the job role and calculate a weighted percentage of matched skills and qualifications between 1 and 100, both inclusive.]

            Qualifications Matching Score :
            [Closely examine the qualifications listed in the job description, Check if the candidate's resume includes evidence of possessing these qualifications. Then, assign weights to qualifications based on their importance to the job role and calculate a weighted percentage of matched qualifications to calculate the score between 1 and 100, both inclusive.]

            Experience Alignment Score :
            [Analyze the candidate's work experience as presented in the resume, Compare the candidate's past roles, responsibilities, and achievements with those outlined in the job description, Assess the relevance and depth of experience. Finally, Quantify the alignment between the candidate's experience and the job requirements to calculate the score between 1 and 100, both inclusive.]

            Education and Certifications Alignment Score :
            [Verify if the candidate's educational background and certifications meet the requirements specified in the job description, Consider the relevance of the candidate's academic achievements to the role, Assign weights to education and certifications based on their importance to the job. Finally, calculate a weighted percentage of educational and certification match. The percentage should be between 1 and 100, both inclusive.]

            Soft Skills and Personal Attributes Score :
            [Evaluate if the candidate's soft skills and personal attributes align with the job requirements, Look for evidence of communication skills, teamwork, leadership, adaptability, etc. Assess cultural fit based on the company's values and work environment. This can be more subjective but can still be quantified based on explicit mentions in the resume. Finally calculate the score, and the score should be between 1 and 100, both inclusive.]

            Overall Fit Score :
            [Combine the results from the above metrics, assigning weights to each based on their importance. Sum up the weighted scores to obtain an overall fit score. Normalize the score to a percentage scale (e.g., out of 100).]

            OUTPUT
            ------
            [The output should  be in this format:
                
                Dict('Keyword_Matching_Score' : Keyword Matching Score,
                'Skills_Matching_Score' : Skills Matching Score,
                'Qualifications_Matching_Score' : Qualifications Matching Score,
                'Experience_Alignment_Score' : Experience Alignment Score,
                'Education_and_Certifications_Alignment_Score' : Education and Certifications Alignment Score,
                'Soft_Skills_and_Personal_Attributes_Score' : Soft Skills and Personal Attributes Score,
                'Overall_Fit_Score' : Overall Fit Score)
            ]
        """

        # Invoke the model with the provided inputs
        self.resp = self.model.invoke(self.human)
        self.scores_json = json.loads(self.resp.additional_kwargs['tool_calls'][0]['function']['arguments'])

        return self.scores_json

