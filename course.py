class Course(object):
    def __init__(self, name, teacher, classroom, time):
        self.name = name
        self.teacher = teacher
        self.classroom = classroom
        self.lesson = time
        if time == "一二节":
            self.lesson = '8:00'
        if time == "三四节":
            self.lesson = '10:15'
        if time == "五六节":
            self.lesson = '14:00'
        if time == "七八节":
            self.lesson = '16:15'
        if time == "九十节":
            self.lesson = '19:00'
        if time == "十一二":
            self.lesson = '21:00'

    def get_course(self):
        return '%s ==> %s @ %s\n\n' % (self.lesson, self.name, self.classroom)
