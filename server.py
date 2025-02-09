# import asyncio
# import websockets
# import json

# async def websocket_handler(websocket, path):
#     print("WebSocket connected!")
#     try:
#         while True:
#             message = await websocket.recv()
#             try:
#                 data = json.loads(message)  # Ensure it's valid JSON
#                 print(f"Received JSON: {data}")
#             except json.JSONDecodeError:
#                 print(f"Received invalid JSON: {message}")

#             response = {"status": "ok", "message": "Message received"}
#             await websocket.send(json.dumps(response))

#     except websockets.exceptions.ConnectionClosed:
#         print("WebSocket disconnected")


# # Start WebSocket Server
# async def start_server():
#     server = await websockets.serve(websocket_handler, "localhost", 8765)
#     print("WebSocket Server running on ws://localhost:8765")
#     await server.wait_closed()

# # Run Server
# if __name__ == "__main__":
#     asyncio.run(start_server())
import asyncio
import websockets
import json

# Set to store connected clients
connected_clients = set()

async def websocket_handler(websocket):
    # Register the client
    connected_clients.add(websocket)
    print("WebSocket connected!")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received JSON: {data}")
            except json.JSONDecodeError:
                print(f"Received invalid JSON: {message}")
                continue

            # Broadcast the received message to all connected clients
            broadcast_message = json.dumps(data)
            for client in connected_clients:
                try:
                    await client.send(broadcast_message)
                except Exception as e:
                    print(f"Error sending message to client: {e}")
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket disconnected")
    finally:
        connected_clients.remove(websocket)

# Start WebSocket Server
async def start_server():
    server = await websockets.serve(websocket_handler, "localhost", 8765)
    print("WebSocket Server running on ws://localhost:8765")
    await server.wait_closed()

# Run Server
if __name__ == "__main__":
    asyncio.run(start_server())
