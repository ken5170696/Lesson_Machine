import requests as rq
import sys
import time
import logging
import threading
import datetime
from splinter import Browser
import asyncio

# variable
# Acount info
Username = "YourUsername"
Password = "YourPassword"
# Website driver address
driverAddress = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'

# Your essential informations
cookies = ""
# url
courseInfoAPILink = 'https://querycourse.ntust.edu.tw/querycourse/api/courses'
LOGIN_PAGE = 'https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection'
INDEX_PAGE = 'https://courseselection.ntust.edu.tw/'
MAIN_PAGE = 'https://courseselection.ntust.edu.tw/First/A06/A06'
courseAddLink = 'https://courseselection.ntust.edu.tw/First/A06/ExtraJoin'
TIMEOUT = 30
lessonCode = [
    "FE1471701",
    "FE1471702"
]

listLength = len(lessonCode)

executable_path = {'executable_path':driverAddress}
browser = Browser('chrome', **executable_path)


def set_interval(func, sec):
    # calls func every sec second
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
    global browser
    listLength = len(lessonCode)
    if listLength <= 0:
        sys.exit("All Down!")
    browser.fill('CourseText',lessonCode[0])
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

    str = '\" %s \" Reply: %s' %(lessonCode[0],alert_text)
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

async def AddCourse(index):
    # Add Course
    print("Course Added: {}".format(lessonCode[index]))
    courseAddData = {"CourseNo":lessonCode[index],"type":3}
    headers = {
        'Cookie': cookies
    }
    
    try:
        courseAdd = rq.post(courseAddLink, json=courseAddData, headers=headers)
        courseAdd.encoding = 'big-5'
    
        del lessonCode[index]

    except:
        print("Add Course Error")

async def GetCourseInfo(index):
    # Get Course informations
    try:
        courseInfoData = {"Semester":"1122","CourseNo":lessonCode[index],"CourseName":"","CourseTeacher":"","Dimension":"","CourseNotes":"","ForeignLanguage":0,"OnlyGeneral":0,"OnleyNTUST":0,"OnlyMaster":0,"Language":"zh"}
        courseInfo = rq.post(courseInfoAPILink, json=courseInfoData)
        courseInfo.encoding = 'big-5'
        # print(courseInfo.content)
        print(courseInfo.json()[0]["CourseNo"], " : ", courseInfo.json()[0]["ChooseStudent"], "/", courseInfo.json()[0]["Restrict2"])

        # Add Course
        if int(courseInfo.json()[0]["ChooseStudent"]) < int(courseInfo.json()[0]["Restrict2"]) : 
            await AddCourse(index)
    except:
        print("POST Error")

async def main():
    listLength = len(lessonCode)
    while listLength > 0 : 
        # Update listLength:
        listLength = len(lessonCode)
        if listLength <= 0:
            sys.exit("All Down!")

        tasks = [GetCourseInfo(i) for i in range(listLength)]
        await asyncio.gather(*tasks)
        time.sleep(0.01)


if __name__ == '__main__':
    init()
    refreshCookiesByTakingAnyLesson()
    set_interval(refreshCookiesByTakingAnyLesson, 60)
    asyncio.run(main())
    