import os
import random
import msvcrt  # Windows keyboard input

GRID_SIZE = 20

player = {"x": 0, "y": 0, "score": 0}
gold = {"x": random.randint(0, GRID_SIZE - 1), "y": random.randint(0, GRID_SIZE - 1)}


def clear_screen():
    os.system("cls")


def draw_board():
    clear_screen()

    print("Gold Miner - Use W/A/S/D to move, Q to quit")
    print(f"Score: {player["score"]}")
    print()

    for y in range(GRID_SIZE):
        row = ""
        for x in range(GRID_SIZE):
            if player["x"] == x and player["y"] == y:
                row += "P "
            elif gold["x"] == x and gold["y"] == y:
                row += "G "
            else:
                row += ". "
        print(row)


def move_player(direction):
    if direction == "w" and player["y"] > 0:
        player["y"] -= 1
    elif direction == "s" and player["y"] < GRID_SIZE - 1:
        player["y"] += 1
    elif direction == "a" and player["x"] > 0:
        player["x"] -= 1
    elif direction == "d" and player["x"] < GRID_SIZE - 1:
        player["x"] += 1


def check_gold():
    global gold

    if player["x"] == gold["x"] and player["y"] == gold["y"]:
        player["score"] += 1
        gold = {
            "x": random.randint(0, GRID_SIZE - 1),
            "y": random.randint(0, GRID_SIZE - 1),
        }


def main():
    while True:
        draw_board()

        key = msvcrt.getch().decode("utf-8").lower()

        if key == "q":
            break

        if key in ["w", "a", "s", "d"]:
            move_player(key)
            check_gold()


if __name__ == "__main__":
    main()