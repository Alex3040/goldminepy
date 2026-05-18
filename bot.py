import random
import threading
import time

import zmq

from game.config import (
    SERVER_IP,
    MOVE_PORT,
    STATE_PORT,
    CLIENT_MOVE_COOLDOWN,
)


DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]


def generate_bot_name():
    return f"Bot{random.randint(1000, 9999)}"


def receive_states(state_socket, bot_name):
    while True:
        message = state_socket.recv_json()

        if (
            message["type"] == "join_response"
            and message["player"] == bot_name
        ):
            if not message["accepted"]:
                print(f"{bot_name} refused: {message['reason']}")
                return

        elif message["type"] == "state":
            players = message["players"]

            if bot_name in players:
                player = players[bot_name]

                print(
                    f"{bot_name} | "
                    f"Score: {player['score']} | "
                    f"Position: ({player['x']}, {player['y']})"
                )


def main():
    bot_name = generate_bot_name()

    print(f"Starting {bot_name}")

    context = zmq.Context()

    move_socket = context.socket(zmq.PUSH)
    move_socket.connect(f"tcp://{SERVER_IP}:{MOVE_PORT}")

    state_socket = context.socket(zmq.SUB)
    state_socket.connect(f"tcp://{SERVER_IP}:{STATE_PORT}")
    state_socket.setsockopt_string(zmq.SUBSCRIBE, "")

    receiver_thread = threading.Thread(
        target=receive_states,
        args=(state_socket, bot_name),
        daemon=True,
    )
    receiver_thread.start()

    move_socket.send_json({
        "type": "join",
        "player": bot_name,
    })

    while True:
        direction = random.choice(DIRECTIONS)

        move_socket.send_json({
            "type": "move",
            "player": bot_name,
            "direction": direction,
        })

        time.sleep(CLIENT_MOVE_COOLDOWN)


if __name__ == "__main__":
    main()