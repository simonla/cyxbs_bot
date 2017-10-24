import json

import requests

url = 'https://wx.idsbllp.cn/redapi2/api/kebiao'

data = {
    'stuNum': 2015213870,
    'idNum': 100714,
    'week': 0
}

header = {
    'API_APP': 'android',
    'Content-Type': 'application/x-www-form-urlencoded'
}


def get_courses(stuNum):
    response = requests.post(url, data=data)
    return response.content.decode()[20:60]
