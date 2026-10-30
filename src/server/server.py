
import asyncio
from websockets.asyncio.server import serve, ServerConnection


async def handler(ws: ServerConnection):
    print("Connected:", ws.remote_address)
    try:
        async for msg in ws:
            print("Message:", msg)
    finally:
        print("Disconnected:", ws.remote_address)

async def main():
    async with serve(handler, "127.0.0.1", 5555):
        print("Listening on port 8765")
        await asyncio.Future()  # run forever

asyncio.run(main())