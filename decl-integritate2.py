from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementNotInteractableException, NoSuchElementException
import csv
from datetime import datetime, timedelta

target_csv = "../../data/declaratii.integritate.eu/declaratii-ani.csv"
days_delta = 2
timeout = 2
end_date = "01.01.2008"
csv_downloads_folder = "/Users/pax/devbox/gov2/data/declaratii.integritate.eu/csvs/"
csv_basename = 'declaraii-'
source_url = "https://declaratii.integritate.eu/index.html"
err_log = "../../data/declaratii.integritate.eu/error.log"
gecko_driver_path = 'geckodriver/geckodriver'
current_date = "14.10.2023"  # custom date for testing

firefox_options = Options()
firefox_options.add_argument("--headless=new")
firefox_options.set_preference("browser.download.folderList", 2)
firefox_options.set_preference("browser.download.dir", csv_downloads_folder)
firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

driver = webdriver.Firefox(service=FirefoxService(executable_path=gecko_driver_path), options=firefox_options)
driver.get(source_url)

try:
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.ID, "form:showAdvancedSearch"))).click()
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "form:advanced-search-panel_content")))
    
    with open(target_csv, "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        header_written = False

        while current_date > end_date:
            start_date = (datetime.strptime(current_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
            
            # Re-locate and interact with date inputs
            try:
                driver.find_element(By.ID, "form:endDate_input").clear()
                driver.find_element(By.ID, "form:endDate_input").send_keys(current_date)
                driver.find_element(By.ID, "form:startDate_input").clear()
                driver.find_element(By.ID, "form:startDate_input").send_keys(start_date)
                
                WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.ID, "form:submitButtonAS"))).click()
            except Exception as e:
                print(f"Error interacting with search form: {e}")
                with open(err_log, 'a') as error_log:
                    error_log.write(f'Error on {current_date}: {e}\n')
                current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
                continue
            
            # Wait for results and handle pagination
            try:
                WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "form:resultsTable")))
                next_page = True
                while next_page:
                    # Re-find elements inside the loop
                    results_table = driver.find_element(By.ID, "form:resultsTable")
                    rows = results_table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header
                    
                    if not header_written:
                        headers = results_table.find_element(By.TAG_NAME, "tr").find_elements(By.TAG_NAME, "th")[:-1]
                        csvwriter.writerow([header.text for header in headers] + ["Vezi declaratie", "page", "rezultate", "start_date", "end_date"])
                        header_written = True
                    
                    for row in rows:
                        try:
                            cells = row.find_elements(By.TAG_NAME, "td")[:-1]
                            link = row.find_element(By.XPATH, ".//a[contains(text(),'Vezi document')]").get_attribute("href")
                            csvwriter.writerow([cell.text for cell in cells] + [link])
                        except StaleElementReferenceException:
                            continue
                    
                    # Check for and click the next page button if it exists
                    next_page_buttons = driver.find_elements(By.XPATH, "//a[@aria-label='Next Page' and not(@class='ui-state-disabled')]")
                    if next_page_buttons:
                        next_page_buttons[0].click()
                    else:
                        next_page = False
            except Exception as e:
                print(f"Error processing results or navigating pages: {e}")
                with open(err_log, 'a') as error_log:
                    error_log.write(f'Error on {current_date}: {e}\n')
            
            current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")

finally:
    driver.quit()
    print("Script completed.")
