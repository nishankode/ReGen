from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RelevanceScorer:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def calculate_relevance_score(self, resume_text, job_description_text):
        # Generate embeddings
        resume_embedding = self.model.encode(resume_text, convert_to_tensor=True)
        job_description_embedding = self.model.encode(job_description_text, convert_to_tensor=True)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(resume_embedding.cpu().numpy().reshape(1, -1), 
                                       job_description_embedding.cpu().numpy().reshape(1, -1))[0][0]
        
        # Convert similarity to score out of 100
        score = (similarity + 1) / 2 * 100
        
        return round(score, 2)

