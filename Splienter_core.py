import time
from splinter import Browser

# variable
Username = "B11015044"
Password = "Ken+20150223-ntust"

# using chrome drive
executable_path = {'executable_path':'C:\Program Files\Google\Chrome\Application\chromedriver.exe'}
browser = Browser('chrome', **executable_path)


browser.visit('https://courseselection.ntust.edu.tw/')
browser.fill('UserName',Username)
browser.fill('Password',Password)
browser.find_by_name('btnLogIn').click()

while browser.is_text_not_present('公告訊息'):
    time.sleep(1)

browser.visit('https://courseselection.ntust.edu.tw/First/A06/A06')
while True:
    if browser.is_text_present('課碼'):
        browser.fill('CourseText',"ECG003301")
        browser.find_by_id('SingleAdd').click()
        alert = browser.get_alert()
        alert.text
        alert.accept()


