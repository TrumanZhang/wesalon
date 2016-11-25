# coding=utf-8
import csv
from user import User


class UserProcess():
    def __init__(self):
        self.data_path = r'users.csv'
        self.users = []
        self.user_sum = 0
        self.man_sum = 0
        self.woman_sum = 0
        self.join_minutes_weekly = []
        self.join_minutes_weekly_dis = [0]* 25   # 0: 0~1 1: 2~2 ... 9: 9~10
        self.job_dic = {}
        self.faculty_dic = {}
        self.faculty_list = []  # trasfromed from  dic
        self.user_map = {}
        self.following_list = []

        self.read_data()
        self.sex_stat()     #sex
        self.join_minutes_weekly_stat() #join minutes distribution
        self.job_stat()     #job
        self.faculty_stat() #faculty
        self.following_stat()

    def read_data(self):
        f = open(self.data_path, "r", encoding='utf-8')
        lines = csv.reader(f)
        index = 0
        csv_lines = 0
        for item in lines:
            csv_lines += 1
            if csv_lines == 1:
                pass
            else:
                user_new = User()
                self.user_sum = user_new.load_data(item, self.user_sum)
                self.users.append(user_new)
                self.join_minutes_weekly.append(user_new.join_minutes_weekly)
                self.user_map[user_new.id] = index
                index += 1

    def sex_stat(self):
        for item in self.users:
            if item.sex == '男':
                self.man_sum += 1
            elif item.sex == '女':
                self.woman_sum += 1
            else:
                pass

    def join_minutes_weekly_stat(self):
        for item in self.users:
            if item.join_minutes_weekly is not None:
                self.join_minutes_weekly_dis[int(item.join_minutes_weekly / 60)] += 1

    def job_stat(self):
        for item in self.users:
            if item.job is None:
                pass
            else:
                if item.job in self.job_dic:
                    self.job_dic[item.job] += 1
                else:
                    self.job_dic[item.job] = 1

    def faculty_stat(self):
        for item in self.users:
            if item.faculty == '':
                pass
            else:
                if item.faculty in self.faculty_dic:
                    self.faculty_dic[item.faculty] += 1
                else:
                    self.faculty_dic[item.faculty] = 1
        for item in self.faculty_dic:
            self.faculty_list.append([item, self.faculty_dic[item]])
        self.faculty_list.sort(key=lambda word: (word[1], word[0]), reverse=True)

    def following_stat(self):
        f = open('followings.csv', "r", encoding='utf-8')
        lines = csv.reader(f)
        csv_lines = 0
        following_dic = {}
        following_in_sex_dic = {}  # 不同性别关注的人在性别的分布
        following_in_faculty_dic = {}  # 不同性别的人关注的人在学院的分布
        following_in_category_dic = {}  # 不同性别大类关注的人在性别大类的分布
        following_in_sex_list = []  # 不同性别关注的人在性别的分布
        following_in_faculty_list = []  # 不同性别的人关注的人在学院的分布
        following_in_category_list = []  # 不同性别大类关注的人在性别大类的分布
        owner_sex_num = {'男': 0, '女': 0}
        owner_category_num = {'工科男': 0, '工科女': 0, '理科男': 0, '理科女': 0, '商科男': 0, '商科女': 0, '文科男': 0, '文科女': 0}
        for item in lines:
            csv_lines += 1
            if csv_lines == 1:
                pass
            else:
                faculty1 = item[4]
                faculty2 = item[5]
                owner_sex = self.users[self.user_map[item[0]]].sex
                friend_sex = self.users[self.user_map[item[2]]].sex
                friend_faculty = self.users[self.user_map[item[2]]].faculty
                friend_category = self.users[self.user_map[item[2]]].category + '科'
                owner_category = self.users[self.user_map[item[0]]].category + '科'
                if faculty1 != faculty2 and faculty1 != '' and faculty2 != '':
                    temp = faculty1 + '+' + faculty2
                    if temp in following_dic:
                        following_dic[temp] += 1
                    else:
                        following_dic[temp] = 1

                if owner_sex != '' and friend_sex != '':
                    following_in_sex_key = owner_sex + '+' + friend_sex
                    if following_in_sex_key in following_in_sex_dic:
                        following_in_sex_dic[following_in_sex_key] += 1
                    else:
                        following_in_sex_dic[following_in_sex_key] = 1
                    owner_sex_num[owner_sex] += 1

                if owner_sex != '' and friend_sex != '' and friend_faculty != '':
                    friend_in_faculty_key = owner_sex + '+' + friend_faculty
                    if friend_in_faculty_key in following_in_faculty_dic:
                        following_in_faculty_dic[friend_in_faculty_key] += 1
                    else:
                        following_in_faculty_dic[friend_in_faculty_key] = 1

                if owner_sex != '' and friend_sex != '':
                    friend_in_category_key = owner_category + owner_sex + '+' + friend_category + friend_sex
                    if friend_in_category_key in following_in_category_dic:
                        following_in_category_dic[friend_in_category_key] += 1
                    else:
                        following_in_category_dic[friend_in_category_key] = 1
                    owner_category_num[owner_category + owner_sex] += 1

        for item in following_dic:
            self.following_list.append([item.split('+'), following_dic[item]])
        self.following_list.sort(key=lambda word: (word[1], word[0][0], word[0][1]), reverse=True)

        for item in following_in_sex_dic:
            following_in_sex_list.append([item.split('+'), following_in_sex_dic[item]])
        for item in following_in_sex_list:
            item.append(round(item[1] / owner_sex_num[item[0][0]], 3))
        following_in_sex_list.sort(key=lambda word: (word[1], word[0][0], word[0][1]), reverse=True)
        print(following_in_sex_list)

        for item in following_in_faculty_dic:
            following_in_faculty_list.append([item.split('+'), following_in_faculty_dic[item]])
        for item in following_in_faculty_list:
            item.append(round(item[1] / owner_sex_num[item[0][0]], 3))
        following_in_faculty_list.sort(key=lambda word: (word[1]), reverse=True)
        following_in_faculty_list.sort(key=lambda word: (word[0][0]), reverse=True)
        print(following_in_faculty_list)

        for item in following_in_category_dic:
            following_in_category_list.append([item.split('+'), following_in_category_dic[item]])
        for item in following_in_category_list:
            item.append(round(item[1] / owner_category_num[item[0][0]], 3))
        following_in_category_list.sort(key=lambda word: (word[1]), reverse=True)
        following_in_category_list.sort(key=lambda word: (word[0][0]), reverse=True)
        print(following_in_category_list)

        f = open(r'doc/following_result.txt', "w", encoding='utf-8')
        f.write('男生女生关注的人在性别的分布：(* 认识 * , 数量, 比例)\n')
        for item in following_in_sex_list:
            f.write('%s\t%s\t%d\t%.3f\n' % (item[0][0], item[0][1], item[1], item[2]))

        f.write('\n男生女生关注的人在院系的分布：(* 认识 *院系, 数量, 比例)\n')
        for item in following_in_faculty_list:
            f.write('%s\t%s\t%d\t%.3f\n' % (item[0][0], item[0][1], item[1], item[2]))

        f.write('\n性别和大类之间关注的比例：\n')
        for item in following_in_category_list:
            f.write('%s\t%s\t%d\t%.3f\n' % (item[0][0], item[0][1], item[1], item[2]))
        f.close()

    def save_data(self):
        rate_woman = round(10.0 / (self.man_sum / self.woman_sum + 1),2)
        rate_man = round(10 - rate_woman, 2)
        print(self.man_sum, self.woman_sum, self.user_sum, rate_man, rate_woman)
        print(self.join_minutes_weekly_dis)
        print(self.job_dic)
        print(self.faculty_list, len(self.faculty_list))

        f = open(r'doc/user_result.txt', "w", encoding='utf-8')
        f.write('性别统计（截止2013.11.16）\n')
        f.write('总人数\t%.0f\n' % self.user_sum)
        f.write('男\t%.0f\n' % self.man_sum)
        f.write('女\t%.0f\n' % self.woman_sum)
        f.write('男女比\t%.2f:%.2f\n' % (rate_man, rate_woman))

        f.write('\n用户每周参与微沙龙时间分布(0~1h 1~2h ...)：\n')
        for item in self.join_minutes_weekly_dis:
            f.write(str(item))
            f.write('\t')
        f.write('\n')

        f.write('\n用户身份统计：\n')
        for item in self.job_dic:
            f.write('%s\t%s\n' % (item, str(self.job_dic[item])))

        f.write('\n院系用户数量分布：\n')
        for item in self.faculty_list:
            f.write('%s\t%s\n' % (item[0], item[1]))

        f.write('\n关注度邻接表：\n')
        for item in self.following_list:
            f.write('%s\t%s\t%d\n' %(item[0][0], item[0][1], item[1]))
        f.close()


def main():
    user_process = UserProcess()
    user_process.save_data()

if __name__ == '__main__':
    main()



