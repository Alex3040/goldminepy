import zmq
import time

from game.config import MOVE_PORT, STATE_PORT, GRID_SIZE
import game.state as state
from game.movement import move_player
from game.gold import check_gold_collision


def main():
    context = zmq.Context()

    move_socket = context.socket(zmq.PULL)
    move_socket.bind(f"tcp://*:{MOVE_PORT}")

    state_socket = context.socket(zmq.PUB)
    state_socket.bind(f"tcp://*:{STATE_PORT}")

    print("Gold Miner server started")
    print(f"Receiving moves on port {MOVE_PORT}")
    print(f"Publishing state on port {STATE_PORT}")

    while True:
        message = move_socket.recv_json()

        if message["type"] == "join":
            player_name = message["player"]

            accepted, reason = state.can_join(player_name)

            state_socket.send_json(
                state.build_join_response(player_name, accepted, reason)
            )

            if accepted:
                state.add_player(player_name)
                state_socket.send_json(state.build_state())

        elif message["type"] == "move":
            player_name = message["player"]
            direction = message["direction"]

            if player_name not in state.players:
                continue

            move_player(state.players, player_name, direction, GRID_SIZE)

            new_gold = check_gold_collision(
                state.players,
                player_name,
                state.gold,
                GRID_SIZE,
            )

            state.set_gold(new_gold)

            state_socket.send_json(state.build_state()) 


if __name__ == "__main__":
    main()