class Student:
    def __init__(self, name):
        self.name = name
        self.applications = []
        self.offers = {}
        self.waiting_list = {}
        self.rejections = {}

    def application_sent(self, application):
        self.applications.append(application)

    def decision_received(self, application):
        school_name = application.school.name
        if application.is_offer():
            self.offers[school_name] = application
            if school_name in self.waiting_list:
                del self.waiting_list[school_name]
        elif application.is_waiting_list():
            self.waiting_list[school_name] = application
        elif application.is_rejection():
            self.rejections[school_name] = application
            if school_name in self.waiting_list:
                del self.waiting_list[school_name]
