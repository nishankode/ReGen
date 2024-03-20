import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import urllib.parse


class LinkedInDescriptionScraper:
    """
    A class to scrape job descriptions from LinkedIn job postings.

    Attributes:
        options (Options): Options for running Edge browser in headless mode.
        service (Service): Edge WebDriver service.
        driver (webdriver): Edge WebDriver instance.
        wait (WebDriverWait): WebDriverWait instance for driver.
    """

    def __init__(self):
        """
        Initializes the LinkedInDescriptionScraper with necessary configurations.
        """
        # Set up options for running Edge browser in headless mode
        self.options = Options()
        self.options.use_chromium = True
        self.options.add_argument("--headless")

        # Set up Edge WebDriver service
        self.service = Service(executable_path=EdgeChromiumDriverManager().install())
        # Initialize Edge WebDriver instance
        self.driver = webdriver.Edge(service=self.service, options=self.options)
        # Set up WebDriverWait with a timeout of 10 seconds
        self.wait = WebDriverWait(self.driver, 10)
        # Maximize the browser window
        self.driver.maximize_window()

    def getJobID(self, job_url):
        """
        Extracts the job ID from the given job URL.

        Args:
            job_url (str): The URL of the job posting.

        Returns:
            str: The extracted job ID.
        """
        # Parse the job URL
        self.parsed_url = urllib.parse.urlparse(job_url)
        # Parse query parameters
        self.query_params = urllib.parse.parse_qs(self.parsed_url.query)
        # Extract the job ID
        self.job_id = self.query_params['currentJobId'][0]
        return self.job_id

    def getDescriptionFromJobID(self, job_id):
        """
        Retrieves the job description using the provided job ID.

        Args:
            job_id (str): The ID of the job posting.

        Returns:
            str: The job description text.
        """
        self.job_id = job_id
        # Construct description URL
        self.description_url = f"https://linkedin.com/jobs-guest/jobs/api/jobPosting/{self.job_id}"
        
        # Open the description URL
        self.driver.get(self.description_url)
        # Add a short delay
        time.sleep(0.5)
        
        # Find and extract job description text
        self.job_description = self.driver.find_element(By.CLASS_NAME, "description__text.description__text--rich").text
        return self.job_description

    def getDescriptionFromUrl(self, job_url):
        """
        Retrieves the job description using the provided job URL.

        Args:
            job_url (str): The URL of the job posting.

        Returns:
            str: The job description text.
        """
        
        self.job_url = job_url
        # Get job ID from URL
        self.job_id = self.getJobID(job_url)
        
        # Construct description URL
        self.description_url = f"https://linkedin.com/jobs-guest/jobs/api/jobPosting/{self.job_id}"
        
        # Open the description URL
        self.driver.get(self.description_url)
        # Add a short delay
        time.sleep(0.5)
        
        # Find and extract job description text
        self.job_description = self.driver.find_element(By.CLASS_NAME, "description__text.description__text--rich").text
       
        return self.job_description

    def getDescription(self, job_id=None, job_url=None):
        """
        Retrieves the job description based on either a provided job ID or URL.

        Args:
            job_id (str): The ID of the job posting.
            job_url (str): The URL of the job posting.

        Returns:
            str: The job description text.
        """
        
        if job_url is None:
            # Get description using Job ID if URL is not provided
            job_description = self.getDescriptionFromJobID(job_id)
        else:
            # Get description using Job URL
            job_description = self.getDescriptionFromUrl(job_url)
        
        return job_description