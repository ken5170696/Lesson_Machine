import requests
data = {"CourseNo": "%0A++++++++++++++++++++++++++++++++BAG009301%0A++++++++++++++++++++++++++++&type=1"}

url = "https://courseselection.ntust.edu.tw/First/A06/Join"
response = requests.post(url, data)
print(response)
