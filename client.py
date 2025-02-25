from pynput import keyboard
import pyautogui as PAG
import tkinter as tk
import time
import sys
import subprocess
import random

class MsgError(Exception):
    pass
    
    # Initiate Connection Variable Data
    ######client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ######server_ip = input("Enter server IP: ")
    ######port = int(input("Enter server port: "))
    

     #  Get the message from the server
def receive_msg(server_ip, port):
    message = client.recv(1024).decode("utf-8")
    if not message:
        raise MsgError("Message is empty")
    elif message == 'SECRETCODE15':
        start_listener()
    else:
        print(f"Server says: {message}")

def flash():
        
    ## Creates a full-screen white flash that smoothly fades to transparent
    flash_window = tk.Tk()  # Use Tk() instead of Toplevel() to avoid overlay issues
    flash_window.attributes("-fullscreen", True)
    flash_window.attributes("-topmost", True)
    flash_window.configure(bg="white")

    # Remove window borders and title box
    flash_window.overrideredirect(True)
        
    # Transparency attribute
    flash_window.attributes("-alpha", 1.0)  # Start fully visible

    ###### Uncomment to extend time screen stays white
    flash_window.update()
    time.sleep(0.5)

    fade_steps = 100  # Number of fade steps
    delay = 25  # Time (ms) between steps

    # Fade out flash
    for i in range(fade_steps):
        alpha = (1 - (i / fade_steps)**4) # Logarithmic looking fade.
        flash_window.attributes("-alpha", alpha)  # Set transparency level
        flash_window.update() # Apply change
        time.sleep(delay / 1000)  # Convert ms to seconds

    flash_window.destroy()  # Close

def tclick():
    PAG.click()
    PAG.click()
    PAG.click()

def rand_site():
    def rand_url():
        urls = [
            # Endless Loops & Confusion
            "https://www.omfgdogs.com/",  # Flashing dogs running forever
            "https://pointerpointer.com/",  # AI points at your cursor wherever it is
            "https://endless.horse/",  # A horse that never stops scrolling
            "https://heeeeeeeey.com/",  # Never-ending "heeeey!"
            "https://hooooooooo.com/",  # Never-ending "hoooo!"
            "https://staggeringbeauty.com/",  # Wiggly worm that reacts to your mouse (seizure warning)

            # Weird & Pointless
            "https://thiswebsitewillselfdestruct.com/",  # Click to watch a countdown timer
            "https://www.sanger.dk/",  # A dancing man follows your cursor
            "https://www.fallingfalling.com/",  # Hypnotic falling animation
            "https://alwaysjudgeabookbyitscover.com/",  # Books with absurd covers
            "https://cant-not-tweet-this.com/",  # Forces a tweet (but you can cancel)

            # Loud & Obnoxious
            "https://annoying.website/",  # Open it and regret it
            "https://www.rainymood.com/",  # Plays never-ending rain sounds
            "https://www.michaelbach.de/ot/",  # Optical illusions overload
            "https://crouton.net/",  # Crouton. Just crouton.

            # Pranks & Mild Trolling
            "https://hackertyper.com/",  # Type anything = "hacking" text appears
            "https://cat-bounce.com/",  # Bouncing cats all over your screen
            "https://theuselessweb.com/",  # Takes you to a **random** useless website
            "https://isitchristmas.com/",  # Always says "No" (unless it's Christmas)
            "https://longdogechallenge.com/",  # How long is this dog?

            # AI & Random Generators
            "https://inspirobot.me/",  # AI-generated inspirational quotes (weird ones)
            "https://clickclickclick.click/",  # Click tracking experiment
            "https://trypap.com/",  # "How strong is your password?" (You'll never win)

            # Games & Distractions
            "https://corndog.io/",  # Find the corndog
            "https://tencents.info/",  # See how rich Jeff Bezos is compared to you
            "https://ncase.me/trust/",  # An interactive trust-building game
            "https://neal.fun/",  # Fun mini-games and experiments

            # Extras
            "https://boredbutton.com",
            "https://boredbutton.com/random",
            "https://clicktheredbutton.com",
            "https://theuselessweb.com"
        ]
        url = random.choice(urls)
        return url

    def open_browser():
        """Opens a URL in the default browser or Google Chrome if available."""
        url = rand_url()
        try:
            webbrowser.open_new_tab(url)  # Open in the system's default browser
        except Exception as e:
            print(f"Failed to open default browser: {e}")

            # Check if the user is on Windows, macOS, or Linux
            if sys.platform.startswith("win"):
                chrome_cmd = "start chrome"
            elif sys.platform.startswith("darwin"):  # macOS
                chrome_cmd = "open -a 'Google Chrome'"
            else:  # Linux
                chrome_cmd = "google-chrome"

            try:
                subprocess.Popen(f"{chrome_cmd} {url}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"Failed to open in Chrome: {e}")
    open_browser()

def receive_input(key):
    try:
        if key.char == 'f':
            print('Flashbang out!')
            flash()

        elif key.char == 'c':
            print("Get clocked")
            tclick()
            
    except AttributeError:  
        # Handle special keys separately
        if key == keyboard.Key.space:
            rand_site()
            print("Space was pressed!")

        elif key == keyboard.Key.pause:
            print('Exiting gracefully')
            return False

def start_listener():
    try:
        with keyboard.Listener(on_press=receive_input) as listener:
            listener.join()  # This will now block, allowing Ctrl+C to exit
    except KeyboardInterrupt:
        pass


def main():

    """ # Initiate Connection Variable Data
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("Enter server IP: ")
    port = int(input("Enter server port: "))
    # Connect and receive_msg() """
    try:
        ####client.connect((server_ip, port))
        ####receive_msg(server_ip, port)
        start_listener()
    except ConnectionRefusedError:
        print("Could not connect. Make sure the server is running and the port is correct.")
    except MsgError as e:
        print(e)
    finally:
        ####client.close()
        pass

if __name__ == '__main__':
    main()
