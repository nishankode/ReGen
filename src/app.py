from scripts.jobDescriptionScraper import LinkedInDescriptionScraper
from scripts.jobListingScraper import LinkedInJobListingScraper
from resumeGenerator import generate_resume_from_json
from resumeRelevancyScore import RelevanceScorer


def get_result():
    print('started ----------------')
    # Job Listing Scraping
    job_listing_scraper = LinkedInJobListingScraper()
    jobs = job_listing_scraper.scrape_linkedin_jobs("Fullstack Developer", "India", 50, "linkedincookies.pkl")

    # Job Description Scraping
    job_description_scraper = LinkedInDescriptionScraper()
    jobs['Job Descriptions'] = jobs['Job ID'].apply(lambda x : job_description_scraper.getDescription(job_id=x))

    # Old Resume Scoring
    resume_relevence_scorer = RelevanceScorer()
    jobs['Old Resume Score'] = jobs['Job Descriptions'].apply(lambda x : resume_relevence_scorer.calculate_relevance_score(old_resume, x))


    generated_json_data = {
    "name": "John Anderson",
    "contact": {
        "email": "john.anderson@gmail.com",
        "linkedin": "linkedin.com/in/johnanderson",
        "github": "github.com/johndevml",
        "phone": "(555) 555-1234",
        "location": "India"
    },
    "summary": "Senior MLOps Engineer with 7+ years of experience in deploying, managing, and optimizing machine learning pipelines and systems at scale. Expertise in building and scaling AI solutions using Docker, Kubernetes, and cloud platforms like AWS and GCP. Skilled in automating end-to-end MLOps workflows, implementing CI/CD pipelines, and leveraging advanced AI tools including TensorFlow and PyTorch. Proven track record in ensuring model performance and reliability through real-time monitoring and optimization, with a focus on problem-solving and continuous improvement.",
    "skills": {
        "mlops_tools": [
        "Docker",
        "Kubernetes",
        "Jenkins",
        "MLflow",
        "Airflow",
        "Argo Workflows",
        "Terraform",
        "Ansible"
        ],
        "machine_learning": [
        "Supervised/Unsupervised Learning",
        "Model Deployment",
        "Model Performance Monitoring"
        ],
        "cloud_platforms": [
        "AWS (EC2, S3, Lambda, SageMaker, EMR, Kinesis, SQS, SNS)",
        "GCP (AI Platform, Compute Engine)"
        ],
        "programming_languages": [
        "Python",
        "SQL"
        ],
        "version_control_ci_cd": [
        "Git",
        "Jenkins",
        "GitHub Actions",
        "TravisCI",
        "Bamboo"
        ],
        "data_engineering": [
        "Apache Spark",
        "Airflow"
        ]
    },
    "experience": [
        {
        "title": "MLOps Engineer",
        "company": "XYZ Corp",
        "location": "India",
        "duration": "June 2022 – Present",
        "responsibilities": [
            "Architected and deployed real-time object detection models for autonomous vehicle systems, using TensorFlow and YOLOv5, with a focus on scalability and performance.",
            "Built and optimized deep learning pipelines on AWS using Kubernetes, enhancing model deployment efficiency and scalability.",
            "Automated deployment and retraining of generative models, including GANs, improving the model development lifecycle.",
            "Developed CI/CD frameworks with Jenkins and MLflow, reducing deployment times and ensuring reliable and maintainable production systems.",
            "Implemented GPU acceleration in model inference pipelines on AWS SageMaker, optimizing processing times and model performance.",
            "Integrated TensorBoard and Prometheus for real-time performance monitoring, ensuring model accuracy and operational reliability."
        ]
        },
        {
        "title": "Junior MLOps Engineer",
        "company": "DataTech Solutions",
        "location": "India",
        "duration": "August 2021 – June 2022",
        "responsibilities": [
            "Designed and managed automated pipelines for deploying generative AI models, enhancing datasets through synthetic data generation.",
            "Containerized NLP models using Docker and Kubernetes for scalable deployment.",
            "Led deployment of computer vision models, improving accuracy and operational efficiency.",
            "Implemented transfer learning for object detection tasks, accelerating the model development process.",
            "Created TensorFlow Serving pipelines for consistent and scalable model deployment.",
            "Implemented logging and error-handling mechanisms using ELK Stack, reducing system downtime."
        ]
        }
    ],
    "projects": [
        {
        "name": "Automated ML Pipeline for Predictive Maintenance in Autonomous Vehicles",
        "company": "XYZ Corp",
        "description": "Developed a real-time object detection pipeline using YOLOv5 and TensorFlow for predicting maintenance issues. Integrated Airflow for orchestrating model training and deployment on AWS Lambda, ensuring high availability and minimal downtime."
        },
        {
        "name": "Real-time Fraud Detection System Using Generative AI",
        "company": "DataTech Solutions",
        "description": "Built a fraud detection system utilizing VAEs for real-time anomaly detection. Deployed on Kubernetes with CI/CD automation using Jenkins, achieving high accuracy and scalability."
        },
        {
        "name": "Generative Image Synthesis Pipeline",
        "company": "XYZ Corp",
        "description": "Developed a GAN-based image synthesis pipeline to augment training datasets, deployed on GCP AI Platform with TensorFlow and Kubernetes, improving model performance and training efficiency."
        }
    ],
    "open_source_contributions": [
        {
        "project": "Kubeflow",
        "contribution": "Developed custom operators for scaling computer vision pipelines on Kubernetes."
        },
        {
        "project": "MLflow",
        "contribution": "Created extensions for tracking and visualizing GAN training metrics."
        },
        {
        "project": "TensorFlow Hub",
        "contribution": "Developed pre-trained models for image classification and segmentation."
        }
    ],
    "education": {
        "degree": "Bachelor of Science in Computer Science",
        "institution": "University of California, Berkeley",
        "graduation_year": "2020",
        "relevant_courses": [
        "Machine Learning",
        "Deep Learning",
        "Cloud Computing",
        "Distributed Systems"
        ]
    },
    "certifications": [
        {
        "name": "AWS Certified Solutions Architect – Associate",
        "issued": "May 2023"
        },
        {
        "name": "Certified Kubernetes Administrator (CKA)",
        "issued": "September 2022"
        },
        {
        "name": "TensorFlow Developer Certification",
        "issued": "March 2022"
        },
        {
        "name": "Google Cloud Professional Data Engineer",
        "issued": "February 2024"
        }
    ],
    "publications_talks": [
        {
        "title": "Building and Deploying Computer Vision Models at Scale with TensorFlow and Kubernetes",
        "event": "O'Reilly AI Conference",
        "year": "2023"
        },
        {
        "title": "Generative AI in Real-World Applications: Challenges and Solutions",
        "platform": "Medium",
        "views": "20,000+"
        },
        {
        "title": "Optimizing Deep Learning Workflows with Airflow and MLflow",
        "event": "PyData Conference",
        "year": "2023"
        }
    ],
    "volunteer_experience": [
        {
        "organization": "AI for Good Hackathon",
        "role": "Mentor",
        "description": "Mentored teams in designing and deploying computer vision models for healthcare applications."
        },
        {
        "organization": "Women Who Code",
        "role": "Workshop Leader",
        "description": "Conducted workshops on Generative AI with a focus on using GANs and VAEs for image synthesis."
        }
    ],
    "technical_proficiencies": {
        "operating_systems": ["Linux (Ubuntu, CentOS)", "Windows"],
        "databases": ["MySQL", "PostgreSQL"],
        "version_control": ["Git"]
    },
    "references": "Available upon request."
    }




    jobs['Generated Json Data'] = None
    jobs['Generated Resume Path'] = jobs[['Job Descriptions', 'Job ID']].apply(lambda x : generate_resume_from_json(generated_json_data, x[1]), axis=1)


    return jobs

if __name__ == '__main__':
    get_result()