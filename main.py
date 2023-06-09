import logging
import threading
import datetime

from splinter import Browser
from selenium.webdriver.chrome.service import Service
import time

import logging

# variable
# Acount info
Username = ""
Password = ""  
# Website driver address
driverAddress = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
# url
LOGIN_PAGE = 'https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection'
INDEX_PAGE = 'https://courseselection.ntust.edu.tw/'
MAIN_PAGE = 'https://courseselection.ntust.edu.tw/First/A06/A06'
TIMEOUT = 30
# Lesson Code
lessonCode = [
    '',
    '',
]
listLength = len(lessonCode)
listIndex = 0
# using chrome drive
#executable_path = {'executable_path':driverAddress}
#browser = Browser('chrome', **executable_path)
my_service = Service(executable_path=driverAddress)
browser = Browser('chrome')

def init():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M',
        handlers=[logging.FileHandler('./log/output.log', 'w', 'utf-8'), ]
    )
    global browser
    browser.visit(INDEX_PAGE)
def login():
    global browser
    browser.fill('UserName',Username)
    time.sleep(1)
    browser.fill('Password',Password)
    time.sleep(1)
    browser.find_by_name('btnLogIn').click()
    time.sleep(1) 
def enterMainPage():
    global browser
    browser.visit(MAIN_PAGE)
def takeLesson():
    global browser, listIndex
    browser.fill('CourseText',lessonCode[listIndex])
    browser.find_by_id('SingleAdd').click()
    now = time.time()
    alert = browser.get_alert()
    
    while alert == None:
        currentPage = browser.url
        if currentPage == LOGIN_PAGE:
            login()
            break
        if currentPage == INDEX_PAGE:
            enterMainPage()
            break
        if time.time()-now>TIMEOUT:
            browser.reload()
            break
        alert = browser.get_alert()
        
    if alert!=None:
        alert_text = alert.text
        alert.accept()
    else:
        alert_text = "錯誤"

    str = '\" %s \" Reply: %s' %(lessonCode[listIndex],alert_text.encode("utf-8"))
    print(str.encode("utf-8"))
    logging.info(str)

    listIndex += 1
    if listIndex == listLength:
        listIndex = 0
    
init()
while True:
    try:
        currentPage = browser.url
    except:
        print("browser error".encode("utf-8"))
        continue

    if currentPage == LOGIN_PAGE:
        try:
            login()
        except:
            print("登入錯誤".encode("utf-8"))         
    elif currentPage == INDEX_PAGE:
        try:
            enterMainPage()
        except:
            print("跳轉錯誤".encode("utf-8"))
    elif currentPage == MAIN_PAGE:
        try:
            takeLesson()
        except:
            print("加選錯誤".encode("utf-8"))
    else:
        browser.visit(INDEX_PAGE)
print("End")
