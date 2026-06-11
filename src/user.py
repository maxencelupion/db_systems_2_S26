from prisma import Prisma

async def list_user(user):
    print(f"[{user.id}] - {user.username}, {user.email}")
    if len(user.groupsJoined) > 0:
        print("Groups joined:")
        for g in user.groupsJoined:
            print(f"[{g.group.id}] - {g.group.name}, {g.group.type}")
    else:
        print("No groups joined yet.")


async def create_user(db: Prisma):
    username = input("Username : ")
    email = input("Email : ")
    try:
        user = await db.user.create(data={"email": email, "username": username})
        print(f"Created : [{user.id}] - {user.username}, {user.email}")
    except Exception as e:
        print(f"Failed to create user: {e}")

async def get_users(db: Prisma):
    users = await db.user.find_many(
        include={"groupsJoined": {"include": {"group": True}}}
    )
    return users

async def user_menu(db: Prisma):
    while True:
        print("[USER] Choose a query: create, list or quit")
        cmd = input("\n> ").strip().lower()

        if cmd == "quit":
            return
        elif cmd == "create":
            await create_user(db)
        elif cmd == "list":
            users = await get_users(db)
            for u in users:
                await list_user(u)
        else:
            print("Unknown command.")
