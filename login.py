# 读取本地密码文件，进行登录验证，若没有本地密码文件，则创建一个
# 本地密码文件格式为：用户名，密码（md5加密）

import hashlib
import os
import sys
import csv


def get_md5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()


def check_file():
    if os.path.exists('./data/user.txt'):
        print('已存在本地密码文件')
        return True
    else:
        print('未检测到本地密码文件，创建中')
        file = open('./data/user.txt', 'w')
        file.close()


def login(user_name, password):
    password = get_md5(password)
    file = open('./data/user.txt', 'r')
    user_id = 0
    for line in file:
        line = line.strip()
        if line == user_name+','+password:
            return True
    return False


def register(user_name, password):
    password = get_md5(password)
    file = open('./data/user.txt', 'a')
    # 检查一下是不是已经注册了
    data = []
    with open('./data/user.txt', 'r') as f:
        for line in f:
            line = line.strip()
            data.append(line)
    for i in data:
        if user_name == i.split(',')[0]:
            print('该用户已经注册')
            return False
            
    file.write(user_name+','+password+'\n')
    file.close()
    print('注册成功')
    if os.path.exists('./data/friend_list.csv')==False:
        file = open('./data/friend_list.csv', 'w')
        file.close()
    data=[]
    with open('./data/friend_list.csv','r',encoding='gb18030') as f:
        reader=csv.reader(f)
        for row in reader:
            data.append(row)
    
    data.append([user_name])
    with open('./data/friend_list.csv','w',encoding='gb18030') as f:
        writer=csv.writer(f)
        writer.writerows(data)

    return True


def login_main():
    while True:
        os.system('clear')
        choice = input('请输入：')
        if choice == '1':
            global user_id
            user_id = login()
            if user_id != False:
                break
            else:
                print('按任意键返回到主界面')
                input()
                continue
        elif choice == '2':
            if register() == True:
                print('按任意键返回到主界面')
                input()
                continue
        else:
            print('输入错误，请重新输入')
            continue
        print('-----------------')
