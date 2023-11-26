import websockets
import asyncio

class WebSocket:

    async def start_server(self):
        try:
            async with websockets.serve(self.handle_request, "localhost", 8765):
                print("Server started. Waiting for connections...")
                await asyncio.Future()
        except Exception as e:
            print(f"Server start failed: {e}")

    async def handle_request(self, websocket, path):
        print(f"Received connection request for path: {path}")

        if path == "/endpoint1/":
            await self.handle_endpoint1(websocket)
        else:
            print(f"Unknown path: {path}")
            await websocket.close()

    async def handle_endpoint1(self, websocket):
        print("Handling endpoint /endpoint1/")
        # Aktionen spezifisch für /endpoint1
        async for message in websocket:
            print(f"Received message for /endpoint1: {message}")
            await websocket.send(f"Server received for /endpoint1: {message}")

    # Offline

    async def send_to_xamarin(self, message):
        async with websockets.connect('ws://localhost:8765') as websocket:
            await websocket.send(message)
            print(f"Nachricht '{message}' an den Xamarin-Client gesendet.")

    async def receive_from_xamarin(self):
        async with websockets.connect('ws://localhost:8765') as websocket:
            while True:
                message = await websocket.recv()
                print(f"Nachricht vom Xamarin-Client erhalten: {message}")

                # Hier kannst du die empfangene Nachricht weiter verarbeiten oder entsprechend reagieren

