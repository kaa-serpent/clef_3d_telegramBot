from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


def parse_research(driver: object):
    """Function that parses the result of research on locksport.fr"""
    prettify_data = ""
    title = driver.find_elements(By.CLASS_NAME, "searchresults-title")[0].text

    prettify_data += "**" + title + "** \n\n"
    for article in driver.find_elements(By.CLASS_NAME, "postbody"):
        title_article = article.find_element(By.TAG_NAME, "h3")
        prettify_data += "-> " + title_article.text + "\n"
    return driver, prettify_data


def login(message=None):

    with open('credentials.json') as f:
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
    WebDriverWait(driver, 10)

    driver.get("https://www.locksport.fr/search.php")

    terme_search = driver.find_element(By.ID, 'keywords')
    terme_title_only = driver.find_element(By.ID, 'sf3')
    terme_search.send_keys(message)
    terme_title_only.click()

    submit_button = driver.find_element(By.CLASS_NAME, "button1")
    # scroll to the submit button using JavaScript
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)

    submit_button.click()
    WebDriverWait(driver, 10)
    # close the webdriver when done

    driver, prettify_data = parse_research(driver)

    return driver, prettify_data


def search(message=None):
    """Function that searches for a specific lock on Locksport.fr"""
    if message == '':
        return ["Pas de mot a rechercher fournis"]
    driver, prettify_data = login(message)
    print(prettify_data)
    driver.quit()
    return prettify_data
