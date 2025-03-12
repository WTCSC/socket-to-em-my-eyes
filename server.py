import socket
import random
import threading
import logging


logging.basicConfig(level=20, 
                    format="%(asctime)s - %(levelname)s - %(message)s", 
                    handlers=[logging.StreamHandler(), logging.FileHandler('app.log')])


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Choose a random port within the allowed range.
    port = random.randint(1024, 11111)
    logging.info(f"Hosting on Port {port}")
    server.bind(('', port))
    
    server.listen(1)
    logging.debug("Waiting for a connection...")
    
    conn, addr = server.accept()
    logging.info(f"Connection accepted from {addr}")
    
    # Send handshake secret code.
    conn.sendall(b"SECRETCODE15")
    
    try:
        while True:
            cmd = input("Enter punishment command an an optional integer delay in seconds (e.g., `flash/click/rand [int]`): ")
            if 'quit' in cmd.lower() or 'exit' in cmd.lower(): # Allow exiting
                break      
            elif ' ' in cmd:
                parts = cmd.split(' ')
                delay = parts[1]
                cmd = parts[0]
                if delay.isdigit():
                    delay = int(delay)      # Send the command with a delay
                    threading.Timer(delay, lambda: conn.sendall(cmd.encode())).start()
                    continue
                else:
                    logging.error('TypeError: Delay must be decimal number')
            
            else:
            # Send the command to the client.
                conn.sendall(cmd.encode())
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        conn.close()
        logging.info("Connection closed.")

if __name__ == '__main__':
    server()
