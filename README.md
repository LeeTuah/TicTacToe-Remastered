# Tic-Tac-Toe Remastered Edition

A fully functional, multi-threaded command-line Tic-Tac-Toe game featuring both Singleplayer (vs AI) and Multiplayer (LAN and Wireless if you have port forwarding or similar setups) modes. This project demonstrates advanced Python networking using Sockets, threading, and custom state management.

## 🌟 Features

* **Multiplayer Support:** Play against friends over LAN or Wirelessly.
* **Room System:** Create, Host, and Join private rooms using unique Room IDs.
* **Singleplayer Mode:** Practice against a randomized AI.
* **Active Window Detection:** Uses `pygetwindow` to ensure game inputs are only registered when the terminal window is active (prevents accidental typing in other apps, and helps if you have multiple instances opened).
* **Live State Updates:** Real-time board updates using ANSI escape codes to clear and redraw the interface.
* **Custom Network Protocol:** Implements a request/response protocol using status codes (e.g., `200`, `403`, `404`) and delimiters.
* **Robust Error Handling:** Handles disconnects, server shutdowns, and opponent interruptions gracefully.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Networking:** `socket` (TCP/IP), `threading`
* **Input Handling:** `pynput` (Key listener), `pygetwindow` (Window focus)
* **OS Support:** Optimized For Windows. Should work on Mac/Linux but not tested.

## 📦 Installation & Setup

### 1. Prerequisites
You will need Python installed. You also need to install the required external libraries:

```bash
pip install pynput pygetwindow
```

### 2. Configuration
Before running the game, you must configure the IP address to match your network.

1.  Open `server/main.py` and `client/multiplayer.py`.
2.  Locate the `SERVER` variable.
3.  If running locally (one machine), set it to `'localhost'` or `'127.0.0.1'`.
4.  If running over LAN, set it to the IPv4 address of the computer running the server (e.g., `'192.168.1.X'`).
5.  If you want to run Wirelessly, use Port Forwarding, VPN or other methods and edit the IPs accordingly

### 3. Running the Game

**Step 1: Start the Server** (ONLY if you are hosting the server, not necessary if hosted seperately).

Open a terminal in the `server/` directory:
```bash
python main.py
```
*The server will start listening on port 6741.*

**Step 2: Start the Client(s)**
Open a new terminal (or multiple for multiplayer) in the `client/` directory:
```bash
python main.py
```

## 🎮 How to Play

### Controls
The game uses the number keys (**1-9**) to place your symbol on the grid.
* **1, 2, 3:** Top Row
* **4, 5, 6:** Middle Row
* **7, 8, 9:** Bottom Row

### Multiplayer Flow
1.  **Host:** Select "Multiplayer" -> "Host a Room".
2.  **Share:** The game will generate an 8-digit **Room ID**. Share this with your friend.
3.  **Wait:** Wait for the friend to join.
4.  **Start:** Once connected, the Host presses `W` to start the match.
5.  **Play:** Moves are relayed instantly between clients.

### Commands (Internal)
The client and server communicate using specific headers (handled automatically by the UI):
* `!host`: Requests a new room.
* `!join <id>`: Attempts to join a room.
* `!start`: Initiates the game loop.
* `!abort`: Signals game end (win/loss/draw).
* `!leave`: Disconnects from a room.

These commands are NOT meant to be used directly, they are just for there for client-server communication.

## 📂 Project Structure

```text
├── server/
│   └── main.py           # Central server logic. Handles connections, rooms, and move relaying.
│
├── client/
│   ├── main.py           # Entry point. Handles the main menu and mode selection.
│   ├── TTT.py            # Core Game Logic. Board rendering, win detection, and input handling.
│   ├── multiplayer.py    # Socket client logic. Handles sending/receiving packets.
│   ├── singleplayer.py   # Handles Code for running in Singleplayer mode.
│   ├── intro.py          # ASCII art animations and loading screens.
```

## 🧠 Technical Architecture

### The "Relay" Pattern
The server does not calculate the game logic. Instead, it acts as a **Stateful Relay**.
1.  **Client A** calculates a move and sends coordinates to the Server.
2.  **Server** verifies `user_data` to see if Client A is `ingame` and linked to an opponent.
3.  **Server** forwards the raw coordinates immediately to **Client B**.
4.  **Client B** updates their local board.

### Win Detection
Win detection is **decentralized**. Both clients check the board state after every move. If a client detects a win (for themselves or the opponent), they send an `!abort` signal to the server to close the game session cleanly.

## ⚠️ Known Limitations
* **Input Blocking:** The `pynput` listener is blocking in some contexts; the threading implementation ensures the UI remains responsive.
* **Focus Requirement:** You must have the terminal window active/focused for keys to register (feature of `pygetwindow` integration).

---


**Created solely by LeeTuah**
