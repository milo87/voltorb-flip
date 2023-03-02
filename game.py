import random
from board import Board
from enum import Enum
from tile import Type
from typing import Optional
import sys


class Action(Enum):
    F = "(F)lip"
    M = "(M)ark"
    Q = "(Q)uit"


def handle_input() -> tuple[Action, Optional[int], Optional[int]]:
    action = None

    while True:
        action = input(f"Choose an action: {[a.value for a in Action]}: ")
        if action and action.upper()[0] in [a.name for a in Action]:
            action = Action[action.upper()[0]]
            break
        else:
            print("Invalid action!")

    if action == action.Q:
        return (action, None, None)
    else:
        selected_tile = input("Choose a tile (x,y): ")
        try:
            x, y = selected_tile.split(",")
            return (action, int(x) - 1, int(y) - 1)
        except ValueError:
            return (Action.F, -1, -1)


def quit(points: int) -> None:
    print(f"Goodbye! You scored {points} points!")
    sys.exit(0)


def render_game(board: Board, level: int, coins: int, total_coins: int) -> None:
    print()
    print(f"Level: {level:02}")
    print()
    print(board)
    print(f"Coins this level: {coins:05}")
    print(f"Coins in total:   {total_coins:05}")
    print()


if __name__ == "__main__":
    board = Board()
    board.setup_board()

    level = 1
    coins = 0
    total_coins = 0

    while True:
        render_game(board, level, coins, total_coins)
        action, x, y = handle_input()
        if action == action.Q:
            quit(total_coins)
        elif action == action.M:
            board.get_cell(x, y).toggle_mark()
        elif action == action.F:
            board.flip_tile(x, y)
            cell = board.get_cell(x, y)
            if cell.type == Type.VOLTORB:
                if level > 1:
                    coins = 0
                    if random.randint(1, 4) == 1:
                        level = level - 1
                    board.setup_board()
            else:
                coins = coins + cell.value()
                if board.check_board():
                    total_coins = total_coins + coins
                    coins = 0
                    level = level + 1
                    board.setup_board()
