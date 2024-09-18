from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from pdfLoader import loadPdfContent

class RelevanceScorer:
    """
    A class to calculate relevance scores between resume and job description texts.

    This class uses a pre-trained Sentence Transformer model to generate embeddings
    for the input texts and calculates their similarity using cosine similarity.

    Attributes:
        model (SentenceTransformer): The pre-trained Sentence Transformer model.
    """

    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        """
        Initialize the RelevanceScorer with a specified model.

        Args:
            model_name (str): The name of the pre-trained Sentence Transformer model to use.
                              Defaults to 'paraphrase-MiniLM-L6-v2'.
        """
        self.model = SentenceTransformer(model_name)

    def calculate_relevance_score(self, resume_text, job_description_text):
        """
        Calculate the relevance score between a resume and a job description.

        This method generates embeddings for both the resume and job description texts,
        calculates their cosine similarity, and returns a score out of 100.

        Args:
            resume_text (str): The text content of the resume.
            job_description_text (str): The text content of the job description.

        Returns:
            float: A relevance score between 0 and 100, rounded to two decimal places.
                   Higher scores indicate greater similarity between the texts.
        """
        # Generate embeddings
        resume_embedding = self.model.encode(resume_text, convert_to_tensor=True)
        job_description_embedding = self.model.encode(job_description_text, convert_to_tensor=True)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(resume_embedding.cpu().numpy().reshape(1, -1), 
                                       job_description_embedding.cpu().numpy().reshape(1, -1))[0][0]
        
        # Convert similarity to score out of 100
        score = (similarity + 1) / 2 * 100
        
        return round(score, 2)
    
    def calculate_relevance_score_new(self, job_id, job_description_text):
        resume_text = loadPdfContent(os.path.join('../generatedResumes', f"{job_id}.pdf"))
        resume_embedding = self.model.encode(resume_text, convert_to_tensor=True)
        job_description_embedding = self.model.encode(job_description_text, convert_to_tensor=True)
        # Calculate cosine similarity
        similarity = cosine_similarity(resume_embedding.cpu().numpy().reshape(1, -1), 
                                       job_description_embedding.cpu().numpy().reshape(1, -1))[0][0]
        
        # Convert similarity to score out of 100
        score = (similarity + 1) / 2 * 100
        
        return round(score, 2)