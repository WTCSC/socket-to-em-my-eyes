import threading
import queue
from pynput import keyboard
import pyautogui as PAG
import tkinter as tk
import time
import sys
import subprocess
import random
import webbrowser
import logging
import argparse
import socket

# Allow for easy changing of log levels
parser = argparse.ArgumentParser(description="Client for remote punishments")
parser.add_argument('--log', type=str, default='WARNING', 
                    help="Choose logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL")
args = parser.parse_args()
level = args.log.upper()

# Set up logging
logging.basicConfig(level=level, 
                    format="%(asctime)s - %(levelname)s - %(message)s", 
                    handlers=[logging.StreamHandler(), logging.FileHandler('app.log')])

# Create MsgError
class MsgError(Exception):
    pass

# Create a global thread-safe command queue.
command_queue = queue.Queue()

# Deploys CS:GO flashbang on press 'f'
def flash():
    try: 
        # Create a Toplevel window attached to the main tkinter root.
        window = tk.Toplevel()
        window.attributes("-fullscreen", True)
        window.attributes("-topmost", True)
        window.configure(bg="white")
        window.overrideredirect(True)
        window.attributes("-alpha", 1.0)

        window.update()
        logging.debug('Flashbang out!')
        time.sleep(0.5)  # Let it display briefly

        fade_steps = 100  # Number of fade steps
        delay = 30        # Time (ms) between steps

        # Fade out flash
        for i in range(fade_steps):
            alpha = (1 - (i / fade_steps)**4)
            window.attributes("-alpha", alpha)
            window.update()
            time.sleep(delay / 1000)
            
        logging.info("Successfully deployed flashbang")
    except Exception as e:
        logging.error(e)
    finally:
        if window:
            window.destroy()

# Triple click on press 'c'
def tclick():
    try:
        PAG.click()
        logging.debug('Click')
        PAG.click()
        logging.debug('Click')
        PAG.click()
        logging.debug('Click')
        logging.info('Successfully triple clicked')
    except Exception as e:
        logging.error(e)

# Open a random distracting site on press 'backspace'
def rand_site():
    urls = [    
        "https://www.omfgdogs.com/",
        "https://pointerpointer.com/",
        "https://heeeeeeeey.com/",
        "https://hooooooooo.com/",
        "https://thiswebsitewillselfdestruct.com/",
        "https://www.sanger.dk/",
        "https://www.fallingfalling.com/",
        "https://alwaysjudgeabookbyitscover.com/",
        "https://cant-not-tweet-this.com/",
        "https://www.rainymood.com/",
        "https://www.michaelbach.de/ot/",
        "https://crouton.net/",
        "https://hackertyper.com/",
        "https://cat-bounce.com/",
        "https://theuselessweb.com/",
        "https://isitchristmas.com/",
        "https://longdogechallenge.com/",
        "https://inspirobot.me/",
        "https://clickclickclick.click/",
        "https://trypap.com/",
        "https://corndog.io/",
        "https://tencents.info/",
        "https://ncase.me/trust/",
        "https://neal.fun/",
        "https://boredbutton.com",
        "https://boredbutton.com/random",
        "https://clicktheredbutton.com",
        "https://theuselessweb.com"
    ]

    url = random.choice(urls)

        #open the chosen url in a new tab
    try:
        webbrowser.open_new_tab(url)    # Attempt to use 'default' browser
        logging.info(f"Opened URL in default browser: {url}") 
    except Exception as e:
        logging.warning(f"Failed to open default browser: {e}")
        logging.info("Trying to open in Google Chrome...")
        if sys.platform.startswith("win"):          #else detect browser and
            chrome_cmd = "start chrome"             #grab the command for chrome
        elif sys.platform.startswith("darwin"):
            chrome_cmd = "open -a 'Google Chrome'"
        elif sys.platform.startswith("linux"):
            chrome_cmd = "google-chrome"
        else:
            raise RuntimeError("Unsupported platform. Cannot open URL.")
        try:        
            subprocess.Popen(f"{chrome_cmd} {url}", shell=True,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
            logging.info(f"Opened URL in Google Chrome: {url}")
        except Exception as e:
            logging.error(e)

# Push commands into the queue instead of calling functions directly
def receive_input(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            if key.char.lower() == 'f':
                command_queue.put("flash")
            elif key.char.lower() == 'c':
                command_queue.put("click")
        else:
            if key == keyboard.Key.backspace:
                command_queue.put("rand")
            elif key == keyboard.Key.pause:  # When Pause is pressed, quit.
                logging.debug('Exiting gracefully via keyboard...')
                command_queue.put("quit")
                return False  # Stops the keyboard listener.
    except Exception as e:
        logging.error(e)

# Start the keyboard listener in its own thread.
def start_listener():
    try:
        with keyboard.Listener(on_press=receive_input) as listener:
            listener.join()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.critical(f"Keyboard listener error: {e}")

# Reads commands from the server and adds them to the queue
def listen_server(client):
    while True:
        try:
            data = client.recv(1024)
            if not data:
                logging.info("Server closed connection.")
                command_queue.put("quit")
                break
            msg = data.decode("utf-8").strip()
            logging.info(f"Received command: {msg}")
            if msg == "flash":
                command_queue.put("flash")
            elif msg == "click":
                command_queue.put("click")
            elif msg == "rand":
                command_queue.put("rand")
            elif msg == "quit":
                command_queue.put("quit")
                break
            else:
                logging.info(f"Unknown command received: {msg}")
        except Exception as e:
            logging.error(e)
            command_queue.put("quit")
            break

def main():

    # Initiate connection variables
    server_ip = input("Enter server IP: ")
    port = int(input("Enter server port: "))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:    # Attempt to connect to the server
        client.connect((server_ip, port))
        message = client.recv(1024).decode("utf-8").strip()
    
        if not message:
            raise MsgError("Message is empty")
        elif message != 'SECRETCODE15':
            logging.critical("Handshake failed. Exiting...")
            client.close()
            return
        logging.info("Handshake successful.")
        
        # Start the server listener thread
        server_thread = threading.Thread(target=listen_server, args=(client,), daemon=True)
        server_thread.start()
        
        # Start the keyboard listener thread
        keyboard_thread = threading.Thread(target=start_listener, daemon=True)
        keyboard_thread.start()
        
        # Create a hidden tkinter root to run the event loop
        root = tk.Tk()
        root.withdraw()
        
        # Process the queue of commands
        def process_commands():
            while not command_queue.empty():
                cmd = command_queue.get()
                if cmd == "flash":
                    flash()
                elif cmd == "click":
                    tclick()
                elif cmd == "rand":
                    rand_site()
                elif cmd == "quit":
                    logging.info("Quit command received. Exiting...")
                    root.quit()
                    return  # Stop queue polling
            root.after(50, process_commands)  # Poll 20 times per second
        
        root.after(50, process_commands)
        root.mainloop()
        
    except ConnectionRefusedError:
        print("Could not connect. Make sure the server is running and the port is correct.")
    except MsgError as e:
        print(e)
    finally:
        client.close()

if __name__ == '__main__':
    main()
