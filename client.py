import socket

class MsgError(Exception):
    pass

def main():
    
    # Initiate Connection Variable Data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("Enter server IP: ")
    port = int(input("Enter server port: "))
    

    def receive_input(start=False):
        while start == True:
            if "Key Input" == 'f':
                pass###Flashbang

     #  Get the message from the server
    def receive_msg(server_ip, port):
        message = client.recv(1024).decode("utf-8")
        if not message:
            raise MsgError("Message is empty")
        elif message == 'SECRETCODE15':
            receive_input(start=True)
        else:
            print(f"Server says: {message}")

        

    # Connect and receive_msg()
    try:
        
        client.connect((server_ip, port))
        receive_msg(server_ip, port)
    except ConnectionRefusedError:
        print("Could not connect. Make sure the server is running and the port is correct.")
    except MsgError as e:
        print(e)
    finally:
        client.close()

if __name__ == '__main__':
    
    main()
