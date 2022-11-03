# shell/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import docker
import asyncio

# This file is a django channels consumer,
# to connect a websocket with a docker container socket.
# No authentication is currently checked, but can be implemented like:
# https://stackoverflow.com/questions/43392889/how-do-you-authenticate-a-websocket-with-token-authentication-on-django-channels


class ShellConsumer(AsyncWebsocketConsumer):
    socket = ""
    bytes = b""

    # Method handles incoming  websocket connections
    async def connect(self):
        # Create docker api client
        # Hardcoded for prototyping
        client = docker.from_env()
        # Get container
        container = client.containers.get("212d500779af")
        # Spawn shell
        result, socket = container.exec_run(cmd="/bin/bash", stdin=True, tty=True, socket=True)
        # Get the socket object and assign it to consumer
        self.socket = socket._sock
        # Activate none blocking mode (https://docs.python.org/2/library/socket.html#socket.socket.setblocking)
        self.socket.setblocking(0)
        # Accept websocket connecting
        await self.accept()
        # Start Coroutine to pull output from docker container
        asyncio.create_task(self.receiveData())

    async def disconnect(self, close_code):
        #Disconnect websocket
        pass

    # Method handles incoming commands from the frontend
    # Commands are send as bytes, so features like autocomplete etc. will work
    async def receive(self, text_data):
        # Encode commands from frontend into binary data
        self.bytes = text_data.encode('utf-8')
        # Send binary data to docker container
        self.socket.sendall(self.bytes)

    # Method receives Data from the container and sends
    # it to the frontend
    async def receiveData(self):
        # Pull output from container
        # Always listen for output inside the buffer
        while True:
            try:
                # Pull 1Kb of data from docker socket
                data = self.socket.recv(1024)
                # Send binary data to frontend
                await self.send(bytes_data=data)
            except:
                # If no data is present to read, an execption is thrown.
                # Catch the exception and wait for 0.01 Seconds.
                await asyncio.sleep(.01)
                pass


