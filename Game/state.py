import random

from game.config import GRID_SIZE, MAX_PLAYERS
from game.gold import spawn_gold


players = {}
gold = spawn_gold(GRID_SIZE, players)


def can_join(player_name):
    if not player_name:
        return False, "Name cannot be empty"

    if len(player_name) > 12:
        return False, "Name is too long"

    if player_name in players:
        return False, "Name already taken"

    if len(players) >= MAX_PLAYERS:
        return False, "Server is full"

    return True, "Accepted"


def add_player(player_name):
    players[player_name] = {
        "x": random.randint(0, GRID_SIZE - 1),
        "y": random.randint(0, GRID_SIZE - 1),
        "score": 0,
    }


def build_state():
    return {
        "type": "state",
        "grid_size": GRID_SIZE,
        "players": players,
        "gold": gold,
    }


def build_join_response(player_name, accepted, reason):
    return {
        "type": "join_response",
        "player": player_name,
        "accepted": accepted,
        "reason": reason,
    }


def set_gold(new_gold):
    global gold
    gold = new_gold