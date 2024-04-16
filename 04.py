from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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
    option.click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, next_dropdown_id)))

time.sleep(2)

# Find the dropdown elements
state_dropdown = Select(driver.find_element(By.ID, "state"))

# Open file to write the output

sym_count = 0
with open("dataset_05.txt", "w") as file:
    # Loop through each option in state dropdown
    for state_index, state_option in enumerate(state_dropdown.options[4:5]):
        current_state_name = state_option.text
        print(current_state_name)
        click_option_and_wait(state_option, "district")

        district_dropdown = Select(driver.find_element(By.ID, "district"))
        district_options = district_dropdown.options[6:7]
        for district_index, district_option in enumerate(district_options):
            current_district_name = district_option.text
            print(current_district_name)
            click_option_and_wait(district_option, "vdc_mun")

            vdc_mun_dropdown = Select(driver.find_element(By.ID, "vdc_mun"))
            vdc_mun_options = vdc_mun_dropdown.options[1:]
            for vdc_mun_index, vdc_mun_option in enumerate(vdc_mun_options):
                current_vdc_mun_name = vdc_mun_option.text
                print(current_vdc_mun_name)
                click_option_and_wait(vdc_mun_option, "ward")

                ward_dropdown = Select(driver.find_element(By.ID, "ward"))
                ward_options = ward_dropdown.options[1:]
                for ward_index, ward_option in enumerate(ward_options):
                    current_ward_name = ward_option.text
                    print(current_ward_name)
                    click_option_and_wait(ward_option, "reg_centre")

                    reg_centre_dropdown = Select(driver.find_element(By.ID, "reg_centre"))
                    reg_centre_options = reg_centre_dropdown.options[1:]
                    for reg_centre_index, reg_centre_option in enumerate(reg_centre_options):
                        current_reg_centre_name = reg_centre_option.text
                        submit_button = driver.find_element(By.ID, "btnSubmit")
                        reset_button = driver.find_element(By.ID, "reset")
                        submit_button.submit()

                        # Your code to process the data

                    # Check if all reg_centres for the current ward are exhausted
                    if reg_centre_options.index(reg_centre_option) == len(reg_centre_options) - 1:
                        # Reset for the next ward
                        ward_dropdown.select_by_index(ward_dropdown.first_selected_option.index + 1)
                        click_option_and_wait(ward_dropdown.first_selected_option, "reg_centre")
                    else:
                        # Continue to the next iteration of the ward loop
                        continue

                # Check if all wards for the current VDC/Mun are exhausted
                if ward_dropdown.first_selected_option.index == len(ward_dropdown.options) - 1:
                    # Reset for the next VDC/Mun
                    vdc_mun_dropdown.select_by_index(vdc_mun_dropdown.first_selected_option.index + 1)
                    click_option_and_wait(vdc_mun_dropdown.first_selected_option, "ward")
                else:
                    # Continue to the next iteration of the VDC/Mun loop
                    continue

            # Check if all VDC/Mun for the current district are exhausted
            if vdc_mun_dropdown.first_selected_option.index == len(vdc_mun_dropdown.options) - 1:
                # Reset for the next district
                district_dropdown.select_by_index(district_dropdown.first_selected_option.index + 1)
                click_option_and_wait(district_dropdown.first_selected_option, "vdc_mun")
            else:
                # Continue to the next iteration of the district loop
                continue

        # Check if all districts for the current state are exhausted
        if district_dropdown.first_selected_option.index == len(district_dropdown.options) - 1:
            # Reset for the next state
            state_dropdown.select_by_index(state_dropdown.first_selected_option.index + 1)
            click_option_and_wait(state_dropdown.first_selected_option, "district")
        else:
            # Continue to the next iteration of the state loop
            continue

# Add a delay to keep the browser window open for some time
time.sleep(5)

# Close the WebDriver
driver.quit()

