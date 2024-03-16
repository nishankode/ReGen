import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from LinkedinLogin import login

class DescriptionScraper:
    """
    A class to scrape job descriptions from LinkedIn job postings.

    Attributes:
        job_link (str): The URL of the LinkedIn job posting.
        email (str): The email address for LinkedIn login. (Optional)
        password (str): The password for LinkedIn login. (Optional)
    """

    def __init__(self, job_link, email=None, password=None):
        """
        Initializes the DescriptionScraper object.

        Args:
            job_link (str): The URL of the LinkedIn job posting.
            email (str): The email address for LinkedIn login. (Optional)
            password (str): The password for LinkedIn login. (Optional)
        """
        self.job_link = job_link
        self.email = email
        self.password = password
        self.options = Options()
        
        # Set options for running Edge browser in headless mode
        self.options.use_chromium = True
        self.options.add_argument("--headless")

        # Set up Edge WebDriver
        self.service = Service(executable_path=EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=self.service, options=self.options)

        # Set up WebDriverWait
        self.wait = WebDriverWait(self.driver, 10)

        # Maximize window
        self.driver.maximize_window()

        # LinkedIn session cookie for bypassing login
        self.cookie="AQEDAUyRaiQFUJWsAAABjkM2c24AAAGOZ0L3blYACOOTb4onVgNoYY2J6PmUv9P7EQ8KAxT0wfrObbDsJcO0S7st3jdfnQb9kLMVdahKkHQxeCmRO-BzuARDytJjq4_V08Kq2bku2EP8swHbATuCTL_X"
        self.timeout = 10
        login(self.driver, self.email, self.password, self.cookie, self.timeout)

    def get_description(self):
        """
        Scrapes the job description from the LinkedIn job posting.

        Returns:
            str: The job description text.
        """
        # Open the job link
        self.driver.get(self.job_link)
        
        # Find and click on the 'See more' button to expand the description
        self.see_more_button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-description__footer-button")))
        self.see_more_button.click()
        
        # Wait for the description element to load, then extract the text
        time.sleep(3)  # Wait briefly to ensure content loads properly
        description_element = self.driver.find_element(By.ID, "job-details")
        description_span = description_element.find_element(By.TAG_NAME, "span")
        job_description = description_span.get_attribute("innerText")

        # Close the WebDriver session
        self.driver.quit()

        return job_description
