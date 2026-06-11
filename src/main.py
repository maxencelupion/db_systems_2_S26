import asyncio

from prisma import Prisma
from user import user_menu
from group import group_menu
from message import message_menu
from join import join_menu


async def main():
    db = Prisma()

    await db.connect()

    while True:
        print("Choose a table: user, message, group, join or quit")
        cmd = input("\n> ").strip().lower()

        if cmd == "quit":
            break
        elif cmd == "user":
            await user_menu(db)
        elif cmd == "message":
            await message_menu(db)
        elif cmd == "group":
            await group_menu(db)
        elif cmd == "join":
            await join_menu(db)
        else:
            print("Unknown command.")

    await db.disconnect()
    print("Disconnected.")


asyncio.run(main())
