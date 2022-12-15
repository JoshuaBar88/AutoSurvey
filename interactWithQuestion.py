from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
import undetected_chromedriver as uc
from contextlib import contextmanager
from selenium.webdriver.support.expected_conditions import staleness_of

import bs4
from bs4 import BeautifulSoup as soup
import requests
import re
import time
import random
import builtins

class Interact():
    """ 
    A set of functions to be used for the Selenium Chrome Webdriver
    Also designed for automated survey taking on the Pulse website 
    """

    def __init__(self, driver=""):
        self.driver = driver # initialized to none, set in open_site
        self.next_page = None
        self.question = None
        self.answers = None
        self.element = None
        self.randoText = ['I do not know', 'I am the Big EE and nothing i do will every fail', 'HAHA i am inevitable like Thanos']

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.driver.find_element(By.TAG_NAME, 'html')
        yield
        WebDriverWait(self.driver, timeout).until(
            staleness_of(old_page)
        )

    def clickNextPage(self, element):
        # example use
        with self.wait_for_page_load(timeout=10):
            self.click(element)
            # nice!
    def getBasics(self, tag):
        answers = []
        life_dict = {
                'name': ['Joshua Barnett'],
                'first_name': ['Joshua'],
                'last_name': ['Barnett'],
                'job': ['software', 'engineer', 'developer'],
                'occupation': ['software', 'engineer', 'developer'],
                'kids': ['0'],
                'children': ['0'],
                'pets': ['reptile','turtle','dog','cat'],
                'age': ['22'],
                'old': ['22'],
                'zip': ['06511'],
                'state': ['ct', 'connecticut'],
                'status': ['single'],
                'income': ['80000'],
                'household': ['80000'],
                # 'year': ['1998'],
                # 'month': ['month', '9', 'september'],
                'date': [('date', '1'), ('day', '1'), ('year', '1998'), ('month', '9', 'september')],
                'day': [('date', '1'), ('day', '1'), ('year', '1998'), ('month', '9', 'september')],
                'birth': [('date', '1'), ('day', '1'), ('year', '1998'), ('month', '9', 'september')],
                'gender': ['male', ' m'],
                'education': ['bachelor', 'b.a'],
                'school': ['bachelor', 'ba', 'collegedegree', 'bachelorsdegree'],
                'degree': ['bachelor', 'ba', 'collegedegree', 'bachelorsdegree'],
                'employment': ['fulltime'],
                'race': ['black', 'africanamericanblack', 'blackorafricanamerican', 'africanamericanorblack'],
                'ethnicity': ['black', 'africanamericanblack', 'blackorafricanamerican', 'africanamericanorblack'],
                'hispanic': ['no'],
                'sexual': ['straight', ' heterosexual'],
                'vehicle': ['2015'],
                'model': ['impala'],
                'male': ['male', 'm'],
                'female': ['male', 'm'],
                'country': ['unitedstates', 'usa', 'u.s.a', ' us ', 'u.s'],
                'county': ['newhaven'],
                'city': ['newhaven'],
                'language': ['english']
        }
        for i,j in life_dict.items():
            if i in tag.text.lower():
                answers += j
        return set(answers)

    def checkWithPage(self, source, element, found):
        question_container = soup(source, features="html.parser")
        keys = element.attrs
        for i,j in keys.items():
            join = ''.join(j)
            # theKey = found+'[{}=\"{}\"]'.format(i, join)
            # ('a',{'class':"mw-redirect"})
            elements = question_container.find_all(found, {i: join})
            try:
                if len(elements) == 1:
                    allElements = question_container.find_all(found)
                    matcher = element in allElements
                    if matcher: return element
                    return elements[0]
            except:
                pass
        
        return element

    def getOptions(self, objects, length):
        forbiddenWords = ['other', 'prefer', 'option']
        goodToGo = [False]
        if length <= 2:
            return objects[0]    
        while False in goodToGo:
            goodToGo = []
            number = random.randint(0, length - 1)
            for i in forbiddenWords:
                try:
                    while len(objects[number].attrs['value']) < 1:
                        number = random.randint(0, length - 1)
                except:
                    pass
                if i in objects[number].text.lower():
                    goodToGo.append(False)
        return objects[number]
        
    def click(self, answer):
        """ 
        Moves to the WebElement item and then clicks it
        returns -- none 
        """
        keys = answer.attrs
        for i,j in keys.items():
            join = ''.join(j)
            theKey = answer.name+'[{}=\"{}\"]'.format(i, join)
            element = self.driver.find_elements(By.CSS_SELECTOR, theKey)
            try:
                if len(element) == 1:
                    ActionChains(self.driver).move_to_element(
                        element[0]).click(element[0]).perform()
                    return True
            except:
                pass
        return False

    def selectClick(self, parent, answer):
        """ 
        Moves to the WebElement item and then clicks it
        returns -- none 
        """
        keys = parent.attrs
        for i,j in keys.items():
            join = ''.join(j)
            theKey = parent.name+'[{}=\"{}\"]'.format(i, join)
            element = self.driver.find_elements(By.CSS_SELECTOR, theKey)
            try:
                if len(element) == 1:
                    value = Select(element[0])
                    ActionChains(self.driver).move_to_element(
                        element[0]).click(element[0]).perform()
                    # self.driver.find_element(By.CSS_SELECTOR, theKey).click()
                    value.select_by_value(answer.attrs['value'])
                    return True
            except:
                pass
        return False

    def clickAll(self,parent, elements):
        validList = ['div', 'option', 'input', 'button', 'span', 'td', 'tr', 'label']
        sorted = [x for x in elements if x.name in validList]
        good = False
        for i in sorted:
            try:
                if 'value' in i.attrs.keys() and i.name == 'option':
                    good = self.selectClick(parent, i)
                else:
                    good = self.click(i)
                    if good: return True
            except Exception as e:
                pass
        return good
        
    def textInChildren(self, parent, elements, key):
        validList = ['div', 'option', 'input', 'button', 'span', 'label']
        sorted = [x for x in elements if x.name in validList]
        goodBoys = []
        for i in sorted:
            go = re.sub('[^A-Za-z0-9]+', '', i.getText().lower())
            if go in key and i not in goodBoys and len(go) > 0:
                goodBoys.append(i)
        return self.clickAll(parent, goodBoys)

    def answerOfBasics(self, element, types, children):
        parent = element
        childOfParent = children
        types = list(types)
        for daType in types:
            if type(daType) == str:
                if daType in parent.text.lower():
                    try:
                        listOfElements = self.textInChildren(parent, childOfParent, daType)
                        if listOfElements:
                            return True
                    except Exception as e:
                        pass
            else:
                try:
                    if daType[0] in parent.text.lower(): 
                        for x in range(1,len(daType)):
                            try:
                                if daType[x] in element.text.lower():
                                    listOfElements = self.textInChildren(parent, childOfParent, daType[x])
                                    if listOfElements:
                                        return True
                            except Exception as e:
                                pass
                except Exception as e:
                    pass
        return False


    def handleSelect(self, parent):
        currentPageSource = self.driver.page_source
        currentValue = self.checkWithPage(currentPageSource, parent, parent.name)
        parent = currentValue
        listOfOptions = parent.find_all('option')
        if len(listOfOptions) > 0:
            if len(self.answers) == 0:
                answer = self.getOptions(listOfOptions, len(listOfOptions))
                self.selectClick(parent, answer)
            else:
                answer = self.answerOfBasics(parent, self.answers, parent.findChildren())
                if not answer:
                    answer = self.getOptions(listOfOptions, len(listOfOptions))
                    self.clickAll(parent, [answer])
    def handleList(self, parent):
        currentPageSource = self.driver.page_source
        currentValue = self.checkWithPage(currentPageSource, parent, parent.name)
        parent = currentValue
        liInputs = parent.find_all('li')
        if len(liInputs) > 0:
            if len(self.answers) == 0: 
                answer = self.getOptions(liInputs, len(liInputs))
                sender = [answer] + answer.findChildren()
                self.clickAll(answer, sender)
            else:
                answer = self.answerOfBasics(parent, self.answers, parent.findChildren())
                if not answer:
                    answer = self.getOptions(liInputs, len(liInputs))
                    sender = [answer] + answer.findChildren()
                    self.clickAll(answer, sender)
    def handleTables(self, parent):
        currentPageSource = self.driver.page_source
        currentValue = self.checkWithPage(currentPageSource, parent, parent.name)
        parent = currentValue
        tableRowData = parent.find_all('tr')
        if len(tableRowData) > 0:
            for x in tableRowData:
                tableData = x.find_all('td')
                if len(self.answers) == 0: 
                    answer = self.getOptions(tableData, len(tableData))
                    sender = [answer] + answer.findChildren()
                    self.clickAll(answer, sender)
                else:
                    answer = self.answerOfBasics(parent, self.answers, parent.findChildren())
                    if not answer:
                        answer = self.getOptions(tableData, len(tableData))
                        sender = [answer] + answer.findChildren()
                        self.clickAll(answer, sender)
    def populateInput(self, inputField, choices):
        keys = inputField.attrs
        answer = None
        if len(self.answers) == 0:
            answer = random.choice(list(choices))
            for i,j in keys.items():
                join = ''.join(j)
                theKey = inputField.name+'[{}=\"{}\"]'.format(i, join)
                element = self.driver.find_elements(By.CSS_SELECTOR, theKey)
                try:
                    if len(element) == 1:
                        ActionChains(self.driver).move_to_element(
                            element[0]).click(element[0]).perform()
                        element[0].send_keys(answer)
                        return True
                except:
                    pass
        else:
            answer = list(choices)[0]
            for i,j in keys.items():
                join = ''.join(j)
                theKey = inputField.name+'[{}=\"{}\"]'.format(i, join)
                element = self.driver.find_elements(By.CSS_SELECTOR, theKey)
                try:
                    if len(element) == 1:
                        ActionChains(self.driver).move_to_element(
                            element[0]).click(element[0]).perform()
                        element[0].send_keys(answer)
                        return True
                except:
                    pass
    def handleInput(self, parent, options):
        currentPageSource = self.driver.page_source
        # currentValue = self.checkWithPage(currentPageSource, parent, parent.name)
        # parent = currentValue
        clickableInputs = []
        for i in options:
            if i.attrs['type'].lower() == 'radio' or i.attrs['type'].lower() == 'checkbox':
                    clickableInputs.append(i)
            if i.attrs['type'].lower() == 'number' or i.attrs['type'].lower() == 'string' or i.attrs['type'].lower() == 'text':
                    self.populateInput(i, self.answers)
        if len(clickableInputs) > 0:
            if len(self.answers) == 0: 
                answer = self.getOptions(clickableInputs, len(clickableInputs))
                sender = [answer] + answer.findChildren()
                self.clickAll(answer, sender)
            else:
                answer = self.answerOfBasics(parent, self.answers, parent.findChildren())
                if not answer:
                    answer = self.getOptions(clickableInputs, len(clickableInputs))
                    sender = [answer] + answer.findChildren()
                    self.clickAll(answer, sender)
    def handleTextArea(self, element):
        currentPageSource = self.driver.page_source
        currentValue = self.checkWithPage(currentPageSource, element, element.name)
        element = currentValue
        self.populateInput(element, self.answers)

    def findingWhichElement(self, tupObject):
        self.question = tupObject[0]
        self.answers = self.getBasics(self.question)
        only_inputCheck = set([True if i.name == 'input' else False for i in tupObject[1]])
        if list(only_inputCheck)[0] != True:
            for i in tupObject[1]:
                self.element = i.name
                if self.element == 'select':
                    self.handleSelect(i)
                if self.element == 'ul' or self.element == 'ol':
                    self.handleList(i)
                if self.element == 'table':
                    self.handleTables(i)
                if self.element == 'textarea':
                    self.handleTextArea(i)
        else:
            self.handleInput(tupObject[0], tupObject[1])

    def goingToNextPage(self, nextList):
        currentUrl = self.driver.current_url
        currentPageSource = self.driver.page_source
        for i in nextList:
            nextElement = self.checkWithPage(currentPageSource, i, i.name)
            self.clickNextPage(nextElement)
            if currentUrl != self.driver.current_url:
                return True
        return False