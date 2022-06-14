'''
This file starts the Checkers game.
'''

import turtle

import drawing
from board import Board
from constants import (
    BACKGROUND_COLOR,
    BOARD_PADDING_PX,
    INITIAL_ROWS,
    NUM_SQUARES,
    SQUARE_SIZE_PX,
    TEXT_SIZE_PX,
    WINDOW_PADDING_PX,
)
from game import Game
from move import Move
from piece import Piece


def main():
    board_size = NUM_SQUARES * SQUARE_SIZE_PX
    window_width = board_size + 2 * BOARD_PADDING_PX
    window_height = board_size + 4 * BOARD_PADDING_PX + 2 * TEXT_SIZE_PX
    turtle.setup(
        WINDOW_PADDING_PX + window_width,
        WINDOW_PADDING_PX + window_height,
    )
    turtle.screensize(window_width, window_height)
    turtle.bgcolor(BACKGROUND_COLOR)
    turtle.tracer(0, 0)

    pen = turtle.Turtle()
    pen.penup()
    pen.hideturtle()

    game = Game(pen)

    screen = turtle.Screen()
    screen.onclick(game.handle_click)

    turtle.done()


if __name__ == "__main__":
    main()
