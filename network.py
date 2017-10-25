import json

import requests

from course import *
from utils import is_on_time

url = 'https://wx.idsbllp.cn/redapi2/api/kebiao'

data = {
    'stuNum': -1,
    'week': -1
}

header = {
    'API_APP': 'android',
    'Content-Type': 'application/x-www-form-urlencoded'
}


def get_courses(stu_num, week=0):
    data['stuNum'] = stu_num
    data['week'] = week
    response = requests.post(url, data=data).json()
    if response['status'] != 200:
        return "network error!"

    now_week = response['nowWeek']
    courses = response['data']
    this_week_course = []
    for resp_course in courses:
        has = False
        for week in resp_course['week']:
            if week == now_week:
                has = True
        if has:
            if is_on_time(resp_course['day'].strip('\''), -1):
                this_week_course.append(
                    course(resp_course['course'], resp_course['teacher'], resp_course['classroom'],
                           resp_course['lesson']))
        else:
            "没有课哦"

    return ' '.join(i.get_course() for i in this_week_course)
