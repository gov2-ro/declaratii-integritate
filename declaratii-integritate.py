from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementNotInteractableException, NoSuchElementException
import csv
from datetime import datetime, timedelta
import os
import sys

 
 
target_csv = "../../data/declaratii.integritate.eu/declaratii-ani.csv"
scrapping_log = "../../data/declaratii.integritate.eu/scrapping-log.csv"
days_delta = 2
timeout = 2 # 5 - Fetch data for each 2-day interval until January 1, 2008
end_date = "01.01.2008"

csv_downloads_folder = "/Users/pax/devbox/gov2/data/declaratii.integritate.eu/csvs/"
csv_basename = 'declaraii-'

source_url = "https://declaratii.integritate.eu/index.html"

err_log = "../../data/declaratii.integritate.eu/error.log"
# gecko_driver_path = '/usr/local/bin/geckodriver'
gecko_driver_path = 'geckodriver/geckodriver'

firefox_options = Options()
# firefox_options.headless = False #deprecated
firefox_options.add_argument("--headless=new")
firefox_options.set_preference("browser.download.folderList", 2)  # Save to a specific directory
firefox_options.set_preference("browser.download.dir", csv_downloads_folder)  # Set the download directory
firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")  # Automatically download files


def log_activity(activity_details):
    with open(scrapping_log, 'a', newline='') as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow(activity_details)

current_date = datetime.now().strftime("%d.%m.%Y")
# current_date = "14.10.2023" #custom
# read last date from scrapping_log and set current_date as that date minus 1 day

runs = 0
while current_date > end_date:
    runs += 1
    try:
        print(f"Run {runs} - {current_date}")
        try:
            with open(scrapping_log, 'r') as log_file:
                log_reader = csv.reader(log_file)
                last_row = list(log_reader)[-1]
                current_date = (datetime.strptime(last_row[1], "%d.%m.%Y") - timedelta(days=1)).strftime("%d.%m.%Y")
        except:
            log_activity([datetime.now(), current_date, '--', 'err', 'pass 56'])
            pass

        driver = webdriver.Firefox(service=FirefoxService(executable_path=gecko_driver_path), options=firefox_options)

        # 1 - Open the URL
        driver.get(source_url)

        # 2 - Click 'Căutare avansată' button if it's already present; otherwise, wait for it
        advanced_search_button = None

        try:
            print('-- init')
            try:
                advanced_search_button = driver.find_element(By.ID, "form:showAdvancedSearch")
            except:
                log_activity([datetime.now(), current_date, '--', 'err', 'pass 59'])
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
                log_activity([datetime.now(), current_date, '--', 'err', 'pass 75'])
                pass

            if advanced_search_panel is None:
                advanced_search_panel = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.ID, "form:advanced-search-panel_content"))
                )

            # 4 - Get the current date

            with open(target_csv, "a", newline="") as csvfile:
                # download csv index
                csvwriter = csv.writer(csvfile)
                # TODO: write saved date to scrapping_log
                log_activity([datetime.now(), current_date, 'csvd?', 'ok', 'saved csv'])

                header = []

                while current_date > end_date:
                    # Input the current start date and end date
                    start_date = (datetime.strptime(current_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
                    print('--- ' + str(start_date) + ' ' + str(current_date))
                    driver.find_element(By.ID, "form:endDate_input").clear()
                    driver.find_element(By.ID, "form:endDate_input").send_keys(current_date)
                    driver.find_element(By.ID, "form:startDate_input").clear()
                    driver.find_element(By.ID, "form:startDate_input").send_keys(start_date)

                    # 5 - Click on the search button if it's already present; otherwise, wait for it
                    search_button = None

                    try:
                        search_button = driver.find_element(By.ID, "form:submitButtonAS")
                    except:
                        breakpoint()
                        pass

                    if search_button is None:
                        try:
                            search_button = WebDriverWait(driver, timeout).until(
                                EC.element_to_be_clickable((By.ID, "form:submitButtonAS"))
                            )
                        except TimeoutException:
                            print(f"Timeout: 86 Search button not found for {start_date} to {current_date}")
                            # current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
                            continue

                    try: 
                        search_button.click()
                    except:
                        try:
                            item = driver.find_element(By.CSS_SELECTOR, "#_t161").get_attribute('innerText')
                            if '10 000' in item:
                                print('has 10k')
                                submit_button = driver.find_element(By.XPATH, "//input[@id='errorForm:inchide' and @type='submit']")
                                if submit_button.is_displayed():
                                    submit_button.click()
                                    print('next')
                                    # save to log, revisit later
                                    with open(err_log, 'a') as error_log:
                                        error_log.write(f'{current_date}\n')
                                    continue
                                    current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
                                    continue
                                else:
                                    pass

                        except NoSuchElementException:
                            print("H3 element or its parent dialog not found")
                            log_activity([datetime.now(), current_date, '--', 'err 165', 'H3 element or its parent dialog not found'])
                            # breakpoint()
                            print('re-init')
                            # os.execv(sys.executable, ['python'] + sys.argv)
                            break

                    # 8 - Find and print the number of results
                    rez_count = 0
                    try:
                        results_count = WebDriverWait(driver, timeout).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//h5[contains(text(),'Rezultatele căutării:')]/span")
                            )
                        )
                        print(f" -> {results_count.text} results for {start_date} to {current_date}")
                        rez_count = results_count.text
                    except:
                        log_activity([datetime.now(), current_date, '-', 'err', 'pass 156'])
                        

                    # 9.0 save csv file
                    export_button = None
                    try:
                        export_button = driver.find_element(By.ID, "form:dataExporter")
                    except:
                        log_activity([datetime.now(), current_date, '--', 'err', 'pass 164'])
                        pass
                    if export_button is None:
                        try:
                            export_button = WebDriverWait(driver, timeout).until(
                                EC.element_to_be_clickable((By.ID, "form:dataExporter"))
                            )
                        except Exception as e:
                            print(e)
                            # TODO: log error    
                    try:
                        driver.execute_script("arguments[0].scrollIntoView();", export_button)
                    except Exception as e:
                        print(e)
                        log_activity([datetime.now(), current_date, '- 178', 'err', str(e)])
                    try:
                        export_button.click() # Click the "Export" button
                        # TODO: change download name
                        log_activity([datetime.now(), current_date, 'real savecsv', 'ok', 'xx saved csv'])
                    except Exception as e:
                        print(e)
                        log_activity([datetime.now(), current_date, '- 183', 'err', str(e)])

                    # 9 - Find the table and save data to CSV file
                    next_page = True
                    nxtpg = 0
                    while next_page:
                        if not header:  
                            try:
                                results_table = WebDriverWait(driver, timeout).until(
                                    EC.presence_of_element_located((By.ID, "form:resultsTable"))
                                )
                                rows = results_table.find_elements(By.TAG_NAME, "tr")
                                header = [header.text for header in rows[0].find_elements(By.TAG_NAME, "th")[:-1]]  # Exclude the last 'Distribuie' header
                                header.append("Vezi declaratie")  
                                header.append("page")  
                                header.append("rezultate")  
                                header.append("start_date")  
                                header.append("end_date")
                                csvwriter.writerow(header)
                            except TimeoutException:
                                print(f"170 Timeout: Results table not found for {start_date} to {current_date}")
                                current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=1)).strftime("%d.%m.%Y")
                                break

                        try:
                            results_table = WebDriverWait(driver, timeout).until(
                                EC.presence_of_element_located((By.ID, "form:resultsTable"))
                            )
                            rows = results_table.find_elements(By.TAG_NAME, "tr")

                            for row in rows[1:]:
                                cells = row.find_elements(By.TAG_NAME, "td")[:-1]  # Exclude the last 'Distribuie' column
                                vezi_declaratie_link = row.find_element(By.XPATH, ".//a[contains(text(),'Vezi document')]").get_attribute("href")
                                row_data = [cell.text for cell in cells]
                                row_data.append(vezi_declaratie_link)  
                                row_data.append(nxtpg)  
                                row_data.append(rez_count)  
                                row_data.append(start_date)  
                                row_data.append(current_date)  
                                csvwriter.writerow(row_data)
                                csvwriter.writerow(row_data)
                        except TimeoutException:
                            print(f"187 Timeout: Results table not found for {start_date} to {current_date}")
                        # check if pagination and if next page active
                        try:
                            pagination = WebDriverWait(driver, timeout).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "ui-paginator-pages"))
                            )

                            # Check for the presence of the "Next" page link
                            next_page_link = driver.find_elements(By.XPATH, "//a[@id='form:resultsTable_paginatorbottom_nextPageLink' and not(contains(@class, 'ui-state-disabled'))]")

                            if not next_page_link:
                                next_page = False
                            else:
                                next_page = True

                                # Scroll to the "Next" page link and then click it
                                try:
                                    driver.execute_script("arguments[0].scrollIntoView();", next_page_link[0])
                                    next_page_link[0].click()
                                    next_page = True
                                    nxtpg += 1
                                    print('    - p ' + str(nxtpg))
                                except ElementNotInteractableException:
                                    next_page = False

                        except (StaleElementReferenceException, NoSuchElementException, TimeoutException):
                            next_page = False
                    # write current_date to scrapping_log

                    log_activity([datetime.now(), current_date, 'tbscrp', '', ''])

                    # Update current_date for the next iteration
                    current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
                    # print('next date')
        except Exception as e:
                print(f"broken loop Error occurred: {e}")
                log_activity([datetime.now(), current_date, 'broken loop', 'err end 281', str(e)])
            
        # Close the browser
        driver.quit()
        print("q1 done")
    except Exception as e:
        print(f"Error occurred: {e}")
        log_activity([datetime.now(), current_date, 'broken loop', 'err end 287 run: ' + str(runs), str(e)])
        # Close the browser
        driver.quit()
        print("q2 done")
        continue

print("done")
log_activity([datetime.now(), current_date, 'done', 'ok', 'finished proper? run: ' + str(runs)])