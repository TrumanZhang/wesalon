# encoding: utf-8


"""
@author: zoulixin
@contact: zoulx15@mails.tsinghua.edu.cn
@time:2016/6/27 0027
"""
import csv



class CSVTool():
    def __init__(self):
        pass

    @classmethod
    def ParseCSVFile(cls,file_path):
        spamreader=[]
        with open(file_path, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            spamreader=list(spamreader)
            spamreader.remove(spamreader[0])
        return spamreader

    @classmethod
    def ParseCSVFile_without_the_first_line(cls, file_path: object, delimiter: object = "::") -> object:
        # InOutInfo.begin_info("start Parsing "+file_path)
        spamreader=[]
        f=open(file_path,"r", encoding= 'utf-8')
        lines=f.readlines()
        lines.remove(lines[0])
        for item in lines:
            temp=item.split(delimiter)
            spamreader.append(temp)
        # InOutInfo.end_info("finish parsing "+file_path)
        return spamreader


    @classmethod
    def ParseCSVFile_with_the_first_line(cls, file_path):
        spamreader = []
        with open(file_path, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            spamreader = list(spamreader)
        return spamreader

