[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/nSbtKKg7)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=18269782)

# Remote Punishment Server and Client

This project consists of a server and client application that allows remote execution of "punishment" commands on the client machine. The server sends commands to the client, which then executes actions such as displaying a flashbang effect, performing triple clicks, or opening random distracting websites.

---

## Features

- **Server-Side Control**: The server can send commands to the client to execute specific actions.
- **Client-Side Execution**: The client listens for commands from the server and executes them locally.
- **Customizable Logging**: Both server and client support customizable logging levels for debugging and monitoring.
- **Thread-Safe Command Queue**: Commands are processed in a thread-safe queue to ensure smooth execution.
- **Handshake Mechanism**: A secret code (`SECRETCODE15`) is used to establish a secure connection between the server and client.

---

## How It Works

### Server
The server listens for incoming connections on a random port (between 1024 and 11111). Once a client connects, the server sends a handshake code (`SECRETCODE15`) to verify the connection. The server then waits for user input to send commands to the client. Commands include:
- `flash`: Displays a flashbang effect on the client.
- `click`: Performs a triple click on the client.
- `rand`: Opens a random distracting website on the client.
- `quit`: Closes the connection.

Commands can also include an optional delay (in seconds) to schedule their execution.

### Client
The client connects to the server using the provided IP address and port. After a successful handshake, the client listens for commands from the server and executes them locally. The client also supports keyboard input for local execution of commands:
- Press `f` to trigger the flashbang effect.
- Press `c` to perform a triple click.
- Press `Backspace` to open a random website.
- Press `Pause` to quit the client.

---

## Installation and Usage

### Prerequisites
- Python 3.x
- Required Python libraries: `pynput`, `pyautogui`, `tkinter`

Install the required libraries using pip:
``` pip instal pynput pyautogui ```


### Running the Server
1. Save the server code in a file named `server.py`.
2. Run the server:
```python server.py```
3. The server will display the port it is hosting on. Use this port to connect the client.

### Running the Client
1. Save the client code in a file named `client.py`.
2. Run the client:
```python client.py --log INFO```
3. Enter the server IP and port when prompted.

---

## Logging
Both the server and client support logging at different levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). By default, the server logs at `INFO` level, and the client logs at `WARNING` level. You can change the logging level using the `--log` argument when running the client.

---

## Command Examples
- Send a flashbang command with a 5-second delay:
```flash 5```
- Send a triple click command:
```click```
- Open a random website:
```rand```


---

## Notes
- Ensure the server and client are running on the same network.
- The client requires a graphical environment to execute commands like `flash` and `click`.
- Use the `quit` command to gracefully close the connection.

---

## License
This project is open-source.
