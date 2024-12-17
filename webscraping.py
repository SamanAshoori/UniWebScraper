from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

# List of URLs to scrape
main_urls = [
    'https://www.mmu.ac.uk/study/undergraduate/subject/computing',
    'https://www.mmu.ac.uk/study/undergraduate/subject/engineering',
    'https://www.mmu.ac.uk/study/undergraduate/subject/accounting-and-finance',
    'https://www.mmu.ac.uk/study/undergraduate/subject/acting-and-drama',
    'https://www.mmu.ac.uk/study/undergraduate/subject/architecture',
    'https://www.mmu.ac.uk/study/undergraduate/subject/art-and-design',
    'https://www.mmu.ac.uk/study/undergraduate/subject/biology-and-conservation',
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
df.to_csv('C:/Users/saman/OneDrive/Coding Portfolio/Web Scraper/UniWebScraper/course_data_new.csv', index=False)

for main_url in main_urls:
    # Open the main webpage
    driver.get(main_url)

    # Locate the div elements with the class 'u-grid gap-8 md\\:u-grid-cols-2'
    course_divs = driver.find_elements(By.CSS_SELECTOR, 'div.u-grid.gap-8.md\\:u-grid-cols-2 div[about]')

    # Extract the URLs from the 'about' attribute
    urls = [div.get_attribute('about') for div in course_divs]

    for url in urls:
        try:
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
            level_of_study_cap = level_of_study.capitalize()

            # Create a DataFrame with the course title, entry requirements, and level of study
            df = pd.DataFrame({'Course Title': [course_title], 'Entry Requirements': [grades], 'Level of Study': [level_of_study_cap]})

            # Append the DataFrame to the CSV file
            df.to_csv('C:/Users/saman/OneDrive/Coding Portfolio/Web Scraper/UniWebScraper/course_data_new.csv', mode='a', index=False, header=False)
        except Exception as e:
            print(f'Failed to scrape the data for {url}: {e}')

# Close the browser
driver.quit()

print('Successfully scraped the data and saved it to course_data_new.csv')