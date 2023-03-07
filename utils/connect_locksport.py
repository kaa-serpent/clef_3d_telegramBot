from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


def loggin(search=None):

    with open('../credentials.json') as f:
        data = json.load(f)
        username = data['LOCKSPORT_USERNAME']
        password = data['LOCKSPORT_PASSWORD']

    # set up a Firefox webdriver with headless mode enabled
    firefox_options = Options()
    firefox_options.headless = False
    driver = webdriver.Firefox(options=firefox_options)

    # navigate to the login page
    login_url = 'https://www.locksport.fr/ucp.php?mode=login'
    driver.get(login_url)

    # fill in the login form and submit it
    username_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'password')
    submit_button = driver.find_element(By.NAME, 'login')
    username_input.send_keys(username)
    password_input.send_keys(password)
    submit_button.click()

    # wait for the login process to complete
    WebDriverWait(driver, 100)

    driver.get("https://www.locksport.fr/search.php")

    terme_search = driver.find_element(By.ID, 'keywords')
    submit_search = driver.find_element(By.CLASS_NAME, "button1")
    terme_search.send_keys(search)
    submit_search.click()
    WebDriverWait(driver, 100)
    # close the webdriver when done
    driver.quit()

    return "ok"


def search(search=None):
    """Function that searches for a specific lock on Locksport.fr"""
    if search is None:
        return ["Pas de mot à rechercher fournis"]
    result = loggin(search)
    print(result)
    return "end of search_on_locksport"
