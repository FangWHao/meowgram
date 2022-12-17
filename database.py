# 管理数据
import pandas
#pandas读取csv中的好友列表，接收user_name，返回好友列表

def get_friend_list(user_name):
    df=pandas.read_csv('./data/friend_list.csv',encoding='utf-8')
    print(df)
    friend_list=df[user_name]
    return friend_list.tolist()

def get_history_message(user_name,friend_name):

    try: #如果没有历史消息，就创建一个空的csv文件
        df=pandas.read_csv('./data/history/'+user_name+'.csv',encoding='utf-8')
    except:
        df=pandas.DataFrame()
        df.to_csv('./data/history/'+user_name+'.csv',encoding='utf-8')
        df=pandas.read_csv('./data/history/'+user_name+'.csv',encoding='utf-8')

    print(df)
    history_message=df[friend_name]
    return history_message.tolist()