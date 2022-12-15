from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import undetected_chromedriver as uc

import bs4
from bs4 import BeautifulSoup as soup
import requests
import re
import time
import random
import builtins
from locatingQandA import Location
from interactWithQuestion import Interact



def beginScheming():
    url = 'file:///Users/joshuabarnett/Desktop/Something/survey2.html'
    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(executable_path="/Users/joshuabarnett/.wdm/drivers/chromedriver", options = options)
    driver.get(url)
    locator = Location(driver)
    interactor = Interact(driver)
    try:
        WebDriverWait(driver, 1).until(
            lambda x: x.current_url == url)
    except TimeoutException:
        print(f"Failed to redirect to {url}, timeout after 10 seconds")
    goToNextPage = True
    while goToNextPage:
        html = driver.page_source
        soup_object = soup(html, features="html5lib")
        allQuestions, nextPage = locator.findAllQuestions(soup_object)
        for i in allQuestions:
            interactor.findingWhichElement(i)
        goToNextPage = interactor.goingToNextPage(nextPage)

if __name__ == '__main__':
    beginScheming()