'''
This file contains tests for test_utils.py.
'''

from testing_utils import make_board_pieces
from piece import Piece
from constants import PLAYER_COLOR_BLACK, PLAYER_COLOR_RED, NUM_SQUARES


def test_make_board_pieces():
    pieces_one = make_board_pieces([
        ". . . . ",
        " r . . .",
        ". B . . ",
        " . . . .",
        ". . . . ",
        " . b . .",
        ". R . . ",
        " . . . .",
    ])
    pieces_one_expected = {
        (1, 6): Piece(1, 6, PLAYER_COLOR_RED),
        (2, 5): Piece(2, 5, PLAYER_COLOR_BLACK, is_king=True),
        (3, 2): Piece(3, 2, PLAYER_COLOR_BLACK),
        (2, 1): Piece(2, 1, PLAYER_COLOR_RED, is_king=True)
    }
    assert(pieces_one == pieces_one_expected)
