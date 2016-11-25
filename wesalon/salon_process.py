# coding=utf-8
import csv
from salon import Salon


class SalonProcess():
    def __init__(self):
        self.data_path = r'E:\document\Python\wesalon\salons.csv'
        self.salons =[]
        self.month = [0] * 13
        self.week = [0] * 7 #salons on Sunday Monday Tuesday ...
        self.place_dic = {}
        self.people_num = [0] * 31
        self.time1 = [0] * 5  #8：11  11：14 14:17 17:20 20:8
        self.time2 = [0] * 24 #0:1 ...
        self.field_dic ={}
        self.field_list = []
        self.salon_map = {}

        self.read_data()
        self.salon_month_stat()
        self.salon_week_stat()
        self.salon_place_stat()
        self.salon_people_num_stat()
        self.salon_launch_time_stat()
        self.salon_field_stat()

    def read_data(self):
        f = open(self.data_path, "r", encoding='utf-8')
        lines = csv.reader(f)
        csv_lines = 0
        index = 0
        for item in lines:
            csv_lines += 1
            if csv_lines == 1:
                pass
            else:
                salon_new = Salon()
                salon_new.load_data(item)
                self.salons.append(salon_new)
                self.salon_map[salon_new.id] = index
                index += 1

    def salon_month_stat(self):
        for item in self.salons:
            if item.status != '已删除' and item.status != '管理员删除':
                self.month[item.date.month] += 1

    def salon_week_stat(self):
        for item in self.salons:
            if item.status != '已删除' and item.status != '管理员删除':
                self.week[item.week] += 1

    def salon_place_stat(self):
        for item in self.salons:
            if item.status != '已删除' and item.status != '管理员删除':
                if item.place in self.place_dic:
                    self.place_dic[item.place] += 1
                else:
                    self.place_dic[item.place] = 1

    def salon_people_num_stat(self):
        for item in self.salons:
            if item.status != '已删除' and item.status != '管理员删除':
                self.people_num[item.people_number] += 1

    def salon_launch_time_stat(self):
        for item in self.salons:
            if item.status != '已删除' and item.status != '管理员删除':
                self.time2[item.time.hour] += 1
                if 8 <= item.time.hour < 20:
                    self.time1[int((item.time.hour - 8)/3)] += 1
                else:
                    self.time1[-1] += 1

    def salon_field_stat(self):
        for item in self.salons:
            if item.status != '已删除' and item.status != '管理员删除':
                if item.field in self.field_dic:
                    self.field_dic[item.field] += 1
                else:
                    self.field_dic[item.field] = 1
        for item in self.field_dic:
                self.field_list.append([item, self.field_dic[item]])
        self.field_list.sort(key=lambda word: (word[1], word[0]), reverse=True)

    def get_salon_info_dic(self): #for sign process
        info_dic = {}
        for item in self.salons:
            if int(item.cross_faculty_number) > 1:
                info_dic[item.id] = [item.date, item.time, 1]
            else:
                info_dic[item.id] = [item.date, item.time, 0]
        return info_dic

    def save_data(self):
        print(self.month)
        print(self.week)
        print(self.place_dic)
        print(self.people_num)
        print(self.time1)
        print(self.time2)
        print(self.field_dic)


        #save names and introduce of salons
        f = open(r'./salon_name.txt', 'w', encoding='utf-8')
        for item in self.salons:
            f.write(item.name)
            f.write('\n')
        f.close()

        f = open(r'./salon_introduce.txt', 'w', encoding='utf-8')
        for item in self.salons:
            f.write(item.detail)
            f.write('\n')
        f.close


        f = open(r'./doc/salon_result.txt', 'w', encoding='utf-8')

        f.write('每个月发起微沙龙(从三月开始)：\n')
        for item in self.month[3:]:
            f.write(str(item))
            f.write('\t')
        f.write('\n')

        f.write('\n每周各天累计微沙龙(from Sunday)：\n')
        for item in self.week:
            f.write(str(item))
            f.write('\t')
        f.write('\n')

        f.write('\n微沙龙发起地点分布：\n')
        for item in self.place_dic:
            f.write('%s\t%s\n'%(item, str(self.place_dic[item])))

        f.write('\n每场微沙龙人数分布（from 3 to 30）：\n')
        for item in self.people_num[3:]:
            f.write(str(item))
            f.write('\t')
        f.write('\n')

        f.write('\n微沙龙时间分布（0:00~1:00 1:00~2:00 2:00~3:00...）：\n')
        for item in self.time2:
            f.write(str(item))
            f.write('\t')
        f.write('\n')

        f.write('\n微沙龙领域统计：\n')
        for item in self.field_list:
            f.write('%s\t%s\n' %(item[0], str(item[1])))


def main():
    salon_process = SalonProcess()
    salon_process.save_data()


if __name__ == '__main__':
    main()