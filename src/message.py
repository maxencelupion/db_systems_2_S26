from datetime import datetime

from prisma import Prisma


async def list_messages(db: Prisma):
    group_id = int(input("group ID: "))
    messages = await db.message.find_many(
       where={"groupId":group_id})
    if len(messages) > 0:
        for m in messages:
         print(f"[{m.id}] {m.content}")
    else:
      print("no message had been send yet.")


async def delete(db: Prisma):
    message_id = int(input("Message ID: "))
    user_id = int(input("User ID: "))
    message = await db.message.find_unique(
        where={"id": message_id}
    )
    if (message is None):
        print(f"the message does not exist.")
    else:
      try:
        if(message.senderId == user_id):
         await db.message.delete(
             where={"id": message_id}
        )
         print(f"message successfully deleted")
        else:
           print(f"Only the sender can delete the message sent.")
      except Exception as e:
        print(f"Failed to remove message.")


async def reply(db: Prisma):
    message_id = int(input("message ID: "))
    user_id = int(input("User ID: "))
    content = input("message : ")
    try:
        message = await db.message.find_unique(
        where={"id": message_id})
        if message is None:
            print("Message not found.")
            return
        if message.groupId > 0 or message.reciverId >0:
         if message.groupId > 0:
           rep = await db.message.create(
            data={"content": content, "senderId": user_id , "groupId": message.groupId,"replyId":message.id ,"timestamp": datetime.now()})
           print(f"user {user_id} replied to message {message_id} with {rep.content}")
         else:
           rep = await db.message.create(
            data={"content": content, "senderId": user_id , "reciverId": message.senderId,"replyId":message.id ,"timestamp": datetime.now()})
           print(f"user {user_id} replied to message {message_id} with {rep.content}")
        else:
            print(f"Failed to reply the message")
    except Exception as e:
        print(f"Failed to reply the message")


async def send(db: Prisma):
    content = input("message : ")
    sender_id = int(input("sender ID : "))
    group_id = int(input("Group ID or 0: "))
    user_id = int(input("reciver ID or 0: "))
    try:
        sender = await db.user.find_unique(
        where={"id": sender_id })
        sender_role = await db.GroupJoined.find_unique(
        where={"userId": sender_id , "groupId": group_id })
        if(group_id !=0 and user_id ==0):
         group = await db.group.find_unique(
         where={"id": group_id})
         if(group.type == GroupType.CHANNEL and sender_role.role==Role.USER):
            print(f"user can not send message in channel")
            return
         message = await db.message.create(data={"content": content, "senderId": sender_id , "groupId": group_id ,"timestamp": datetime.now()})
         print(f"user {sender.username} send {message.content} in {group.name}")
        elif(group_id ==0 and user_id !=0):
         reciver = await db.user.find_unique(
         where={"id": user_id})
         message = await db.message.create(data={"content": content, "senderId": sender_id , "receiverId": user_id ,"timestamp": datetime.now()})
         print(f"user  {sender.username} send {message.content} to {reciver.username}")
        else:
         print(f"Failed to send the message")
    except Exception as e:
        print(e)
        print(f"Failed to send the message")


async def recent_chat(db: Prisma):
    sender_id = int(input("sender ID : "))
    message = await db.message.find_first(
     where={"senderId": sender_id},
     orderBy={"timestamp": "desc"}
    )
    if message:
     print(message.content)
    else:
     print(f"recently no message has been sent")


async def get_replies(db: Prisma):
   message_id = int(input("message ID: "))
   try:
    message = await db.message.find_first(
        where={"id": message_id}
    )
    replies = await db.message.find_many(
        where={"replyId": message_id}
    )
    print(message.content)
    for r in replies:
     print(r.content)
   except:
    print(f"Failed to find the message")


async def search_by_sender(db: Prisma):
    group_id = int(input("group ID: "))
    user_id = int(input("user ID: "))
    messages = await db.message.find_many(
        where={"groupId": group_id , "senderId": user_id}
    )
    if len(messages) == 0:
        print(f"user did not send message in group.")
    else:
        for m in messages:
            print(m.content)

async def edit_message(db: Prisma):
    text = input("new message : ")
    message_id = int(input("Message ID: "))
    user_id = int(input("User ID: "))
    message = await db.message.find_unique(
        where={"id": message_id}
    )
    if (message is None):
        print(f"the message does not exist.")
    else:
        if(message.senderId == user_id):
         await db.message.update(
            where={"id": message_id},
            data={"content":text}
          )
         print(f"message successfully edited")
        else:
           print(f"Only the sender can edit the message sent.")

async def private_chat(db: Prisma):
    first_id = int(input("first user ID: "))
    second_id = int(input("second user ID: "))
    messages = await db.query_raw(f"CALL private_chat({first_id}, {second_id});")
    for message in messages:
        print(
            f"Message [{message['f0']}] "
            f"from {message['f3']} "
            f"to {message['f4']} "
            f"at {message['f2']}: "
            f"{message['f1']}"
        )

async def message_menu(db: Prisma):

    while True:
        print("[message] Choose a query: list_messages,private_chat, edit_message, delete, reply, search_by_sender, send, recent_chat, get_replies or quit")
        cmd = input("\n> ").strip().lower()

        if cmd == "quit":
            return
        elif cmd == "list_messages":
            await list_messages(db)
        elif cmd == "delete":
            await delete(db)
        elif cmd == "reply":
            await reply(db)
        elif cmd == "send":
            await send(db)
        elif cmd == "recent_chat":
            await recent_chat(db)
        elif cmd == "get_replies":
            await get_replies(db)
        elif cmd == "search_by_sender":
            await search_by_sender(db)
        elif cmd == "edit_message":
            await edit_message(db)
        elif cmd == "private_chat":
            await private_chat(db)
        else:
            print("Unknown command.")
