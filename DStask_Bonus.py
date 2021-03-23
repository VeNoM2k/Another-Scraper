#Ashish Gour
#gourashish666@gmail.com

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

#install chrome and corresponding chrome driver
#load chrome driver location in PATH variable
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
job_driver = webdriver.Chrome(PATH)

url = 'https://jobs.lever.co/dreamsports'
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
#print(page.content)

jobs = []

#page = requests.get(url)
#soup = BeautifulSoup(page.content, 'html.parser')
#print(soup)

results = soup.find_all('div',{'class': 'postings-group'})
#print(len(results))
for result in results:
	postings = result.find_all('div',{'class': 'posting'})
	#print(len(postings))
	for posting in postings:
		one_job = []
		page = posting.find('a',{'class': 'posting-title'})
		job_url = page.get('href')
		title_tag = page.find('h5',{'data-qa': 'posting-name'})
		position_name = title_tag.text
		one_job.append(position_name)
		categories = page.find('div',{'class': 'posting-categories'})
		location_tag = categories.find('span', {'class': 'sort-by-location posting-category small-category-label'})
		location = location_tag.text
		one_job.append(location)
		jobId_tag = categories.find('span', {'class': 'sort-by-team posting-category small-category-label'})
		jobId = jobId_tag.text
		one_job.append(jobId)
		one_job.append(job_url)
		#print(position_name, location, jobId, job_url,)
		
		#Bonus
		job_driver.get(job_url)
		job_soup = BeautifulSoup(job_driver.page_source, 'html.parser')
		#job_page = requests.get(job_url)
		#job_soup = BeautifulSoup(job_page.content, 'html.parser')
		job_results = job_soup.find_all('div',{'class': 'section page-centered'})
		count = 0
		for job_result in job_results:
			if count < 4:
				job_divs = job_result.find_all('div')
				list1 = []
				for each_job_div in job_divs:
					list1.append(each_job_div.text)
				one_job.append(list1)
				count = count +1

		jobs.append(one_job)
		#print('Done*************')

frame = pd.DataFrame(jobs, columns = ['Position Name', 'Location', 'JobID', 'Page URL', 'Description', 'Job Description', 'Requirements: Must have', 'Requirements: Good to have'])
#print(frame)
frame.to_csv('Jobs.csv')

job_driver.close()
driver.close()
