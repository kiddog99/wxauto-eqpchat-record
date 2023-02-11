# wxauto robot


from wxauto import *
from bot import Eqp_db_bot
import time

# 获取当前微信客户端
wx = WeChat()

#test
#file1 = 'D:\正儿八经的工作文件\【20220104】信息化系统建设\BaiduNetdiskWorkspace\chatGPT\wechat-auto\export\Eqp_export.csv'
#wx.Search('加班狗听大佬们安排')
#wx.ChatWith(who)  # 打开`文件传输助手`聊天窗口
#wx.SendFiles_test([file1,])  # 向`文件传输助手`发送上述三个文件
# 注：为保证发送文件稳定性，首次发送文件可能花费时间较长，后续调用会缩短发送时间


#创建机器人
bot = Eqp_db_bot.bot()

#跳转到Eqp群
wx.Search('加班狗听大佬们安排')
last_code = wx.GetLastMessage[-1]
print('last_code is :', last_code)
#last_code = '4285348243406'
fix_word = '@kiddog'
send_file_word = 'kiddog发送采集文件'
# 持续获取Eqp群的信息
while 1:
    group_msg = wx.GetAllMessage
    if group_msg[-1][-1] != last_code:
        group_msg_rev = group_msg[::-1]
        for msg in group_msg_rev:
            if msg[-1] != last_code:
                print(msg)
                if msg[1].startswith(fix_word):
                    print(msg[0], 'gogogo')
                    query = msg[1].replace(fix_word, '').strip()
                    re = bot.put_in_db_from_group(query)
                    if re == '404':
                        reply = '录入错误，请检查您输入的信息格式是否正确'
                        wx.SendMsg(reply)
                    else:
                        reply = msg[1]+'''
                        
                        ****信息收集成功，采集编号为''' + re
                        WxUtils.SetClipboard(reply)
                        wx.ChatWith('加班狗听大佬们安排')
                        wx.SendClipboard()
                if msg[1].startswith(send_file_word):
                    re = bot.read_db()
                    print(re)
                    if re == '404':
                        reply = '数据库读取错误'
                        wx.SendMsg(reply)
                    else:
                        wx.ChatWith('加班狗听大佬们安排')
                        wx.SendFiles_test([re,])
                        time.sleep(5)
            else:
                break
        print('break********************')
        last_code = wx.GetAllMessage[-1][-1]
        print('last_code rev:', last_code)
    time.sleep(5)