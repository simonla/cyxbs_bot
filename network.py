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


def get_courses(stu_num, week=0, offset=0):
    data['stuNum'] = stu_num
    data['week'] = week
    response = requests.post(url, data=data).json()
    if response['status'] != 200:
        return "network error!"
    now_week = response['nowWeek']
    courses = response['data']
    courses = filter(lambda x: now_week in x['week'] and is_on_time(x['day'].strip('\''), -1 + offset), courses)
    this_week_course = list(map(lambda x: Course(x['course'], x['teacher'], x['classroom'],
                                                 x['lesson']), courses))
    return ''.join(i.get_course() for i in this_week_course)
