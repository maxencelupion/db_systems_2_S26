import asyncio
from datetime import datetime

from prisma import Prisma


async def list_members(group):
    if len(group.members) > 0:
        print("Members:")
        for m in group.members:
            print(f"[{m.user.id}] - {m.user.username}, {m.user.email} with role {m.role}")
    else:
        print("No members yet.")

async def remove_member(db: Prisma):
    group_id = int(input("Group ID: "))
    group = await db.group.find_unique(
        where={"id": group_id},
        include={"members": {"include": {"user": True}}}
    )
    await list_members(group)
    user_id = int(input("User ID: "))
    try:
        member = await db.groupjoined.find_unique(
            where={"groupId_userId": {"groupId": group_id, "userId": user_id}}
        )

        if member and member.role == "OWNER":
            print(f"Cannot remove owner from group [{group_id}]")
            return

        await db.groupjoined.delete(
            where={"groupId_userId": {"groupId": group_id, "userId": user_id}}
        )
        print(f"Removed member from group [{group_id}]")
    except Exception as e:
        print(f"Failed to remove member from group [{group_id}]: {e}")


async def add_member(db: Prisma):
    group_id = int(input("Group ID: "))
    user_id = int(input("User ID: "))
    role = input("Role (USER, ADMIN or OWNER): ")
    try:
        await db.group.update(
            where={"id": group_id},
            data={"members": {"create": {"userId": user_id, "role": role, "joinedAt": datetime.now()}}}
        )
        print(f"Added member to group [{group_id}]")
    except Exception as e:
        print(f"Failed to add member to group [{group_id}]: {e}")


async def create_group(db: Prisma):
    name = input("Name : ")
    type = input("Type (CHANNEL or GROUP): ")
    try:
        group = await db.group.create(data={"name": name, "type": type})
        print(f"Created : [{group.id}] - {group.name}, {group.type}")
        return group
    except Exception as e:
        print(f"Failed to create group: {e}")


async def get_groups(db: Prisma):
    groups = await db.group.find_many(
        include={"members": {"include": {"user": True}}}
    )
    return groups

async def group_menu(db: Prisma):

    while True:
        print("[GROUP] Choose a query: create, list, add-member, remove-member or quit")
        cmd = input("\n> ").strip().lower()

        if cmd == "quit":
            return
        elif cmd == "create":
            await create_group(db)
        elif cmd == "list":
            groups = await get_groups(db)
            for g in groups:
                last_msg_info = f"last message at {g.lastMessageAt}" if g.lastMessageAt else "no messages yet"
                print(f"[{g.id}] - {g.name}, {g.type}, {last_msg_info}")
                await list_members(g)
        elif cmd == "add-member":
            await add_member(db)
        elif cmd == "remove-member":
            await remove_member(db)
        else:
            print("Unknown command.")
