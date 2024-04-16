from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Initialize the WebDriver without headless mode to show the browser window
options = webdriver.ChromeOptions()
# options.headless = False
# driver = webdriver.Chrome(options=options)
# options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors") 
#options.add_argument("headless") 
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome(options=options)
# Open the webpage
# driver.get("https://election.gov.np/np/page/voter-list-db")
driver.get("https://voterlist.election.gov.np/bbvrs1/index_2.php")
# Define a function to click an option and wait for the next dropdown to become clickable
def click_option_and_wait(option, next_dropdown_id):
    option.click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, next_dropdown_id)))

time.sleep(5)
# Find the dropdown elements
state_dropdown = Select(driver.find_element(By.ID, "state"))
# //*[@id="state"]
# Loop through each option in state dropdown
for state_option in state_dropdown.options[4:5]:
    click_option_and_wait(state_option, "district")
    
    district_dropdown = Select(driver.find_element(By.ID, "district"))
    for district_option in district_dropdown.options[6:7]:
        click_option_and_wait(district_option, "vdc_mun")
        
        vdc_mun_dropdown = Select(driver.find_element(By.ID, "vdc_mun"))
        for vdc_mun_option in vdc_mun_dropdown.options[1:]:
            click_option_and_wait(vdc_mun_option, "ward")
            
            ward_dropdown = Select(driver.find_element(By.ID, "ward"))
            for ward_option in ward_dropdown.options[1:]:
                click_option_and_wait(ward_option, "reg_centre")
                
                reg_centre_dropdown = Select(driver.find_element(By.ID, "reg_centre"))
                for reg_centre_option in reg_centre_dropdown.options[1:]:
                    # Print innerHTML of the current reg_centre option
                    print("InnerHTML of current reg_centre:", reg_centre_option.text)

# Add a delay to keep the browser window open for some time
time.sleep(5)

# Close the WebDriver
driver.quit()
