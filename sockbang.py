import socket
import random

def serverget():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = random.randint(1024, 49151)  # Port range from 1024 to 49151
    print(f"Hosting on Port {port}")

    server.bind(('', port))
    
    server.listen(1)
    print("Waiting for a connection...")

    conn, addr = server.accept()

    

    print(f"Connection on {conn} from {addr}")

    conn.sendall(b"SECRETCODE15")
    
    conn.close()

serverget()
