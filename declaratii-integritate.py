from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementNotInteractableException, NoSuchElementException
import csv
from datetime import datetime, timedelta


last_date = '15.07.2021'
target_csv = "../../data/declaratii.integritate.eu/declaratii-ani-x12.csv"
target_stats_csv = "../../data/declaratii.integritate.eu/stats12.csv"
days_delta = 12
timeout = 4
# 5 - Fetch data for each 2-day interval until January 1, 2008
end_date = "01.01.2020"

source_url = "https://declaratii.integritate.eu/index.html"
gecko_driver_path = '/usr/local/bin/geckodriver'

firefox_options = Options()
firefox_options.headless = False
driver = webdriver.Firefox(service=FirefoxService(executable_path=gecko_driver_path), options=firefox_options)

# 1 - Open the URL
driver.get(source_url)

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
if not last_date:
    current_date = datetime.now().strftime("%d.%m.%Y")
else: 
    current_date = last_date


with open(target_csv, "a", newline="") as csvfile, open(target_stats_csv, "a", newline="") as statsfile:
    csvwriter = csv.writer(csvfile)
    header = []
    stats_writer = csv.writer(statsfile)
    stats_header = ["start_date", "current_date", "results_count", "daily_total"]
    # stats_writer.writerow(stats_header)
    
    while current_date > end_date:
        dailystats = 0
        # Input the current start date and end date
        start_date = (datetime.strptime(current_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
        print('--- ' + str(start_date) + ' ' + str(current_date))
        driver.find_element(By.ID, "form:endDate_input").clear()
        driver.find_element(By.ID, "form:endDate_input").send_keys(current_date)
        driver.find_element(By.ID, "form:startDate_input").clear()
        driver.find_element(By.ID, "form:startDate_input").send_keys(start_date)

       
        footer = driver.find_element(By.ID, "footer")
        if footer:
            print('have footer')
        else:
            print('no footer')
        try:
            e10k =  driver.find_element(By.XPATH, "//form[@id='errorForm']/span[contains(text(),'mult de 10 000 de rezultate')]")
            if e10k:
                print (e10k.text)
                breakpoint()
            else:
                print ('ok 10k')
        except:
            pass

            # stats_writer.writerow([start_date, current_date, '10k-1 124', '0'])
            # current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
            # submit_button = driver.find_elements(By.XPATH, "//input[@id='errorForm:inchide' and @type='submit']")
            # if submit_button:
            #     try:                   
            #         submit_button[0].click()
            #         print("Clicked on the 'Închide' button.")     
            #     except:
            #         print(' //ERR 133: no submit button')
            #         breakpoint()
            #         pass
            #     break     


        # check 10k limt
        try:
            error_message = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//form[@id='errorForm']/span[contains(text(),' mult de 10 000 de rezultate']")
                )
            )
            if error_message:
                print(f" 10k-1 124  {start_date} to {current_date}")
                stats_writer.writerow([start_date, current_date, '10k-1 124', '0'])
                current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
                submit_button = driver.find_elements(By.XPATH, "//input[@id='errorForm:inchide' and @type='submit']")
                if submit_button:
                    try:                   
                        submit_button[0].click()
                        print("Clicked on the 'Închide' button.")     
                    except:
                        print(' //ERR 133: no submit button')
                        breakpoint()
                        pass
                    break                # TODO: click on change date, continue
                # breakpoint()
                pass
            
            continue
        except:
            pass

        # 6 - Check for the 'Căutarea întoarce mai mult de 10 000 de rezultate' message
        # error_form = driver.find_elements_by_id("errorForm")
        error_form = driver.find_elements(By.XPATH, "//form[@id='errorForm']")

        if error_form and error_form[0].text != '':
            print(f"// Err: 10k-2 139 for {start_date} to {current_date}")
            stats_writer.writerow([start_date, current_date, '10k2 139', '0'])
            current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
            submit_button = driver.find_elements(By.XPATH, "//input[@id='errorForm:inchide' and @type='submit']")
            if submit_button:
                try:                   
                    submit_button[0].click()
                    print("Clicked on the 'Închide' button.")     

                except:
                    pass
                break
        else:
            # print("The form with id 'errorForm' does not exist.")
            pass
        

        # 7 - Check for the 'Nu s-au găsit rezultate' message
        try:
            no_results_message = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@id='form:j_idt142_content']/h5[text()='Nu s-au găsit rezultate']")
                )
            )
          
            print(f" --> 0 results between {start_date} and {current_date}")
            stats_writer.writerow([start_date, current_date, '0', '0'])
            current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
            continue
        except:
            pass
        
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
                print(f"Timeout: 86 Search button not found for {start_date} to {current_date}")
                # current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
                continue

        search_button.click()

        # 8 - Find and print the number of results
        try:
            results_count = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h5[contains(text(),'Rezultatele căutării:')]/span[@id='form:_t148']")
                )
            )
            print(f" -> {results_count.text} results for {start_date} to {current_date}")
            stats_writer.writerow([start_date, current_date, results_count.text, dailystats])
            
        except:
            pass

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
                    header.append("Vezi declaratie")  # Add the 'Vezi declaratie' header
                    header.append("page")  # Add the 'page' header
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
                    row_data.append(vezi_declaratie_link)  # Add the 'Vezi declaratie' link
                    row_data.append(nxtpg)  # Add the 'Vezi declaratie' link
                    csvwriter.writerow(row_data)
                    dailystats += 1
            except TimeoutException:
                print(f"218 Timeout1: Results table not found for {start_date} to {current_date}")
                stats_writer.writerow([start_date, current_date, 'TO-1 218', '0'])
            # check if pagination and if next page active
            try:
                pagination = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ui-paginator-pages"))
                )

            
                # Check for the presence of the "Next" page link
                next_page_link = driver.find_elements(By.XPATH, "//a[@id='form:resultsTable_paginatorbottom_nextPageLink' and not(contains(@class, 'ui-state-disabled'))]")

                if not next_page_link:
                    next_page = False
                    # break  # No more pages to scrape
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
                        # pass  # Break the loop if the element is not interactable

            except (StaleElementReferenceException, NoSuchElementException, TimeoutException):
                next_page = False
                # pass  # Pagination section is not present
        
        # Update current_date for the next iteration

        current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
        # print('next date')
    

# Close the browser
driver.quit()
print("Finish")
