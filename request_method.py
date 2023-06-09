import requests as rq
import sys
import time

# Your essential informations
cookies = ""
lessonCode = [
    "FE1581701",
    "CS3051701",
]

listLength = len(lessonCode)
listIndex = 0

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