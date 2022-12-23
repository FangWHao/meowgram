import socketserver
import login
import database
import os
import time
import datetime
import pickle  # 以list的形式使用TCP发送数据


connect_list=[] # 保存连接的客户端
connect_list_chat=[] # 保存连接的客户端，用于聊天
id_list=[] # 保存客户端的id
name_list=[] # 保存客户端的用户名
i=0

group_file_name='./data/group.csv'

# 初始化一下，建立文件夹data，子目录包含group_history和history

if os.path.exists('./data')==False:
    os.mkdir('./data')
if os.path.exists('./data/group_history')==False:
    os.mkdir('./data/group_history')
if os.path.exists('./data/history')==False:
    os.mkdir('./data/history')

class sqServer(socketserver.BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)

        while True:
            data = self.request.recv(1024)
            if not data:
                print('Client disconnected')
                print('Client address:',self.client_address)
                print('pre',name_list)
                try: # 从列表中删除断开连接的客户端
                    i=connect_list.index(self.request)
                    connect_list.pop(i)
                    name_list.pop(i)
                    connect_list_chat.pop(i)
                    print('after',name_list)
                except: # 说明这个是聊天socket
                    print('聊天socket断开连接',self.request)
                
                break

            print('Received', data.decode('utf-8'), 'from', self.client_address,self.request)

            # 对数据进行处理
            data=data.decode('utf-8')
            if data[0]=='X': # 代表成功登录后建立新的专用的聊天socket
                data=data[1:]
                data=data.strip()
                connect_list_chat.append(self.request)
                print('成功建立聊天socket ',self.request)

            elif data=='exit': # 代表退出登录
                self.request.sendall('exit'.encode('utf-8'))
            elif data[0]=='A': # A代表添加朋友/群聊
                if(data[1]=='F'):  # F代表添加朋友
                    data=data[2:]
                    data=data.split(' ')
                    user_name=data[0]
                    friend_name=data[1]
                    print(user_name,'尝试添加好友',friend_name)
                    if database.add_friend(user_name, friend_name)==True:
                        self.request.sendall('添加成功'.encode('utf-8'))
                        print('添加成功')
                    else :
                        self.request.sendall('添加失败'.encode('utf-8'))
                        print('添加失败')

                elif(data[1]=='G'): # G代表添加群聊
                    data=data[2:]
                    data=data.split(' ')
                    user_name=data[0]
                    group_name=data[1]
                    print(user_name,'尝试添加群聊',group_name)
                    if database.add_group(user_name, group_name)==True:
                        self.request.sendall('添加成功'.encode('utf-8'))
                        print('添加成功')
                    else :
                        self.request.sendall('添加失败'.encode('utf-8'))
                        print('添加失败')

            elif data[0]=='C': # C代表创建群聊
                data=data[1:]
                data=data.split(' ')
                user_name=data[0]
                group_name=data[1]
                print(user_name,'尝试创建群聊',group_name)
                if database.create_group(user_name, group_name)==True:
                    self.request.sendall('创建成功'.encode('utf-8'))
                    print('创建成功')
                else :
                    self.request.sendall('创建失败'.encode('utf-8'))
                    print('创建失败')

            elif data[0]=='L': # L表示登录
                data=data[1:]
                data=data.split(' ')
                user_name=data[0]
                password=data[1]
                is_success=login.login(user_name, password)
                print(self.client_address,'尝试登录,用户名为：',user_name)
                #self.request.sendall(str(user_id).encode('utf-8'))
                #print(user_id,type(user_id))
                if is_success==True:
                    if user_name in name_list:
                        self.request.sendall('该用户尝试重复登录'.encode('utf-8'))
                        print(self.client_address,'该用户尝试重复登录')
                        continue
                    self.request.sendall('登录成功'.encode('utf-8'))
                    print(self.client_address,'登录成功,用户名为：',user_name)
                    connect_list.append(self.request)
                    name_list.append(user_name)
                    continue
                else:
                    self.request.sendall('登录失败'.encode('utf-8'))
                    print(self.client_address,'登录失败')
                    continue

            elif data[0]=='R': # R表示注册
                data=data[1:]
                data=data.split(' ')
                user_name=data[0]
                password=data[1]
                if login.register(user_name, password)==True:
                    print(self.client_address, '尝试注册,用户名为：',user_name)
                    self.request.sendall('注册成功'.encode('utf-8'))
                else:
                    print(self.client_address, '尝试注册,用户名为：',user_name)
                    self.request.sendall('注册失败'.encode('utf-8'))
            
            elif data[0]=='F': # Friend来get一下朋友和群聊列表
                data=data[1:]   
                data=data.strip()
                user_name=data
                print(user_name,"尝试获取好友列表")
                friend_list=database.get_friend_list(user_name)
                print('读取到列表： ',friend_list)
                friend_list_data=pickle.dumps(friend_list)
                self.request.sendall(friend_list_data)
                print('发送成功')

            elif data[0]=='H': # H代表历史消息
                if data[1]=='P': # P代表Private
                    source_name=data[2:].strip().split(' ')[0]
                    target_name=data[2:].strip().split(' ')[1]
                    print(source_name,'尝试获取',target_name,'的历史消息')
                    history_message=database.get_history_message(source_name, target_name)
                    history_message_data=pickle.dumps(history_message)
                    self.request.sendall(history_message_data)
                    print('发送成功')
                elif data[1]=='G': # G代表Group
                    source_name=data[2:].strip().split(' ')[0]
                    group_name=data[2:].strip().split(' ')[1]
                    print(source_name,'尝试获取',group_name,'的历史消息')
                    history_message=database.get_group_history_message(group_name)
                    history_message_data=pickle.dumps(history_message)
                    self.request.sendall(history_message_data)
                    print('发送成功')

            elif data[0]=='M': # M表示消息
                if data[1]=='G': # G表示群聊 Group
                    source_name=data[2:].strip().split(' ')[0]
                    gourp_name=data[2:].strip().split(' ')[1]
                    data=data[2:].strip().split(' ')[2:]
                    # 把data转换成字符串
                    data=' '.join(data)
                    print(source_name,'尝试发送群聊消息',gourp_name,data)
                    group_member=database.get_group_member(gourp_name)
                    print('群成员列表：',group_member)
                    for i in group_member:
                        if i in name_list:
                            if i!=source_name:
                                connect_list_chat[name_list.index(i)].sendall(('G'+gourp_name+' '+source_name+' '+data).encode('utf-8'))
                    print('发送成功')
                    database.save_group_message(gourp_name, source_name+' '+data)
                if data[1]=='P': # P表示私聊
                    source_name=data[2:].strip().split(' ')[0]
                    target_name=data[2:].strip().split(' ')[1]
                    data=data[2:].strip().split(' ')[2:]
                    # 把data转换成字符串
                    data=' '.join(data)
                    if target_name in name_list:  # 对方要是在线的话
                        print(data,type(data))
                        print(connect_list[name_list.index(target_name)],type(connect_list[name_list.index(target_name)]))
                        print('send success')
                        connect_list_chat[name_list.index(target_name)].sendall(('P'+source_name+' '+data).encode('utf-8'))
                        database.save_message(source_name, target_name, data, 'r')
                        database.save_message(target_name, source_name, data, 's')
                    else: # 对方要是不在线的话
                        print('target not online!')
                        database.save_message(source_name, target_name, data, 'r')
                        database.save_message(target_name, source_name, data, 's')
            
server=socketserver.ThreadingTCPServer(('localhost', 9000), sqServer)
server.serve_forever()