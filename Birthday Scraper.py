# Birthday Scraper
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

path_to_chromedriver = '/Users/danjones/Downloads/chrome-mac-arm64' # change path as needed

driver = webdriver.Chrome()

wait = WebDriverWait(driver, 30)
driver.get("https://lcr.churchofjesuschrist.org/report/birthday-list?lang=eng")

wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(ACCOUNT)
time.sleep(1)
wait.until(EC.element_to_be_clickable((By.ID, "okta-signin-submit"))).click()
time.sleep(1)
wait.until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(PASSWORD)
time.sleep(1)
wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Verify']"))).click()
print("Logged in")

wait.until(EC.visibility_of_element_located((By.ID, "menuItem7")))
print(driver.title)
driver.get("https://lcr.churchofjesuschrist.org/report/birthday-list?lang=eng")
print(driver.title)

# Locate the select element
select_element = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@class='sc-xne1im-0 kWhksG']//select[@class='sc-11vq36o-0 dvAIOs'])[3]"))
)

# Create a Select object
select = Select(select_element)

# Select an option by its value (e.g., to show 3 months)
select.select_by_value('12')

# Wait for the table to load
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "tr.sc-zkgtp5-0.iooGpB.sc-bee01cd9-2.jbMyIm")))

# Get all the rows
rows = driver.find_elements(By.CSS_SELECTOR, "tr.sc-zkgtp5-0.iooGpB.sc-bee01cd9-2.jbMyIm")
print("Found {} rows".format(len(rows)))
# Create an empty list to hold the data
data = []

# Iterate through each row
for row in rows:
    # Get all the columns in the row
    cols = row.find_elements(By.TAG_NAME, "td")
    
    # Extract the text from each column
    date = cols[0].text
    name = cols[1].text
    age = cols[2].text
    phone = cols[3].text
    address = cols[4].text
    
    # Append the data to the list
    data.append([date, name, age, phone, address])

# Create a DataFrame from the list
df = pd.DataFrame(data, columns=["Date", "Name", "Age", "Phone", "Address"])

# Export the DataFrame to a CSV file
df.to_csv("birthdays.csv", index=False)
print("Exported data to CSV file")
print("Done")