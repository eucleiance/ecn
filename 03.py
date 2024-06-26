from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import time

# Initialize the WebDriver without headless mode to show the browser window
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors") 
options.add_argument('--disable-gpu')  
driver = webdriver.Chrome(options=options)

# Open the webpage
site_input = "https://voterlist.election.gov.np/bbvrs1/index_2.php"
site_database = "https://voterlist.election.gov.np/bbvrs1/view_ward_1.php"

#driver.get("https://voterlist.election.gov.np/bbvrs1/index_2.php")
driver.get(site_input)

# Define a function to click an option and wait for the next dropdown to become clickable 
def click_option_and_wait(option, next_dropdown_id):
    try:
        option.click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, next_dropdown_id)))
    except StaleElementReferenceException:
        state_dropdown = Select(driver.find_element(By.ID, "state"))
        district_dropdown = Select(driver.find_element(By.ID, "district"))
        vdc_mun_dropdown = Select(driver.find_element(By.ID, "vdc_mun"))
        ward_dropdown = Select(driver.find_element(By.ID, "ward"))
        reg_centre_dropdown = Select(driver.find_element(By.ID, "reg_centre"))
        option.click() 
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, next_dropdown_id)))

def locate_all():
    try:
        state_dropdown = Select(driver.find_element(By.ID, "state"))
        district_dropdown = Select(driver.find_element(By.ID, "district"))
        vdc_mun_dropdown = Select(driver.find_element(By.ID, "vdc_mun"))
        ward_dropdown = Select(driver.find_element(By.ID, "ward"))
        reg_centre_dropdown = Select(driver.find_element(By.ID, "reg_centre"))
    except NoSuchElementException as e:
        print("Element not found:", e)
    except StaleElementReferenceException as e:
        print("Stale element reference:", e)

# def click_option_and_wait(option, next_dropdown_id):
#     option.click()
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, next_dropdown_id)))

def click_option_and_wait_xpath(option, XPATH_str):
    option.click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, XPATH_str)))

time.sleep(2)

sym_count = 0
with open("dataset_04.txt", "w") as file:
    # Loop through each option in state dropdown
    state_dropdown = Select(driver.find_element(By.ID, "state"))
    for state_option in state_dropdown.options[4:5]:
        state_opt_bak = state_option
        locate_all()
        # state_option.click()
        click_option_and_wait(state_option, "district")
        current_state_name = state_option.text
        total_states_count = len(state_dropdown.options)-1
        print(f"{total_states_count} States")
        print(current_state_name)

        
        district_dropdown = Select(driver.find_element(By.ID, "district"))
        for district_option in district_dropdown.options[6:7]:
            district_opt_bak = district_option
            locate_all()

            click_option_and_wait(state_option, "district")
            click_option_and_wait(district_option, "vdc_mun")

            current_district_name = district_option.text
            total_district_count = len(district_dropdown.options)-1
            print(f"{total_district_count} Districts")
            print(current_district_name)
            # click_option_and_wait(district_option, "vdc_mun")
            
            vdc_mun_dropdown = Select(driver.find_element(By.ID, "vdc_mun"))
            for vdc_mun_option in vdc_mun_dropdown.options[1:]:
                vdc_mun_opt_bak = vdc_mun_option
                locate_all()
                # state_option.click()
                # district_option.click()
                # vdc_mun_option.click()

                click_option_and_wait(state_option, "district")
                click_option_and_wait(district_option, "vdc_mun")
                click_option_and_wait(vdc_mun_option, "ward")

                current_vdc_mun_name = vdc_mun_option.text
                total_vdc_mun_count = len(vdc_mun_dropdown.options)-1
                print(f"{total_vdc_mun_count} VDC/MUN(s)")
                print(current_vdc_mun_name)
                # click_option_and_wait(vdc_mun_option, "ward")
                
                ward_dropdown = Select(driver.find_element(By.ID, "ward"))
                for ward_option in ward_dropdown.options[1:]:
                    ward_opt_bak = ward_option
                    locate_all()
                    click_option_and_wait(state_option, "district")
                    click_option_and_wait(district_option, "vdc_mun")
                    click_option_and_wait(vdc_mun_option, "ward")
                    click_option_and_wait(ward_option, "reg_centre")

                    current_ward_name = ward_option.text
                    total_ward_count = len(ward_dropdown.options)-1
                    print(f"{total_ward_count} Wards")
                    print(current_ward_name)
                    # click_option_and_wait(ward_option, "reg_centre")
                    
                    reg_centre_dropdown = Select(driver.find_element(By.ID, "reg_centre"))
                    for reg_centre_option in reg_centre_dropdown.options[1:]:
                        locate_all()
                        click_option_and_wait(state_option, "district")
                        click_option_and_wait(district_option, "vdc_mun")
                        click_option_and_wait(vdc_mun_option, "ward")
                        click_option_and_wait(ward_option, "reg_centre")
                        reg_centre_option.click()

                        current_reg_centre_name = reg_centre_option.text
                        total_reg_centre_count = len(reg_centre_dropdown.options)-1

                        # reg_centre_option.click()

                        print(f"{total_reg_centre_count} Reg Centres")
                        print(current_reg_centre_name)
                        form = driver.find_element(By.ID, "frmSubmit")
                        driver.execute_script("arguments[0].setAttribute('target', '_blank')", form)

                        submit_button = driver.find_element(By.ID, "btnSubmit")
                        reset_button = driver.find_element(By.ID, "reset")
                        submit_button.click()

                        # Switch to the new tab
                        windows = driver.window_handles
                        driver.switch_to.window(windows[-1])  # Switches to the latest opened tab

                        # time.sleep(1000)
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="frmSubmit"]/table/tbody/tr[2]/td/table/thead/tr[2]/th/a[12]')))

                        alphabet_to_click = driver.find_element(By.XPATH, '//*[@id="frmSubmit"]/table/tbody/tr[2]/td/table/thead/tr[2]/th/a[12]')
                        alphabet_to_click.click()

                        hundred_rows = driver.find_element(By.XPATH, '//*[@id="tbl_data_length"]/label/select/option[4]')
                        hundred_rows.click()

                        total_pages_text = driver.find_element(By.XPATH, '//*[@id="tbl_data_info"]').text
                        print(total_pages_text)
                        total_pages_str = total_pages_text.split()[-7]  # Get the string containing the number
                        total_pages = int(total_pages_str.replace(',', ''))  # Remove commas and convert to integer
                        print(total_pages)
                        if total_pages > 0 and total_pages <= 100:
                            iterator = 1
                        elif total_pages > 100 and total_pages <= 200:
                            iterator = 2
                        elif total_pages > 200 and total_pages <= 300:
                            iterator = 3
                        elif total_pages > 300 and total_pages <= 400:
                            iterator = 4
                        elif total_pages > 400 and total_pages <= 500:
                            iterator = 5
                        elif total_pages > 500 and total_pages <= 600:
                            iterator = 6
                        else:
                            iterator = 7

                        print(iterator)

                        for i in range (1, (iterator+1)):
                            row_number = 1
                            entries_on_page = driver.find_elements(By.XPATH, '//*[@id="tbl_data"]/tbody/tr')
                            # for row in entries_on_page:
                            #     entries_xpath = f'//*[@id="tbl_data"]/tbody/tr[{row_number}]'
                            #     row_number = row_number + 1
                            #     entries = driver.find_element(By.XPATH, entries_xpath)
                            #     cell_texts = [cell.text for cell in entries.find_elements(By.XPATH, './/td')]
                            #     data = ', '.join(cell_texts)
                            #     print(data)
                            #     sym_count = sym_count + 1
                            #     file.write("S/N: {}  State: {}  District: {}  VDC: {}  Ward: {}  VB: {} Entry: {}\n".format(sym_count, current_state_name, current_district_name, current_vdc_mun_name, current_ward_name, current_reg_centre_name, data))
                            # file.write("\n")
                            # file.write("\n")
                            next_btn = driver.find_element(By.XPATH, '//*[@id="tbl_data_next"]')
                            next_btn.click()

                        driver.close()
                        driver.switch_to.window(windows[0])
                        driver.get(site_input)
                        driver.refresh()
                        # Locate Everything Again



                        # time.sleep(1000)
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'state')))
                        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'district')))
                        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'vdc_mun')))
                        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ward')))
                        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'reg_centre')))

                        # Write innerHTML of the current reg_centre option to file
                        #file.write("VDC: {}  Ward: {}  VB: {}\n".format(current_vdc_mun_name, current_ward_name, current_reg_centre_name))
# Add a delay to keep the browser window open for some time
time.sleep(5)

# Close the WebDriver
driver.quit()
