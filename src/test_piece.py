'''
This file contains tests for piece.py.
'''


from piece import Piece
from board import Board
from move import Move
from testing_utils import make_board_pieces
from constants import PLAYER_COLOR_BLACK, PLAYER_COLOR_RED
from move import Move


def test_check_is_inside():
    piece_one = Piece(3, 6, PLAYER_COLOR_BLACK)
    piece_two = Piece(9, 8, PLAYER_COLOR_BLACK)
    piece_three = Piece(4, -1, PLAYER_COLOR_BLACK)
    assert(piece_one.check_is_inside())
    assert(not piece_two.check_is_inside())
    assert(not piece_three.check_is_inside())


def test_maybe_promote_to_king():
    piece_one = Piece(3, 7, PLAYER_COLOR_BLACK)
    piece_one.maybe_promote_to_king()
    assert(piece_one.is_king)
    piece_two = Piece(3, 6, PLAYER_COLOR_BLACK)
    piece_two.maybe_promote_to_king()
    assert(not piece_two.is_king)
    piece_three = Piece(4, 0, PLAYER_COLOR_RED)
    piece_three.maybe_promote_to_king()
    assert(piece_three.is_king)
    piece_four = Piece(4, 3, PLAYER_COLOR_RED)
    piece_four.maybe_promote_to_king()
    assert(not piece_four.is_king)


def test_move_by():
    piece_one = Piece(3, 6, PLAYER_COLOR_BLACK)
    piece_one_moved = piece_one.move_by(1, 1)
    assert(
        piece_one_moved.board_x == 4 and
        piece_one_moved.board_y == 7 and
        piece_one_moved.color == PLAYER_COLOR_BLACK and
        piece_one_moved.is_king
    )
    piece_two = Piece(9, 8, PLAYER_COLOR_BLACK)
    assert(
        piece_two.move_by(-1, 1) is None
    )
    piece_three = Piece(4, 1, PLAYER_COLOR_RED)
    piece_three_moved = piece_three.move_by(1, -1)
    assert(
        piece_three_moved.board_x == 5 and
        piece_three_moved.board_y == 0 and
        piece_three_moved.color == PLAYER_COLOR_RED and
        piece_three_moved.is_king
    )
    piece_four = Piece(4, 3, PLAYER_COLOR_RED)
    piece_four_moved = piece_four.move_by(-1, 1)
    assert(
        piece_four_moved.board_x == 3 and
        piece_four_moved.board_y == 4 and
        piece_four_moved.color == PLAYER_COLOR_RED and
        not piece_four_moved.is_king
    )


def test_get_allowed_steps():
    piece_one = Piece(3, 6, PLAYER_COLOR_BLACK)
    assert(piece_one.get_allowed_steps() == [(1, 1), (-1, 1)])
    piece_two = Piece(4, 1, PLAYER_COLOR_RED)
    assert(piece_two.get_allowed_steps() == [(1, -1), (-1, -1)])
    piece_three = Piece(3, 4, PLAYER_COLOR_BLACK, is_king=True)
    assert(
        piece_three.get_allowed_steps() == [(1, -1), (-1, -1), (1, 1), (-1, 1)]
    )


def test_get_normal_moves():
    pieces = make_board_pieces([
        "B . . . ",
        " . . . .",
        ". r . R ",
        " . . . .",
        ". . . . ",
        " b . . b",
        ". . . . ",
        " . . . .",
    ])
    piece_one = pieces[(2, 5)]
    piece_two = pieces[(6, 5)]
    piece_three = pieces[(1, 2)]
    piece_four = pieces[(7, 2)]
    piece_five = pieces[(0, 7)]
    board = Board(pieces)
    piece_one_move_right = piece_one.move_by(-1, -1)
    piece_one_move_left = piece_one.move_by(1, -1)
    move_piece_one_to_left = Move(piece_one, piece_one_move_left)
    move_piece_one_to_right = Move(piece_one, piece_one_move_right)
    assert(piece_one.get_normal_moves(board) == [
        move_piece_one_to_left, move_piece_one_to_right
        ]
    )
    piece_two_move_right_upper = piece_two.move_by(-1, -1)
    piece_two_move_right_lower = piece_two.move_by(1, 1)
    piece_two_move_left_upper = piece_two.move_by(1, -1)
    piece_two_move_left_lower = piece_two.move_by(-1, 1)
    move_piece_two_to_left_upper = Move(piece_two, piece_two_move_left_upper)
    move_piece_two_to_right_upper = Move(piece_two, piece_two_move_right_upper)
    move_piece_two_to_left_lower = Move(piece_two, piece_two_move_left_lower)
    move_piece_two_to_right_lower = Move(piece_two, piece_two_move_right_lower)
    assert(piece_two.get_normal_moves(board) == [
        move_piece_two_to_left_upper,
        move_piece_two_to_right_upper,
        move_piece_two_to_right_lower,
        move_piece_two_to_left_lower
        ]
    )
    piece_three_move_right = piece_three.move_by(1, 1)
    piece_three_move_left = piece_three.move_by(-1, 1)
    move_piece_three_to_left = Move(piece_three, piece_three_move_left)
    move_piece_three_to_right = Move(piece_three, piece_three_move_right)
    assert(piece_three.get_normal_moves(board) == [
        move_piece_three_to_right,
        move_piece_three_to_left
        ]
    )
    piece_four_move_left = piece_four.move_by(-1, 1)
    move_piece_four_to_left = Move(piece_four, piece_four_move_left)
    assert(piece_four.get_normal_moves(board) == [move_piece_four_to_left])
    piece_five_move_right_lower = piece_five.move_by(1, -1)
    move_piece_five_to_right_lower = Move(
        piece_five, piece_five_move_right_lower
    )
    assert(piece_five.get_normal_moves(board) == [
        move_piece_five_to_right_lower
        ]
    )
    pieces_two = make_board_pieces([
        ". . . . ",
        " . . . .",
        ". . . . ",
        " . . . .",
        ". . . . ",
        " b . . .",
        "r . . . ",
        " b . . .",
    ])
    board_two = Board(pieces_two)
    piece_six = pieces_two[(0, 1)]
    assert(piece_six.get_normal_moves(board_two) == [])


def test_get_capture_moves():
    pieces = make_board_pieces([
        ". . . . ",
        " . . . .",
        ". . . b ",
        " . . . R",
        ". . . . ",
        " . r . .",
        ". b . B ",
        " . . . .",
    ])
    board = Board(pieces)
    piece_one = pieces[(6, 5)]
    piece_two = pieces[(7, 4)]
    piece_three = pieces[(3, 2)]
    piece_four = pieces[(2, 1)]
    piece_five = pieces[(6, 1)]
    piece_two_capture_move = piece_two.move_by(-2, 2)
    move_piece_two = Move(piece_two, piece_two_capture_move, piece_one)
    assert(piece_two.get_capture_moves(board) == [move_piece_two])
    piece_three_capture_move = piece_three.move_by(-2, -2)
    move_piece_three = Move(piece_three, piece_three_capture_move, piece_four)
    assert(piece_three.get_capture_moves(board) == [move_piece_three])
    assert(piece_five.get_capture_moves(board) == [])
