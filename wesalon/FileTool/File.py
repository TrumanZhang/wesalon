# encoding: utf-8


"""
@author: zoulixin
@contact: zoulx15@mails.tsinghua.edu.cn
@time:2016/6/27 0027
"""
import sys
import os
from Config import Config

class File():
    def __init__(self):
        pass




    # if the file not exist create the file,
    # else do noting
    @classmethod
    def create_file_without_delete(cls,path):
        if not(File.file_existornot(path)):
            f=open(path,'w')
            f.close()



    # determine the file exist or not
    @classmethod
    def file_exist_or_not(cls,path):
        os.path.isfile(path)
        pass


    # add information in the file
    @classmethod
    def file_add_info(cls,path,info):
        if File.file_exist_or_not(path):
            f=open(path,'a')
            f.write(info+'\n')
        else:
            File.create_file_without_delete(path)
            File.file_add_info(path,info)


    # create a dictionary
    @classmethod
    def create_dir(cls,path):
        os.makedirs(path)


    # get the file name from the path
    @classmethod
    def get_filename_fromdir(cls,path):
        path=str(path)
        res=path.split('/')
        return res[len(res)-1]


    # remove the root path in the path
    @classmethod
    def remove_root_path(cls,path):
        path=str(path)
        return path.replace(Config.root_path,'')


    @classmethod
    def delete_file_folder(cls,src):
        '''delete files and folders'''
        if os.path.isfile(src):
            try:
                os.remove(src)
            except:
                pass
        elif os.path.isdir(src):
            for item in os.listdir(src):
                itemsrc = os.path.join(src, item)
                cls.delete_file_folder(itemsrc)
            try:
                os.rmdir(src)
            except:
                pass

    @classmethod
    def save_list_with_path(cls,list_file,path):
        f=open(path,mode='w')
        res=""
        for i in range(len(list_file)-1):
            res+=str(list_file[i])+","
        res+=str(list_file[i-1])
        f.writelines(res)

    @classmethod
    def read_list_from_file(cls,path):
        f=open(path,mode="r")
        line=f.readlines()
        listres=[float(i) for i in line[0].split(",")]
        return listres


    @classmethod
    def replace_file_name(cls,path,replace_condition):
        import os
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)) == True:
                if file.find('.') < 0:
                    newname = file + replace_condition
                    os.rename(os.path.join(path, file), os.path.join(path, newname))
                    print(file)
        pass






if __name__ == '__main__':
    pass