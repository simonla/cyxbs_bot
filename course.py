class course(object):
    def __init__(self, name, teacher, classroom, time):
        self.name = name
        self.teacher = teacher
        self.classroom = classroom
        self.lesson = time
        if time == "一二节":
            self.lesson = '8:00~9:40'
        if time == "三四节":
            self.lesson = '10:15~11:55'
        if time == "五六节":
            self.lesson = '14:00~13:40'
        if time == "七八节":
            self.lesson = '16:15~17:55'
        if time == "九十节":
            self.lesson = '19:00~20:40'
        if time == "十一二":
            self.lesson = '21:00~22:40'

    def get_course(self):
        return '⌚%s ==> %s @ %s\n\n' % (self.lesson, self.name, self.classroom)
