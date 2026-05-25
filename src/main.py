import asyncio

from prisma import Prisma


async def main():
    db = Prisma()

    await db.connect()
    print("Commands : create, list, quit")

    while True:
        cmd = input("\n> ").strip().lower()

        if cmd == "quit":
            break
        elif cmd == "create":
            email = input("Email : ")
            user = await db.user.create(data={"email": email})
            print(f"Created : {user.id} - {user.email}")
        elif cmd == "list":
            users = await db.user.find_many()
            for u in users:
                print(f"  [{u.id}] - {u.email}")
        else:
            print("Unknown command.")

    await db.disconnect()
    print("Disconnected.")


asyncio.run(main())
