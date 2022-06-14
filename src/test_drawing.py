'''
This file contains tests for drawing.py.
'''

from drawing import (
    board_coord_to_screen_coord_center,
    board_coord_to_screen_coord_corner,
    screen_coord_to_board_coord,
    check_cell_is_gray
)
import math
import turtle


def test_board_coord_to_screen_coord_center():
    assert(board_coord_to_screen_coord_center(3) == -25)
    assert(board_coord_to_screen_coord_center(8) == 225)
    assert(board_coord_to_screen_coord_center(-5) == -425)
    assert(board_coord_to_screen_coord_center(0) == -175)


def test_board_coord_to_screen_coord_corner():
    assert(board_coord_to_screen_coord_corner(3) == -50)
    assert(board_coord_to_screen_coord_corner(8) == 200)
    assert(board_coord_to_screen_coord_corner(-5) == -450)
    assert(board_coord_to_screen_coord_corner(0) == -200)


def test_screen_coord_to_board_coord():
    assert(screen_coord_to_board_coord(-50) == 3)
    assert(screen_coord_to_board_coord(-200) == 0)
    assert(screen_coord_to_board_coord(200) is None)
    assert(screen_coord_to_board_coord(-450) is None)


def test_check_cell_is_gray():
    assert(check_cell_is_gray(2, 1))
    assert(check_cell_is_gray(4, 3))
    assert(check_cell_is_gray(3, 6))
    assert(check_cell_is_gray(6, 3))
    assert(check_cell_is_gray(8, 1))
    assert(check_cell_is_gray(8, 1))
    assert(check_cell_is_gray(1, 8))
    assert(not check_cell_is_gray(8, 8))
    assert(not check_cell_is_gray(1, 1))
    assert(not check_cell_is_gray(4, 6))
