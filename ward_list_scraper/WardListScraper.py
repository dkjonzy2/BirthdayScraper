# Birthday Scraper
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import os
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

path_to_chromedriver = '/Users/danjones/Downloads/chrome-mac-arm64' # change path as needed

driver = webdriver.Chrome()

wait = WebDriverWait(driver, 30)
driver.get("https://lcr.churchofjesuschrist.org/report/birthday-list?lang=eng")

try:
    username_field = wait.until(EC.element_to_be_clickable((By.NAME, "identifier")))
    print("Username field located")
    username_field.send_keys(os.environ['LCR_ACCOUNT'])
    print("Username entered")
except Exception as e:
    print(f"Error locating or entering username: {e}")

time.sleep(1)

try:
    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Next']")))
    print("Next button located")
    next_button.click()
    print("Next button clicked")
except Exception as e:
    print(f"Error locating or clicking next button: {e}")

time.sleep(1)

try:
    password_field = wait.until(EC.element_to_be_clickable((By.NAME, "credentials.passcode")))
    print("Password field located")
    password_field.send_keys(os.environ['LCR_PASSWORD'])
    print("Password entered")
except Exception as e:
    print(f"Error locating or entering password: {e}")

time.sleep(1)

try:
    verify_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Verify']")))
    print("Verify button located")
    verify_button.click()
    print("Verify button clicked")
except Exception as e:
    print(f"Error locating or clicking verify button: {e}")

print("Logged in")

wait.until(EC.visibility_of_element_located((By.ID, "menuItem7")))
print(driver.title)
driver.get("https://lcr.churchofjesuschrist.org/records/member-list?lang=eng")
print(driver.title)

# Wait for the table to load
time.sleep(5)

# Get all the rows
rows = driver.find_elements(By.CSS_SELECTOR, "#mainContent > div:nth-child(5) > table > tbody > tr")

print("Found {} rows".format(len(rows)))

# Create an empty list to hold the data
data = []

# Iterate through each row
for row in rows:
    # Get all the columns in the row
    cols = row.find_elements(By.TAG_NAME, "td")
    
    # Extract the text from each column
    name = cols[1].text
    gender = cols[3].text
    age = cols[4].text
    birthdate = cols[5].text
    
    # Extract the address, handling line breaks
    address_html = cols[6].get_attribute('innerHTML')
    address = address_html.replace('<br>', ', ').replace('\n', '').strip()
    
    phone = cols[7].text
    email = cols[8].text
    
    # Append the data to the list
    data.append([name, gender, age, birthdate, address, phone, email])

# Create a DataFrame from the list
df = pd.DataFrame(data, columns=["Name", "Gender", "Age", "Birthdate", "Address", "Phone", "Email"])

# Export the DataFrame to a CSV file
df.to_csv("members.csv", index=False)
print("Exported data to CSV file")
print("Done")