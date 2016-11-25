# coding=utf-8
from datetime import datetime

class Salon:
    def __init__(self):
        self.id = None
        self.name = None
        self.owner_id = None
        self.type = None  #student, teache lauch ...
        self.date = None
        self.week = None
        self.time = None
        self.status = None
        self.field = None
        self.place = None
        self.people_number = None
        self.actual_people_number = None
        self.cross_faculty_number = None
        self.owner_faculty = None
        self.whether_takeaway = None
        self.detail = None
        self.interest = None

    def load_data(self, data):
        if len(data) == 30: # verify the correct of input
            self.id = data[0]
            self.name = data[1]
            self.owner_id = data[22]
            self.type = data[3]  # student, teache lauch ...
            self.date = datetime.strptime(data[4], '%Y年%m月%d日')
            self.week = self.date.weekday()
            self.time = datetime.strptime(data[5], '%H:%M')
            self.status = data[7] #delete or succeed
            self.field = data[8]
            self.place = data[9]
            self.people_number = int(data[11])
            self.actual_people_number = int(data[13])
            self.cross_faculty_number = data[14]
            self.owner_faculty = data[15]
            self.whether_takeaway = data[24]
            self.detail = data[28]
            interest_set = data[29]
            str1 = interest_set.replace(',', '+')
            str2 = str1.replace('，','+')
            str3 = str2.replace(' ', '+')
            str4 = str3.replace('\n', '')
            self.interest = str4.replace('、', '+')