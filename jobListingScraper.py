import pickle
import time
import urllib.parse
import math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class LinkedInJobListingScraper:
    """
    A class to scrape job listings from LinkedIn job search results.

    Attributes:
        driver (webdriver): The Selenium WebDriver instance.
        wait (WebDriverWait): WebDriverWait instance for the driver.
    """

    def __init__(self):
        """
        Initializes the LinkedInJobListingScraper with necessary configurations.
        """
        self.options = Options()
        self.options.use_chromium = True
        # self.options.add_argument("--headless")  # Uncomment for headless mode

        self.service = Service(executable_path=EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.maximize_window()

    def load_cookies(self, cookies_file):
        """
        Load cookies from a file and add them to the current session.
        
        Args:
            cookies_file (str): The path to the cookies file.
        """
        self.driver.get("https://www.linkedin.com")
        with open(cookies_file, "rb") as file:
            cookies = pickle.load(file)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

    def generate_linkedin_url(self, job_title, location, start):
        """
        Generates LinkedIn job search URL based on job title, location, and start index.

        Args:
            job_title (str): The job title to search for.
            location (str): The location to search in.
            start (int): The starting index for pagination.

        Returns:
            str: The constructed LinkedIn job search URL.
        """
        base_url = "https://www.linkedin.com/jobs/search?"
        params = {
            "keywords": job_title,
            "location": location,
            "refresh": "true",
            'start': start
        }
        return base_url + urllib.parse.urlencode(params)

    def fetch_job_listings(self, linkedin_url):
        """
        Fetches job listings from the given LinkedIn search URL.

        Args:
            linkedin_url (str): The LinkedIn job search URL.

        Returns:
            list: A list of job listing elements.
        """
        self.driver.get(linkedin_url)
        time.sleep(5)
        table = self.driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')
        return table.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')

    def parse_job_data(self, job):
        """
        Parses the job listing element to extract job details.

        Args:
            job (WebElement): The job listing web element.

        Returns:
            dict: A dictionary containing job details.
        """
        div1 = job.find_element(By.TAG_NAME, 'div')
        div2 = div1.find_element(By.TAG_NAME, 'div')
        div3 = div2.find_elements(By.TAG_NAME, 'div')[0]
        div4 = div3.find_element(By.CLASS_NAME, 'job-card-list__entity-lockup')
        div5 = div4.find_element(By.CLASS_NAME, 'flex-grow-1')
        title_div = div5.find_element(By.CLASS_NAME, 'artdeco-entity-lockup__title')
        job_title_img = title_div.find_element(By.TAG_NAME, 'a')

        job_title = job_title_img.text.split('\n')[0]
        job_link = job_title_img.get_attribute('href')
        company_name = div5.find_element(By.CLASS_NAME, 'artdeco-entity-lockup__subtitle').text
        job_location = div5.find_element(By.CLASS_NAME, 'artdeco-entity-lockup__caption').text

        return {
            'Job Title': job_title,
            'Job Post Url': job_link,
            'Company Name': company_name,
            'Location': job_location
        }

    def get_jobs_data(self, jobs):
        """
        Extracts job data from the list of job elements.

        Args:
            jobs (list): List of job elements.

        Returns:
            pd.DataFrame: DataFrame containing the job details.
        """
        lst = []
        for i, job in enumerate(jobs):
            # Scroll logic based on job index
            if i in [6, 12, 18, 21]:
                scroll_factor = [0.3, 0.5, 0.7, 1][[6, 12, 18, 21].index(i)]
                self.driver.execute_script(f'elem = document.getElementsByClassName("jobs-search-results-list")[0]; elem.scrollTo(0, elem.scrollHeight*{scroll_factor});')

            try:
                job_data = self.parse_job_data(job)
                lst.append(job_data)
            except NoSuchElementException:
                pass

        return pd.DataFrame(lst)

    def scrape_linkedin_jobs(self, job_title, location, num_results, cookies_file):
        """
        Scrapes LinkedIn job listings and returns the job details.

        Args:
            job_title (str): The job title to search for.
            location (str): The location to search in.
            num_results (int): The number of results to scrape.
            cookies_file (str): The path to the cookies file.

        Returns:
            pd.DataFrame: DataFrame containing all scraped job details.
        """
        self.load_cookies(cookies_file)
        num_pages = math.ceil(num_results / 25)
        starts = [i * 25 for i in range(num_pages)]

        all_jobs = []
        for start in starts:
            print(f"Scraping page starting at {start}")
            linkedin_url = self.generate_linkedin_url(job_title, location, start)
            jobs = self.fetch_job_listings(linkedin_url)
            jobs_data = self.get_jobs_data(jobs)
            all_jobs.append(jobs_data)

        jobs_dataframe = pd.concat(all_jobs).reset_index(drop=True)
        jobs_dataframe['Job ID'] = jobs_dataframe['Job Post Url'].apply(lambda x: x.split('/')[5])
        return jobs_dataframe

    def close(self):
        """
        Closes the WebDriver session.
        """
        self.driver.quit()

