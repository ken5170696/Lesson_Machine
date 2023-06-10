import requests as rq
import sys
import time
import logging
import threading
import datetime
from splinter import Browser

# variable
# Acount info
Username = "YourUsername"
Password = "YourPassword"
# Website driver address
driverAddress = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'

# url
LOGIN_PAGE = 'https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection'
INDEX_PAGE = 'https://courseselection.ntust.edu.tw/'
MAIN_PAGE = 'https://courseselection.ntust.edu.tw/First/A06/A06'
TimeRefreshCookies = 60
TIMEOUT = 30
lessonCode = [
    "FE1621702",
    "FE1471701",
    "GE3612301",
    "CHG303301",
    "FE1591701",
    "TCG136301"
]


cookies = ""
listLength = len(lessonCode)
listIndex = 0

executable_path = {'executable_path':driverAddress}
browser = Browser('chrome', **executable_path)

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

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
    listLength = len(lessonCode)
    if listLength <= 0:
        sys.exit("All Down!")
    if listIndex >= listLength:
        listIndex = 0
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

    str = '\" %s \" Reply: %s' %(lessonCode[listIndex],alert_text)
    print(str)
    logging.info(str)

def refreshCookiesByTakingAnyLesson():
    global cookies
    while True:
        try:
            currentPage = browser.url
        except:
            print("browser error")
            continue

        if currentPage == LOGIN_PAGE:
            try:
                login()
            except:
                print("登入錯誤")
        elif currentPage == INDEX_PAGE:
            try:
                enterMainPage()
            except:
                print("跳轉錯誤")
        elif currentPage == MAIN_PAGE:
            try:
                takeLesson()
                break
            except:
                print("加選錯誤")
        else:
            browser.visit(INDEX_PAGE)
    cookiesDic = browser.cookies.all()
    cookies = ''
    for key,value in cookiesDic.items():
        cookies += str(key)+'='+str(value)+'; '
    cookies = cookies[:-2]
    print(cookies)



init()
refreshCookiesByTakingAnyLesson()
set_interval(refreshCookiesByTakingAnyLesson, TimeRefreshCookies)

while listLength > 0 :
    
    # Update listIndex:
    listLength = len(lessonCode)
    if listLength <= 0:
        sys.exit("All Down!")
    if listIndex >= listLength:
        listIndex = 0
        print("")
    print(listIndex + 1 , "/" , listLength , " : ")
    
    # Get Course informations
    courseInfoAPILink = 'https://querycourse.ntust.edu.tw/querycourse/api/courses'
    courseInfoData = {"Semester":"1121","CourseNo":lessonCode[listIndex],"CourseName":"","CourseTeacher":"","Dimension":"","CourseNotes":"","ForeignLanguage":0,"OnlyGeneral":0,"OnleyNTUST":0,"OnlyMaster":0,"Language":"zh"}

    courseInfo = rq.post(courseInfoAPILink, json=courseInfoData)
    courseInfo.encoding = 'big-5'
    # print(courseInfo.content)
    print(courseInfo.json()[0]["CourseNo"], " : ", courseInfo.json()[0]["ChooseStudent"], "/", courseInfo.json()[0]["Restrict2"])

    # Add Course
    if int(courseInfo.json()[0]["ChooseStudent"]) < int(courseInfo.json()[0]["Restrict2"]) : 
        print("Course Added: {}".format(lessonCode[listIndex]))
        
        courseAddLink = 'https://courseselection.ntust.edu.tw/First/A06/ExtraJoin'
        courseAddData = {"CourseNo":lessonCode[listIndex],"type":3}
        headers = {
            'Cookie': cookies
        }
        courseAdd = rq.post(courseAddLink, json=courseAddData, headers=headers)
        courseAdd.encoding = 'big-5'
        
        del lessonCode[listIndex]
    
    listIndex += 1
        
    time.sleep(0.01)