'''
This file contains tests for move.py.
'''

from move import Move
from piece import Piece
from constants import PLAYER_COLOR_BLACK, PLAYER_COLOR_RED


def test_is_capture():
    piece_one = Piece(3, 6, PLAYER_COLOR_BLACK)
    piece_two = Piece(5, 8, PLAYER_COLOR_BLACK)
    move = Move(piece_one, piece_two)
    assert(not move.is_capture())
    piece_three = Piece(4, 6, PLAYER_COLOR_RED)
    move = Move(piece_one, piece_two, piece_three)
    assert(move.is_capture())
