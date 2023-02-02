# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

# notes:
# - 0,0 = bottom left

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    check_body_position(is_move_safe, game_state)
    check_board_boundaries(is_move_safe, game_state)
    check_other_snakes(is_move_safe, game_state)

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


def check_board_boundaries(is_move_safe, game_state):
    my_head = game_state["you"]["body"][0]  # Coordinates of your head

    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    if is_move_safe["up"] and my_head["y"] == board_height - 1:
        is_move_safe["up"] = False
    if is_move_safe["down"] and my_head["y"] == 0:
        is_move_safe["down"] = False
    if is_move_safe["left"] and my_head["x"] == 0:
        is_move_safe["left"] = False
    if is_move_safe["right"] and my_head["x"] == board_width - 1:
        is_move_safe["right"] = False


def check_other_snakes(is_move_safe, game_state):
    me = game_state["you"]
    my_head = me["body"][0]
    other_snakes = game_state["board"]["snakes"]
    for snake in other_snakes:
        if snake["id"] == me["id"]:
            continue  # tested in other function

        check_snake_vs_head(my_head, snake["body"], is_move_safe)


def move_left(d: dict):
    return {
        "x": d["x"] - 1,
        "y": d["y"],
    }


moves = {
    "left": lambda d: {
        "x": d["x"] - 1,
        "y": d["y"],
    },
    "right": lambda d: {
        "x": d["x"] + 1,
        "y": d["y"]
    },
    "down": lambda d: {
        "x": d["x"],
        "y": d["y"] - 1,
    },
    "up": lambda d: {
        "x": d["x"],
        "y": d["y"] + 1,
    },
}


def check_body_position(is_move_safe, game_state):
    head = game_state["you"]["body"][0]
    body = game_state["you"]["body"][1:]

    check_snake_vs_head(head, body, is_move_safe)


def check_snake_vs_head(head, body, is_move_safe):
    for meat in body:
        for key in ["left", "right", "down", "up"]:
            if not is_move_safe[key]:
                continue

            new_head = moves[key](head)
            if new_head == meat:
                is_move_safe[key] = False


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
