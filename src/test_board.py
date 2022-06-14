'''
This file contains tests for board.py.
'''

import random
from copy import copy
from pytest import approx

from testing_utils import make_board_pieces
from board import Board
from piece import Piece
from move import Move
from constants import PLAYER_COLOR_BLACK, PLAYER_COLOR_RED


def test_get_all_moves():
    pieces_one = make_board_pieces([
        ". . . . ",
        " r . . .",
        ". B . . ",
        " . . . .",
        ". . b . ",
        " . R . .",
        ". . . . ",
        " . . . .",
    ])
    board_one = Board(pieces_one)
    red_all_moves_on_board_one = board_one.get_capture_moves(PLAYER_COLOR_RED)
    black_all_moves_on_board_one = (
        board_one.get_capture_moves(PLAYER_COLOR_BLACK)
    )
    assert(
        board_one.get_all_moves(PLAYER_COLOR_RED) == red_all_moves_on_board_one
    )
    assert(
        board_one.get_all_moves(PLAYER_COLOR_BLACK) ==
        black_all_moves_on_board_one
    )
    pieces_two = make_board_pieces([
        "r r r r ",
        " r r r r",
        "r r r r ",
        " . . . .",
        ". . . . ",
        " b b b b",
        "b b b b ",
        " b b b b",
    ])
    board_two = Board(pieces_two)
    red_all_moves_on_board_two = board_two.get_normal_moves(PLAYER_COLOR_RED)
    assert(
        board_two.get_all_moves(PLAYER_COLOR_RED) == red_all_moves_on_board_two
    )
    black_all_moves_on_board_two = (
        board_two.get_normal_moves(PLAYER_COLOR_BLACK)
    )
    assert(
        board_two.get_all_moves(PLAYER_COLOR_BLACK) ==
        black_all_moves_on_board_two
    )


def test_get_capture_moves():
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
    board_one = Board(pieces_one)
    piece_one = pieces_one[(1, 6)]
    piece_two = pieces_one[(2, 5)]
    piece_three = pieces_one[(3, 2)]
    piece_four = pieces_one[(2, 1)]
    piece_one_move = piece_one.move_by(2, -2)
    move_piece_one = Move(piece_one, piece_one_move, piece_two)
    piece_four_move = piece_four.move_by(2, 2)
    move_piece_four = Move(piece_four, piece_four_move, piece_three)
    assert(board_one.get_capture_moves(PLAYER_COLOR_RED) == [
        move_piece_four,
        move_piece_one
    ])
    piece_two_move = piece_two.move_by(-2, 2)
    move_piece_two = Move(piece_two, piece_two_move, piece_one)
    assert(board_one.get_capture_moves(PLAYER_COLOR_BLACK) == [move_piece_two])
    pieces_two = make_board_pieces([
        "r r r r ",
        " r r r r",
        "r r r r ",
        " . . . .",
        ". . . . ",
        " b b b b",
        "b b b b ",
        " b b b b",
    ])
    board_two = Board(pieces_two)
    assert(board_two.get_capture_moves(PLAYER_COLOR_RED) == [])
    assert(board_two.get_capture_moves(PLAYER_COLOR_BLACK) == [])


def test_get_normal_moves():
    pieces_one = make_board_pieces([
        ". . . . ",
        " . . . .",
        ". B . . ",
        " . . . .",
        ". . . . ",
        " . . . .",
        ". . . b ",
        " . . . R",
    ])
    board_one = Board(pieces_one)
    assert(board_one.get_normal_moves(PLAYER_COLOR_RED) == [])
    pieces_two = make_board_pieces([
        ". . . . ",
        " r . . .",
        ". B . . ",
        " . . . .",
        ". . . . ",
        " . . . .",
        ". . . b ",
        " . . . R",
    ])
    board_two = Board(pieces_two)
    piece_one_board_two = pieces_two[(1, 6)]
    piece_one_board_two_move = piece_one_board_two.move_by(-1, -1)
    move_piece_one_board_two = Move(
        piece_one_board_two, piece_one_board_two_move
    )
    assert(board_two.get_normal_moves(PLAYER_COLOR_RED) == [
        move_piece_one_board_two
        ]
    )


def test_get_piece_at():
    pieces = make_board_pieces([
        ". . . . ",
        " r . . .",
        ". B . . ",
        " . . . .",
        ". . . . ",
        " . b . .",
        ". R . . ",
        " . . . .",
    ])
    board = Board(pieces)
    assert(board.get_piece_at(1, 6) == Piece(1, 6, PLAYER_COLOR_RED))
    assert(board.get_piece_at(2, 5) == Piece(
        2, 5, PLAYER_COLOR_BLACK, is_king=True
        )
    )
    assert(board.get_piece_at(3, 2) == Piece(3, 2, PLAYER_COLOR_BLACK))
    assert(board.get_piece_at(2, 1) == Piece(
        2, 1, PLAYER_COLOR_RED, is_king=True
        )
    )
    assert(board.get_piece_at(6, 5) is None)


def test_get_stats():
    pieces_one = make_board_pieces([
        ". . . . ",
        " r . . b",
        ". B . . ",
        " . . . .",
        ". . b . ",
        " . R . .",
        ". . . . ",
        " . . . .",
    ])
    board_one = Board(pieces_one)
    assert(board_one.get_stats() == (3, 2, 1, 1))
    pieces_two = make_board_pieces([
        "r r r r ",
        " r r r r",
        "r r r r ",
        " . . . .",
        ". . . . ",
        " b b b b",
        "b b b b ",
        " b b b b",
    ])
    board_two = Board(pieces_two)
    assert(board_two.get_stats() == (12, 12, 0, 0))
    pieces_three = make_board_pieces([
        ". . . . ",
        " r . . .",
        ". . . . ",
        " . . . .",
        ". . . . ",
        " . R . .",
        ". . . . ",
        " . . . .",
    ])
    board_three = Board(pieces_three)
    assert(board_three.get_stats() == (0, 2, 0, 1))
    pieces_four = make_board_pieces([
        ". . . . ",
        " b . . .",
        ". . . . ",
        " . . . .",
        ". . . . ",
        " . . . .",
        ". . . . ",
        " . . . .",
    ])
    board_four = Board(pieces_four)
    assert(board_four.get_stats() == (1, 0, 0, 0))


def test_get_score():
    pieces_one = make_board_pieces([
        ". . . . ",
        " r . . b",
        ". B . . ",
        " . . . .",
        ". . b . ",
        " . R . .",
        ". . . . ",
        " . . . .",
    ])
    board_one = Board(pieces_one)
    assert(board_one.get_score() == approx(0.8))
    pieces_two = make_board_pieces([
        "r r r r ",
        " r r r r",
        "r r r r ",
        " . . . .",
        ". . . . ",
        " b b b b",
        "b b b b ",
        " b b b b",
    ])
    board_two = Board(pieces_two)
    assert(board_two.get_score() == approx(1))
    pieces_three = make_board_pieces([
        ". . . . ",
        " r . . .",
        ". . . . ",
        " . . . .",
        ". . . . ",
        " . R . .",
        ". . . . ",
        " . . . .",
    ])
    board_three = Board(pieces_three)
    assert(board_three.get_score() == 10000000000)
    pieces_four = make_board_pieces([
        ". . . . ",
        " b . . .",
        ". . . . ",
        " . . . .",
        ". . . . ",
        " . . . .",
        ". . . . ",
        " . . . .",
    ])
    board_four = Board(pieces_four)
    assert(board_four.get_score() == -10000000000)


def test_get_text_score():
    pieces_one = make_board_pieces([
        ". . . . ",
        " r . . b",
        ". B . . ",
        " . . . .",
        ". . b . ",
        " . R . .",
        ". . . . ",
        " . . . .",
    ])
    board_one = Board(pieces_one)
    assert(
        board_one.get_text_score() == "     You    3 (1) : (1) 2    Computer"
    )
    pieces_two = make_board_pieces([
        "r r r r ",
        " r r r r",
        "r r r r ",
        " . . . .",
        ". . . . ",
        " b b b b",
        "b b b b ",
        " b b b b",
    ])
    board_two = Board(pieces_two)
    assert(
        board_two.get_text_score() == "     You   12 (0) : (0) 12   Computer"
    )
    pieces_three = make_board_pieces([
        ". . . . ",
        " r . . .",
        ". . . . ",
        " . . . .",
        ". . . . ",
        " . R . .",
        ". . . . ",
        " . . . .",
    ])
    board_three = Board(pieces_three)
    assert(
        board_three.get_text_score() == "     You    0 (0) : (1) 2    Computer"
    )
    pieces_four = make_board_pieces([
        ". . . . ",
        " b . . .",
        ". . . . ",
        " . . . .",
        ". . . . ",
        " . . . .",
        ". . . . ",
        " . . . .",
    ])
    board_four = Board(pieces_four)
    assert(
        board_four.get_text_score() == "     You    1 (0) : (0) 0    Computer"
    )


def test_apply_move():
    pieces_one = make_board_pieces([
        ". . . . ",
        " r . . b",
        ". B . . ",
        " . . . .",
        ". . b . ",
        " . R . .",
        ". . . . ",
        " . . . .",
    ])
    board_one = Board(pieces_one)
    piece_to_move = pieces_one[(3, 2)]
    captured_piece = pieces_one[(4, 3)]
    piece_to_move_after_move = piece_to_move.move_by(2, 2)
    move_piece_to_move = Move(
        piece_to_move, piece_to_move_after_move, captured_piece
    )
    board_one_after_the_move = board_one.apply_move(move_piece_to_move)
    pieces_two = make_board_pieces([
        ". . . . ",
        " r . . b",
        ". B . . ",
        " . . R .",
        ". . . . ",
        " . . . .",
        ". . . . ",
        " . . . .",
    ])
    board_two = Board(pieces_two)
    assert(board_one_after_the_move == board_two)
    piece_to_move_two = pieces_two[(5, 4)]
    piece_to_move_two_after_move = piece_to_move_two.move_by(1, 1)
    move_piece_to_move_two = Move(
        piece_to_move_two, piece_to_move_two_after_move
    )
    board_two_after_the_move = board_two.apply_move(move_piece_to_move_two)
    pieces_three = make_board_pieces([
        ". . . . ",
        " r . . b",
        ". B . R ",
        " . . . .",
        ". . . . ",
        " . . . .",
        ". . . . ",
        " . . . .",
    ])
    board_three = Board(pieces_three)
    assert(board_two_after_the_move == board_three)
