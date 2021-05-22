###
# NOT USED ANYMORE (replaced by scraper_requests, 100 times faster)
###

###
# Download an Excel file by using Selenium webdriver
###

import time
import json
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver import ActionChains

def open_driver(url: str):
    """
    Open the webpage from the given url.
    :param url: link to webpage
    :return: driver object
    """

    # Defining firefox webdriver
    options = Options()
    options.add_argument('--headless')

    profile = FirefoxProfile()
    profile.set_preference("browser.download.dir", "/home/jaak/Documents/Programming/qteam_scraper/data/")
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")


    driver = webdriver.Firefox(executable_path='geckodriver', options=options, firefox_profile=profile)
    driver.get(url)

    return driver

def wait_for_element_to_load(driver: WebDriver, xpath: str):
    """
    Checks if an element is loaded on a page
    :param driver: webdriver
    :return: nothing
    """

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
    click(driver, xpath_enter_button)

def click(driver: WebDriver, xpath: str):
    """Click on the element with the given xpath when this element is loaded

    Args:
        driver (WebDriver)
        xpath (str): xpath of element that needs to be clicked on
    """
    wait_for_element_to_load(driver, xpath)
    print('[SCRAPER] click', xpath)
    time.sleep(2) # Time doesn't matter -> sleep for safety
    driver.find_element_by_xpath(xpath).click()

def double_click(driver: WebDriver, xpath: str):
    """Doubleclick on the element with the given xpath when this element is loaded

    Args:
        driver (WebDriver)
        xpath (str): xpath of element that needs to be clicked on
    """
    wait_for_element_to_load(driver, xpath)
    print('[SCRAPER] doubleclick', xpath)
    source = driver.find_element_by_xpath(xpath)
    action = ActionChains(driver)
    time.sleep(2) # Time doesn't matter -> sleep for safety
    action.double_click(source).perform()

def download_excel(driver: WebDriver):
    """Navigate to the excel file and download it

    Args:
        driver (WebDriver)
    """

    xpath_document_list = '//*[@id="IconImg_Txt_btnListing"]'
    xpath_public_folders = '//*[@id="ListingURE_listColumn_0_0_0"]'
    xpath_renewi_folder = '//*[@id="ListingURE_listColumn_0_0_1"]'
    xpath_next_page = '//*[@id="IconImg_ListingURE_goForwardButton"]'
    xpath_overzicht_vloot_banden = '//*[@id="ListingURE_listColumn_0_0_1"]'
    xpath_run_query = '//*[@id="theBttnpromptsOKButton"]'
    xpath_document_actions = '//*[@id="IconImg_Txt_iconMenu_icon_docMenu"]'
    xpath_save_to_computer_as = '//*[@id="iconMenu_menu_docMenu_span_text_saveDocComputerAs"]'
    xpath_save_as_excel = '//*[@id="saveDocComputerMenu_span_text_saveXLS"]'

    # New window gets opened and old one closed -> switch to new window
    driver.switch_to.window(driver.window_handles[0])

    # Switch frame
    wait_for_element_to_load(driver, '//*[@id="headerPlusFrame"]')
    driver.switch_to.frame('headerPlusFrame')

    click(driver, xpath_document_list)

    wait_for_element_to_load(driver, '//*[@id="dataFrame"]')
    driver.switch_to.frame('dataFrame')
    wait_for_element_to_load(driver, '//*[@id="workspaceFrame"]')
    driver.switch_to.frame('workspaceFrame')
    wait_for_element_to_load(driver, '//*[@id="workspaceBodyFrame"]')
    driver.switch_to.frame('workspaceBodyFrame')

    double_click(driver, xpath_public_folders)
    double_click(driver, xpath_renewi_folder)
    click(driver, xpath_next_page)
    double_click(driver, xpath_overzicht_vloot_banden)

    wait_for_element_to_load(driver, '//*[@id="webiViewFrame"]')
    driver.switch_to.frame('webiViewFrame')

    click(driver, xpath_run_query)
    click(driver, xpath_document_actions)
    click(driver, xpath_save_to_computer_as)
    click(driver, xpath_save_as_excel)


def main():
    print('[SCRAPER] Start scraper')
    # Path of directory where this file is in
    file_dir = os.path.dirname(os.path.realpath(__file__))

    login_url = 'http://bonew.qteam.be/InfoViewApp/logon.jsp'
    with open(f'{file_dir}/config.json') as config:
        data = json.load(config)
        username = data['qteam']['username']
        password = data['qteam']['password']
    
    driver = open_driver(login_url)
    # Select the frame where the login box is in
    wait_for_element_to_load(driver, '//*[@id="infoView_home"]')
    driver.switch_to.frame('infoView_home')

    # Wait for login page to load
    xpath_username_field = '//*[@id="usernameTextEdit"]'
    wait_for_element_to_load(driver, xpath_username_field)
    
    login(driver, username, password)

    download_excel(driver)

    print('[SCRAPER] Excel file downloaded')

if __name__ == '__main__':
    main()