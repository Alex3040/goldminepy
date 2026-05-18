import os, sys, threading, time, msvcrt

import zmq

from game.config import SERVER_IP, MOVE_PORT, STATE_PORT, CLIENT_MOVE_COOLDOWN

last_move_time = 0.12

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def render(state, my_name):
    clear_screen()

    grid_size = state["grid_size"]
    players = state["players"]
    gold = state["gold"]

    print("Gold Miner")
    print("Use W/A/S/D to move. Press Q to quit.")
    print()

    for name, player in players.items():
        label = "YOU" if name == my_name else name
        print(f"{label}: score={player['score']} position=({player['x']}, {player['y']})")

    print()

    for y in range(grid_size):
        row = ""

        for x in range(grid_size):
            cell = ". "

            if gold["x"] == x and gold["y"] == y:
                cell = "$ "

            for name, player in players.items():
                if player["x"] == x and player["y"] == y:
                    cell = "P " if name == my_name else "B "

            row += cell

        print(row)


def receive_states(state_socket, my_name):
    while True:
        message = state_socket.recv_json()

        if message["type"] == "join_response" and message["player"] == my_name:
            if not message["accepted"]:
                print(f"Join refused: {message['reason']}")
                os._exit(0)

        elif message["type"] == "state":
            render(message, my_name)


def main():
    if len(sys.argv) < 2:
        print("Usage: python player_client.py <player_name>")
        return

    player_name = sys.argv[1]

    context = zmq.Context()

    move_socket = context.socket(zmq.PUSH)
    move_socket.connect(f"tcp://{SERVER_IP}:{MOVE_PORT}")

    state_socket = context.socket(zmq.SUB)
    state_socket.connect(f"tcp://{SERVER_IP}:{STATE_PORT}")
    state_socket.setsockopt_string(zmq.SUBSCRIBE, "")

    receiver_thread = threading.Thread(
        target=receive_states,
        args=(state_socket, player_name),
        daemon=True,
    )
    receiver_thread.start()

    move_socket.send_json({
        "type": "join",
        "player": player_name,
    })

    while True:
        try:
            key = msvcrt.getch().decode("utf-8").lower()
        except:
            continue

        if key == "q":
            break

        now = time.time()

        last_move_time = 0

        if now - last_move_time < CLIENT_MOVE_COOLDOWN:
            continue

        direction = None

        if key == "w":
            direction = "UP"
        elif key == "s":
            direction = "DOWN"
        elif key == "a":
            direction = "LEFT"
        elif key == "d":
            direction = "RIGHT"
        else:
            continue

        if direction:
            time.sleep(2)  # Small delay to add planned delay for testing purposes.
            move_socket.send_json({
                "type": "move",
                "player": player_name,
                "direction": direction,
            })
            last_move_time = now


if __name__ == "__main__":
    main()