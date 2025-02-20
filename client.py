import socket
from pynput import keyboard
import pyautogui as PAG
import tkinter as tk
import time

class MsgError(Exception):
    pass

def main():
    
    # Initiate Connection Variable Data
    ######client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ######server_ip = input("Enter server IP: ")
    ######port = int(input("Enter server port: "))
    

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

    def flash():
        
        ## Creates a full-screen white flash that smoothly fades to transparent.
        flash_window = tk.Tk()  # Use Tk() instead of Toplevel() to avoid overlay issues
        flash_window.attributes("-fullscreen", True)
        flash_window.attributes("-topmost", True)
        flash_window.configure(bg="white")

        # Remove window decorations (title bar, borders)
        flash_window.overrideredirect(True)
        
        # Enable transparency
        flash_window.attributes("-alpha", 1.0)  # Start fully visible

        ###### Uncomment to extend time screen stays white
        ###flash_window.update()
        ###time.sleep(1)

        fade_steps = 100  # Number of fade steps
        delay = 25  # Time per step in milliseconds

        # Gradually reduce window transparency
        for i in range(fade_steps):
            alpha = (1 - (i / fade_steps)**4) # Logarithmic looking fade.
            flash_window.attributes("-alpha", alpha)  # Set transparency level
            flash_window.update() # Apply change
            time.sleep(delay / 1000)  # Convert ms to seconds

        flash_window.destroy()  # Close flash window after fade-out

    def dclick():
        PAG.click()
        PAG.click()
        PAG.click()

    def on_press(key):
        try:
            if key.char == 'f':
                flash()
            if key.char == 'c':
                dclick()
        except AttributeError:
            pass

    def start_listener():
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        listener.join()

    # Connect and receive_msg()
    try:
        ######client.connect((server_ip, port))
        ######receive_input(start=True)
        ###receive_msg(server_ip, port)
        start_listener()
    except ConnectionRefusedError:
        print("Could not connect. Make sure the server is running and the port is correct.")
    except MsgError as e:
        print(e)
    finally:
        pass######client.close()

if __name__ == '__main__':
    
    main()
