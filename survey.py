from operator import truediv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import bs4
from bs4 import BeautifulSoup as soup
import requests
import re
import time
import random

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
            'state': [' ct ', 'Connecticut'],
            'status': ['single'],
            'income': ['80000'],
            'household': ['80000'],
            'birth': [('date', '1'), ('day', '1'), ('year', '1998'), ('month', '9', 'september')],
            'gender': ['male', ' m'],
            'education': ['bachelor', 'b.a'],
            'school': ['bachelor', 'b.a'],
            'degree': ['bachelor', 'b.a'],
            'employment': ['full time'],
            'race': ['black'],
            'ethnicity': ['black'],
            'hispanic': ['no'],
            'sexual': ['straight', ' heterosexual'],
            'vehicle': ['2015'],
            'model': ['impala'],
            'male': ['male', 'm'],
            'female': ['male', 'm'],
            'country': ['united states', 'usa', 'u.s.a', ' us ', 'u.s'],
            'county': ['new haven'],
            'city': ['new haven']
    }
    for i,j in life_dict.items():
        for x in tag:
            if i in x.text.lower():
                answers += j
    return set(answers)
def answerOfBasics(element, types):
    if type(list(types)[0]) == str:
        for i in element:
            for j in types:
                try:
                    driver.find_element_by_xpath(f'//{i.name}[contains(translate(normalize-space(.), \'ABCDEFGHIJKLMNOPQRSTUVWXYZ\', \'abcdefghijklmnopqrstuvwxyz\'), \'{j}\')]').click()
                    return True
                except Exception:
                    pass
    else:
        first = element[0]
        for j in types:
            try:
                if j[0] in first.parent.text.lower(): 
                    gottem = driver.find_element_by_xpath(f'//{first.parent.name}[contains(translate(normalize-space(.), \'ABCDEFGHIJKLMNOPQRSTUVWXYZ\', \'abcdefghijklmnopqrstuvwxyz\'),\'{j[0]}\')]')
                    for x in range(1,len(j)):
                        try:
                            if j[x] in gottem.text.lower():
                                gottem.find_element_by_xpath(f'//{first.name}[contains(translate(normalize-space(.), \'ABCDEFGHIJKLMNOPQRSTUVWXYZ\', \'abcdefghijklmnopqrstuvwxyz\'),\'{j[x]}\')]').click()
                                return True
                        except Exception:
                            pass
            except Exception:
                pass
    return None

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
                driver.find_element_by_id(keys['id']).clear()
                driver.find_element_by_id(keys['id']).send_keys(answer)
                return True
        except:
            pass
        try:
            if len(question_container.find_all(element.name, attrs={'name' : str(keys['name'])})) == 1:
                driver.find_element_by_name(keys['name']).clear()
                driver.find_element_by_name(keys['name']).send_keys(answer)
                return True
        except:
            pass
        try:
            tag = element.name + '.'
            cssFinder =  tag + '.'.join(keys['class'])
            driver.find_element_by_css_selector(cssFinder).clear()
            driver.find_element_by_css_selector(cssFinder).send_keys(answer)
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
                except Exception:
                    pass
                try:
                    if j in i.attrs['name'].lower() and 'hidden' not in i.attrs['name'].lower():
                        next = i
                        mult.append(next)
                except Exception:
                    pass
                try:
                    if j in i.attrs['class'].lower() and 'hidden' not in i.attrs['class'].lower():
                        next = i
                        mult.append(next)
                except Exception:
                    pass
                try:
                    if j in i.attrs['value'].lower() and 'hidden' not in i.attrs['value'].lower():
                        next = i
                        mult.append(next)
                except Exception:
                    pass
                try:
                    if j in i.attrs['type'].lower() and 'hidden' not in i.attrs['type'].lower():
                        next = i
                        mult.append(next)
                except Exception:
                    pass
                try:
                    if j in i.text.lower():
                        next = i
                        mult.append(next)
                        break
                except Exception:
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
                    except Exception:
                        pass
                    try:
                        if j in i.attrs['name'].lower() and 'hidden' not in i.attrs['name'].lower():
                            next = i
                            mult.append(next)
                    except Exception:
                        pass
                    try:
                        if j in ''.join(i.attrs['class']) and 'hidden' not in ''.join(i.attrs['class']):
                            next = i
                            mult.append(next)
                    except Exception:
                        pass
                    try:
                        if j in i.attrs['value'].lower() and 'hidden' not in i.attrs['value'].lower():
                            next = i
                            mult.append(next)
                    except Exception:
                        pass
                    try:
                        if j in i.attrs['type'].lower() and 'hidden' not in i.attrs['type'].lower():
                            next = i
                            mult.append(next)
                    except Exception:
                        pass
                    try:
                        if j in i.text.lower():
                            next = i
                            break
                    except Exception:
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
                    except Exception:
                        pass
                    try:
                        if j in i.attrs['name'].lower() and 'hidden' not in i.attrs['name'].lower():
                            next = i
                            mult.append(next)
                    except Exception:
                        pass
                    try:
                        if j in i.attrs['class'] and 'hidden' not in i.attrs['class']:
                            next = i
                            mult.append(next)
                    except Exception:
                        pass
                    try:
                        if j in i.attrs['value'].lower() and 'hidden' not in i.attrs['value'].lower():
                            next = i
                            mult.append(next)
                    except Exception:
                        pass
                    try:
                        if j in i.attrs['type'].lower() and 'hidden' not in i.attrs['type'].lower():
                            next = i
                            mult.append(next)
                    except Exception:
                        pass
                    try:
                        if j in i.text.lower():
                            next = i
                            mult.append(next)
                            break
                    except Exception:
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
                    except Exception:
                        pass
                    try:
                        if j in i.attrs['name'].lower() and 'hidden' not in i.attrs['name'].lower():
                            next = i
                    except Exception:
                        pass
                    try:
                        if j in i.attrs['class'] and 'hidden' not in i.attrs['class']:
                            next = i
                    except Exception:
                        pass
                    try:
                        if j in i.attrs['value'].lower() and 'hidden' not in i.attrs['value'].lower():
                            next = i
                    except Exception:
                        pass
                    try:
                        if j in i.attrs['type'].lower() and 'hidden' not in i.attrs['type'].lower():
                            next = i
                    except Exception:
                        pass
                    try:
                        if j in i.text.lower():
                            next = i
                            break
                    except Exception:
                        pass
    return set(mult)
def tryClicking(object):
    keys = object.attrs
    try:
        if len(question_container.find_all(element.name, attrs={'id' : str(keys['id'])})) == 1:
            element = driver.find_element_by_id(keys['id'])
            driver.execute_script("arguments[0].click();", element)
            return True
    except:
        pass
    try:
        if len(question_container.find_all(element.name, attrs={'name' : str(keys['name'])})) == 1:
            element = driver.find_element_by_name(keys['name'])
            driver.execute_script("arguments[0].click();", element) 
            return True
    except:
        pass
    try:
        tag = object.name + '.'
        cssFinder =  tag + '.'.join(keys['class'])
        element = driver.find_element_by_css_selector(cssFinder)
        driver.execute_script("arguments[0].click();", element)
        return True
    except:
        return False
def randoClick(element) :
    attributes = element.attrs
    keys = attributes.keys()
    try:
        for i in keys:
            if i == 'id' and len(question_container.find_all(element.name, attrs={'id' : str(attributes['id'])})) == 1:
                try:
                    driver.find_element_by_xpath(f'//{element.name}[@id='+'\''+ attributes['id']+'\''+']').click()
                    return True
                except Exception:
                    pass
            elif i == 'name' and len(question_container.find_all(element.name, attrs={'name' : str(attributes['name'])})) == 1:
                try:
                    driver.find_element_by_xpath(f'//{element.name}[@name='+'\''+ attributes['name']+'\''+']').click()
                    return True
                except Exception:
                    pass
            elif i == 'class':
                try:
                    cssFinder =  ' '.join(attributes['class'])
                    driver.find_element_by_xpath(f'//{element.name}[@class=\'{cssFinder}\']').click()
                    return True
                except Exception:
                    pass
    except Exception:
        return False
         
    # if randoClick(answer, correctKey) != False:
    # driver.find_element_by_xpath(randoClick(answer, correctKey)).click()
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
    soup_object = soup(source, features="html.parser")
    if soup_object.find('section') != None:
        question_container_temp = soup_object.find('section')
    if soup_object.find('form') != None:
        question_container_temp = soup_object.find('form')
    else:
        question_container_temp = soup_object
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
    finalQuestions = []
    for i,j in elementList.items():
        finale[i] = {}
        finale[i]['questions'] = []
        for x in j:
            holder = x
            while holder not in questions:
                holder = holder.parent
            if holder not in finale[i]['questions']:
                finale[i]['questions'].append(holder)
                finalQuestions.append(holder)
    return finale
def tryClickingSelect(element, answer):
    try:
        if len(question_container.find_all(element.name, attrs={'name' : str(element.attrs['name'])})) == 1:
            value = Select(driver.find_element_by_name(element.attrs['name']))
            value.select_by_value(answer.attrs['value'])
            return True
    except:
        pass
    try:
        if len(question_container.find_all(element.name, attrs={'id' : str(element.attrs['id'])})) == 1:
            value = Select(driver.find_element_by_name(element.attrs['id']))
            value.select_by_value(answer.attrs['value'])
            return True
    except:
        return False

def answer():
    global driver
    global question_container

    options = Options()
    url = 'https://surveymyopinion.researchnow.com/survey/standalone?id=05fa40c1-3f5f-453e-a6de-13fea7720b20'
    #url = 'https://dkr1.ssisurveys.com/projects/estart?ekey=RwqiqMmC2faoI7gqezAr5w**&GID=6000446&sname=0y-fxX4umTymepORtzNfTXz2kQY'
    # url = 'https://survey.alchemer.com/s3/6953135/HRB-CT-Survey-2022-Restructures?respondent=6514c15a-9755-a189-2d3a-f53f3ac84ebc'
    #url = 'https://edgesurvey.innovatemr.net/#/survey/age?survNum=vzdQ7N36&supCode=654&PID=2107-ALd-umrf9-xioe3-pasfuf_-202201&Lang=english&langCode=EN&jb_id=8436148&chkOeValid=1&oeQuestionIds=8878&AGE=ageval&GENDER=genderval&REGION=regionval&cntryCode=US&supId=QLB&RAIJuris=false&uid=rEB2G4G4k7ijJrEJnyD4uoeDZRJK1GTqpEWnKor&isp=1&start=1&isQuestionsExists=1'
    #options.add_experimental_option("debuggerAddress","lcalhost:9222")
    options.add_experimental_option("detach", True)
    #options.add_experimental_option("prefs",{'profile.managed_default_content_settings.javascript':2})
    driver = webdriver.Chrome(executable_path="/Users/joshuabarnett/.wdm/drivers/chromedriver", options = options)
    # chrome_prefs = {}
    # options.experimental_options["prefs"] = chrome_prefs
    # chrome_prefs["profile.default_content_settings"] = {"javascript": 2}
    # chrome_prefs["profile.managed_default_content_settings"] = {"javascript": 2}
    # driver = webdriver.Chrome("your chromedriver path here",options=options)
    #driver.get("https://www.surveyjunkie.com/member") item.removeAttribute(\"class\")
    driver.get(url)
    WebDriverWait(driver, 1)
     # noCss = 'document.querySelectorAll(\'style,link[rel=\"stylesheet\"]\').forEach(item => item.remove());
    # noCss = 'nodeList = document.querySelectorAll("*");\nfor (let i = 0; i < nodeList.length; i++){\n  blow = nodeList[i].style; blow.setProperty(\'text-transform\',\'lowercase\');\n}'
    # driver.execute_script(noCss)

    #birth = driver.find_element_by_tag_name('select').click()
    find_ids = ''
    html = driver.page_source
    soup_object = soup(html, features="html.parser")
    go = True
    while go:
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
            # if soup_object.find('section') != None:
            #     question_container = soup_object.find('section')
            # if soup_object.find('form') != None:
            #     question_container = soup_object.find('form')
            # else:
            question_container = soup_object
            listElements = [x for x in question_container.find_all('ul') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()]
            selection = [x for x in question_container.find_all('select') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()]
            tables = [x for x in question_container.find_all('tr') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values()]
            next_page = list(nextPage(soup_object))
            only_inputs = [x for x in question_container.find_all('input') if 'hidden' not in x.attrs.keys() and 'hidden' not in x.attrs.values() and x not in next_page]
            allOptions = {'listElements': listElements, 'selection': selection, 'tables': tables, 'only_inputs': only_inputs}
            questionIds = question_container.find_all('div', attrs={'id' : re.compile(r'question|Question')}) + question_container.find_all('span', attrs={'id' : re.compile(r'question|Question')})
            questionClasses = question_container.find_all('div', attrs={'class' : re.compile(r'question|Question')}) + question_container.find_all('span', attrs={'class' : re.compile(r'question|Question')})
            questionNames = question_container.find_all('div', attrs={'name' : re.compile(r'question|Question')}) + question_container.find_all('span', attrs={'name' : re.compile(r'question|Question')})
            headerTag = question_container.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            questionArray = set(questionClasses + questionIds + questionNames + headerTag)
            if len(questionArray) <= 1:
                questionArray = question_container.find_all('div')

            mainAttract = getNumberOfQuestion(allOptions, questionArray)
            mult = 'reg'
            for key,quest in mainAttract.items():
                if key == 'selection':
                    answersToQuestions = getBasics(quest['questions'])
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
                                else:
                                    answer = answerOfBasics(listOfOptions, answersToQuestions)
                                    if answer == None:
                                        answer = getOptions(listOfOptions, len(listOfOptions))
                                        randoClick(answer)
                        except Exception:
                            pass
                completedQuestions += quest['questions']
                if key == 'listElements':
                    answersToQuestions = getBasics(quest['questions'])
                    inputs_update = []
                    for i in range(len(listElements)):
                        numberofq -= 1
                        liInputs = [x.find('input') for x in listElements[i].find_all('li') if x.find('input') != None]
                        if len(liInputs) == 0:
                            liInputs = [x.find('a') for x in listElements[i].find_all('li') if x.find('a') != None]
                        if len(liInputs) == 0:
                            break
                        try:
                            if mult == 'mult':
                                for i in range(int(len(liInputs)/2)):
                                    answer = getOptions(liInputs, len(liInputs))
                                    randoClick(answer)
                            else:
                                if len(answersToQuestions) == 0: 
                                    answer = getOptions(liInputs, len(liInputs))
                                else:
                                    answer = answerOfBasics(liInputs, answersToQuestions)
                                    if answer == None:
                                        answer = getOptions(listOfOptions, len(listOfOptions))
                                        randoClick(answer)
                        except Exception:
                            pass
                if key == 'tables':
                    answersToQuestions = getBasics(quest['questions'])
                    inputs_update = []
                    for i in range(len(tables)):
                        try:
                            inputs_update = []
                            tableData = tables[i].find_all('td')
                            looper = False
                            for j in tableData:
                                holder = j
                                input = j.find('input')
                                if input:
                                    if tryClicking(input) == False:
                                        looper = True
                                    else:
                                        inputs_update.append(input)
                                        looper = False
                                else:
                                    looper = True
                                if looper == True:
                                    try:
                                        while tryClicking(holder) == False and type(holder) == bs4.element.Tag:
                                            holder = holder.next
                                        holder = holder.parent
                                        for x in holder.contents:
                                            if type(x) != bs4.element.Tag:
                                                pass
                                            if tryClicking(x):
                                                inputs_update.append(x)
                                    except Exception:
                                        pass

                            if len(inputs_update) > 0:
                                if mult == 'mult':
                                    for i in range(int(len(inputs_update)/2)):
                                        answer = getOptions(inputs_update, len(inputs_update))
                                        if randoClick(answer, correctKey) == False:
                                            tryClicking(answer)
                                else:
                                    if len(answersToQuestions) == 0: 
                                        answer = getOptions(inputs_update, len(inputs_update))
                                    else:
                                        answer = answerOfBasics(inputs_update, answersToQuestions)
                                        if answer == None:
                                            answer = getOptions(listOfOptions, len(listOfOptions))
                                        randoClick(answer)
                        except Exception:
                            pass
                if key == 'only_inputs':
                    answersToQuestions = getBasics(quest['questions'])
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
                                    randoClick(answer)
                            else:
                                if len(answersToQuestions) == 0: 
                                    answer = getOptions(inputs_update, len(inputs_update))
                                else:
                                    answer = answerOfBasics(inputs_update, answersToQuestions)
                                    if answer == None:
                                        answer = getOptions(inputs_update, len(inputs_update))
                                        randoClick(answer)
                    except Exception:
                        pass
            

            currentPageSource = driver.page_source
            for i in range(len(next_page)):
                if noDisplay(next_page[i]):
                    next_page = checkWithPage(currentPageSource, next_page[i], next_page[i].name)
                    break
            randoClick(next_page)
        except Exception as e:
            print(e)
            #go = False

    

if __name__ == '__main__':
    #driver = webdriver.Chrome(executable_path="/Users/joshuabarnett/.wdm/drivers/chromedriver/80.0.3987.106/mac64/chromedriver", options = options)
    #driver = webdriver.Chrome(ChromeDriverManager().install()) 
    answer()

    
    
    
    

