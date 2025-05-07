from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv
import pandas

PAGE_NO = 11

load_dotenv()

class GetJobs():
    def __init__(self):
        self.ACCOUNT_EMAIL = os.environ["EMAIL"]
        self.ACCOUNT_PASSWORD = os.environ["PASSWORD"]
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.home_url = "https://www.linkedin.com/home"
        self.jobs_titles = []
        self.jobs_links = []
        self.python_jobs = []
        self.python_links = []
        

    def login(self):
        self.driver.get(self.home_url)
        # Reject cookies
        # Find a button that has the html attribute action-type and the value DENY
        time.sleep(2)
        reject_button = self.driver.find_element(By.CSS_SELECTOR, value="button[action-type = 'DENY']")
        reject_button.click()

        # Sign in
        # Find the button for sign in with mail
        time.sleep(2)
        sign_in_button = self.driver.find_element(By.LINK_TEXT, value='Sign in with email')
        sign_in_button.click()

        # Find an <input> element where the id contains username
        time.sleep(3)
        email_field = self.driver.find_element(By.CSS_SELECTOR, value='input[id=username]')
        email_field.send_keys(self.ACCOUNT_EMAIL)

        # Find an <input> element where the id contains password
        time.sleep(4)
        password_field = self.driver.find_element(By.CSS_SELECTOR, value='input[id=password]')
        password_field.send_keys(self.ACCOUNT_PASSWORD, Keys.ENTER)


    def search_jobs(self):
        # Search for Python jobs
        # Find an <input> element where the attribute value is Search
        time.sleep(2)
        search_field = self.driver.find_element(By.CSS_SELECTOR, value='input[placeholder=Search]')
        search_field.send_keys('Python')
        time.sleep(1)
        search_field.send_keys(Keys.ENTER)

        # Press 'all jobs' link text
        time.sleep(4)
        all_jobs = self.driver.find_element(By.LINK_TEXT, value='See all job results in Romania')
        all_jobs.click()


    def get_jobs(self):
        page_no = 1
        while page_no < PAGE_NO: 

            # Scroll the linstings
            time.sleep(4.2)
            for _ in range(2):
                listings_xpath = '//*[@id="main"]/div/div[2]/div[1]/div'
                
                listings_tab = self.driver.find_element(By.XPATH, value=listings_xpath)
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;", listings_tab)
                time.sleep(2)

            # Get all listings from all the pages 
            time.sleep(4)
            all_listings = self.driver.find_elements(By.CSS_SELECTOR, value='#main li .ember-view a')
            
            for listing in all_listings:
                job_title = listing.get_attribute('aria-label')
                self.jobs_titles.append(job_title) 
            
                job_link = listing.get_attribute('href') 
                self.jobs_links.append(job_link)

            page_number_button = self.driver.find_element(By. CSS_SELECTOR, value=f"button[aria-label = 'Page {str(page_no+1)}']") 
            page_number_button.click()
            page_no += 1 

        # Filter only Python jobs and links
        self.filter_jobs()


    def filter_jobs(self):        
        for title in self.jobs_titles:
            if 'Python' in title:
                py_idx = self.jobs_titles.index(title)
                self.python_jobs.append(self.jobs_titles[py_idx])
                self.python_links.append(self.jobs_links[py_idx])


    def export_data(self):
        jobs_data = {}

        for i in range(len(self.python_jobs)):
            jobs_data_dict = {
                'Job title' : self.python_jobs[i],
                'Job link' : self.python_links[i]
            }
            jobs_data[i] = jobs_data_dict
        print(jobs_data)
        # Export data to excel with pandas
        # Make a pandas DataFrame from the dictionary 
        df = pandas.DataFrame.from_dict(jobs_data, orient='index')
        print(df)

        # Export to excel
        df.to_excel(excel_writer='data.xlsx', index=False)