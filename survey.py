from logging.config import valid_ident
from operator import truediv
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

#/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --no-first-run --no-default-browser-check
#Update the chromedriver i have
#api fine one
def getBasics(tag):
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
            'birth': [('date', '1'), ('day', '1'), ('year', '1998'), ('month', '9', 'september')],
            'gender': ['male', ' m'],
            'education': ['bachelor', 'b.a'],
            'school': ['bachelor', 'ba', 'collegedegree', 'bachelorsdegree'],
            'degree': ['bachelor', 'ba', 'collegedegree', 'bachelorsdegree'],
            'employment': ['fulltime'],
            'race': ['black', 'africanamericanblack'],
            'ethnicity': ['black', 'africanamericanblack'],
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
        for x in tag:
            if i in x.text.lower():
                answers += j
    return set(answers)
def answerOfBasics(element, types):
    keys = {x:y for (x,y) in element.attrs.items() if x == 'id' or x == 'name'}
    parent = question_container.find(element.name, attrs=keys)
    childOfParent = parent.findChildren()
    if type(list(types)[0]) == str:
        for j in types:
            try:
                listOfElements = textInChildren(parent, childOfParent, j)
                if listOfElements:
                    return True
            except Exception as e:
                pass
    else:
        for j in types:
            try:
                if j[0] in element.text.lower(): 
                    for x in range(1,len(j)):
                        try:
                            if j[x] in element.text.lower():
                                listOfElements = textInChildren(parent, childOfParent, j[x])
                                if listOfElements:
                                    return True
                        except Exception as e:
                            pass
            except Exception as e:
                pass
    return None
def answerOfOptions(elements, types):
    element = elements[0].parent.parent
    parent = element
    childOfParent = parent.findChildren()
    if type(list(types)[0]) == str:
        try:
            listOfElements = textInChildren('nope', childOfParent, types)
            if listOfElements:
                return True
        except Exception as e:
            pass
    else:
        for j in types:
            try:
                if j[0] in element.text.lower(): 
                    for x in range(1,len(j)):
                        try:
                            if j[x] in element.text.lower():
                                listOfElements = textInChildren('nope', childOfParent, j[x])
                                if listOfElements:
                                    return True
                        except Exception as e:
                            pass
            except Exception as e:
                pass
    return None
def clickAll(parent, elements):
    validList = ['div', 'option', 'input', 'button', 'span', 'td', 'tr', 'a']
    sorted = [x for x in elements if x.name in validList]
    good = False
    for i in sorted:
        try:
            if 'value' in i.attrs.keys() and i.name == 'option':
                good = tryClickingSelect(parent, i)
            else:
                good = tryClicking(i)
        except Exception as e:
            pass
    return good
def textInChildren(parent, elements, key):
    validList = ['div', 'option', 'input', 'button', 'span', 'label', 'a']
    sorted = [x for x in elements if x.name in validList]
    goodBoys = []
    if parent == 'nope':
        for i in sorted:
            two = i.findNextSibling() if i.findNextSibling() != None else i.findChild()
            three = i.findPreviousSibling() if i.findPreviousSibling() != None else i.parent
            for j in [i, two, three]:
                try:
                    go = re.sub('[^A-Za-z0-9]+', '', j.getText().lower())
                    if go in key:
                        goodBoys.append(i)
                except:
                    pass
        return clickAll(parent, goodBoys)
    else:
        for i in sorted:
            go = re.sub('[^A-Za-z0-9]+', '', i.getText().lower())
            if go == key:
                if i.name == 'span':
                    value = i.findPreviousSibling()
                    goodBoys.append(value)
                else:
                    goodBoys.append(i)
        return clickAll(parent, goodBoys)

def getQuestionType(quest, type):
    #call APi if need be
    finale = []
    try:
        if type != 'text':
            for i in quest:
                if i.find_all('input') and i.find(type):
                    finale.append(i)
            return len(finale)
        else:
            for i in quest:
                if 'all' in i.text.lower():
                    return 'mult'
            return 'reg'
    except Exception as e:
        pass
def noDuplicate(objects):
    one = {key: value for key,value in objects[0].attrs.items() if type(value) == str}
    two = {key: value for key,value in objects[1].attrs.items() if type(value) == str}
    diff = {}
    for (key, value) in set(one.items()):
         if (key, value) not in set(two.items()):
            diff.update({key: value})
    if len(diff) == 0:
        return 'class'
    if 'id' in diff.keys():
        return 'id'
    if 'name' in diff.keys():
        return 'name'
    

def getOptions(objects, length):
    if length <= 2:
        return objects[0]
    number = random.randint(0, length - 1)
    try:
        while len(objects[number].attrs['value']) < 1:
            number = random.randint(0, length - 1)
    except:
        pass
    return objects[number]
def populateInput(element, types):
    keys = element.attrs
    answer = None
    for i in list(types):
        answer = i
        try:
            if len(question_container.find_all(element.name, attrs={'id' : str(keys['id'])})) == 1:
                driver.find_element(By.ID, keys['id']).clear()
                driver.find_element(By.ID, keys['id']).send_keys(answer)
                return True
        except:
            pass
        try:
            if len(question_container.find_all(element.name, attrs={'name' : str(keys['name'])})) == 1:
                driver.find_element(By.NAME, keys['name']).clear()
                driver.find_element(By.NAME, keys['name']).send_keys(answer)
                return True
        except:
            pass
        try:
            tag = element.name + '.'
            cssFinder =  tag + '.'.join(keys['class'])
            driver.find_element(By.CSS_SELECTOR, cssFinder).clear()
            driver.find_element(By.CSS_SELECTOR, cssFinder).send_keys(answer)
            return True
        except:
            return False

def nextPage(html):
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
def trySurveyLink(object):
    keys = object.attrs
    try:
        driver.get(keys['href'])
        return True
    except:
        pass
def tryClicking(object):
    keys = object.attrs
    try:
        if len(question_container.find_all(object.name, attrs={'id' : str(keys['id'])})) == 1:
            element = driver.find_element(By.ID, keys['id'])
            driver.execute_script("arguments[0].click();", element)
            return True
    except:
        pass
    try:
        if len(question_container.find_all(object.name, attrs={'name' : str(keys['name'])})) == 1:
            element = driver.find_element(By.NAME, keys['name'])
            driver.execute_script("arguments[0].click();", element) 
            return True
    except:
        pass
    try:
        tag = object.name + '.'
        cssFinder =  tag + '.'.join(keys['class'])
        element = driver.find_element(By.CSS_SELECTOR, cssFinder)
        driver.execute_script("arguments[0].click();", element)
        return True
    except:
        return False
         
def compare(one, two):
    score = 0
    which = []
    if len(one) > len(two):
        which = two
        for i in which:
            if i in one:
                score += 1
    else:
        which = one
        for i in which:
            if i in two:
                score += 1
    if score >= len(which) - 1:
        return True
    else: return False
     
def checkWithPage(source, element, found):
    question_container_temp = soup(source, features="html.parser")
    selection = [x for x in question_container_temp.find_all(found) if compare(element.attrs.values(), x.attrs.values())]
    return selection[0]
def noDisplay(element):
    attributes = element.attrs
    if 'class' not in attributes.keys():
        return True
    cssFinder =  ' '.join(attributes['class']).strip().lower()
    if 'display:none' in cssFinder:
        return False
    else:
        return True
def getNumberOfQuestion(elementList, questions):
    finale = {}
    for i,j in elementList.items():
        finale[i] = {}
        finale[i]['questions'] = []
        if len(j) >= 1:
            for x in questions:
                holder = x.findChildren()
                sameName = [p for p in holder if p.name == j[0].name]
                if len(sameName) >= 1:
                    finale[i]['questions'].append(x)
    return finale
def tryClickingSelect(element, answer):
    try:
        if len(question_container.find_all(element.name, attrs={'name' : str(element.attrs['name'])})) == 1:
            value = Select(driver.find_element(By.NAME, element.attrs['name']))
            driver.find_element(By.NAME, element.attrs['name']).click()
            value.select_by_value(answer.attrs['value'])
            return True
    except:
        pass
    try:
        if len(question_container.find_all(element.name, attrs={'id' : str(element.attrs['id'])})) == 1:
            value = Select(driver.find_element(By.ID, element.attrs['id']))
            driver.find_element(By.ID, element.attrs['id']).click()
            value.select_by_value(answer.attrs['value'])
            return True
    except:
        pass
    try:
        tag = element.name + '.'
        cssFinder =  tag + '.'.join(element.attrs['class'])
        value = Select(driver.find_element(By.CSS_SELECTOR, cssFinder))
        #driver.find_element(By.CSS_SELECTOR, cssFinder).click()
        # driver.execute_script("arguments[0].click();", ele)
        value.select_by_value(answer.attrs['value'])
    except:
        return False

def answer():
    global driver
    global question_container

    # options = Options()
    # options.add_argument("start-maximized")
    # options.add_argument("--disable-site-isolation-trials")
    # # Chrome is controlled by automated test software
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_experimental_option("detach", True)
    url = 'https://www.surveyjunkie.com/member'
    #url = 'https://us.toluna.com/SurveyCenter/surveys'
    #url = 'file:///Users/joshuabarnett/Desktop/Something/div.html'
    #J9806712z98
    options = uc.ChromeOptions()
    #options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    #options.add_argument("--auto-open-devtools-for-tabs")
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    #driver = uc.Chrome(options=options, version_main=94)
    #options.add_experimental_option("debuggerAddress","lcalhost:9222")
    #options.add_experimental_option("prefs",{'profile.managed_default_content_settings.javascript':2})
    #driver = webdriver.Chrome(executable_path="/Users/joshuabarnett/.wdm/drivers/chromedriver", options = options)
    driver = uc.Chrome(options=options)
    #driver.maximize_window()
    #driver.execute_script('return navigator.webdriver')
    # stealth(driver,
    #   languages=["en-US", "en"],
    #   vendor="Google Inc.",
    #   platform="Win32",
    #   webgl_vendor="Intel Inc.",
    #   renderer="Intel Iris OpenGL Engine",
    #   fix_hairline=True,
    # )

    #time.sleep(2)
    #driver.get(url)
    #driver.execute_script('Array.from(document.querySelectorAll(\"*\")).forEach(element => {\n  const events = getEventListeners(element)\n  if (Object.keys(events).length !== 0) {\n    console.log(element, events)\n  }\n})')
    # body = driver.execute_cdp_cmd("Runtime.evaluate", {"expression": "document.body"})
    # listeners = driver.execute_cdp_cmd("DOMDebugger.getEventListeners", {"objectId": body["result"]["objectId"]})
    #ma = driver.get_log('browser')
    # driver.find_element(By.XPATH, '//html/body/div[2]/div[1]/a[2]').click()
    # time.sleep(1)
    # driver.find_element(By.XPATH, '//html/body/div[16]/form[1]/input[2]').send_keys('sbjoshuabang@gmail.com')
    # driver.find_element(By.XPATH, '//html/body/div[16]/form[1]/input[3]').send_keys('batman1')
    # time.sleep(1)
    # driver.find_element(By.XPATH, '//html/body/div[16]/form[1]/button').click()
    #  # noCss = 'document.querySelectorAll(\'style,link[rel=\"stylesheet\"]\').forEach(item => item.remove());
    # # noCss = 'nodeList = document.querySelectorAll("*");\nfor (let i = 0; i < nodeList.length; i++){\n  blow = nodeList[i].style; blow.setProperty(\'text-transform\',\'lowercase\');\n}'
    # selfDie = 'lins = document.querySelectorAll(\'a\')\nvalues = []\nfor (i = 0; i < lins.length; i++) {\n  avalue = lins[i]\nif (avalue.className.includes(\'survey\')) {\n  avalue.setAttribute(\'target\', \'_self\')\n}\n}'
    # driver.execute_script(selfDie)


    # html = driver.page_source
    # soup_object = soup(html, features="html.parser")
    # allLinks = soup_object.find_all('a', attrs={'class' : re.compile(r'survey|Survey')})
    allLinks = ['https://spectrumsurveys.com/#/start-survey?211=111&212=22,311&213=82500&214=113&215=114&216=114&217=113&218=112&219=111&220=111&223=3&224=5&225=51&228=153&229=20111&230=&231=511&244=112&245=112&1010=112&1031=113,111,112,114,115,117&1032=118&1033=144&1034=116&1036=181&1037=112,114&1039=126,126,120&1040=112&1044=114&1045=111&1051=115&1055=134,129,135,133,137,116,116&1062=111&1096=112,113,114&1101=117&1233=117&1246=119,135&1499=112&1735=118&1809=113&1956=111&survey_id=9498994&supplier_id=79&type=1&pid=8061428&externalSystemUserId=4871b861-49cd-b7bc-f5b0-7eaa97d3d39e&uuid=313d973e2fb611edb76c02b393b2fb33']
    trying = 0

    go = True
    for i in allLinks:
        if 'surveyjunkie' in driver.current_url:
            go = False
            # selfDie = 'lins = document.querySelectorAll(\'a\')\nvalues = []\nfor (i = 0; i < lins.length; i++) {\n  avalue = lins[i]\nif (avalue.className.includes(\'survey\')) {\n  avalue.setAttribute(\'target\', \'_self\')\n}\n}'
            # driver.execute_script(selfDie)
            # html = driver.page_source
            # soup_object = soup(html, features="html.parser")
            # allLinks += [x for x in soup_object.find_all('a', attrs={'class' : re.compile(r'survey|Survey')}) if x not in allLinks]
        go = True
        driver.get(i)
        #geterdone = trySurveyLink(i)
        trying = 0
        while go and trying <= 5:
            try:
                geterdone = True
                if geterdone:
                    trying += 1
                    print(driver.current_url)
                    if url != driver.current_url:
                        url = driver.current_url
                        html = driver.page_source
                        soup_object = soup(html, features="html.parser")
                    else:
                        html = driver.page_source
                        soup_object = soup(html, features="html.parser")
                    try:
                        listElements = []
                        selection = []
                        only_inputs = []
                        tables = []
                        questionArray = []
                        questionIds = []
                        questionClasses = []
                        questionNames = []
                        inputs_update = []
                        mainAttract = None
                        completedQuestions = []
                        answersToQuestions = None
                        question_container = None
                        question_container = soup_object
                        listElements = [x for x in question_container.find_all('ul') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()] + [x for x in question_container.find_all('ol') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()]
                        selection = [x for x in question_container.find_all('select') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()]
                        tables = [x for x in question_container.find_all('table') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()]
                        next_page = list(nextPage(soup_object))
                        only_inputs = [x for x in question_container.find_all('input') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values() and x not in next_page]
                        allOptions = {'listElements': listElements, 'selection': selection, 'tables': tables, 'only_inputs': only_inputs}
                        questionIds = question_container.find_all('div', attrs={'id' : re.compile(r'question|Question')}) + question_container.find_all('span', attrs={'id' : re.compile(r'question|Question')})
                        questionClasses = question_container.find_all('div', attrs={'class' : re.compile(r'question|Question')}) + question_container.find_all('span', attrs={'class' : re.compile(r'question|Question')})
                        questionNames = question_container.find_all('div', attrs={'name' : re.compile(r'question|Question')}) + question_container.find_all('span', attrs={'name' : re.compile(r'question|Question')})
                        headerTag = question_container.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                        questionArray = set(questionClasses + questionIds + questionNames + headerTag)
                        if len(questionArray) == 0:
                            questionArray = question_container.find_all('div')
                        mainAttract = getNumberOfQuestion(allOptions, questionArray)
                        mult = 'reg'
                        for key,quest in mainAttract.items():
                            if key == 'selection':
                                answersToQuestions = getBasics(quest['questions'])
                                workingKey = None
                                inputs_update = []
                                for i in range(len(selection)):
                                    currentPageSource = driver.page_source
                                    currentValue = checkWithPage(currentPageSource, selection[i], 'select')
                                    selection[i] = currentValue
                                    correctKey = None
                                    try:    
                                        listOfOptions = selection[i].find_all('option')
                                        if len(listOfOptions) > 1:
                                            if len(answersToQuestions) == 0: 
                                                answer = getOptions(listOfOptions, len(listOfOptions))
                                                tryClickingSelect(selection[i], answer)
                                                if workingKey != False:
                                                    workingKey = True
                                            else:
                                                answer = answerOfBasics(selection[i], answersToQuestions)
                                                if workingKey != False:
                                                    workingKey = True
                                                if answer == None:
                                                    answer = getOptions(listOfOptions, len(listOfOptions))
                                                    clickAll(selection[i], [answer])
                                                    if workingKey != False:
                                                        workingKey = True
                                    except Exception as e:
                                        print(e)
                                        pass
                                if workingKey:
                                    completedQuestions += quest['questions']
                            if key == 'listElements' and len([x for x in completedQuestions if x in quest['questions']]) == 0:
                                answersToQuestions = getBasics(quest['questions'])
                                workingKey = None
                                inputs_update = []
                                for i in range(len(listElements)):
                                    liInputs = [x.find('input') for x in listElements[i].find_all('li') if x.find('input') != None]
                                    if len(liInputs) == 0:
                                        liInputs = [x.find('a') for x in listElements[i].find_all('li') if x.find('a') != None]
                                    if len(liInputs) == 0:
                                        break
                                    try:
                                        if mult == 'mult':
                                            for i in range(int(len(liInputs)/2)):
                                                answer = getOptions(liInputs, len(liInputs))
                                                sender = [answer] + answer.findChildren()
                                                clickAll(answer, sender)
                                                if workingKey != False:
                                                    workingKey = True
                                        else:
                                            if len(answersToQuestions) == 0: 
                                                answer = getOptions(liInputs, len(liInputs))
                                                sender = [answer] + answer.findChildren()
                                                clickAll(answer, sender)
                                                if workingKey != False:
                                                    workingKey = True
                                            else:
                                                answer = answerOfBasics(listElements[i], answersToQuestions)
                                                if answer == None:
                                                    answer = getOptions(liInputs, len(liInputs))
                                                    sender = [answer] + answer.findChildren()
                                                    clickAll(answer, sender)
                                                    if workingKey != False:
                                                        workingKey = True
                                    except Exception as e:
                                        print(e)
                                        pass
                            if key == 'tables' and len([x for x in completedQuestions if x in quest['questions']]) == 0:
                                answersToQuestions = getBasics(quest['questions'])
                                workingKey = None
                                inputs_update = []
                                for i in range(len(tables)):
                                    try:
                                        inputs_update = []
                                        tableRowData = tables[i].find_all('tr')
                                        for x in tableRowData:
                                            tableData = x.find_all('td')
                                            if len(tableData) > 0:
                                                if mult == 'mult':
                                                    for i in range(int(len(tableData)/2)):
                                                        if len(answersToQuestions) == 0:
                                                            answer = answerOfBasics(tables[i], answersToQuestions)
                                                            if answer == None:
                                                                answer = getOptions(tableData, len(tableData))
                                                                sender = [answer] + answer.findChildren()
                                                                clickAll(answer, sender)
                                                        else:
                                                            answer = getOptions(tableData, len(tableData)) 
                                                            sender = [answer] + answer.findChildren()
                                                            clickAll(answer, sender)
                                                else:
                                                    if len(answersToQuestions) == 0: 
                                                        answer = getOptions(tableData, len(tableData))
                                                        sender = [answer] + answer.findChildren()
                                                        clickAll(answer, sender)
                                                        if workingKey != False:
                                                            workingKey = True
                                                    else:
                                                        answer = answerOfBasics(tables[i], answersToQuestions)
                                                        if answer == None:
                                                            answer = getOptions(tableData, len(tableData))
                                                            sender = [answer] + answer.findChildren()
                                                            clickAll(answer, sender)
                                    except Exception as e:
                                        print(e)
                                        pass
                            if key == 'only_inputs' and len([x for x in completedQuestions if x in quest['questions']]) == 0:
                                answersToQuestions = getBasics(quest['questions'])
                                if len(answersToQuestions) == 0:
                                    answersToQuestions = getBasics(questionArray)
                                workingKey = None
                                inputs_update = []
                                try:
                                    for i in range(len(only_inputs)):
                                        if only_inputs[i].attrs['type'].lower() == 'radio' or only_inputs[i].attrs['type'].lower() == 'checkbox':
                                            inputs_update.append(only_inputs[i])
                                        if only_inputs[i].attrs['type'].lower() == 'number' or only_inputs[i].attrs['type'].lower() == 'string' or only_inputs[i].attrs['type'].lower() == 'text':
                                            populateInput(only_inputs[i], answersToQuestions)
                                    if len(inputs_update) > 0:
                                        if mult == 'mult':
                                            for i in range(int(len(inputs_update)/2)):
                                                answer = getOptions(inputs_update, len(inputs_update))
                                                tryClicking(answer)
                                                if workingKey != False:
                                                    workingKey = True
                                        else:
                                            if len(answersToQuestions) == 0: 
                                                answer = getOptions(inputs_update, len(inputs_update))
                                                tryClicking(answer)
                                                if workingKey != False:
                                                    workingKey = True
                                            else:
                                                answer = answerOfOptions(inputs_update, answersToQuestions)
                                                if answer == None:
                                                    answer = getOptions(inputs_update, len(inputs_update))
                                                    tryClicking(answer)
                                                    if workingKey != False:
                                                        workingKey = True
                                except Exception as e:
                                    print(e)
                                    pass
                        

                        currentPageSource = driver.page_source

                        theU = driver.current_url
                        for i in range(len(next_page)):
                            if noDisplay(next_page[i]):
                                next_page = checkWithPage(currentPageSource, next_page[i], next_page[i].name)
                                tryClicking(next_page)
                                if theU != driver.current_url:
                                    break
                        if 'surveyjunkie' in theU:
                            go = False
                        if theU == driver.current_url:
                            trying += 1
                    except Exception as e:
                        print(e)
                        trying += 1
                else:
                    go = False
            except Exception as e:
                print(e)
                go = False


    

if __name__ == '__main__':
    #driver = webdriver.Chrome(executable_path="/Users/joshuabarnett/.wdm/drivers/chromedriver/80.0.3987.106/mac64/chromedriver", options = options)
    #driver = webdriver.Chrome(ChromeDriverManager().install()) 
    answer()

    
    
    
    

