# -*- coding: utf-8 -*-
# 管理数据
import csv
import os
#pandas读取csv中的好友列表，接收user_name，返回好友列表

def get_friend_list(user_name):
    data=[]
    if os.path.exists('./data/friend_list.csv')==False:
        file=open('./data/friend_list.csv','w',encoding='gb18030')
        file.close()
    with open('./data/friend_list.csv','r',encoding='gb18030') as f:
        reader=csv.reader(f)
        for row in reader:
            data.append(row)
    print('读取的好友列表为：')
    print(data)
    for i in range(len(data)):
        if data[i][0]==user_name:
            return data[i][1:]

    '''
    df=pandas.read_csv('./data/friend_list.csv',encoding='utf-8')
    print(df)
    friend_list=df[user_name]
    return friend_list.tolist()
    '''

# 私聊部分
def get_history_message(user_name,friend_name):
    data=[]
    if os.path.exists('./data/history/'+user_name+'.csv')==False:
        file=open('./data/history/'+user_name+'.csv','w',encoding='gb18030')
        file.close()
    with open('./data/history/'+user_name+'.csv','r',encoding='gb18030') as f:
        reader=csv.reader(f)
        for row in reader:
            data.append(row)
    print('读取的历史消息为：')
    print(data)

    if data==[]:
        return []

    for i in range(len(data)):
        if data[i][0]==friend_name:
            return data[i][1:]
    '''
    try: #如果没有历史消息，就创建一个空的csv文件
        df=pandas.read_csv('./data/history/'+user_name+'.csv',encoding='utf-8')
    except:
        df=pandas.DataFrame()
        df.to_csv('./data/history/'+user_name+'.csv',encoding='utf-8')
        df=pandas.read_csv('./data/history/'+user_name+'.csv',encoding='utf-8')

    print(df)
    history_message=df[friend_name]
    return history_message.tolist()
    '''
def save_message(user_name,friend_name,message,flag):  #flag=0表示发送，flag=1表示接收
    # 使用csv函数来读取csv文件
    data=[]
    #如果没有历史消息，就创建一个空的csv文件
    if os.path.exists('./data/history/'+friend_name+'.csv')==False:
        file=open('./data/history/'+friend_name+'.csv','w',encoding='gb18030')
        file.close()
    with open('./data/history/'+friend_name+'.csv','r',encoding='gb18030') as f:
        reader=csv.reader(f)
        for row in reader:
            data.append(row)
    
    is_exist=False
    for i in range(len(data)):
        if data[i][0]==user_name:
            is_exist=True
            data[i].append(flag+message)
            break

    if is_exist==False:
        data.append([user_name,flag+message])

    with open('./data/history/'+friend_name+'.csv','w',encoding='gb18030') as f:
        writer=csv.writer(f)
        writer.writerows(data)

# 群聊部分
def get_group_history_message(group_name): #格式为“发送者 时间 内容”
    data=[]
    if os.path.exists('./data/group_history/'+group_name+'.csv')==False:
        file=open('./data/group_history/'+group_name+'.csv','w',encoding='gb18030')
        file.close()
    with open('./data/group_history/'+group_name+'.csv','r',encoding='gb18030') as f:
        reader=csv.reader(f)
        for row in reader:
            data.append(row)
    print('读取的群聊历史消息为：')
    print(data)
    if not data:
        return []
    return data[0]

def save_group_message(group_name,message): 
    # 使用csv函数来读取csv文件
    data=[]
    #如果没有历史消息，就创建一个空的csv文件
    if os.path.exists('./data/group_history/'+group_name+'.csv')==False:
        file=open('./data/group_history/'+group_name+'.csv','w',encoding='gb18030')
        file.close()
    with open('./data/group_history/'+group_name+'.csv','r',encoding='gb18030') as f:
        reader=csv.reader(f)
        for row in reader:
            data.append(row)
    if not data:
        data.append([message])
    else:
        data[0].append(message)

    with open('./data/group_history/'+group_name+'.csv','w',encoding='gb18030') as f:
        writer=csv.writer(f)
        writer.writerows(data)

def get_group_member(group_name):
    # 所有的群成员信息都存储在group_member.csv中
    data=[]
    if os.path.exists('./data/group_member.csv')==False:
        file=open('./data/group_member.csv','w',encoding='gb18030')
        file.close()
    with open('./data/group_member.csv','r',encoding='gb18030') as f:
        reader=csv.reader(f)
        for row in reader:
            data.append(row)
    print('读取的群成员信息为：')
    print(data)

    for i in range(len(data)):
        if data[i][0]==group_name:
            return data[i][1:]

    return []

def add_friend(user_name,friend_name):
    # 使用csv函数来读取csv文件
    data=[]
    #如果没有朋友列表，就创建一个空的csv文件
    if os.path.exists('./data/friend_list.csv')==False:
        file=open('./data/friend_list.csv','w',encoding='gb18030')
        file.close()
    with open('./data/friend_list.csv','r',encoding='gb18030') as f:
        reader=csv.reader(f)
        for row in reader:
            data.append(row)
    is_exist_friend=-1
    is_exist_user=-1
    # 判断一下要加的用户是否存在
    friend_name='f'+friend_name
    for i in range(len(data)):
        if data[i][0]==friend_name:
            is_exist_friend=i
        if data[i][0]==user_name:
            is_exist_user=i
    file1=open('./data/user.txt', 'r')
    user_list=file1.readlines()
    file1.close()
    flag=False
    for i in range(len(user_list)):
        if user_list[i].split(',')[0]==friend_name[1:]:
            flag=True
            break
    if flag==False:
        return False
    if is_exist_user==-1:
        data.append([user_name,friend_name])
    else:
        data[is_exist_user].append(friend_name)
    data[is_exist_friend].append('f'+user_name)
    with open('./data/friend_list.csv','w',encoding='gb18030') as f:
        writer=csv.writer(f)
        writer.writerows(data)
    return True
    

def add_group(user_name,group_name):
    # 使用csv函数来读取csv文件
    data=[]
    #如果没有群列表，就创建一个空的csv文件
    if os.path.exists('./data/group_member.csv')==False:
        file=open('./data/group_member.csv','w',encoding='gb18030')
        file.close()
    with open('./data/group_member.csv','r',encoding='gb18030') as f:
        reader=csv.reader(f)
        for row in reader:
            data.append(row)
    is_exist=False
    for i in range(len(data)):
        if data[i][0]==group_name:
            is_exist=True
            data[i].append(user_name)
            data1=[]
            if os.path.exists('./data/friend_list.csv')==False:
                file1=open('./data/friend_list.csv','w',encoding='gb18030')
                file1.close()
            with open('./data/friend_list.csv','r',encoding='gb18030') as f:
                reader=csv.reader(f)
                for row in reader:
                    data1.append(row)
            for j in range(len(data1)):
                if data1[j][0]==user_name:
                    data1[j].append('g'+group_name)
                    break
            break
    with open('./data/group_member.csv','w',encoding='gb18030') as f:
        writer=csv.writer(f)
        writer.writerows(data)
    with open('./data/friend_list.csv','w',encoding='gb18030') as f:
        writer=csv.writer(f)
        writer.writerows(data1)
    return is_exist  #如果群不存在，就返回False

def create_group(user_name,group_name):
    # 使用csv函数来读取csv文件
    data=[]
    #如果没有群列表，就创建一个空的csv文件
    if os.path.exists('./data/group_member.csv')==False:
        file=open('./data/group_member.csv','w',encoding='gb18030')
        file.close()
    with open('./data/group_member.csv','r',encoding='gb18030') as f:
        reader=csv.reader(f)
        for row in reader:
            data.append(row)
    is_exist=True
    for i in range(len(data)):
        if data[i][0]==group_name:
            is_exist=False
            break
    if is_exist==True:
        data.append([group_name,user_name])
    with open('./data/group_member.csv','w',encoding='gb18030') as f:
        writer=csv.writer(f)
        writer.writerows(data)

    data1=[]
    if os.path.exists('./data/friend_list.csv')==False:
        file1=open('./data/friend_list.csv','w',encoding='gb18030')
        file1.close()
    with open('./data/friend_list.csv','r',encoding='gb18030') as f:
        reader=csv.reader(f)
        for row in reader:
            data1.append(row)
    for j in range(len(data1)):
        if data1[j][0]==user_name:
            data1[j].append('g'+group_name)
            break
    with open('./data/friend_list.csv','w',encoding='gb18030') as f:
        writer=csv.writer(f)
        writer.writerows(data1)

    return is_exist 
    '''
    try: #如果没有历史消息，就创建一个空的csv文件
        df=pandas.read_csv('./data/history/'+friend_name+'.csv',encoding='utf-8',index_col=0)
    except:
        df=pandas.DataFrame()
        df.to_csv('./data/history/'+friend_name+'.csv',encoding='utf-8')
        df=pandas.read_csv('./data/history/'+friend_name+'.csv',encoding='utf-8',index_col=0)
    # 如果没有用户，就新建一个
    if user_name not in df.columns:
        print("新建用户")
        df[user_name]=pandas.Series()
    if flag=='r':
        print(user_name,flag+message)
        print("hhhhhhh")
        print(pandas.Series(flag+message))
        #df=df.append({user_name:flag+message},ignore_index=True)
        message_list=df[user_name].tolist()
        print("list 1   ",message_list)
        message_list.append(flag+message)
        print("list 2 ",message_list)
        df[user_name]=pandas.Series(message_list)
    else:
        print(user_name)
        df[user_name]=df[user_name].append(pandas.Series(flag+message))
    df.to_csv('./data/history/'+friend_name+'.csv',encoding='utf-8',index=False)
    '''