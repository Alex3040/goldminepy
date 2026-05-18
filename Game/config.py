# Config file for the game. All numbers directly below should be integers. 
MAX_PLAYERS = int(100)
GRID_SIZE = int(20)

CLIENT_MOVE_COOLDOWN = 0.5  # Minimum time (in seconds) between moves from the same client

MOVE_PORT = 5555    # Port for receiving client moves
STATE_PORT = 5556   # Port for pushing game state to client

SERVER_IP = "127.0.0.1"  # IP address of the server (localhost)

