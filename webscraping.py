from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

# URL of the website to scrape
urls = [
    'https://www.mmu.ac.uk/study/undergraduate/course/bsc-computer-science',
    'https://www.mmu.ac.uk/study/undergraduate/course/beng-electrical-and-electronic-engineering'
]

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
chrome_options.add_argument("--allow-insecure-localhost")  # Allow insecure localhost

# Set up the Chrome driver
service = Service('C:/Users/saman/Documents/chromedriver-win64/chromedriver.exe')  # Update with the correct path to chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Create an empty DataFrame with the desired columns and save it to the CSV file
df = pd.DataFrame(columns=['Course Title', 'Entry Requirements', 'Level of Study'])
df.to_csv('C:/Users/saman/OneDrive/Coding Portfolio/Web Scraper/UniWebScraper/course_Data_New1.3.csv', index=False)

for url in urls:
    # Open the webpage
    driver.get(url)

    # Extract the course title
    course_title = driver.find_element(By.TAG_NAME, 'h1').text.strip()

    # Extract the first <p> element from the <div class="links">
    entry_requirements_div = driver.find_element(By.CLASS_NAME, 'entry-requirements')
    first_paragraph = entry_requirements_div.find_element(By.TAG_NAME, 'p').text.strip()
    first_paragraph_grades = first_paragraph.find('grades ')  # Find the index of the word 'grades '
    grades = first_paragraph[first_paragraph_grades + 7: first_paragraph_grades + 10]  # Extract the grades

    # Extract the level of study from the URL
    level_of_study = url.split('/study/')[1].split('/')[0]
    cap_level_of_study = level_of_study.capitalize() # Capitalize the level of study properly (e.g., 'undergraduate' -> 'Undergraduate')

    # Create a DataFrame with the course title, entry requirements, and level of study
    df = pd.DataFrame({'Course Title': [course_title], 'Entry Requirements': [grades], 'Level of Study': [cap_level_of_study]})

    # Append the DataFrame to the CSV file
    df.to_csv('C:/Users/saman/OneDrive/Coding Portfolio/Web Scraper/UniWebScraper/course_Data_New1.3.csv', mode='a', index=False, header=False)

# Close the browser
driver.quit()

print('Successfully scraped the data and saved it to course_data_new.csv')