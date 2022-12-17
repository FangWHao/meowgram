import socket
import threading
import pickle
import os
from time import sleep

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9000))


user_id=-1
user_name=''
friend_list=[]
# 使用双线程，一个接收，一个发送

def recv():
    while True:
        try:
            buf=sock.recv(1024)
            if not buf:
                continue
            print(buf.decode('utf-8'))
        except:
            print('服务器已断开连接')
            break

def send():
    while True:
        data_send=input()
        data_send='M'+str(user_id)+' '+data_send # M表示消息
        sock.sendall(data_send.encode('utf-8'))
        print('发送成功')

def start_client_chat():
    t1=threading.Thread(target=recv)
    t2=threading.Thread(target=send)
    t1.start()
    t2.start()

def start_client_login():
    global user_id
    global user_name
    while True:
        print('请输入用户名和密码')
        user_name=input('请输入用户名：')
        password=input('请输入密码：')
        data_send=user_name+' '+password
        data_send='L'+data_send
        sock.sendall(data_send.encode('utf-8'))

        buf=sock.recv(1024)
        print(buf.decode('utf-8'))

        if buf.decode('utf-8')!='False':
            print('登录成功')
            print('登录成功，您现在正在以用户'+user_name+'的身份进入聊天室')
            user_id=int(buf.decode('utf-8'))
            return buf.decode('utf-8')
        
        else:
            print('登录失败，请重新输入')
            continue

def start_client_register():
    while True:
        user_name=input('请输入用户名：')
        password=input('请输入密码：')
        data_send=user_name+' '+password
        data_send='R'+data_send
        sock.sendall(data_send.encode('utf-8'))

        buf=sock.recv(1024)
        print(buf.decode('utf-8'))

        if buf.decode('utf-8')=='注册成功':
            break
        
        else:
            print('注册失败，请重新输入')
            continue

def get_friend_list():
    global friend_list
    data_send='F'+str(user_name)
    sock.sendall(data_send.encode('utf-8'))

    buf=sock.recv(1024)
    print('好友列表：')
    friend_list=pickle.loads(buf)
    #print(friend_list)
    #输出fiend_list，f代表私聊，g代表群聊
    # f使用蓝色输出，g使用绿色输出
    for i in range(len(friend_list)):
        if friend_list[i][0]=='g':
            print('\033[32m'+str(i)+friend_list[i][1:]+'\033[0m')
        else:
            print('\033[34m'+str(i)+friend_list[i][1:]+'\033[0m')

def get_history_message(friend_name):
    data_send='H'+str(user_name)+' '+str(friend_name)
    sock.sendall(data_send.encode('utf-8'))

    buf=sock.recv(1024)
    print('历史消息：')
    history_message=pickle.loads(buf)
    print(history_message)
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
        start_client_login()
    elif choice=='2':
        start_client_register()

        start_client_login()
    else:
        print('输入错误，按任意键退出')
        input()
        exit(0)
        
    #登录成功后，进入聊天界面
    print('-----------------')
    
    # get好友列表和群列表
    get_friend_list()
    start_client_chat()
    print("请输入要进行聊天的编号")
    num=input()
    os.system('clear')
    print('-----------------')
    get_history_message(friend_list[num][1:])