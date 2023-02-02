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
        "author": "Team Flying Snakes",
        "color": "#D36750",
        "head": "fang",
        "tail": "freckled",
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
    check_other_snake_collisions(is_move_safe, game_state)

    # Choose a random move from the safe ones
    next_move = pick_a_move(is_move_safe, game_state)

    print(f"MOVE {game_state['turn']}: {next_move}")
    model = {"move": next_move}
    if game_state['turn'] % 5 == 0:
        model['shout'] = random.choice(shouts)
    return model


shouts = [
    'IMA FIRIN MY LAZER!!1',
    'MY POWER GOES TO 9000!!!1',
    'GET SNAKED!',
]


def pick_a_move(is_move_safe, game_state):
    # Are there any safe moves left?
    safe_moves = [
        move
        for move, isSafe in is_move_safe.items()
        if isSafe
    ]

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    food_move = find_food(game_state)
    if food_move in safe_moves:
        return food_move

    next_move = random.choice(safe_moves)

    return next_move


def find_food(is_move_safe, game_state):
    head = game_state["you"]["body"][0]
    food_coords = {
        to_tuple(food)
        for food in game_state["board"]["food"]
    }

    for key, action in moves.items():
        if is_move_safe[key] is False:
            continue

        head_coords = action(head)
        head_coords = to_tuple(head_coords)
        if head_coords in food_coords:
            return key


def check_other_snake_collisions(is_move_safe, game_state):
    me = game_state["you"]
    my_head = me["body"][0]
    my_health = me["health"]
    other_snakes = game_state["board"]["snakes"]

    for snake in other_snakes:
        if snake["id"] == me["id"]:
            continue  # tested in other function

        other_possible_moves = get_possible_moves(snake)

        for key in moves:
            if is_move_safe[key] is False:
                continue

            my_possible_move = to_tuple(moves[key](my_head))
            if my_possible_move not in other_possible_moves:
                continue

            # is_move_safe[key] = False
            other_health = snake["health"]
            if other_health >= my_health:
                is_move_safe[key] = False


def to_tuple(d):
    return d["x"], d["y"]


def get_possible_moves(snake):
    return {
        to_tuple(action(snake["body"][0]))
        for action in moves.values()
    }


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
