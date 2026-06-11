import asyncio
from datetime import datetime
from prisma.enums import Role

from prisma import Prisma

async def list_groupchats(db: Prisma):
    user_id = int(input("user ID: "))
    join = await db.GroupJoined.find_many(
       where={"userId":user_id},
       orderBy={"joinedAt": "desc"}
       )
    if len(join) > 0: 
        print(f"user {user_id} ")
        for j in join:
         print(f"joined group {j.groupId} at {j.joinedAt}")
    else:
      print(f"user [{user_id}] have not join any group yet.")

async def change_role(db: Prisma):
    group_id = int(input("Group ID: "))
    user_id = int(input("User ID: "))
    role = input("Role (USER, ADMIN or OWNER): ")
    if role not in ["USER", "ADMIN", "OWNER"]:
        print("Invalid role.")
        return
    try:
        await db.GroupJoined.update(
            where={"groupId_userId": {
                "groupId": group_id,"userId": user_id}},
            data={"role":role}
            )
        print(f"successfully, changed user {user_id} role into {role} in {group_id}")
    except Exception as e:
        print(f"Failed to change user {user_id} role in {group_id}")

async def OwnersAdmins (db: Prisma):
    group_id = int(input("Group ID: "))
    try:
     groups = await db.GroupJoined.find_many(
        where={
            "groupId": group_id ,
            "OR": [
                { "role": Role.ADMIN  },
                { "role": Role.OWNER  },] }
     )
     return groups
    except Exception as e:
        print(f"Failed to find the group.")

async def Users_Role (db: Prisma):
    group_id = int(input("Group ID: "))
    user_id = int(input("User ID: "))
    try:
     user = await db.GroupJoined.find_unique(
        where={
             "groupId_userId": {
                    "groupId": group_id,
                    "userId": user_id }}
     )
     if user is None:
            print("User is not in this group.")
            return None 
     return user.role
    except Exception as e:
        print(f"Failed to find.")

async def existence_user (db: Prisma):
    group_id = int(input("Group ID: "))
    user_id = int(input("User ID: "))
    user = await db.GroupJoined.find_unique(
        where={
            "groupId_userId": {
                "groupId": group_id,
                "userId": user_id } }
     )
    if user is None:
        print(f"User {user_id} is NOT in group {group_id}")
    else:
        print(f"there is user {user_id} in {group_id} ")

async def join_menu(db: Prisma):

    while True:
        print("[GROUPJOINED] Choose a query: list_groupchats, change_role, owners/admins, users_role, existence_user or quit")
        cmd = input("\n> ").strip().lower()

        if cmd == "quit":
            return
        elif cmd == "list_groupchats":
            await list_groupchats(db)
        elif cmd == "change_role":
            await change_role(db)
        elif cmd == "owners/admins":
            groups = await OwnersAdmins(db)
            if not groups:
              print("No admins/owners found")
            else:
                for g in groups:
                    print(g)
        elif cmd == "users_role":
            role = await Users_Role(db)
            print(role)
        elif cmd == "existence_user":
            await existence_user(db)
        else:
            print("Unknown command.")
