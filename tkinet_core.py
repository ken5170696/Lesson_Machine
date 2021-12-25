import threading
import datetime

from splinter import Browser
from time import sleep
#GUI

import tkinter as tk
from tkinter.constants import CENTER, END, FALSE, LEFT
window = tk.Tk()

window.title('WannaTakeClass')
screen_width, screen_height = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (screen_width, screen_height))
#window.configure(background='white')


missionloop = 0

#function
def add_event():
    consoleMesOut('add class: %s' %lesson_code_entry.get())
    lesson_list.insert("end", lesson_code_entry.get())

executable_path = {'executable_path':'C:\Program Files\Google\Chrome\Application\chromedriver.exe'}
browser = Browser('chrome', **executable_path)
def login_event():
    # splienter
    browser.visit('https://courseselection.ntust.edu.tw/')
    if username_entry.get() != '' and password_entry.get() != '':
        browser.fill('UserName',username_entry.get())
        sleep(1)
        browser.fill('Password',password_entry.get())
        
        browser.find_by_name('btnLogIn').click()
        consoleMesOut('Login to student page. Plz check the webpage out.')
        consoleMesOut('And click the Login button by yourself, lol.')
    else:
        consoleMesOut('Username and password can not be empty!')
sleep(1)
def mission():
    global missionloop
    while missionloop:
        for i,listbox_entry in enumerate(lesson_list.get(0, END)):
            browser.fill('CourseText',lesson_list.get(i))
            browser.find_by_id('SingleAdd').click()
            alert = browser.get_alert()
            consoleMesOut('\" %s \" Reply: %s' %(listbox_entry,alert.text))
            alert.accept()
            
missionThread = threading.Thread(target = mission)

def start_event():
    global missionloop
    browser.visit('https://courseselection.ntust.edu.tw/First/A06/A06') # change here to select pages : First -> AddAndSub
    if browser.is_text_present('課碼'):
        if lesson_list.get(0) != '':
            consoleMesOut('Mission start')
            missionloop = 1
            while missionloop:
                for i,listbox_entry in enumerate(lesson_list.get(0, END)):
                    browser.fill('CourseText',lesson_list.get(i))
                    browser.find_by_id('SingleAdd').click()
                    alert = browser.get_alert()
                    while alert == None:
                        if browser.current_url != 'https://courseselection.ntust.edu.tw/First/A06/A06' :
                            browser.visit('https://courseselection.ntust.edu.tw/First/A06/A06')
                            break
                        alert = browser.get_alert()
                        browser.fill('CourseText',lesson_list.get(i))
                        browser.find_by_id('SingleAdd').click()
                    consoleMesOut('\" %s \" Reply: %s' %(listbox_entry,alert.text))
                    alert.accept()
        else:
            consoleMesOut('Lesson code is empty')




def stop_event():
    global missionloop
    if missionloop == 1:
        consoleMesOut('Mission stop.')
        missionloop = 0
        missionThread.join()
    else:
        consoleMesOut('Mission has\'t start.')

def items_selected(event):
    selected_indies = event.widget.curselection()
    consoleMesOut('delete class: %s' %lesson_list.get(selected_indies))
    lesson_list.delete(selected_indies)

def consoleMesOut(str):
    Console_list.insert(END,str)
    Console_list.yview(END)

def timerFunc():
    start_event()



header_label = tk.Label(window, text='WannaTakeClass', font=("Terminal", 30))
header_label.grid(column=0, row=0)

div_width = screen_width/2
div_height = ((screen_height-30)/5)
align_mode = 'nswe'
pad = 2

main_Frame = tk.Frame(window)
main_Frame.grid(column=0, row=1)
main_Frame.rowconfigure(0, weight=0)
main_Frame.rowconfigure(1, weight=0)
main_Frame.rowconfigure(2, weight=0)

#Website_login_frame 
Website_login_frame = tk.Frame(main_Frame, width = div_width  , height=div_height) #, bg="red"
Website_login_frame.grid(column=0, row=0, padx=pad, pady=pad, sticky='W'+'N')
login_info_title = tk.Label(Website_login_frame, text='Website Login', font=("Terminal", 18))
login_info_title.grid(column=0, row = 0, padx = 5, pady = 5 ,sticky= 'W')

username_label = tk.Label(Website_login_frame, text='\tUsername', font=("Terminal", 15), height=1)
username_label.grid(column=0, row = 1, padx = 5, pady = 5)
username_entry = tk.Entry(Website_login_frame, width=50, font=("Terminal", 12))
username_entry.grid(column=1, row = 1, padx = 5, pady = 5)

password_label = tk.Label(Website_login_frame, text='\tPassword', font=("Terminal", 15), height=1)
password_label.grid(column=0, row = 2, padx = 5, pady = 5)
password_entry = tk.Entry(Website_login_frame, show="*", width=50, font=("Terminal", 12))
password_entry.grid(column=1, row = 2, padx = 5, pady = 5)

#Lesson_frame 
lesson_frame  = tk.Frame(main_Frame, width = div_width , height=div_height*3) #, bg="blue"
lesson_frame.grid(column=0, row=1, padx=pad, pady=pad, sticky='W'+'N')

lesson_title = tk.Label(lesson_frame, text='Lesson(click to delete item in the list)', font=("Terminal", 18))
lesson_title.grid(column=0, row = 0, padx = 5, pady = 5 ,sticky= 'W',columnspan=3)

lesson_code_label = tk.Label(lesson_frame, text='\tLesson Code', font=("Terminal", 15))
lesson_code_label.grid(column=0, row = 1, padx = 5, pady = 5)
lesson_code_entry = tk.Entry(lesson_frame, width=50, font=("Terminal", 12))
lesson_code_entry.grid(column=1, row = 1, padx = 5, pady = 5)
lesson_code_add =  tk.Button(lesson_frame, text='Add', font=("Terminal", 15), command=add_event)
lesson_code_add.grid(column=2, row = 1, padx = 5, pady = 5)

lesson_list_label = tk.Label(lesson_frame, text='\tLesson List', font=("Terminal", 15))
lesson_list_label.grid(column=0, row = 2, padx = 5, pady = 5,columnspan=3,sticky= 'WN')
lesson_list = tk.Listbox(lesson_frame, font=("Terminal", 12))
lesson_list.grid(column=1, row = 2, padx = 5, pady = 5,columnspan=3,sticky= 'W')

#Action_frame 
Action_frame  = tk.Frame(main_Frame)#, bg="yellow"
Action_frame.grid(column=0, padx=pad, pady=pad, sticky='W'+'N')

Action_title = tk.Label(Action_frame, text='Acttion ', font=("Terminal", 18))
Action_title.grid(column=0, row = 0, padx = 5, pady = 5 ,sticky= 'w',columnspan=3)

space_title = tk.Label(Action_frame, text='\t', font=("Terminal", 18))
space_title.grid(column=0, row = 1, padx = 5, pady = 5 ,sticky= 'w')

login_btn =  tk.Button(Action_frame, text='login', font=("Terminal", 20), command=login_event,)
login_btn.grid(column=1, row = 1, padx = 5, pady = 5,sticky= 'n'+'e'+'w'+'s')

start_btn =  tk.Button(Action_frame, text='start', font=("Terminal", 20), command=start_event)
start_btn.grid(column=2, row = 1, padx = 5, pady = 5,sticky= 'n'+'e'+'w'+'s')

stop_btn =  tk.Button(Action_frame, text='stop', font=("Terminal", 20), command=stop_event)
stop_btn.grid(column=3, row = 1, padx = 5, pady = 5,sticky= 'n'+'e'+'w'+'s')


lesson_list.bind('<<ListboxSelect>>', items_selected)

#Console_frame 
Console_frame  = tk.Frame(main_Frame, width = div_width , height=div_height*5,bd = 2)#, bg="green"
Console_frame.grid(column=1, row=0, padx=pad, pady=pad, rowspan=3, sticky=align_mode)
Console_frame.rowconfigure(0, weight=0)
Console_frame.rowconfigure(1, weight=1)


Console_title = tk.Label(Console_frame, text='Console {}'.format(datetime.datetime.now()), font=("Terminal", 18))
Console_title.grid(column=0, row = 0, padx = 5, pady = 5 ,sticky= 'W')


Console_list = tk.Listbox(Console_frame, font=("Terminal", 12),width=70,height=40)
Console_list.grid(column=0, row = 1, padx = 5, pady = 5,rowspan=3,sticky= 'W'+'N') 


# prompt
prompt = [
    'Welcome to \'WannaTakeClass\'!',
    ' ',
    'Fisrt, u hav to enter your username and password, ',
    'and click the \'login\' button.',
    ' ',
    'The website will show up if soon, ',
    'after that, u may hav to verify something',
    'to proof that u r not bot by yourself.',
    ' ',
    'Next, if u login successfully,',
    'plz add the lesson code, and click start button.',
    'U ganna see it runs automatically!'
]

for i, promptstr in enumerate(prompt):
    consoleMesOut(promptstr)
window.mainloop()

