from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

# URL of the EduRank page for the UK
main_url = 'https://edurank.org/geo/gb/'

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

# Open the EduRank UK page
driver.get(main_url)

# Locate the university links
university_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/uni/"]')

# Extract the URLs of universities
university_urls = [link.get_attribute('href') for link in university_links]

# Create an empty DataFrame with the desired columns and save it to the CSV file
df = pd.DataFrame(columns=['University Name', 'University URL'])
df.to_csv('C:/Users/saman/OneDrive/Coding Portfolio/Web Scraper/UniWebScraper/university_data.csv', index=False)

# Initialize a counter and a set to track added universities
counter = 1
added_universities = set()

for university_url in university_urls:
    try:
        # Open the university page
        driver.get(university_url)

        # Extract the university name and remove ": Statistics"
        university_name = driver.find_element(By.TAG_NAME, 'h1').text.strip().replace(": Statistics", "")

        # Skip if the university has already been added
        if university_name in added_universities:
            continue

        # Locate the <a> element that contains .ac.uk in its href attribute
        university_ac_link = driver.find_element(By.CSS_SELECTOR, 'a[href*=".ac.uk"]')
        university_ac_url = university_ac_link.get_attribute('href')

        # Clean up the URL to end at .ac.uk
        university_ac_url = university_ac_url.split('.ac.uk')[0] + '.ac.uk'

        # Create a DataFrame with the university name and URL
        df = pd.DataFrame({'University Name': [university_name], 'University URL': [university_ac_url]})

        # Append the DataFrame to the CSV file
        df.to_csv('C:/Users/saman/OneDrive/Coding Portfolio/Web Scraper/UniWebScraper/university_data.csv', mode='a', index=False, header=False)

        # Print the university name and its position in the list
        print(f'{counter}. {university_name} added')

        # Increment the counter and add the university to the set
        counter += 1
        added_universities.add(university_name)
    except Exception as e:
        print(f'Failed to scrape the data for {university_url}: {e}')

# Close the browser
driver.quit()

print('Successfully scraped the data and saved it to university_data.csv')