'''
This file contains functions that can be useful to use in files for testing.
'''

from piece import Piece
from constants import PLAYER_COLOR_BLACK, PLAYER_COLOR_RED, NUM_SQUARES


def make_board_pieces(definition):
    '''
        Function -- make_board_pieces
            Converts definition of the board state into dictionary format,
                where the key is the coordinate of the piece on the board
                and the value is the Piece object
        Parameters:
            definition -- state of the board.
                It is list with 8 strings, each string represents the row on
                the board with dots representing gray cells, space represents
                white cell, "B" is black king piece, "R" is red king piece,
                "r" is red piece, "b" is black piece.
        Returns:
            Pieces state on the board in dictionary format, accepted by the
            Board constructor.
    '''
    definition = list(reversed(definition))
    result = {}
    for y in range(NUM_SQUARES):
        for x in range(NUM_SQUARES):
            ch = definition[y][x]
            if ch == "B":
                result[(x, y)] = Piece(
                    board_x=x,
                    board_y=y,
                    color=PLAYER_COLOR_BLACK,
                    is_king=True,
                )
            elif ch == "b":
                result[(x, y)] = Piece(
                    board_x=x,
                    board_y=y,
                    color=PLAYER_COLOR_BLACK,
                    is_king=False,
                )
            elif ch == "R":
                result[(x, y)] = Piece(
                    board_x=x,
                    board_y=y,
                    color=PLAYER_COLOR_RED,
                    is_king=True,
                )
            elif ch == "r":
                result[(x, y)] = Piece(
                    board_x=x,
                    board_y=y,
                    color=PLAYER_COLOR_RED,
                    is_king=False,
                )
    return result
