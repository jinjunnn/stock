# import telethon
# from telethon import TelegramClient
# from telethon import Button
# from telethon.tl.functions.messages import AddChatUserRequest # 邀请好友加入Group
# from telethon.tl.functions.channels import InviteToChannelRequest #邀请用户加入Channel
# from telethon.tl.types import InputPhoneContact # 构建Contact
# from telethon.tl.functions.contacts import ImportContactsRequest#添加到 Contact 
# from telethon.tl.functions.contacts import GetContactsRequest# 获取联系人
from telethon.tl.functions.contacts import DeleteContactsRequest# 获取联系人

# from telethon.tl.functions.channels import JoinChannelRequest#添加群聊
# from telethon.tl.functions.users import GetFullUserRequest#获得个人的相信信息
# import record
name = 'anon'
api_id = 8149287
api_hash = '955176e7c610c3ad95bd018eae169339'

from telethon.sync import TelegramClient
from telethon import functions, types

with TelegramClient(name, api_id, api_hash) as client:
    result = client(functions.contacts.GetContactsRequest(
        hash=0
    ))
    for user in result.users:
        if user.status == None:
            print(user.id,user.status)
            client(functions.contacts.DeleteContactsRequest(
                id=[user.id]
            ))


# Use your own values from my.telegram.org

# client = TelegramClient('anon', api_id, api_hash)
# contacts = client(GetContactsRequest(hash=0))
# print(contacts)




# 遍历所有聊天对话
async def iter_dialogs():
    async for dialog in client.iter_dialogs():
        
        if isinstance(dialog.entity,telethon.tl.types.User):
          print('user')
          # 保存user
          # record.write_chats(dialog.entity.id,dialog.entity.title,dialog.entity.username,dialog.entity.participants_count,'User')
        elif isinstance(dialog.entity,telethon.tl.types.Channel):
          print(dialog.id,dialog.entity.megagroup,dialog.entity.title)
          # 保存channel消息
          if dialog.entity.megagroup==True:
            # record.write_chats(dialog.entity.id,dialog.entity.title,dialog.entity.username,dialog.entity.participants_count,'Channel')
            await get_user_in_chatroom(dialog.entity.id)
        elif isinstance(dialog.entity,telethon.tl.types.Chat):
          print('chat')
          # 保存群消息
          # record.write_chats(dialog.entity.id,dialog.entity.title,dialog.entity.username,dialog.entity.participants_count,'Chat')
          # await get_user_in_chatroom(dialog.entity.id)
          await get_user_in_chatroom(dialog.id)

#通过群id获得群消息
async def get_chatroom_info(chatroom_id):
    chatroom_info = await client.get_entity(chatroom_id)
    print(chatroom_info.stringify())

#这段代码是通过id获得群成员的信息，获得
async def get_user_in_chatroom(chatroom_id):
    async for user in client.iter_participants(chatroom_id):
        try:
          if user.username != None:
            full = await client(GetFullUserRequest(user.id))
            bio = full.about
            record.write_user(user.id,user.username,user.first_name,user.last_name,bio)
        except:
          print(1234)




#这段代码是通过电话号码添加用户为好友,phone必填，first_name必填，last_name选填
# contact = InputPhoneContact(client_id=0, phone="+8613924596034",first_name="福田 -科学馆- 梦婷 (超好fw)",last_name="")
async def add_contact(phone,first_name,last_name):
    contact = InputPhoneContact(client_id=0, phone=phone,first_name=first_name,last_name=last_name)
    result = await client(ImportContactsRequest(contacts=[contact]))


#自己加入群组，当前好像只能进入聊天群组
# endpoint = 'https://t.me/tonghua666'
# endpoint = 'https://t.me/TG6198'
async def join_group(endpoint):
    results = await client(JoinChannelRequest(endpoint))
    print(results.stringify())

#邀请好友进入频道
async def invite_user_to_channel(channel_id,uid):
    user = await client.get_entity(uid)
    r = await client(InviteToChannelRequest(channel_id,[user]))
    print(r.stringify())

#邀请好友进入群聊
async def invite_user_to_group(group_id,uid):
    user = await client.get_entity(uid)
    r = await client(AddChatUserRequest(group_id,user,fwd_limit=10))

#发送消息
async def send_message(chat_id,message):
    msg = await client.send_message(chat_id,message) 
    print(msg.raw_text)

#发送文件
async def send_file(chat_id,message):
    msg = await client.send_file(chat_id,message)

#保存有效地消息
async def save_message(chat_id):
    async for message in client.iter_messages(chat_id):
        print(message.id, message.text)
        print(message.stringify())
        return
        if message.photo:
            # path = await message.download_media()
            # print('File saved to', path)  # printed after download is done
            pass 

async def main():
    # Getting information about yourself
    # me = await client.get_me()
    # print(me.stringify())
    # await iter_all_users_in_dialogs()
    #1228203377==深广少妇宫
    # print(12345)
    # await get_chatroom_info(779532121)
    # await get_user_in_chatroom(779532121)
    await iter_dialogs()
    # markdown 发送消息
    # await client.send_message('me', '!(http://static.runoob.com/images/runoob-logo.png)可视电话！(http://static.runoob.com/images/runoob-logo.png)福克斯SDK粉红色快递费')
 


    # await client.send_message('me', 'Hello, **world**!', parse_mode='md')

    # await client.send_message('me', 'Hello, <i>world</i>!', parse_mode='html')

    # # If you logged in as a bot account, you can send buttons
    # from telethon import events, Button

    # @client.on(events.CallbackQuery)
    # async def callback(event):
    #     await event.edit('Thank you for clicking {}!'.format(event.data))

    # # Single inline button
    # await client.send_message('me', 'A single button, with "clk1" as data',
    #                           buttons=Button.inline('Click me', b'clk1'))

    # # Matrix of inline buttons
    # await client.send_message('me', 'Pick one from this grid', buttons=[
    #     [Button.inline('Left'), Button.inline('Right')],
    #     [Button.url('Check this site!', 'https://example.com')]
    # ])

    # # Reply keyboard
    # await client.send_message('me', 'Welcome', buttons=[
    #     Button.text('Thanks!', resize=True, single_use=True),
    #     Button.request_phone('Send phone'),
    #     Button.request_location('Send location')
    # ])

    # # Forcing replies or clearing buttons.
    # await client.send_message('me', 'Reply to me', buttons=Button.force_reply())
    # await client.send_message('me', 'Bye Keyboard!', buttons=Button.clear())

    # # Scheduling a message to be sent after 5 minutes
    # from datetime import timedelta
    # await client.send_message('me', 'Hi, future!', schedule=timedelta(minutes=5))


# with client:
#     client.loop.run_until_complete(main())


# 这个是另一个文件夹的代码

# import os, sys
# import csv
# import leancloud
# from leancloud import cloud
# import requests
# import re

# leancloud.init("ELXEVn8IoKWzNVU52gmYKnn6-gzGzoHsz", master_key="kYWSFq2AwQyBhujn5oIBo64n")

# # 打开硬盘
# fd = os.open("user.csv",os.O_RDWR|os.O_CREAT)


# def search_bio(content):
#     url = None
#     username = None
#     if re.search('https://t.me/', content) is not None:
#         #用户的地址里面包含链接，需要做什么呢
#         url = re.findall('https://t.me/[a-zA-Z0-9_]*',content)[0]
#     if re.search('@[a-zA-Z0-9_]{6,20}', content) is not None:
#         username = re.findall('@[a-zA-Z0-9_]*',content)[0]
#     return(url,username)

# def write_chats(id,title,username,participants_count,chat_type):
#     print(id,title,username,participants_count)
#     # cloud.run('write_chats',id=id,title=title,username=username,participants_count=participants_count,chat_type=chat_type)

# def write_contacts(contacts):
#     cloud.run('write_contacts',contacts=contacts)
#     return

# def write_user(_id,u_name,f_name,l_name,bio):
#     result = search_bio(bio)
#     csv_writer = csv.writer(fd)
#     csv_writer.writerow(_id,u_name,f_name,l_name,result[1],result[0],bio)
#     csv_writer.save()

# # def put_row(_id,u_name,f_name,l_name,username,url,bio):
# #     primary_key = [('uid',_id),('username',u_name)]
# #     attribute_columns = [('firstName',f_name), ('lastName',l_name), ('userName',username), ('url',url), ('bio',bio)]
# #     row = Row(primary_key, attribute_columns)
# #     condition = Condition(RowExistenceExpectation.EXPECT_NOT_EXIST) 
# #     consumed, return_row = client.put_row(table_name, row)
# #     print ('Write succeed, consume %s write cu.' % consumed.write)








# import telethon
# from telethon import TelegramClient
# from telethon import Button
# from telethon.tl.functions.messages import AddChatUserRequest # 邀请好友加入Group
# from telethon.tl.functions.channels import InviteToChannelRequest #邀请用户加入Channel
# from telethon.tl.types import InputPhoneContact # 构建Contact
# from telethon.tl.functions.contacts import ImportContactsRequest#添加到 Contact 
# from telethon.tl.functions.channels import JoinChannelRequest#添加群聊
# from telethon.tl.functions.users import GetFullUserRequest#获得个人的相信信息
# from telethon.utils import pack_bot_file_id,resolve_bot_file_id
# # import record


# # Use your own values from my.telegram.org
# api_id = 8149287
# api_hash = '955176e7c610c3ad95bd018eae169339'
# client = TelegramClient('anon', api_id, api_hash)








# # 遍历所有聊天对话
# async def iter_dialogs():
#     async for dialog in client.iter_dialogs():
#         if isinstance(dialog.entity,telethon.tl.types.User):
#           print(dialog.entity.id,dialog.entity.username)
#           pass
        
#         #检查这个是不是一个频道
#         elif isinstance(dialog.entity,telethon.tl.types.Channel):
#           print(dialog.id,dialog.entity.id,dialog.entity.title,dialog.entity.username,dialog.entity.participants_count)
#           if dialog.entity.megagroup==True:
#             pass

#         #这是一个小的group，因为大的group是channel
#         elif isinstance(dialog.entity,telethon.tl.types.Chat):
#           pass

# #通过群id获得群信息
# async def get_chatroom_info(chatroom_id):
#     chatroom_info = await client.get_entity(chatroom_id)
#     print(chatroom_info.stringify())


# #这段代码是通过id获得群成员的信息，获得
# async def get_user_in_chatroom(chatroom_id):
#     async for user in client.iter_participants(chatroom_id):
#         try:
#           if user.username != None:
#             full = await client(GetFullUserRequest(user.id))
#             bio = full.about
#             record.write_user(user.id,user.username,user.first_name,user.last_name,bio)
#         except:
#           print('pass')


# #这段代码是通过电话号码添加用户为好友,phone必填，first_name必填，last_name选填
# # contact = InputPhoneContact(client_id=0, phone="+8613924596034",first_name="福田 -科学馆- 梦婷 (超好fw)",last_name="")
# async def add_contact(phone,first_name,last_name):
#     contact = InputPhoneContact(client_id=0, phone=phone,first_name=first_name,last_name=last_name)
#     result = await client(ImportContactsRequest(contacts=[contact]))


# #自己加入群组，当前好像只能进入聊天群组
# # endpoint = 'https://t.me/tonghua666'
# # endpoint = 'https://t.me/TG6198'
# async def join_group(endpoint):
#     results = await client(JoinChannelRequest(endpoint))
#     print(results.stringify())

# #邀请好友进入频道
# async def invite_user_to_channel(channel_id,uid):
#     user = await client.get_entity(uid)
#     r = await client(InviteToChannelRequest(channel_id,[user]))
#     print(r.stringify())

# #邀请好友进入群聊
# async def invite_user_to_group(group_id,uid):
#     user = await client.get_entity(uid)
#     r = await client(AddChatUserRequest(group_id,user,fwd_limit=10))

# #发送消息
# async def send_message(chat_id,message):
#     msg = await client.send_message(chat_id,message) 
#     print(msg.raw_text)

# #发送图文
# # image可以是多张，如果是多张只能够上传本地文件
# async def send_file(chat_id,image,caption):
#     msg = await client.send_file(chat_id,image,caption)


# #保存有效地消息
# async def iter_message(chat_id):
#     async for message in client.iter_messages(chat_id):
#         # print(message.stringify())
#         if message.photo:
#             # path = await message.download_media()
#             # print('File saved to', path) 
#             # result = await message.forward_to('me')

#             # 这段代码是根据file_id上传图片
#             # file_id = pack_bot_file_id(message.photo)
#             # print('photo id',file_id)  # printed after download is done
#             pass 
#         else:
#           try:
#               print(message.from_id.user_id)
#           except AttributeError as e:
#               pass
    

# async def main():
#     # Getting information about yourself
#     # me = await client.get_me()
#     # print(me.stringify())
#     #1228203377==深广少妇宫
#     # await iter_dialogs()
#     # 这个是保存消息内容
#     # await save_message(1171231402)
#     # markdown 发送消息
#     # await client.send_message('me', '!(http://static.runoob.com/images/runoob-logo.png)可视电话！(http://static.runoob.com/images/runoob-logo.png)福克斯SDK粉红色快递费')
#     # await client.send_message('me', 'Hello, **world**!', parse_mode='md')

#     # 记录dialogs 中的用户
#     # await get_user_in_chatroom(1541642830)

#     #遍历群消息
#     # await iter_message(1541642830)# 老师小群
#     await iter_message(1578373148)# 大群
#     # await iter_dialogs()
#     # await client.send_message('me', 'Hello, <i>world</i>!', parse_mode='html')

#     # # If you logged in as a bot account, you can send buttons
#     # from telethon import events, Button

#     # @client.on(events.CallbackQuery)
#     # async def callback(event):
#     #     await event.edit('Thank you for clicking {}!'.format(event.data))

#     # # Single inline button
#     # await client.send_message('me', 'A single button, with "clk1" as data',
#     #                           buttons=Button.inline('Click me', b'clk1'))




# with client:
#     client.loop.run_until_complete(main())