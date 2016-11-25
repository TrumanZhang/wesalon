# coding=utf-8
from datetime import datetime

category_dic = {
    '经管学院' : '商',
    '法学院' : '文',
    '社科学院' : '文',
    '生命学院' : '工',
    '土木系' :  '工',
    '电子系' : '工',
    '建筑学院' : '工',
    '人文学院' : '文',
    '计算机系' : '工',
    '航院' : '工',
    '美术学院' : '文',
    '工物系' : '工',
    '软件学院' : '工',
    '材料学院' : '工',
    '环境学院' : '工',
    '自动化系' : '工',
    '汽车系' : '工',
    '物理系' : '理',
    '机械系' : '工',
    '新闻学院' : '文',
    '热能系' : '工',
    '化学系' : '理',
    '水利系' : '工',
    '化工系' : '工',
    '医学院' : '理',
    '电机系' : '工',
    '工业工程系' : '工',
    '公管学院' : '文',
    '核研院' : '工',
    '外文系' : '文',
    '精仪系' : '工',
    '数学系' : '理',
    '教研院' : '文',
    '地球科学中心' : '工',
    '微纳电子系' : '工',
    '交叉信息院' : '工',
    '建管系' : '工',
    '马克思主义学院' : '文',
    '中文系' : '文',
    '机械学院' : '工',
    '金融学院' : '商',
    '研究生院' : '文',
    '生医系' : '工',
    '新雅书院' : '文',
    '图书馆' : '文',
    '计算机' : '工',
    '药学院' : '工',
    '建筑技术' : '工',
    '学生处' : '文',
    '高研院' : '文',
    '信研院' : '工',
    '全球创新学院' : '工',
    '党办校办' : '文',
    '清华 - 伯克利深圳学院' : '工',
    '微电子所' : '工',
    '科研院' : '工',
}

class User:
    def __init__(self):
        self.id = None
        self.name = None
        self.sex = None
        self.job = None
        self.student_from = None
        self.faculty = None
        self.reg_time = None
        self.last_login_time = None
        self.whole_join_minutes = None
        self.join_minutes_weekly = None
        self.interest = []
        self.number = None
        self.category = []

    def load_data(self, data, num):
        if len(data) == 29: # verify the correct of input
            interest_set = data[28]
            str1 = interest_set.replace(',', '+')
            str2 = str1.replace('，','+')
            str3 = str2.replace(' ', '+')
            str4 = str3.replace('\n', '+')
            self.interest = str4.replace('、', '+')
            self.id = data[0]
            self.name = data[3]
            self.sex = data[12]
            self.faculty = data[9]
            if self.faculty in category_dic:
                self.category = category_dic[self.faculty]
            else:
                self.category = '工'
            self.reg_time = datetime.strptime(data[14], '%Y-%m-%d %H:%M:%S')
            self.last_login_time = datetime.strptime(data[15], '%Y-%m-%d %H:%M:%S')
            self.whole_join_minutes = data[19]
            weeks = int((self.last_login_time - self.reg_time).days /7 ) + 1
            if weeks != 0:
                self.join_minutes_weekly = float(self.whole_join_minutes) / weeks
            student_number = data[2]
            self.number = num + 1
            if student_number == '':
                return self.number
            else:
                #self.number = num + 1
                if student_number[4] == '0':
                    self.job = '本科'
                elif student_number[4] == '2':
                    self.job = '硕士'
                elif student_number[4] == '3':
                    self.job = '博士'
                elif student_number[4] == '6':
                    self.job = '教工'
                elif student_number[4] == '9':
                    self.job = '教师'
                else:
                    pass
                # get student home from student_number
                if student_number[5] == '1':
                    self.student_from = '普通'
                elif student_number[5] == '7':
                    self.student_from = '港澳台'
                elif student_number[5] == '8':
                    self.student_from = '留学生'
                else:
                    pass
                return self.number
        else:
            return num

