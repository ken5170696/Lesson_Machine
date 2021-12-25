import logging
import threading
import datetime

from splinter import Browser
import time

import logging

# variable
# Acount info
Username = "YOUR_STUDENT_NUMBER"
Password = "YOUR_PASSWORD"
# Website driver address
driverAddress = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
# url
LOGIN_PAGE = 'https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection'
INDEX_PAGE = 'https://courseselection.ntust.edu.tw/'
MAIN_PAGE = 'https://courseselection.ntust.edu.tw/First/A06/A06'
# Lesson Code
lessonCode = [
    'LESSON_CODE_1_HERE',
    'LESSON_CODE_2_HERE'
]
listLength = len(lessonCode)
listIndex = 0
# using chrome drive
executable_path = {'executable_path':driverAddress}
browser = Browser('chrome', **executable_path)

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
        if time.time()-30>now:
            browser.reload()
            break
        alert = browser.get_alert()
        
    if alert!=None:
        alert_text = alert.text
        alert.accept()
    else:
        alert_text = "錯誤"

    str = '\" %s \" Reply: %s' %(lessonCode[listIndex],alert_text)
    print(str)
    logging.info(str)

    listIndex += 1
    if listIndex == listLength:
        listIndex = 0
    
init()
while True:
    currentPage = browser.url
    if currentPage == LOGIN_PAGE:
        try:
            login()
        except:
            print("登入錯誤")         
    if currentPage == INDEX_PAGE:
        try:
            enterMainPage()
        except:
            print("跳轉錯誤")
    if currentPage == MAIN_PAGE:
        try:
            takeLesson()
        except:
            print("加選錯誤")
    time.sleep(1)
print("End")
