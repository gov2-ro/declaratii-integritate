from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementNotInteractableException, NoSuchElementException
import csv
from datetime import datetime, timedelta

timeout = 10  # Increase the timeout value
gecko_driver_path = '/usr/local/bin/geckodriver'
target_csv = "../../data/declaratii.integritate.eu/decl-integritate.csv"  # Updated CSV path

# Create a new instance of the Firefox driver
firefox_options = Options()
firefox_options.headless = False
driver = webdriver.Firefox(service=FirefoxService(executable_path=gecko_driver_path), options=firefox_options)

# 1 - Open the URL
driver.get("https://declaratii.integritate.eu/index.html")

# 2 - Click 'Căutare avansată' button if it's already present; otherwise, wait for it
advanced_search_button = None

try:
    advanced_search_button = driver.find_element(By.ID, "form:showAdvancedSearch")
except:
    pass

if advanced_search_button is None:
    advanced_search_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, "form:showAdvancedSearch"))
    )

advanced_search_button.click()

# 3 - Wait for the advanced search panel to load if it's already present; otherwise, wait for it
advanced_search_panel = None

try:
    advanced_search_panel = driver.find_element(By.ID, "form:advanced-search-panel_content")
except:
    pass

if advanced_search_panel is None:
    advanced_search_panel = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, "form:advanced-search-panel_content"))
    )

# 4 - Get the current date
current_date = datetime.now().strftime("%d.%m.%Y")

# 5 - Fetch data for each 2-day interval until January 1, 2008
end_date = "01.01.2008"

with open(target_csv, "w", newline="") as csvfile:  # Updated CSV path
    csvwriter = csv.writer(csvfile)
    header = []

    while current_date > end_date:
        # Input the current start date and end date
        start_date = (datetime.strptime(current_date, "%d.%m.%Y") - timedelta(days=2)).strftime("%d.%m.%Y")

        driver.find_element(By.ID, "form:endDate_input").clear()
        driver.find_element(By.ID, "form:endDate_input").send_keys(current_date)
        driver.find_element(By.ID, "form:startDate_input").clear()
        driver.find_element(By.ID, "form:startDate_input").send_keys(start_date)

        # 5 - Click on the search button if it's already present; otherwise, wait for it
        search_button = None

        try:
            search_button = driver.find_element(By.ID, "form:submitButtonAS")
        except:
            pass

        if search_button is None:
            try:
                search_button = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.ID, "form:submitButtonAS"))
                )
            except TimeoutException:
                print(f"Timeout: Search button not found for {start_date} to {current_date}")
                current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=1)).strftime("%d.%m.%Y")
                continue

        search_button.click()

        # Handle pagination if the pagination section is present
        try:
            pagination = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ui-paginator-pages"))
            )

            while True:
                results_table = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.ID, "form:resultsTable"))
                )
                rows = results_table.find_elements(By.TAG_NAME, "tr")

                if not header:
                    header = [header.text for header in rows[0].find_elements(By.TAG_NAME, "th")[:-1]]  # Exclude the last 'Distribuie' header
                    header.append("Vezi declaratie")  # Add the 'Vezi declaratie' header
                    csvwriter.writerow(header)

                for row in rows[1:]:
                    cells = row.find_elements(By.TAG_NAME, "td")[:-1]  # Exclude the last 'Distribuie' column
                    vezi_declaratie_link = row.find_element(By.XPATH, ".//a[contains(text(),'Vezi document')]").get_attribute("href")
                    row_data = [cell.text for cell in cells]
                    row_data.append(vezi_declaratie_link)  # Add the 'Vezi declaratie' link
                    csvwriter.writerow(row_data)

                # Check for the presence of the "Next" page link
                next_page_link = driver.find_elements(By.XPATH, "//a[@id='form:resultsTable_paginatorbottom_nextPageLink' and not(contains(@class, 'ui-state-disabled'))]")

                if not next_page_link:
                    break  # No more pages to scrape

                # Scroll to the "Next" page link and then click it
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", next_page_link[0])
                    next_page_link[0].click()
                except ElementNotInteractableException:
                    break  # Break the loop if the element is not interactable

        except (StaleElementReferenceException, NoSuchElementException, TimeoutException):
            pass  # Pagination section is not present

        # Update current_date for the next iteration
        current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=1)).strftime("%d.%m.%Y")

# Close the browser
driver.quit()
print("Finish")
