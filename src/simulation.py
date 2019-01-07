import pandas as pd
from src.Registry import Registry
from src.Application import Application
import csv


def load_data(filename):
    column_datatype = {'User Name': 'str',
                       'Law School': 'str',
                       'Sent_delta': 'int32',
                       'Decision_delta': 'int32',
                       'Waitlisted': 'bool',
                       'Accepted': 'bool',
                       'Rejected': 'bool',
                       'Pending': 'bool'}
    df = pd.read_csv(filename)[list(column_datatype.keys())]
    df = df.drop_duplicates()
    return df.astype(column_datatype)


def extract_events(df, registry):
    event_queue = []
    for idx, row in df.iterrows():
        student = registry.get_or_create_student(row['User Name'])
        school = registry.get_or_create_school(row['Law School'])
        application_time = row['Sent_delta']
        application = registry.get_application(student, school)
        if application is None:
            application = registry.create_application(student, school, application_time)
            event_queue.append([application_time, application, 'send'])
        decision_time = application_time + row['Decision_delta']
        if row['Accepted']:
            event_queue.append([decision_time, application, Application.OFFER])
        elif row['Rejected']:
            event_queue.append([decision_time, application, Application.REJECTION])
        elif row['Waitlisted']:
            event_queue.append([decision_time, application, Application.WAITING_LIST])
    event_queue.sort(key=lambda s: s[0])
    return event_queue


def simulate():
    registry = Registry()
    df = load_data('../data/qpig_dynamic_sample.csv')
    result = [['User Name', 'Application Time', 'Number of Offers', 'Number of Waiting List', 'Number of Rejections']]
    for event in extract_events(df, registry):
        time, application, operation = event
        if operation == 'send':
            application.send_application()
            student = application.student
            result.append([student.name, time, len(student.offers), len(student.waiting_list), len(student.rejections)])
        else:
            application.send_decision(operation, time)
    with open('../data/output.csv', 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in result:
            writer.writerow(row)


if __name__ == '__main__':
    simulate()
