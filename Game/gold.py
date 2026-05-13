import random


def spawn_gold(grid_size, players=None):
    while True:
        gold = {
            "x": random.randint(0, grid_size - 1),
            "y": random.randint(0, grid_size - 1),
        }

        if players is None:
            return gold

        occupied = False

        for player in players.values():
            if player["x"] == gold["x"] and player["y"] == gold["y"]:
                occupied = True
                break

        if not occupied:
            return gold


def check_gold_collision(players, player_name, gold, grid_size):
    player = players[player_name]

    if player["x"] == gold["x"] and player["y"] == gold["y"]:
        player["score"] += 1
        return spawn_gold(grid_size, players)

    return gold