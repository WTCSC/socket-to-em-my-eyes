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

# Allow for easy changing of log levels
parser = argparse.ArgumentParser(description="Solo punishment client")
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
cmd_queue = queue.Queue()

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
        delay = 25        # Time (ms) between steps

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

    try:
        webbrowser.open_new_tab(url)
        logging.info(f"Opened URL in default browser: {url}")
    except Exception as e:
        logging.warning(f"Failed to open default browser: {e}")
        logging.info("Trying to open in Google Chrome...")
        if sys.platform.startswith("win"):
            chrome_cmd = "start chrome"
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

# push commands into the queue instead of calling functions directly.
def receive_input(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            if key.char.lower() == 'f':
                cmd_queue.put("flash")
            elif key.char.lower() == 'c':
                cmd_queue.put("click")
        else:
            if key == keyboard.Key.backspace:
                cmd_queue.put("rand")
            elif key == keyboard.Key.pause:  # When Pause Break is pressed, quit.
                logging.debug('Exiting gracefully via keyboard...')
                cmd_queue.put("quit")
                return False  # Stops the keyboard listener
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

def main():
    # Start the keyboard listener thread.
    keyboard_thread = threading.Thread(target=start_listener, daemon=True)
    keyboard_thread.start()
    
    # Create a hidden tkinter root to run the event loop.
    root = tk.Tk()
    root.withdraw()
    
    # Process the queue of commands
    def process_commands():
        while not cmd_queue.empty():
            cmd = cmd_queue.get()
            if cmd == "flash":
                flash()
            elif cmd == "click":
                tclick()
            elif cmd == "rand":
                rand_site()
            elif cmd == "quit":
                logging.info("Quit command received. Exiting...")
                root.quit()
                return  # End queue polling
        root.after(50, process_commands)  # Poll 20 times a second
    
    root.after(50, process_commands)
    root.mainloop()

if __name__ == '__main__':
    main()
