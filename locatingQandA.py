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

import bs4
from bs4 import BeautifulSoup as soup
import requests
import re
import time
import random
import builtins

class Location():
    """ 
    A set of functions to be used for the Selenium Chrome Webdriver
    Also designed for automated survey taking on the Pulse website 
    """

    def __init__(self, driver=""):
        self.driver = driver # initialized to none, set in open_site
        self.next_page = None

    def noHidden(self, element):
        keys = element.attrs.keys()
        values = element.attrs.values()
        true = []
        if 'hidden' not in keys and 'nav' not in keys and 'menu' not in keys: true.append(True)
        else: true.append(False)
        for i in values:
            if type(i) == str:
                if 'hidden' not in i and 'nav' not in i and 'menu' not in i: true.append(True)
                else: true.append(False)
            else:
                if 'hidden' not in ''.join(i) and 'nav' not in ''.join(i) and 'menu' not in ''.join(i): true.append(True)
                else: true.append(False)
        final = set(true)
        if list(final)[0] and len(final) == 1: return True
        return False


    def nextPage(self, html):
        checkNextPage = ['next', 'continue', 'submit', 'commit', 'forward', 'navigat', 'begin']
        next = None
        mult = []
        for i in html.find_all('input'):
            if 'hidden' in i.attrs.keys() or 'hidden' in i.attrs.values():
                pass
            else:
                for j in checkNextPage:
                    try:
                        if j in i.attrs['id'].lower() and 'hidden' not in i.attrs['id'].lower():
                            next = i
                            mult.append(next)
                    except Exception as e:
                        pass
                    try:
                        if j in i.attrs['name'].lower() and 'hidden' not in i.attrs['name'].lower():
                            next = i
                            mult.append(next)
                    except Exception as e:
                        pass
                    try:
                        if j in i.attrs['class'].lower() and 'hidden' not in i.attrs['class'].lower():
                            next = i
                            mult.append(next)
                    except Exception as e:
                        pass
                    try:
                        if j in i.attrs['value'].lower() and 'hidden' not in i.attrs['value'].lower():
                            next = i
                            mult.append(next)
                    except Exception as e:
                        pass
                    try:
                        if j in i.attrs['type'].lower() and 'hidden' not in i.attrs['type'].lower():
                            next = i
                            mult.append(next)
                    except Exception as e:
                        pass
                    try:
                        if j in i.text.lower():
                            next = i
                            mult.append(next)
                            break
                    except Exception as e:
                        pass
        if next == None:
            for i in html.find_all('button'):
                if 'hidden' in i.attrs.keys() or 'hidden' in i.attrs.values():
                    pass
                else:
                    for j in checkNextPage:
                        try:
                            if j in i.attrs['id'].lower() and 'hidden' not in i.attrs['id'].lower():
                                next = i
                                mult.append(next)
                        except Exception as e:
                            pass
                        try:
                            if j in i.attrs['name'].lower() and 'hidden' not in i.attrs['name'].lower():
                                next = i
                                mult.append(next)
                        except Exception as e:
                            pass
                        try:
                            if j in ''.join(i.attrs['class']) and 'hidden' not in ''.join(i.attrs['class']):
                                next = i
                                mult.append(next)
                        except Exception as e:
                            pass
                        try:
                            if j in i.attrs['value'].lower() and 'hidden' not in i.attrs['value'].lower():
                                next = i
                                mult.append(next)
                        except Exception as e:
                            pass
                        try:
                            if j in i.attrs['type'].lower() and 'hidden' not in i.attrs['type'].lower():
                                next = i
                                mult.append(next)
                        except Exception as e:
                            pass
                        try:
                            if j in i.text.lower():
                                next = i
                                break
                        except Exception as e:
                            pass
        if next == None:
            for i in html.find_all('a'):
                if 'hidden' in i.attrs.keys() or 'hidden' in i.attrs.values():
                    pass
                else:
                    for j in checkNextPage:
                        try:
                            if j in i.attrs['id'].lower() and 'hidden' not in i.attrs['id'].lower():
                                next = i
                                mult.append(next)
                        except Exception as e:
                            pass
                        try:
                            if j in i.attrs['name'].lower() and 'hidden' not in i.attrs['name'].lower():
                                next = i
                                mult.append(next)
                        except Exception as e:
                            pass
                        try:
                            if j in i.attrs['class'] and 'hidden' not in i.attrs['class']:
                                next = i
                                mult.append(next)
                        except Exception as e:
                            pass
                        try:
                            if j in i.attrs['value'].lower() and 'hidden' not in i.attrs['value'].lower():
                                next = i
                                mult.append(next)
                        except Exception as e:
                            pass
                        try:
                            if j in i.attrs['type'].lower() and 'hidden' not in i.attrs['type'].lower():
                                next = i
                                mult.append(next)
                        except Exception as e:
                            pass
                        try:
                            if j in i.text.lower():
                                next = i
                                mult.append(next)
                                break
                        except Exception as e:
                            pass
        if next == None:
            for i in html.find_all('img'):
                if 'hidden' in i.attrs.keys() or 'hidden' in i.attrs.values():
                    pass
                else:
                    for j in checkNextPage:
                        try:
                            if j in i.attrs['id'].lower() and 'hidden' not in i.attrs['id'].lower():
                                next = i
                        except Exception as e:
                            pass
                        try:
                            if j in i.attrs['name'].lower() and 'hidden' not in i.attrs['name'].lower():
                                next = i
                        except Exception as e:
                            pass
                        try:
                            if j in i.attrs['class'] and 'hidden' not in i.attrs['class']:
                                next = i
                        except Exception as e:
                            pass
                        try:
                            if j in i.attrs['value'].lower() and 'hidden' not in i.attrs['value'].lower():
                                next = i
                        except Exception as e:
                            pass
                        try:
                            if j in i.attrs['type'].lower() and 'hidden' not in i.attrs['type'].lower():
                                next = i
                        except Exception as e:
                            pass
                        try:
                            if j in i.text.lower():
                                next = i
                                break
                        except Exception as e:
                            pass
        return set(mult)

    def findAllQuestions(self, html):
        question_container = html
        self.next_page = list(self.nextPage(question_container))
        groupedQandA = []
        elementTags = ['input', 'ul', 'ol', 'select', 'table', 'textarea']
        allTheQuestions = question_container.find_all(['div', 'span'], attrs={'class' : re.compile(r'question|Question')}) + question_container.find_all(['div', 'span'], attrs={'name' : re.compile(r'question|Question')}) + question_container.find_all(['div', 'span'], attrs={'id' : re.compile(r'question|Question')}) + question_container.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if len(allTheQuestions) <= 1:
            allTheQuestions = question_container.find_all('div')
        allTheQuestions = [x for x in allTheQuestions if self.noHidden(x)]
        listElements = [x for x in question_container.find_all('ul') if self.noHidden(x)] + [x for x in question_container.find_all('ol') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()]
        selection = [x for x in question_container.find_all('select') if self.noHidden(x)]
        tables = [x for x in question_container.find_all('table') if self.noHidden(x)]
        textarea = [x for x in question_container.find_all('textarea') if self.noHidden(x)]
        only_inputs = [x for x in question_container.find_all('input') if self.noHidden(x) and x not in self.next_page]
        allEl = listElements + selection + tables + textarea + only_inputs + allTheQuestions
        unHolyElements = [x for x in question_container.find_all() if not self.noHidden(x)]
        unHolyChildren = sum([x.findChildren() for x in unHolyElements], [])
        preUnholy = set(allEl)
        check = [x for x in preUnholy if x not in unHolyChildren and x not in unHolyElements]
        topDownStructure = sorted(check, key=lambda x: (x.sourceline, x.sourcepos))
        currentQuest = []

        currentAnswers = []
        for elements in topDownStructure:
            if len(currentAnswers) > 0 and elements in allTheQuestions:
                groupedQandA.append((currentQuest[0], currentAnswers.copy()))
                currentQuest.clear()
                currentQuest.append(elements)
                currentAnswers.clear()
            elif elements in allTheQuestions and len(currentQuest) == 0:
                currentQuest.append(elements)
            elif len(currentQuest) > 0 and elements.name in elementTags:
                currentAnswers.append(elements)
        if len(currentAnswers) != 0:
            groupedQandA.append((currentQuest[0], currentAnswers.copy()))
        return groupedQandA, self.next_page
    
    def findAnswersForQuestions(self, question):
        # listElements = [x for x in question_container.find_all('ul') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()] + [x for x in question_container.find_all('ol') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()]
        # selection = [x for x in question_container.find_all('select') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()]
        # tables = [x for x in question_container.find_all('table') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()]
        # textarea = [x for x in question_container.find_all('textarea') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()]
        # only_inputs = [x for x in question_container.find_all('input') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()]
        print()