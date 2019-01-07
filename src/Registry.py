from src.Student import Student
from src.School import School
from src.Application import Application


class Registry:
    def __init__(self):
        self.students = {}
        self.schools = {}
        self.applications = {}

    def get_or_create_student(self, name):
        if name in self.students:
            return self.students[name]
        else:
            student = Student(name)
            self.students[name] = student
            return student

    def get_or_create_school(self, name):
        if name in self.schools:
            return self.schools[name]
        else:
            school = School(name)
            self.schools[name] = school
            return school

    def create_application(self, student, school, time):
        key = (student.name, school.name)
        assert key not in self.applications, key
        application = Application(student, school, time)
        self.applications[key] = application
        return application

    def get_application(self, student, school):
        key = (student.name, school.name)
        return self.applications.get(key, None)

    def get_applicant_info(self, student):
        print('{} has {} offers, {} waiting lists, {} rejections'.format(student.name, len(student.offers),
                                                                         len(student.waiting_list),
                                                                         len(student.rejections)))
