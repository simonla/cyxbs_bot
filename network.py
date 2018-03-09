import requests
from PIL import Image

from course import *
from utils import is_on_time, get_week
from io import BytesIO

url_course = 'https://wx.idsbllp.cn/redapi2/api/kebiao'

url_stu_info = 'https://we.cqu.pt/api/others/student.php?key='

url_photo = 'https://we.cqu.pt/api/others/photos.php?id='

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
    response = requests.post(url_course, data=data).json()
    now_week = get_week(response['nowWeek'], offset)
    courses = response['data']
    courses = filter(lambda x: now_week in x['week'] and is_on_time(x['hash_day'], offset), courses)
    this_week_course = list(map(lambda x: Course(x['course'], x['teacher'], x['classroom'], x['lesson']), courses))
    return ''.join(i.get_course() for i in this_week_course)


def get_name_by_stu_num(stu_num):
    resp = requests.get(url_stu_info + str(stu_num)).json()
    return resp['data']['rows'][0]['xm'] if resp['data']['total'] == 1 else '亲你学号输错啦'


def get_stu_infos_by_info(info):
    return requests.get(url_stu_info + info).json()['data']['rows']


def get_photo(stu_num_photo):
    url = 'https://we.cqu.pt/api/others/photos.php?id=%s' % (stu_num_photo,)
    photo_url = requests.get(url).json()['data']
    photo = requests.get(photo_url).content
    image = Image.open(BytesIO(photo))
    bio = BytesIO(photo)
    bio.name = 'image.jpeg'
    image.save(bio, 'JPEG')
    bio.seek(0)
    return bio
