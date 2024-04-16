from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver (assuming Chrome in this example)
driver = webdriver.Chrome()

# Open the webpage
driver.get("https://election.gov.np/np/page/voter-list-db")

# Define a function to click an option and wait for the next dropdown to become clickable
def click_option_and_wait(xpath, next_xpath):
    option = driver.find_element(By.XPATH, xpath)
    option.click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_xpath)))

# Loop through each option in state dropdown
for state_option_index in range(2, 9):  # assuming the index of options starts from 2
    state_xpath = f"/html/body/div/div[2]/div[1]/div[2]/div/div[1]/div/form/div[2]/select/option[{state_option_index}]"
    click_option_and_wait(state_xpath, "/html/body/div/div[2]/div[1]/div[2]/div/div[1]/div/form/div[3]/select")

    # Loop through each option in district dropdown
    district_dropdown = Select(driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[2]/div/div[1]/div/form/div[3]/select"))
    for district_option_index in range(2, len(district_dropdown.options)):
        district_xpath = f"/html/body/div/div[2]/div[1]/div[2]/div/div[1]/div/form/div[3]/select/option[{district_option_index}]"
        click_option_and_wait(district_xpath, "/html/body/div/div[2]/div[1]/div[2]/div/div[1]/div/form/div[4]/select")

        # Loop through each option in vdc_mun dropdown
        vdc_mun_dropdown = Select(driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[2]/div/div[1]/div/form/div[4]/select"))
        for vdc_mun_option_index in range(2, len(vdc_mun_dropdown.options)):
            vdc_mun_xpath = f"/html/body/div/div[2]/div[1]/div[2]/div/div[1]/div/form/div[4]/select/option[{vdc_mun_option_index}]"
            click_option_and_wait(vdc_mun_xpath, "/html/body/div/div[2]/div[1]/div[2]/div/div[1]/div/form/div[5]/select")

            # Loop through each option in ward dropdown
            ward_dropdown = Select(driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[2]/div/div[1]/div/form/div[5]/select"))
            for ward_option_index in range(2, len(ward_dropdown.options)):
                ward_xpath = f"/html/body/div/div[2]/div[1]/div[2]/div/div[1]/div/form/div[5]/select/option[{ward_option_index}]"
                click_option_and_wait(ward_xpath, "/html/body/div/div[2]/div[1]/div[2]/div/div[1]/div/form/div[6]/select")

                # Loop through each option in reg_centre dropdown
                reg_centre_dropdown = Select(driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[2]/div/div[1]/div/form/div[6]/select"))
                for reg_centre_option_index in range(2, len(reg_centre_dropdown.options)):
                    reg_centre_xpath = f"/html/body/div/div[2]/div[1]/div[2]/div/div[1]/div/form/div[6]/select/option[{reg_centre_option_index}]"
                    # Print innerHTML of the current reg_centre option
                    reg_centre_option = driver.find_element(By.XPATH, reg_centre_xpath)
                    print("InnerHTML of current reg_centre:", reg_centre_option.text)

# Close the WebDriver
driver.quit()

