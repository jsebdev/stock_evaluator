from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By


def check_popup(driver):
    try:
        xbutton = driver.find_element(
            By.XPATH, '//*[@id="myLightboxContainer"]/section/button[1]')
        xbutton.click()
        # print('button clicked')
    except Exception:
        pass
