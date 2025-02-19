import socket
import random


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = random.randint(1024, 49151)
print(f"Hosting on Port {port}")

server.bind('', port)