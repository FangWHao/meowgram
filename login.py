# 读取本地密码文件，进行登录验证，若没有本地密码文件，则创建一个
# 本地密码文件格式为：用户名，密码（md5加密）

import hashlib
import os
import sys


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
        user_id += 1
        line = line.strip()
        if line == user_name+','+password:
            # print('用户id为：'+str(user_id))
            return user_id
    return False


def register(user_name, password):
    password = get_md5(password)
    file = open('./data/user.txt', 'a')
    file.write(user_name+','+password+'\n')
    file.close()
    print('注册成功')
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
