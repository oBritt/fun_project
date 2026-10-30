import asyncio
from websockets.asyncio.client import connect

SERVER = "wss://liger-tops-raccoon.ngrok-free.app"

async def main():
    async with connect(SERVER) as ws:
        print("Connected to server")
        await ws.send("Hello from client")
        async for msg in ws:
            print("Server says:", msg)

asyncio.run(main())