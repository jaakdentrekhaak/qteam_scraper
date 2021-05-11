url = 'https://file-examples.com/index.php/sample-documents-download/sample-xls-download/'

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# options = Options()

# options.set_preference("browser.download.folderList",2)
# options.set_preference("browser.download.manager.showWhenStarting", False)
# options.set_preference
# ("browser.download.dir","/home/jaak/Documents/Programming/qteam_scraper/data/")
# options.set_preference
# ("browser.helperApps.neverAsk.saveToDisk",
# "application/vnd.sealed.xls")
# options.set_preference
# ("browser.helperApps.neverAsk.openFile",
# "application/vnd.sealed.xls")

profile = FirefoxProfile()
# # profile.set_preference("browser.download.folderList",2)
# profile.set_preference("browser.download.manager.showWhenStarting", False)
# profile.set_preference
# ("browser.download.dir","/home/jaak/Documents/Programming/qteam_scraper/data/")
# profile.set_preference
# ("browser.helperApps.neverAsk.saveToDisk",
# "application/xls;text/csv")

profile.set_preference("browser.download.dir", "/home/jaak/Documents/Programming/qteam_scraper/data/")
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.helperApps.alwaysAsk.force", False)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")


driver = webdriver.Firefox(executable_path='/lib/geckodriver-v0.27.0-linux64/geckodriver', firefox_profile=profile)
driver.get(url)

driver.find_element_by_xpath('/html/body/div[1]/main/section/div/div[2]/div/div/table/tbody/tr[1]/td[5]/a[1]').click()

driver.quit()