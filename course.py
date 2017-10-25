class course(object):
    def __init__(self, name, teacher, classroom, time):
        self.name = name
        self.teacher = teacher
        self.classroom = classroom
        self.lesson = time

    def get_course(self):
        return self.name + self.teacher + self.classroom + self.lesson
