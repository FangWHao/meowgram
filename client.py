import socket
import threading
import pickle
import os
import time
import datetime
from time import sleep
#sock  用于实现登录，接收好友列表等功能
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9000))

#sock1 只用于实现接受消息
sock1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock1.connect(('localhost',9000))

user_id = -1
user_name = ''
friend_list = []
message_count = [0]*100  # 消息计数

in_chat = 0  # 0表示未在聊天，1表示在聊天
chat_with = ' '  # 聊天对象

# 使用双线程，一个接收，一个发送


def recv():  # 接收消息
    while True:
        # try:
        buf = b''
        while True:
            packet = sock1.recv(1024) #注意，要是消息长度超过1024，会出问题，这里要改进
            if not packet or len(packet) < 1024:
                buf += packet
                break
            buf += packet

        buf = buf.decode('utf-8')
        source_name = buf.strip().split(' ')[0]
        time = buf.strip().split(' ')[1]+' '+buf.strip().split(' ')[2]
        message = buf.strip().split(' ')[3]
        if in_chat == 0:  # 未在聊天，提醒新消息
            try:
                message_count[friend_list.index('f'+source_name)] += 1
            except:
                message_count[friend_list.index('g'+source_name)] += 1
            os.system('clear')
            print('-----------------')
            print('好友列表：')
            for i in range(len(friend_list)):
                if friend_list[i][0] == 'g':
                    print('\033[32m'+str(i)+'   ' +
                          friend_list[i][1:]+'\033[0m', end='')
                else:
                    print('\033[34m'+str(i)+'   ' +
                          friend_list[i][1:]+'\033[0m', end='')
                # 新消息来的话用红色输出数量
                if message_count[i] != 0:
                    print('\033[31m'+'  ('+str(message_count[i])+')'+'\033[0m')
                else:
                    print(' ')
            print('请输入要进行聊天的编号')
        else: # 在聊天
            if chat_with == source_name: # 如果是正在聊天的对象发来的消息
                print(time)
                print('\033[34m'+source_name+': '+message+'\033[0m')
                #print('\033[32m'+source_name+'\033[0m'+' '+time+' '+message)
            else: # 如果不是正在聊天的对象发来的消息
                print('你有一条来自'+'\033[34m'+source_name+'\033[0m'+'的消息')
        # except:
        #    print('服务器已断开连接')
        #    break


def send():
    while True:
        data_send = input()
        data_send = 'M'+str(user_id)+' '+data_send  # M表示消息
        sock.sendall(data_send.encode('utf-8'))
        print('发送成功')


def start_client_chat():
    t1 = threading.Thread(target=recv)
    t2 = threading.Thread(target=send)
    t1.start()
    t2.start()


def start_client_login():
    global user_id
    global user_name
    while True:
        print('请输入用户名和密码')
        user_name = input('请输入用户名：')
        password = input('请输入密码：')
        data_send = user_name+' '+password
        data_send = 'L'+data_send
        sock.sendall(data_send.encode('utf-8'))

        buf = sock.recv(1024)
        print(buf.decode('utf-8'))

        if buf.decode('utf-8') != 'False':
            print('登录成功')
            print('登录成功，您现在正在以用户'+user_name+'的身份进入聊天室')
            sock1.sendall(("X"+user_name).encode('utf-8')) # 将用户名发送给服务器，服务器将其加入到在线用户列表中
            user_id = int(buf.decode('utf-8'))
            return buf.decode('utf-8')

        else:
            print('登录失败，请重新输入')
            continue


def start_client_register():
    while True:
        user_name = input('请输入用户名：')
        password = input('请输入密码：')
        data_send = user_name+' '+password
        data_send = 'R'+data_send
        sock.sendall(data_send.encode('utf-8'))

        buf = sock.recv(1024)
        print(buf.decode('utf-8'))

        if buf.decode('utf-8') == '注册成功':
            break

        else:
            print('注册失败，请重新输入')
            continue


def get_friend_list():
    global friend_list
    data_send = 'F'+str(user_name)
    sock.sendall(data_send.encode('utf-8'))

    buf = sock.recv(1024)
    print('好友列表：')
    friend_list = pickle.loads(buf)
    # print(friend_list)
    # 输出fiend_list，f代表私聊，g代表群聊
    # f使用蓝色输出，g使用绿色输出
    for i in range(len(friend_list)):
        if friend_list[i][0] == 'g':
            print('\033[32m'+str(i)+'   '+friend_list[i][1:]+'\033[0m')
        else: 
            print('\033[34m'+str(i)+'   '+friend_list[i][1:]+'\033[0m')


def get_history_message(friend_name):
    data_send = 'H'+str(user_name)+' '+str(friend_name)
    sock.sendall(data_send.encode('utf-8'))
    buf=b''
    while True:
        packet = sock.recv(1024)
        if not packet or len(packet) < 1024:
            buf += packet
            break
        buf += packet
    print('历史消息：')
    history_message = pickle.loads(buf)
    # print(history_message)
    if not history_message:
        return
    for i in range(len(history_message)):
        recieve_or_send = history_message[i][0]
        time = history_message[i][1:].strip().split(' ')[0]+'  '+history_message[i][1:].strip().split(' ')[1]
        message = history_message[i][1+len(time):]
        # 绿色为自己发送的消息，蓝色为好友发送的消息
        print(time)
        if recieve_or_send == 's':
            print('\033[32m'+user_name+': '+message+'\033[0m')
        else:
            print('\033[34m'+friend_name+': '+message+'\033[0m')


def send_to_friend(friend_name):
    while True:
        print('请输入要发送的消息,输入exit退出')
        data_send = input()
        if data_send == 'exit':
            os.system('clear')
            break
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        data_send = 'MP'+str(user_name)+' ' + \
            str(friend_name)+' '+now+' '+data_send
        sock.sendall(data_send.encode('utf-8'))
        print('发送成功')

def send_to_group(group_name):
    while True:
        print('请输入要发送的消息,输入exit退出')
        data_send = input()
        if data_send == 'exit':
            os.system('clear')
            break
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        data_send = 'MG'+str(user_name)+' ' + \
            str(group_name)+' '+now+' '+data_send
        sock.sendall(data_send.encode('utf-8'))
        print('发送成功')

'''
while True:
    data_send=input('请输入：')
    data_send=str(user_id)+' '+data_send
    sock.sendall(data_send.encode('utf-8'))

    buf=sock.recv(1024)
    print(buf.decode('utf-8'))

sock.close()
'''


def check_dir():
    folder = os.path.exists('data')
    if folder == False:
        os.mkdir('data')
        print('首次运行，创建文件夹')
    else:
        print('完成初始化，文件夹完整')


if __name__ == '__main__':

    # 登录
    os.system('clear')
    print('-----------------')
    print('欢迎使用本系统')
    print('-----------------')
    print('输入1进行登录，输入2进行注册')
    print('-----------------')

    choice = input('请输入：')
    if choice == '1':
        start_client_login()
    elif choice == '2':
        start_client_register()

        start_client_login()
    else:
        print('输入错误，按任意键退出')
        input()
        exit(0)

    # 登录成功后，进入聊天界面
    os.system('clear')
    # start_client_chat()

    # 开启一个线程，用于接收消息
    t1 = threading.Thread(target=recv)
    t1.start()

    while True:
        print('-----------------')
        # get好友列表和群列表
        get_friend_list()
        print("请输入要进行聊天的编号")
        num = int(input())
        os.system('clear')
        if friend_list[num][0] == 'f':
            in_chat = True
            chat_with = friend_list[num][1:]
            message_count[num]=0
            print('正在与'+friend_list[num][1:]+'聊天')
            get_history_message(friend_list[num][1:])
            send_to_friend(friend_list[num][1:])
            print('聊天结束')
            chat_with = ''
            in_chat = False
        else:
            in_chat = True
            chat_with = friend_list[num][1:]
            message_count[num]=0
            print('正在'+friend_list[num][1:]+'中群聊')
            get_history_message(friend_list[num][1:])
            send_to_group(friend_list[num][1:])
        

