import login
import client
import os

import threading

# 初始化，检查文件夹完整性

def check_dir():
    folder=os.path.exists('data')
    if folder==False:
        os.mkdir('data')
        print('首次运行，创建文件夹')
    else:
        print('完成初始化，文件夹完整')



if __name__ == '__main__':

    #登录
    os.system('clear')
    print('-----------------')
    print('欢迎使用本系统')
    print('-----------------')
    print('输入1进行登录，输入2进行注册')
    print('-----------------')

    choice=input('请输入：')
    if choice=='1':
        client.start_client_login()
    elif choice=='2':
        client.start_client_register()

        client.start_client_login()
    else:
        print('输入错误，按任意键退出')
        input()
        exit(0)
        
    #登录成功后，进入聊天界面
    print('-----------------')
    
    # get好友列表和群列表
    client.get_friend_list()
    client.start_client_chat()
    print("请输入要进行聊天的编号")
    num=input()
    os.system('clear')
    print('-----------------')
    client.get_
    print
        