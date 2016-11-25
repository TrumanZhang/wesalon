# coding=utf-8
from datetime import datetime


class Sign:
    def __init__(self):
        self.salon_id = None
        self.user_id = None
        self.user_faculty = None
        self.user_status = None
        self.salon_status = None
        self.user_job = None
        self.user_from = None
        self.feel = None
        self.date = None
        self.time = None
        self.is_cross = None

    def load_data(self, data, info_dic):
        if len(data) == 14:
            self.salon_id = data[0]
            self.user_id = data[1]
            self.user_status = data[4]
            self.user_faculty = data[3]
            self.salon_status = data[9]
            self.feel = data[13]
            self.date = info_dic[self.salon_id][0]
            self.time = info_dic[self.salon_id][1]
            self.is_cross = info_dic[self.salon_id][2]

            student_number = data[10]
            if student_number != '':
                if student_number[4] == '0':
                    self.user_job = '本科'
                elif student_number[4] == '2':
                    self.user_job = '硕士'
                elif student_number[4] == '3':
                    self.user_job = '博士'
                elif student_number[4] == '6':
                    self.user_job = '教工'
                elif student_number[4] == '9':
                    self.user_job = '教师'
                else:
                    pass
                # get student home from student_number
                if student_number[5] == '1':
                    self.user_from = '普通'
                elif student_number[5] == '7':
                    self.user_from = '港澳台'
                elif student_number[5] == '8':
                    self.user_from = '留学生'
                else:
                    pass
