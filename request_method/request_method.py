import requests as rq
import sys
import time
import json
import os
import logging

settingsFile = "request_method/settings.json"
logPath = "request_method/log/"

# variable init
with open(settingsFile, 'r', newline='') as jsonfile:
    data = json.load(jsonfile)
    
cookies = data["cookies"]
lessonCode = data["lessonCode"]

listLength = len(lessonCode)
listIndex = 0

# file init
isExist = os.path.exists(logPath)
if not isExist:
   # Create a new directory because it does not exist
   os.makedirs(logPath)
   print("The log directory is created!")

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M',
        handlers=[logging.FileHandler(logPath + 'output.log', 'w', 'utf-8'), ]
    )

# Start
while listLength > 0 :
    
    # Update listIndex:
    listLength = len(lessonCode)
    if listLength <= 0:
        sys.exit("All Down!")
    if listIndex >= listLength:
        listIndex = 0
        print("")
        logging.info("")
    
    outputStr = "{}/{}:".format((listIndex + 1), (listLength))
    print(outputStr)
    logging.info(outputStr)
    
    # Get Course informations
    courseInfoAPILink = 'https://querycourse.ntust.edu.tw/querycourse/api/courses'
    courseInfoData = {"Semester":"1121","CourseNo":lessonCode[listIndex],"CourseName":"","CourseTeacher":"","Dimension":"","CourseNotes":"","ForeignLanguage":0,"OnlyGeneral":0,"OnleyNTUST":0,"OnlyMaster":0,"Language":"zh"}

    courseInfo = rq.post(courseInfoAPILink, json=courseInfoData)
    courseInfo.encoding = 'big-5'
    outputStr = str(courseInfo.json()[0]["CourseNo"]) + " : " + str(courseInfo.json()[0]["ChooseStudent"]) + "/" + str(courseInfo.json()[0]["Restrict2"])
    print(outputStr)
    logging.info(outputStr)
    
    # Add Course
    if int(courseInfo.json()[0]["ChooseStudent"]) < int(courseInfo.json()[0]["Restrict2"]) : 
        outputStr = "Course Added: {}".format(lessonCode[listIndex])
        print(outputStr)
        logging.info(outputStr)
        
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