

def move_player(players, player_name, direction, grid_size):
    player = players[player_name]

    if direction == "UP" and player["y"] > 0:
        player["y"] -= 1

    elif direction == "DOWN" and player["y"] < grid_size - 1:
        player["y"] += 1

    elif direction == "LEFT" and player["x"] > 0:
        player["x"] -= 1

    elif direction == "RIGHT" and player["x"] < grid_size - 1:
        player["x"] += 1