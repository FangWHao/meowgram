import socketserver
import login
import database
import os
import pandas
import pickle  # 以list的形式使用TCP发送数据
connect_list=[] # 保存连接的客户端
id_list=[] # 保存客户端的id
name_list=[] # 保存客户端的用户名
i=0

group_file_name='./data/group.csv'
'''
group_file=pandas.read_csv(group_file_name)

# group.csv 中第一行是群名字，第二行是群id，第三行之后是群成员的id
group_name_list=group_file.iloc[0].values.tolist()
group_id_list=group_file.iloc[1].values.tolist()
group_member_list=group_file.iloc[2:].values.tolist()
'''


class sqServer(socketserver.BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)

        while True:
            data = self.request.recv(1024)
            if not data:
                print('Client disconnected')
                print('Client address:',self.client_address)
                i=connect_list.index(self.client_address)
                connect_list.pop(i)
                id_list.pop(i)
                name_list.pop(i)
                break

            print('Received', data.decode('utf-8'), 'from', self.client_address)


            # 对数据进行处理
            data=data.decode('utf-8')
            if data[0]=='L': # L表示登录
                data=data[1:]
                data=data.split(' ')
                user_name=data[0]
                password=data[1]
                user_id=login.login(user_name, password)
                print(self.client_address,'尝试登录,用户名为：',user_name)
                self.request.sendall(str(user_id).encode('utf-8'))
                print(user_id,type(user_id))
                if user_id!=False:
                    print(self.client_address,'登录成功,用户名为：',user_name)
                    connect_list.append(self.client_address)
                    name_list.append(user_name)
                    
                    continue
                else:
                    print(self.client_address,'登录失败')
                    continue

            elif data[0]=='R': # R表示注册
                data=data[1:]
                data=data.split(' ')
                user_name=data[0]
                password=data[1]
                login.register(user_name, password)
                print(self.client_address, '尝试注册,用户名为：',user_name)
                self.request.sendall('注册成功'.encode('utf-8'))

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
                source_name=data[1:].strip().split(' ')[0]
                target_name=data[1:].strip().split(' ')[1]
                print(source_name,'尝试获取',target_name,'的历史消息')
                history_message=database.get_history_message(source_name, target_name)
                history_message_data=pickle.dumps(history_message)
                self.request.sendall(history_message_data)
                print('发送成功')

            elif data[0]=='M': # M表示消息
                data=data[1:]
                data=data.split(' ')
                user_id=data[0]
                if data[1]=='G': # G表示群聊 Group
                    group_id=data[2]
                    data=data[3:]
                    for i in range(len(id_list)):
                        if id_list[i] in group_member_list[group_id_list.index(group_id)]:
                            connect_list[i].sendall(data.encode('utf-8'))
                            print('send success')
                
                if data[1]=='P': # P表示私聊 Private
                    user_id=data[2]
                    data=data[3:]
                    if user_id in id_list:
                        index=id_list.index(user_id)
                        connect_list[index].sendall(data.encode('utf-8'))
                        print('send success')

            '''群发消息的template
            for i in connect_list:
                if i==self.request:
                    print("发送成功")
                    continue
                print('send to', i)
                print(type(data))
                data_send="来自"+str(self.client_address)+"的消息："+data.decode('utf-8')+"\r\n"
                try:
                    i.sendall(data_send.encode('utf-8'))
                    print('send success')
                except:
                    print('send fail')
                    connect_list.remove(i)
                    id_list.remove(i)
                    name_list.remove(i)
                    print('removed', i)
                    continue
            #self.request.sendall(data)
            '''
server=socketserver.ThreadingTCPServer(('localhost', 9000), sqServer)
server.serve_forever()