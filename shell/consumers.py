import asyncio
import socket

import docker
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings


class ShellConsumer(AsyncJsonWebsocketConsumer):
    socket = None
    docker_listener = None

    async def connect(self):
        # Create docker api client
        client = docker.from_env()

        # Get the container. Please ensure the container ID is correct
        container = client.containers.get(settings.KALI_CONTAINER_ID)

        # Spawn shell
        exec_instance = container.exec_run(cmd="/bin/bash", stdin=True, tty=True, socket=True)
        self.socket: socket.socket = exec_instance.output._sock

        # Set the socket to non-blocking mode
        self.socket.setblocking(False)

        await self.accept()

        try:
            # Create a task that listens to the output of the docker container and sends it to the frontend via the
            # WebSocket connection
            self.docker_listener = asyncio.create_task(self._container_listen())
        except Exception as e:
            await self.close()
            raise e

    async def disconnect(self, close_code):
        # Clean up (close socket, etc.) when WebSocket disconnects

        if self.docker_listener is not None:
            # Stop listening to the output of the docker container
            self.docker_listener.cancel()

        if self.socket is not None:
            # Close the docker container socket
            self.socket.close()

    async def receive_json(self, content, **kwargs):
        # Get the command that the user sent
        command = content.get("message")

        if command:
            # Append newline to execute the command in the shell
            command_with_newline = command + '\n'
            # Send the command to the Docker container's shell
            self.socket.sendall(command_with_newline.encode('utf-8'))

    async def _container_listen(self):
        """
        This function listens for output of the docker container and sends it to the websocket client (i.e. the
        frontend).
        """
        while True:
            try:
                data = self.socket.recv(1024)
                if data:
                    # Send data to the WebSocket client
                    await self.send(text_data=f'\n{data.decode()}')
            except BlockingIOError:
                # Wait briefly before trying to read again
                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                # When the task should be cancelled (i.e. the websocket connection should be closed), break the loop
                break
