class School:
    def __init__(self, name):
        self.name = name
        self.applications = []
        self.offers = {}
        self.waiting_list = {}
        self.rejections = {}

    def application_received(self, application):
        self.applications.append(application)

    def decision_sent(self, application):
        student_name = application.student.name
        if application.is_offer():
            self.offers[student_name] = application
            if student_name in self.waiting_list:
                del self.waiting_list[student_name]
        elif application.is_waiting_list():
            self.waiting_list[student_name] = application
        elif application.is_rejection():
            self.rejections[student_name] = application
            if student_name in self.waiting_list:
                del self.waiting_list[student_name]
