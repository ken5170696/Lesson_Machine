import logging
import threading
import datetime
from splinter import Browser
import time
import logging

# variable
# Acount info
Username = "B11015044"
Password = "Ken+20150223-ntust"
# Website driver address
driverAddress = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
# url
LOGIN_PAGE = 'https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection'
INDEX_PAGE = 'https://courseselection.ntust.edu.tw/'
MAIN_PAGE = 'https://courseselection.ntust.edu.tw/First/A06/A06'
# Lesson Code
lessonCode = [
    'FE1471702',
    'FE1851701',
    'FE1935701'
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
    logging.debug("Initializing")
    global browser
    browser.visit(INDEX_PAGE)
    
def login():
    logging.debug("Try to login the account")
    global browser
    browser.fill('UserName',Username)
    time.sleep(1)
    browser.fill('Password',Password)
    time.sleep(1)
    btnLogIn = browser.find_by_name('btnLogIn')
    while btnLogIn == None:
        btnLogIn = browser.find_by_name('btnLogIn')
    btnLogIn.click()
    time.sleep(1) 
    
def enterMainPage():
    logging.debug("Enter Main Page")
    global browser
    browser.visit(MAIN_PAGE)
def takeLesson():
    logging.debug("Enter Main Page")
    global browser, listIndex
    browser.fill('CourseText',lessonCode[listIndex])
    browser.find_by_id('SingleAdd').click()
    alert = browser.get_alert()
    while alert == None:
        if currentPage == LOGIN_PAGE:
            login()
        if currentPage == INDEX_PAGE:
            enterMainPage()
        alert = browser.get_alert()
        
    str = '\" %s \" Reply: %s' %(lessonCode[listIndex],alert.text)
    print(str)
    logging.info(str)
    
    alert.accept()
    listIndex += 1
    if listIndex == listLength:
        listIndex = 0
    
init()
while True:
    currentPage = browser.url
    if currentPage == LOGIN_PAGE:
        login()
    elif currentPage == INDEX_PAGE:
        enterMainPage()
    elif currentPage == MAIN_PAGE:
        takeLesson()
    else:
        logging.debug("Page Not Invovled")

print("End")
