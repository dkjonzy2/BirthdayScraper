# Klaviyo Agency Partners Scraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

path_to_chromedriver = '/Users/danjones/Downloads/chrome-mac-arm64' # change path as needed

driver = webdriver.Chrome()

wait = WebDriverWait(driver, 30)
driver.get("https://connect.klaviyo.com/")

# Click the "Load More" button until all results are loaded
while True:
    try:
        load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test-load-more-button]")))
        load_more_button.click()
        time.sleep(2)  # wait for new results to load
    except Exception as e:
        print("No more 'Load More' button found or error occurred:", e)
        break

# Extract all the names and tiers of the agency partners
data = []
try:
    partner_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-test-service-partner-card]")))
    for element in partner_elements:
        name = element.find_element(By.CSS_SELECTOR, "h2[data-test-partner-name]").text.strip()
        tier = element.find_element(By.CSS_SELECTOR, "div[data-test-tier-name]").text.strip()
        data.append({"Name": name, "Tier": tier})
    print(f"Found {len(data)} partners")
except Exception as e:
    print(f"Error extracting data: {e}")

# Create a DataFrame from the list
df = pd.DataFrame(data)

# Export the DataFrame to a CSV file
df.to_csv("klaviyo_agency_partners.csv", index=False)
print("Exported data to CSV file")
print("Done")

driver.quit()