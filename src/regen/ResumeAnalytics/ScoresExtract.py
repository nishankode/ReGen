from langchain_core.pydantic_v1 import BaseModel

class Scores(BaseModel):
    Keyword_Matching_Score: float
    Skills_Matching_Score: float
    Qualifications_Matching_Score: float
    Experience_Alignment_Score: float
    Education_and_Certifications_Alignment_Score: float
    Soft_Skills_and_Personal_Attributes_Score: float
    Overall_Fit_Score: float