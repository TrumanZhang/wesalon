# coding=utf-8


modal = '我你他啊哈啦在和就吗的得又再从呢们后与于'


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if u'\u0030' <= uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar):
        return False
    else:
        return True


f = open('salon_name.txt', 'r', encoding='utf-8')
lines = f.readlines()
dic = {}
for item in lines:
        for length in range(2, 11):
            if length < len(item):
                for start in range(0, len(item) - length + 1):
                    string = item[start: start + length]
                    if string in dic:
                        dic[string] += 1
                    else:
                        dic[string] = 1
words = []
for item in dic:
    flag = 0
    for index in range(len(item)):
        if is_other(item[index]) or item[index] in modal:
            flag = 1
            break
    if flag == 0:
        words.append([item, dic[item]])
words.sort(key = lambda word:(word[1], word[0]), reverse= True)
print(words[:300])
print(len(words))

f = open(r"doc/salon_name_result.txt", 'w', encoding='utf-8')
for item in words[:10000]:
    f.write(item[0])
    f.write('\t')
    f.write(str(item[1]))
    f.write('\n')
f.close()