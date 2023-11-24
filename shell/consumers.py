import json
import asyncio
import docker
from channels.generic.websocket import AsyncWebsocketConsumer


class ShellConsumer(AsyncWebsocketConsumer):
    socket = None

    async def connect(self):
        await self.accept()
        try:
            # Create docker api client
            client = docker.from_env()

            # Get container - ensure the container ID is correct
            container = client.containers.get("ee4e4821b163")

            # Spawn shell
            exec_instance = container.exec_run(cmd="/bin/bash", stdin=True, tty=True, socket=True)
            self.socket = exec_instance.output._sock

            # Set the socket to non-blocking mode
            self.socket.setblocking(0)

            # Start Coroutine to pull output from docker container
            asyncio.create_task(self.receive_data())
        except Exception as e:
            print(f"An error occurred: {e}")
            await self.close()

    async def disconnect(self, close_code):
        # Clean up (close socket, etc.) when WebSocket disconnects
        if self.socket is not None:
            self.socket.close()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return

        print(f"Received data: {text_data}")

        try:
            command_data = json.loads(text_data)
            command = command_data.get("message")

            if command:
                # Append newline to execute the command in the shell
                command_with_newline = command + '\n'
                # Send the command to the Docker container's shell
                self.socket.sendall(command_with_newline.encode('utf-8'))
        except json.JSONDecodeError:
            print("Received non-JSON data")

    async def receive_data(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if data:
                    # Send data to the WebSocket client
                    await self.send(text_data=data.decode())
            except BlockingIOError:
                # Wait briefly before trying to read again
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"An error occurred while receiving data: {e}")
                break