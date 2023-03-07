import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import urllib.request


def get_post_title_on_page(driver, prettify_data, count_title):
    # parse the posts titles
    for article in driver.find_elements(By.CLASS_NAME, "postbody"):
        title_article = article.find_element(By.TAG_NAME, "h3")
        prettify_data.append(str(count_title) + "-> " + title_article.text + "\n")
        count_title += 1
    return prettify_data, count_title


def parse_title_research(driver: object):
    """Function that parses the result of research on locksport.fr"""
    print("parsing results...")
    count_title = 1
    prettify_titles = []
    title = driver.find_elements(By.CLASS_NAME, "searchresults-title")[0].text

    prettify_titles.append("**" + title + "** \n\n")

    # loop through the pages
    while True:

        prettify_titles, count_title = get_post_title_on_page(driver, prettify_titles, count_title)

        # check if there is a next page button
        next_page_button = driver.find_elements(By.XPATH,
                                                "//li[@class='arrow next']/a[@class='button button-icon-only' and @rel='next']")
        if not next_page_button:
            print("no more pages to click")
            break
        # click the next page button
        next_page_button[0].click()

        # wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "phpbb")))

    return driver, prettify_titles


def research(driver: object, str_to_research: str):
    """Function that research on locksport.fr"""
    print("researching...")
    driver.get("https://www.locksport.fr/search.php")

    try:
        driver.find_element(By.ID, 'keywords')
    except:
        print("non connecté")
        driver.quit()

    terme_search = driver.find_element(By.ID, 'keywords')
    terme_title_only = driver.find_element(By.ID, 'sf3')
    terme_search.send_keys(str_to_research)
    terme_title_only.click()

    submit_button = driver.find_element(By.CLASS_NAME, "button1")

    # scroll to the submit button using JavaScript
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)
    submit_button.click()

    WebDriverWait(driver, 10)
    return driver


def login():
    with open('credentials.json') as f:
        data = json.load(f)
        username = data['LOCKSPORT_USERNAME']
        password = data['LOCKSPORT_PASSWORD']

    # set up a Firefox webdriver with headless mode enabled
    firefox_options = Options()
    firefox_options.headless = True  # comment this line to see the browser in action
    driver = webdriver.Firefox(options=firefox_options)

    # navigate to the login page
    login_url = 'https://www.locksport.fr/ucp.php?mode=login'
    driver.get(login_url)

    print("accepting cookies...")
    cookies_button = driver.find_element(By.CLASS_NAME, 'cc-btn')
    cookies_button.click()
    WebDriverWait(driver, 10)

    print("logging in...")
    username_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'password')
    submit_button = driver.find_element(By.NAME, 'login')
    username_input.send_keys(username)
    password_input.send_keys(password)

    driver.execute_script("arguments[0].scrollIntoView();", submit_button)
    submit_button.click()

    # wait for the login process to complete
    WebDriverWait(driver, 10)

    return driver


def search(message=None):
    """Function that searches for a specific lock on Locksport.fr"""
    if message == '':
        return "Pas de mot(s) a rechercher fourni(s)"
    else:
        print("searching for " + message)
    driver = login()
    driver = research(driver, message)
    driver, prettify_data = parse_title_research(driver)
    driver.quit()
    return prettify_data


def title_article(message=None):
    """Function that searches for a specific topic on Locksport.fr"""
    if message == '':
        return "Pas de mot(s) a rechercher fourni(s)"
    else:
        print("searching for " + message)
    driver = login()
    driver = research(driver, message)

    element = driver.find_element(By.XPATH, '//div[contains(@class, "postbody")]/h3/a')
    # click element
    element.click()

    # wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "phpbb")))

    # create a folder to store the pictures if it doesn't exist
    if not os.path.exists('./pictures'):
        os.makedirs('./pictures')
    else:
        # delete the pictures in the folder
        for file in os.listdir('./pictures'):
            os.remove('./pictures/' + file)

    screenshot_name = 0

    # loop through the pages
    while True:
        for post in driver.find_elements(By.CLASS_NAME, "postbody"):
            post_body = post.find_element(By.CLASS_NAME, 'content')

            post_body.screenshot('./pictures/screenshot_' + str(screenshot_name) + '.png')
            screenshot_name += 1

        # check if there is a next page button
        next_page_button = driver.find_elements(By.XPATH,
                                                "//li[@class='arrow next']/a[@class='button button-icon-only' and @rel='next']")
        if not next_page_button:
            print("no more pages to click")
            break
        # click the next page button
        next_page_button[0].click()

    driver.quit()
