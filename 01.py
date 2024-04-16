# nix-shell -p python39 python311Packages.selenium chromedriver

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Initialize the WebDriver (assuming Chrome in this example)
# driver = webdriver.Chrome()

# Disable headless mode to show the browser window
options = webdriver.ChromeOptions()
options.headless = False

# Initialize the WebDriver with options
driver = webdriver.Chrome(options=options)

# Open the webpage
driver.get("https://election.gov.np/np/page/voter-list-db")



driver.implicitly_wait(5)

# Find the dropdown elements
vdc_mun_dropdown = Select(driver.find_element(By.ID, "vdc_mun"))
ward_dropdown = Select(driver.find_element(By.ID, "ward"))
reg_centre_dropdown = Select(driver.find_element(By.ID, "reg_centre"))
submit_button = driver.find_element(By.XPATH, "//*[@id='btnSubmit']")


# vdc_mun_dropdown = Select(driver.find_element_by_id("vdc_mun"))
# ward_dropdown = Select(driver.find_element_by_id("ward"))
# reg_centre_dropdown = Select(driver.find_element_by_id("reg_centre"))
# submit_button = driver.find_element_by_xpath("//*[@id='btnSubmit']")

# Loop through each option in vdc_mun dropdown
for vdc_option in vdc_mun_dropdown.options[1:]:
    # Select vdc_mun option
    vdc_mun_dropdown.select_by_value(vdc_option.get_attribute("value"))
    
    # Wait for ward dropdown to be interactive
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ward")))
    
    # Loop through each option in ward dropdown
    for ward_option in ward_dropdown.options[1:]:
        # Select ward option
        ward_dropdown.select_by_value(ward_option.get_attribute("value"))
        
        # Wait for reg_centre dropdown to be interactive
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "reg_centre")))
        
        # Loop through each option in reg_centre dropdown
        for reg_centre_option in reg_centre_dropdown.options[1:]:
            # Select reg_centre option
            reg_centre_dropdown.select_by_value(reg_centre_option.get_attribute("value"))
            
            # Click submit button
            #submit_button.click()
            print("InnerHTML of current reg_centre:", reg_centre_option.text)
# Close the WebDriver
driver.quit()

