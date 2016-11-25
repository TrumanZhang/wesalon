# coding=utf-8
import csv
from salon_process import SalonProcess
from user_process import UserProcess
from sign import Sign
from collections import deque


class SignProcess():
    def __init__(self):
        self.data_path = r'signs.csv'
        self.signs = []
        self.faculty_dic = {}
        self.faculty_list = []
        self.launch_faculty_dic = {}
        self.launch_faculty_list = []
        self.teacher = [0, 0] #lanuch, join
        self.teacher_time = [0] * 24
        self.teacher_faculty_dic ={}
        self.teacher_faculty_list = []
        self.teaching_stuff = [0, 0] #lanuch, join
        self.teaching_stuff_time = [0] * 24
        self.teaching_stuff_faculty_dic ={}
        self.teaching_stuff_faculty_list = []
        self.salon_user_list = []
        self.user_friend_list = []

        self.user = UserProcess()
        self.salon = SalonProcess()
        self.read_data()
        self.sign_faculty_stat()
        self.sign_launch_faculty_stat()
        self.teacher_stat()
        self.teaching_stuff_stat()
        self.coauthor_stat()
        self.sex_ratio_stat()
        self.education_stat()
        self.interest_stat()
        self.friend_stat()

    def read_data(self):
        info_dic = self.salon.get_salon_info_dic() #[date, time, isCross]
        f = open(self.data_path, "r", encoding='utf-8')
        lines = csv.reader(f)
        csv_lines = 0
        for item in lines:
            csv_lines += 1
            if csv_lines == 1:
                pass
            else:
                sign_new = Sign()
                sign_new.load_data(item, info_dic)
                self.signs.append(sign_new)

        index = -1
        temp = None
        for item in self.signs:
            if item.salon_status != '已删除' and item.salon_status != '管理员删除' and item.user_status != '已退出':
                if item.salon_id == temp:
                    self.salon_user_list[index][1].append(item.user_id)
                else:
                    temp = item.salon_id
                    index += 1
                    self.salon_user_list.append([temp, [item.user_id]])

    def sign_faculty_stat(self):
        for item in self.signs:
            if item.salon_status != '已删除' and item.salon_status != '管理员删除' and item.user_status != '已退出':
                if item.user_faculty in self.faculty_dic:
                    self.faculty_dic[item.user_faculty][0] += 1
                    self.faculty_dic[item.user_faculty][1] += item.is_cross
                else:
                    self.faculty_dic[item.user_faculty] = [1, item.is_cross]

        for item in self.faculty_dic:
                self.faculty_list.append([item, self.faculty_dic[item]])
        self.faculty_list.sort(key=lambda word: (word[1][0], word[1][1]), reverse=True)

    def sign_launch_faculty_stat(self):
        for item in self.signs:
            if item.salon_status != '已删除' and item.salon_status != '管理员删除' and item.user_status == '已发起':
                if item.user_faculty in self.launch_faculty_dic:
                    self.launch_faculty_dic[item.user_faculty] += 1
                else:
                    self.launch_faculty_dic[item.user_faculty] = 1
        for item in self.launch_faculty_dic:
                self.launch_faculty_list.append([item, self.launch_faculty_dic[item]])
        self.launch_faculty_list.sort(key=lambda word: (word[1], word[0]), reverse=True)

    def teacher_stat(self):
        for item in self.faculty_dic:
            self.teacher_faculty_dic[item] = 0
        for item in self.signs:
            if item.salon_status != '已删除' and item.salon_status != '管理员删除' and item.user_job == '教师':
                self.teacher_time[item.time.hour] += 1
                self.teacher_faculty_dic[item.user_faculty] += 1
                if item.user_status == '已发起':
                    self.teacher[0] += 1
                elif item.user_status != '已退出':
                    self.teacher[1] += 1
                else:
                    pass
        for item in self.teacher_faculty_dic:
                self.teacher_faculty_list.append([item, self.teacher_faculty_dic[item]])
        self.teacher_faculty_list.sort(key=lambda word: (word[1], word[0]), reverse=True)

    def teaching_stuff_stat(self):
        for item in self.faculty_dic:
            self.teaching_stuff_faculty_dic[item] = 0
        for item in self.signs:
            if item.salon_status != '已删除' and item.salon_status != '管理员删除' and item.user_job == '教工':
                self.teaching_stuff_time[item.time.hour] += 1
                self.teaching_stuff_faculty_dic[item.user_faculty] += 1
                if item.user_status == '已发起':
                    self.teaching_stuff[0] += 1
                elif item.user_status != '已退出':
                    self.teaching_stuff[1] += 1
                else:
                    pass
        for item in self.teaching_stuff_faculty_dic:
            self.teaching_stuff_faculty_list.append([item, self.teaching_stuff_faculty_dic[item]])
        self.teaching_stuff_faculty_list.sort(key=lambda word: (word[1], word[0]), reverse=True)

    def coauthor_stat(self):
        # coautho network statistitc and Erdo number
        '''salon_people =[]
        index = - 1
        temp = 0
        for item in self.signs:
            if item.salon_status != '已删除' and item.salon_status != '管理员删除' and item.user_status != '已退出':
                if item.salon_id == temp:
                    salon_people[index].append(item.user_id)
                else:
                    index += 1
                    salon_people.append([])
                    temp = item.salon_id
                    salon_people[index].append(item.user_id)
        '''

        adj_dic = {} #adj link, need save
        for item in self.salon_user_list:
            for node1 in item[1]:
                for node2 in item[1]:
                    if node1 != node2:
                        temp = node1 + '\t' + node2
                        if temp in adj_dic:
                            adj_dic[temp] += 1
                        else:
                            adj_dic[temp] = 1

        user_circle_dic = {}
        user_circle_list = []
        for item in self.salon_user_list:
            for node1 in item[1]:
                if node1 not in user_circle_dic:
                    user_circle_dic[node1] = []
                for node2 in item[1]:
                    if node1 != node2:
                        if node2 in user_circle_dic[node1]:
                            pass
                        else:
                            user_circle_dic[node1].append(node2)
        for item in user_circle_dic:
            user_circle_list.append([item, len(user_circle_dic[item])])
        user_circle_list.sort(key = lambda word: (word[1], word[0]), reverse = True)
        for item in user_circle_dic:
            self.user_friend_list.append([item, user_circle_dic[item]])
        f = open(r'doc/coauthor.txt', 'w', encoding='utf-8')
        f.write('通过微沙龙结交朋友数排名\n')
        for index in range(100):
            f.write('%s\t%d\n' % (self.user.users[self.user.user_map[user_circle_list[index][0]]].name, user_circle_list[index][1]))

        #cacluate Erdo number
        erdo_dic = {}
        erdo_list = []
        queue = deque()
        erdo = user_circle_list[0][0]
        queue.append(erdo)
        for item in self.user.users:
            erdo_dic[item.id] = -1
        erdo_dic[erdo] = 0

        while len(queue) != 0:
            temp = queue.popleft()
            layer = erdo_dic[temp]
            for child in user_circle_dic[temp]:
                if erdo_dic[child] == -1:
                    erdo_dic[child] = layer + 1
                    queue.append(child)
        for item in erdo_dic:
            erdo_list.append([item, erdo_dic[item]])
        erdo_list.sort(key=lambda word: (word[1], word[0]), reverse=True)
        f.write('\n埃尔德什数分析:\n')
        erdo_max = int(erdo_list[0][1])
        erdo_layer = [0] * (erdo_max + 1)
        erdo_uncover = 0
        for item in erdo_list:
            if item[1] != -1:
                erdo_layer[item[1]] += 1
            else:
                erdo_uncover += 1
        print(erdo_layer)
        print(erdo_uncover)
        f.write('埃尔德什数从0开始的数量:\n')
        for i in range(0, erdo_max + 1):
            f.write('%d\t%d\n' % (i, erdo_layer[i]))
        f.write('不在埃尔德什范围内的人数\t%d\n'% erdo_uncover)
        f.write('\n详细信息：\n')
        for item in erdo_list:
            f.write('%s\t%s\t%d\n' % (item[0], self.user.users[self.user.user_map[item[0]]].name, item[1]))
        f.close()

    def sex_ratio_stat(self):
        '''
        salon_user_list = []
        index = -1
        temp = None
        for item in self.signs:
            if item.salon_status != '已删除' and item.salon_status != '管理员删除' and item.user_status != '已退出':
                if item.salon_id == temp:
                    salon_user_list[index][1].append(item.user_id)
                else:
                    temp = item.salon_id
                    index += 1
                    salon_user_list.append([temp, [item.user_id]])
        '''

        sex_ratio_dic = {}
        sex_ratio_list = []
        for item in self.salon_user_list:
            man = 0
            woman = 0
            for people in item[1]:
                index = self.user.user_map[people]
                if self.user.users[index].sex == '男':
                    man += 1
                elif self.user.users[index].sex == '女':
                    woman += 1
                else:
                    pass
            if woman == 0:
                rate = 1000
            else:
                rate = man / woman
            ratio = str(round(rate,3))
            if ratio in sex_ratio_dic:
                sex_ratio_dic[ratio] += 1
            else:
                sex_ratio_dic[ratio] = 1
        for item in sex_ratio_dic:
            sex_ratio_list.append([item, sex_ratio_dic[item]])
        sex_ratio_list.sort(key=lambda word: (word[1], word[0]), reverse=True)
        print(sex_ratio_list)

        sex_field_dic = {}
        sex_field_list = []
        for item in self.salon_user_list:
            salon_index = self.salon.salon_map[item[0]]
            for people in item[1]:
                user_index = self.user.user_map[people]
                field = self.salon.salons[salon_index].field
                if field not in sex_field_dic:
                    sex_field_dic[field] = [0, 0, 0]
                if self.user.users[user_index].sex == '男':
                    sex_field_dic[field][0] += 1
                elif self.user.users[user_index].sex == '女':
                    sex_field_dic[field][1] += 1
                else:
                    pass
        for item in sex_field_dic:
            if sex_field_dic[item][1] != 0:
                sex_field_dic[item][2] = sex_field_dic[item][0] / sex_field_dic[item][1]
            else:
                sex_field_dic[item][2] = 1000
        for item in sex_field_dic:
            sex_field_list.append([item, sex_field_dic[item]])
        sex_field_list.sort(key=lambda word: word[1][2])
        print(sex_field_list)

        sex_interest_dic = {}
        sex_interest_list =[]
        for item in self.salon_user_list:
            salon_index = self.salon.salon_map[item[0]]
            for people in item[1]:
                user_index = self.user.user_map[people]
                interest_set = self.salon.salons[salon_index].interest.split('+')
                for interest in interest_set:
                    if interest not in sex_interest_dic:
                        sex_interest_dic[interest] = [0, 0, 0]
                    if self.user.users[user_index].sex == '男':
                        sex_interest_dic[interest][0] += 1
                    elif self.user.users[user_index].sex == '女':
                        sex_interest_dic[interest][1] += 1
                    else:
                        pass
        for item in sex_interest_dic:
            if sex_interest_dic[item][1] != 0:
                sex_interest_dic[item][2] = sex_interest_dic[item][0] / sex_interest_dic[item][1]
            else:
                sex_interest_dic[item][2] = 1000
        for item in sex_interest_dic:
            sex_interest_list.append([item, sex_interest_dic[item]])
        sex_interest_list.sort(key=lambda word: word[1][2])
        print(sex_interest_list)

        f = open(r'doc/sex_ratio.txt', 'w', encoding='utf-8')
        f.write('男女比分布（男/女，1000表示没有女生）\n')
        for item in sex_ratio_list:
            f.write('%s\t%d\n' % (item[0], item[1]))
        f.write('\n微沙龙各主题男女数量和比值\n')
        for item in sex_field_list:
            f.write('%s\t%d\t%d\t%.3f\n' %(item[0], item[1][0], item[1][1], item[1][2]))
        f.write('\n微沙龙各兴趣领域男女数量和比值\n')
        for item in sex_interest_list:
            f.write('%s\t%d\t%d\t%.3f\n' % (item[0], item[1][0], item[1][1], item[1][2]))
        f.close()

    def education_stat(self):
        undergraduate_interest_dic = {}
        master_interest_dic = {}
        doctor_interest_dic = {}
        undergraduate_interest_list = []
        master_interest_list = []
        doctor_interest_list = []
        for item in self.salon_user_list:
            salon_index = self.salon.salon_map[item[0]]
            interest_set = self.salon.salons[salon_index].interest.split('+')
            for people in item[1]:
                user_index = self.user.user_map[people]
                if self.user.users[user_index].job == '本科':
                    for temp in interest_set:
                        if temp in undergraduate_interest_dic:
                            undergraduate_interest_dic[temp] += 1
                        else:
                            undergraduate_interest_dic[temp] = 1
                if self.user.users[user_index].job == '硕士':
                    for temp in interest_set:
                        if temp in master_interest_dic:
                            master_interest_dic[temp] += 1
                        else:
                            master_interest_dic[temp] = 1
                if self.user.users[user_index].job == '博士':
                    for temp in interest_set:
                        if temp in doctor_interest_dic:
                            doctor_interest_dic[temp] += 1
                        else:
                            doctor_interest_dic[temp] = 1
        for item in undergraduate_interest_dic:
            undergraduate_interest_list.append([item, undergraduate_interest_dic[item]])
        undergraduate_interest_list.sort(key=lambda word: (word[1], word[0]), reverse=True)
        print(undergraduate_interest_list)

        for item in master_interest_dic:
            master_interest_list.append([item, master_interest_dic[item]])
        master_interest_list.sort(key=lambda word: (word[1], word[0]), reverse=True)
        print(master_interest_list)

        for item in doctor_interest_dic:
            doctor_interest_list.append([item, doctor_interest_dic[item]])
        doctor_interest_list.sort(key=lambda word: (word[1], word[0]), reverse=True)
        print(doctor_interest_list)

        education_pattern = []
        faculty_pattern = []
        cross_education = 0
        cross_faculty = 0
        cross_all = 0
        cross_education_in_faculty_dic = {}  #本研交叉的院系分布
        cross_education_in_interest_dic = {}  # 本研交叉的兴趣领域分布
        cross_faculty_in_faculty_dic = {} #院系交叉的院系分布
        cross_faculty_in_interest_dic ={} #院系交叉的兴趣领域分布
        cross_all_in_interest_dic = {}  # 本研、跨院系的兴趣领域分布
        cross_all_in_faculty_dic = {}  # 本研、跨院系的兴趣领域分布
        cross_all_faculty_pattern_dic = {}
        #cross_all_interest_pattern_dic ={}
        cross_education_in_faculty_list = []  # 本研交叉的院系分布
        cross_education_in_interest_list = []  # 本研交叉的兴趣领域分布
        cross_faculty_in_faculty_list = []  # 院系交叉的院系分布
        cross_faculty_in_interest_list = []  # 院系交叉的兴趣领域分布
        cross_all_in_interest_list = []  # 本研、跨院系的兴趣领域分布
        cross_all_in_faculty_list = []  # 本研、跨院系的兴趣领域分布
        cross_all_faculty_pattern_list = []
        index = -1
        for item in self.salon_user_list:
            index += 1
            education_pattern.append([])
            faculty_pattern.append([])
            for people in item[1]:
                user_index = self.user.user_map[people]
                if self.user.users[user_index].job not in education_pattern[index] and self.user.users[user_index].job is not None:
                    education_pattern[index].append(self.user.users[user_index].job)
                if self.user.users[user_index].faculty not in faculty_pattern[index] and self.user.users[user_index].faculty is not None:
                    faculty_pattern[index].append(self.user.users[user_index].faculty)
            education_pattern[index].sort()
            faculty_pattern[index].sort()

        for index in range(len(education_pattern)):
            salon_user = self.salon_user_list[index]
            salon_index = self.salon.salon_map[salon_user[0]]
            interest_set = self.salon.salons[salon_index].interest.split('+')
            people = salon_user[1]
            if '本科' in education_pattern[index] and ('硕士' in education_pattern[index] or '博士' in education_pattern[index]): #本研交叉
                cross_education +=1
                for man in people:
                    user_index = self.user.user_map[man]
                    faculty = self.user.users[user_index].faculty
                    if faculty in cross_education_in_faculty_dic:
                        cross_education_in_faculty_dic[faculty] += 1
                    else:
                        cross_education_in_faculty_dic[faculty] = 1
                for interest in interest_set:
                    if interest in cross_education_in_interest_dic:
                        cross_education_in_interest_dic[interest] += 1
                    else:
                        cross_education_in_interest_dic[interest] = 1

                if len(faculty_pattern[index]) > 1: #本研 跨院系
                    cross_all += 1
                    for man in people:
                        user_index = self.user.user_map[man]
                        faculty = self.user.users[user_index].faculty
                        if faculty in cross_all_in_faculty_dic:
                            cross_all_in_faculty_dic[faculty] += 1
                        else:
                            cross_all_in_faculty_dic[faculty] = 1
                    for interest in interest_set:
                        if interest in cross_all_in_interest_dic:
                            cross_all_in_interest_dic[interest] += 1
                        else:
                            cross_all_in_interest_dic[interest] = 1

                    faculty_pattern_key = faculty_pattern[index][0]
                    for s in faculty_pattern[index][1:]:
                        faculty_pattern_key = faculty_pattern_key + '+' + s
                    if faculty_pattern_key in cross_all_faculty_pattern_dic:
                        cross_all_faculty_pattern_dic[faculty_pattern_key] += 1
                    else:
                        cross_all_faculty_pattern_dic[faculty_pattern_key] = 1

                    '''
                    interest_set.sort()
                    interest_pattern_key = interest_set[0]
                    for t in interest_set[1:]:
                        interest_pattern_key = interest_pattern_key + '+' + t
                    if interest_pattern_key in cross_all_interest_pattern_dic:
                        cross_all_interest_pattern_dic[interest_pattern_key] += 1
                    else:
                        cross_all_interest_pattern_dic[interest_pattern_key] = 1
                    '''

            if len(faculty_pattern[index]) > 1:  #  跨院系
                cross_faculty += 1
                for man in people:
                    user_index = self.user.user_map[man]
                    faculty = self.user.users[user_index].faculty
                    if faculty in cross_faculty_in_faculty_dic:
                        cross_faculty_in_faculty_dic[faculty] += 1
                    else:
                        cross_faculty_in_faculty_dic[faculty] = 1
                for interest in interest_set:
                    if interest in cross_faculty_in_interest_dic:
                        cross_faculty_in_interest_dic[interest] += 1
                    else:
                        cross_faculty_in_interest_dic[interest] = 1

        for item in cross_all_faculty_pattern_dic:
            cross_all_faculty_pattern_list.append([item, cross_all_faculty_pattern_dic[item]])
        cross_all_faculty_pattern_list.sort(key=lambda word: (word[1], word[0]), reverse=True)

        for item in cross_education_in_faculty_dic:
            cross_education_in_faculty_list.append([item, cross_education_in_faculty_dic[item]])
        cross_education_in_faculty_list.sort(key=lambda word: (word[1], word[0]), reverse=True)

        for item in cross_education_in_interest_dic:
            cross_education_in_interest_list.append([item, cross_education_in_interest_dic[item]])
        cross_education_in_interest_list.sort(key=lambda word: (word[1], word[0]), reverse=True)

        for item in cross_faculty_in_faculty_dic:
            cross_faculty_in_faculty_list.append([item, cross_faculty_in_faculty_dic[item]])
        cross_faculty_in_faculty_list.sort(key=lambda word: (word[1], word[0]), reverse=True)

        for item in cross_faculty_in_interest_dic:
            cross_faculty_in_interest_list.append([item, cross_faculty_in_interest_dic[item]])
        cross_faculty_in_interest_list.sort(key=lambda word: (word[1], word[0]), reverse=True)

        for item in cross_all_in_faculty_dic:
            cross_all_in_faculty_list.append([item, cross_all_in_faculty_dic[item]])
        cross_all_in_faculty_list.sort(key=lambda word: (word[1], word[0]), reverse=True)

        for item in cross_all_in_interest_dic:
            cross_all_in_interest_list.append([item, cross_all_in_interest_dic[item]])
        cross_all_in_interest_list.sort(key=lambda word: (word[1], word[0]), reverse=True)

        print(cross_education)
        print(cross_faculty)
        print(cross_all)
        print(cross_education_in_faculty_list)
        print(cross_faculty_in_faculty_list)
        print(cross_all_in_faculty_list)
        print(cross_all_faculty_pattern_list)
        print(cross_education_in_interest_list)
        print(cross_faculty_in_interest_list)
        print(cross_all_in_interest_list)

        f = open(r'doc/cross_result.txt', 'w', encoding='utf-8')
        f.write('本科生参与微沙龙的兴趣领域分布\n')
        for item in undergraduate_interest_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n研究生参与微沙龙的兴趣领域分布\n')
        for item in master_interest_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n博士生参与微沙龙的兴趣领域分布\n')
        for item in doctor_interest_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n跨本研微沙龙总数:\t%d\n' % cross_education)
        f.write('\n跨院系微沙龙总数:\t%d\n' % cross_faculty)
        f.write('\n跨本研且跨院系微沙龙总数:\t%d\n' % cross_all)

        f.write('\n各院系参与跨本硕微沙龙的数量\n')
        for item in cross_education_in_faculty_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n各院系参与跨院系微沙龙的数量(以这个数据为准)\n')
        for item in cross_faculty_in_faculty_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n各院系参与跨本研且跨院系微沙龙的数量\n')
        for item in cross_all_in_faculty_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n参与跨本研且跨院系微沙龙的院系组合分布\n')
        for item in cross_all_faculty_pattern_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n各兴趣领域的跨本硕微沙龙的数量\n')
        for item in cross_education_in_interest_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n各兴趣领域的跨院系微沙龙的数量\n')
        for item in cross_faculty_in_interest_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n各兴趣领域的跨本研且跨院系微沙龙的数量\n')
        for item in cross_all_in_interest_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.close()

    def interest_stat(self):
        user_interest_dic = {}
        user_interest_list = []
        salon_interest_dic = {}
        salon_interest_list = []
        interest_adj_dic = {}
        interest_adj_list =[]

        for item in self.user.users:
            interest_set = item.interest.split('+')
            for interest in interest_set:
                if interest != '':
                    if interest in user_interest_dic:
                        user_interest_dic[interest] += 1
                    else:
                        user_interest_dic[interest] = 1
        for item in user_interest_dic:
            user_interest_list.append([item, user_interest_dic[item]])
        user_interest_list.sort(key=lambda word: (word[1], word[0]), reverse=True)
        print(user_interest_list)

        for item in self.salon.salons:
            interest_set = item.interest.split('+')
            for interest in interest_set:
                if interest in salon_interest_dic:
                    salon_interest_dic[interest] += 1
                else:
                    salon_interest_dic[interest] = 1
        for item in salon_interest_dic:
            salon_interest_list.append([item, salon_interest_dic[item]])
        salon_interest_list.sort(key=lambda word: (word[1], word[0]), reverse=True)
        print(salon_interest_list)

        for item in self.user.users:
            interest_set = item.interest.split('+')
            for interest1 in interest_set:
                for interest2 in interest_set:
                    if interest1 != '' and interest2 != '' and interest1 != interest2:
                        temp = interest1 + '+' + interest2
                        if temp in interest_adj_dic:
                            interest_adj_dic[temp] += 1
                        else:
                            interest_adj_dic[temp] = 1
        for item in interest_adj_dic:
            interest_adj_list.append([item.split('+'), interest_adj_dic[item]])
        interest_adj_list.sort(key=lambda word: (word[1], word[0][0],word[0][1]), reverse=True)
        print(interest_adj_list)

        f = open(r'doc/interest_result.txt', "w", encoding='utf-8')
        f.write('各兴趣领域感兴趣人数：\n')
        for item in user_interest_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n各兴趣领域微沙龙个数：\n')
        for item in salon_interest_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n兴趣领域邻接表：\n')
        for item in interest_adj_list:
            f.write('%s\t%s\t%d\n' % (item[0][0], item[0][1], item[1]))

    def friend_stat(self):
        friend_in_sex_dic ={}  #不同性别认识的人在性别的分布
        friend_in_faculty_dic = {} #不同性别的人认识的人在学院的分布
        friend_in_category_dic = {} #不同性别大类认识的人在性别大类的分布
        friend_in_sex_list =[]  #不同性别认识的人在性别的分布
        friend_in_faculty_list = [] #不同性别的人认识的人在学院的分布
        friend_in_category_list = [] #不同性别大类认识的人在性别大类的分布
        owner_sex_num = {'男': 0, '女': 0}
        owner_category_num = {'工科男': 0, '工科女': 0, '理科男': 0, '理科女': 0, '商科男': 0, '商科女': 0, '文科男': 0,'文科女': 0}
        for item in self.user_friend_list:
            owner = item[0]
            owner_index = self.user.user_map[owner]
            owner_sex = self.user.users[owner_index].sex
            owner_category = self.user.users[owner_index].category + '科'
            friends = item[1]
            if owner_sex != '':
                for friend in friends:
                    friend_index = self.user.user_map[friend]
                    friend_sex = self.user.users[friend_index].sex
                    friend_faculty = self.user.users[friend_index].faculty
                    friend_category = self.user.users[friend_index].category + '科'
                    if friend_sex != '':
                        friend_in_sex_key = owner_sex + '+' + friend_sex
                        if friend_in_sex_key in friend_in_sex_dic:
                            friend_in_sex_dic[friend_in_sex_key] += 1
                        else:
                            friend_in_sex_dic[friend_in_sex_key] = 1
                        owner_sex_num[owner_sex] += 1

                    if friend_faculty != '':
                        friend_in_faculty_key = owner_sex + '+' + friend_faculty
                        if friend_in_faculty_key in friend_in_faculty_dic:
                            friend_in_faculty_dic[friend_in_faculty_key] += 1
                        else:
                            friend_in_faculty_dic[friend_in_faculty_key] = 1

                    if friend_category != '' and friend_sex != '':
                        friend_in_category_key = owner_category + owner_sex + '+' + friend_category + friend_sex
                        if friend_in_category_key in friend_in_category_dic:
                            friend_in_category_dic[friend_in_category_key] += 1
                        else:
                            friend_in_category_dic[friend_in_category_key] = 1
                        owner_category_num[owner_category + owner_sex] += 1

        for item in friend_in_sex_dic:
            friend_in_sex_list.append([item.split('+'), friend_in_sex_dic[item]])
        for item in friend_in_sex_list:
            item.append(round(item[1]/owner_sex_num[item[0][0]],3))
        friend_in_sex_list.sort(key=lambda word: (word[1], word[0][0], word[0][1]), reverse=True)
        print(friend_in_sex_list)

        for item in friend_in_faculty_dic:
            friend_in_faculty_list.append([item.split('+'), friend_in_faculty_dic[item]])
        for item in friend_in_faculty_list:
            item.append(round(item[1] / owner_sex_num[item[0][0]], 3))
        friend_in_faculty_list.sort(key=lambda word: (word[1]), reverse=True)
        friend_in_faculty_list.sort(key=lambda word: (word[0][0]), reverse=True)
        print(friend_in_faculty_list)

        for item in friend_in_category_dic:
            friend_in_category_list.append([item.split('+'), friend_in_category_dic[item]])
        for item in friend_in_category_list:
            item.append(round(item[1] / owner_category_num[item[0][0]], 3))
        friend_in_category_list.sort(key=lambda word: (word[1]), reverse=True)
        friend_in_category_list.sort(key=lambda word: (word[0][0]), reverse=True)
        print(friend_in_category_list)

        f = open(r'doc/friend_result.txt', "w", encoding='utf-8')
        f.write('男生女生通过微沙龙认识的人在性别的分布：(* 认识 * , 数量, 比例)\n')
        for item in friend_in_sex_list:
            f.write('%s\t%s\t%d\t%.3f\n' % (item[0][0], item[0][1], item[1], item[2]))

        f.write('\n男生女生通过微沙龙认识的人在院系的分布：(* 认识 *院系, 数量, 比例)\n')
        for item in friend_in_faculty_list:
            f.write('%s\t%s\t%d\t%.3f\n' % (item[0][0], item[0][1], item[1], item[2]))

        f.write('\n性别和大类之间认识的比例：\n')
        for item in friend_in_category_list:
            f.write('%s\t%s\t%d\t%.3f\n' % (item[0][0], item[0][1], item[1], item[2]))
        f.close()

    def save_data(self):
        print(self.faculty_list)
        print(self.launch_faculty_list)
        print(self.teacher)
        print(self.teacher_time)
        print(self.teacher_faculty_list)
        print(self.teaching_stuff)
        print(self.teaching_stuff_time)
        print(self.teaching_stuff_faculty_list)


        f = open(r'salon_feeling.txt', 'w', encoding='utf-8')
        for item in self.signs:
            f.write(item.feel)
            f.write('\n')
        f.close()


        f = open(r'doc/sign_result.txt', "w", encoding='utf-8')
        #f.write('各院系参与人次、参与跨学科微沙龙人次（截止2013.11.11）\n')
        f.write('各院系参与人次（截止2013.11.16）\n')
        for item in self.faculty_list:
            #f.write('%s\t%d\t%d\n' % (item[0], item[1][0], item[1][1]))
            f.write('%s\t%d\n' % (item[0], item[1][0]))

        f.write('\n各院系发起微沙龙次数（截止2013.11.16）\n')
        for item in self.launch_faculty_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n教师发起次数\t%d\n教师参与人次\t%d\n' % (self.teacher[0], self.teacher[1]))

        f.write('\n各院系教师参与微沙龙人次\n')
        for item in self.teacher_faculty_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n教师参与微沙龙时间分布（0:00~1:00, 1:00~2:00 ...）\n')
        for item in self.teacher_time:
            f.write('%d\t' % item)
        f.write('\n')

        f.write('\n教工发起次数\t%d\n教工参与人次\t%d\n' % (self.teaching_stuff[0], self.teaching_stuff[1]))

        f.write('\n各院系教工参与微沙龙人次\n')
        for item in self.teaching_stuff_faculty_list:
            f.write('%s\t%d\n' % (item[0], item[1]))

        f.write('\n教工参与微沙龙时间分布（0:00~1:00, 1:00~2:00 ...）\n')
        for item in self.teaching_stuff_time:
            f.write('%d\t' % item)
        f.close()


def main():
    sign_process = SignProcess()
    sign_process.save_data()

if __name__ == '__main__':
    main()

