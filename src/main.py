import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver import ActionChains

def open_driver(url: str):
    """
    Open the webpage from the given url.
    :param url: link to webpage
    :return: driver object
    """

    # Defining firefox webdriver
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path='/lib/geckodriver-v0.27.0-linux64/geckodriver', options=options)
    driver.get(url)

    return driver

def wait_for_element_to_load(driver: WebDriver, xpath: str):
    """
    Checks if an element is loaded on a page
    :param driver: webdriver
    :return: nothing
    """

    print(f'Waiting for element element to load: {xpath}')
    while len(driver.find_elements_by_xpath(xpath)) == 0:
        time.sleep(0.1)

def login(driver: WebDriver, username: str, password: str):
    """
    Fill in the username and password and press enter.
    :param driver: webdriver
    :param username: username
    :param password: user password
    :return: nothing
    """
    xpath_username_field = '//*[@id="usernameTextEdit"]'
    xpath_password_field = '//*[@id="passwordTextEdit"]'
    xpath_enter_button = '/html/body/div/div/div[4]/form/div[2]/input'

    driver.find_element_by_xpath(xpath_username_field).clear()
    driver.find_element_by_xpath(xpath_username_field).send_keys(username)
    driver.find_element_by_xpath(xpath_password_field).clear()
    driver.find_element_by_xpath(xpath_password_field).send_keys(password)
    driver.find_element_by_xpath(xpath_enter_button).click()

def click(driver: WebDriver, xpath: str):
    """Click on the element with the given xpath when this element is loaded

    Args:
        driver (WebDriver)
        xpath (str): xpath of element that needs to be clicked on
    """
    wait_for_element_to_load(driver, xpath)
    driver.find_element_by_xpath(xpath).click()

def double_click(driver: WebDriver, xpath: str):
    """Doubleclick on the element with the given xpath when this element is loaded

    Args:
        driver (WebDriver)
        xpath (str): xpath of element that needs to be clicked on
    """
    wait_for_element_to_load(driver, xpath)
    source = driver.find_element_by_xpath(xpath)
    action = ActionChains(driver)
    action.double_click(source)

def download_excel(driver: WebDriver):
    """Navigate to the excel file and download it

    Args:
        driver (WebDriver)
    """

    xpath_document_list = '//*[@id="IconImg_Txt_btnListing"]'
    xpath_next_page = '//*[@id="IconImg_ListingURE_goForwardButton"]'
    xpath_overzicht_vloot_banden = '//*[@id="ListingURE_listColumn_0_0_1"]'
    xpath_run_query = '//*[@id="theBttnpromptsOKButton"]'
    xpath_save_as_excel2007 = '//*[@id="saveDocComputerMenu_span_text_saveXLSX"]'

    # New window gets opened and old one closed -> switch to new window
    driver.switch_to.window(driver.window_handles[0])

    # Switch frame
    wait_for_element_to_load(driver, '//*[@id="headerPlusFrame"]')
    driver.switch_to.frame('headerPlusFrame')

    click(driver, xpath_document_list)
    double_click(driver, xpath_next_page) # not working
    click(driver, xpath_overzicht_vloot_banden)
    click(driver, xpath_run_query)
    click(driver, xpath_save_as_excel2007)


def main():
    login_url = 'http://bonew.qteam.be/InfoViewApp/logon.jsp'
    username = 'RENEWI'
    password = 'not_my_password'
    
    driver = open_driver(login_url)

    # Select the frame where the login box is in
    wait_for_element_to_load(driver, '//*[@id="infoView_home"]')
    driver.switch_to.frame('infoView_home')

    # Wait for login page to load
    xpath_username_field = '//*[@id="usernameTextEdit"]'
    wait_for_element_to_load(driver, xpath_username_field)
    
    login(driver, username, password)

    download_excel(driver)

if __name__ == '__main__':
    main()