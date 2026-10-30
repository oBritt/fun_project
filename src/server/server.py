
import asyncio
from websockets.asyncio.server import serve, ServerConnection
from src.core.commands import (
    Command,
    commands_dict,
    IdentifyCommand
)

import json

class Client:
    def __init__(self, client_id: int, ws: ServerConnection):
        self.id: int = client_id
        self.ws: ServerConnection = ws
        self.name = ""


    def message_received(self, msg: str):
        pass


class Server:

    def __init__(self):
        self.id = 1
        self.connected_users: list[Client] = []
        self.id_asked = None


    def remove_client_with_id(self, client_id) -> None:
        self.connected_users = [c for c in self.connected_users if c.id != client_id]

    async def handler(self, ws: ServerConnection) -> None:
        client = Client(self.id, ws)
        self.connected_users.append(client)
        real_ip = ws.request.headers.get("X-Forwarded-For", ws.remote_address)
        print(f"\n[+] Client {self.id} connected ({real_ip})")
        self.id += 1

        msg = IdentifyCommand.to_json([])
        await ws.send(msg)

        try:
            async for msg in ws:
                try:
                    data = json.loads(msg)
                except json.JSONDecodeError:
                    print(f"[Client] Received non-JSON message: {msg}")
                    continue

                if data['status'] == 'error':

                  continue

                if data['action'] == 'identify':
                    client.name = data['result']
                else:
                    print(data['result'])

        except Exception as e:
            print(f"\n[!] Error with client {client.id}: {e}")
        finally:
            self.remove_client_with_id(client.id)
            print(f"\n[-] Client {client.id} disconnected")


    async def execute(self, cls: Command, args: list[str]):
        if cls.is_server_side():
            await self.execute_server(cls, args)
        else:
            await self.execute_client(cls, args)


    async def execute_server(self, cls: Command, args: list[str]):
        result = await cls.execute(args, server=self)
        if result is not None:
            print(result)

    async def execute_client(self, cls: Command, args: list[str]):
        if not self.id_asked:
            print("[!] No client selected. Use 'select <client_id>' first.")
            return

        matching_clients = [c for c in self.connected_users if c.id == self.id_asked]
        if not matching_clients:
            print(f"[!] Client ID {self.id_asked} is no longer connected.")
            return
        msg = cls.to_json(args)
        client = [c for c in self.connected_users if c.id == self.id_asked][0]
        await client.ws.send(msg)


    async def console(self):

        print("Type 'help' for a list of commands.")
        while True:
            try:
                line = await asyncio.to_thread(input, "> ")
                parts = line.strip().split()
                if not parts:
                    continue

                name, args = parts[0], parts[1:]

                cls = commands_dict.get(name)
                if cls is None:
                    print(f"Unknown command: {name}. Type 'help' for a list.")
                    continue

                if not cls.validate_args(args):
                    print()
                    continue

                await self.execute(cls, args)



            except Exception as e:
                print(f"[!] Console error: {e}")


    def start(self) -> None:
        async def serving() -> None:
            async with serve(self.handler, "127.0.0.1", 5555):
                await self.console()

        asyncio.run(serving())



def _main():
    s = Server()
    s.start()

if __name__ == "__main__":
    _main()
