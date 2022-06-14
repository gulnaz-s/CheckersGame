'''
This file handles everything related to drawing in the game.
Only methods that do not have a Turtle as a parameter can be tested.
The origin on the board is the lower left corner of the lower left cell.
'''

import math
import turtle

from constants import (
    BACKGROUND_COLOR,
    BOARD_BORDER_COLOR,
    BOARD_PADDING_PX,
    KING_CROWN_COLOR,
    KING_CROWN_RADIUS_PX,
    NUM_SQUARES,
    PIECE_RADIUS_PX,
    SQUARE_SIZE_PX,
    TEXT_COLOR,
    TEXT_SIZE_PX,
    TEXT_FONT,
    BLACK_TRACE_WIDTH,
    RED_TRACE_WIDTH,
    BLACKS_COLOR,
    REDS_COLOR,
    LIGHT_CELL_COLOR,
    DARK_CELL_COLOR
)


def board_coord_to_screen_coord_center(board_coord):
    '''
        Function -- board_coord_to_screen_coord_center
            Converts coordinate from the board format to screen format in px
        Parameters:
            board_coord -- coordinate on the board that is the center of square
        Returns:
            Coordinate in screen format in px
    '''
    return (
        SQUARE_SIZE_PX * (board_coord - (NUM_SQUARES / 2)) + SQUARE_SIZE_PX / 2
    )


def board_coord_to_screen_coord_corner(board_coord):
    '''
        Function -- board_coord_to_screen_coord_corner
            Converts coordinate from the board format to screen format in px
        Parameters:
            board_coord -- coordinate on the board that is the lower left
                corner of the cell
        Returns:
            Coordinate in screen format in px
    '''
    return SQUARE_SIZE_PX * (board_coord - (NUM_SQUARES / 2))


def screen_coord_to_board_coord(screen_coord):
    '''
        Function -- screen_coord_to_board_coord
            Converts coordinate from the screen format in px to board format
        Parameters:
            screen_coord -- coordinate from the screen in px
        Returns:
            Coordinate in board format or None if screen_coord is outside of
            the board
    '''
    result = math.floor(screen_coord / SQUARE_SIZE_PX + NUM_SQUARES / 2)
    if not (0 <= result < NUM_SQUARES):
        return None
    return result


def check_cell_is_gray(board_x, board_y):
    '''
        Function -- check_cell_is_gray
            Checks whether selected cell should be painted in gray
        Parameters:
            board_x -- coordinate of the cell in board format
            board_y -- coordinate of the cell in board format.
        Returns:
            True if cell should be gray. Otherwise, False.
    '''
    return board_x % 2 != board_y % 2


def draw_square(a_turtle, screen_x, screen_y, size, pen_color, fill_color):
    '''
        Function -- draw_square
            Draws a square
        Parameters:
            a_turtle -- a turtle used to draw
            screen_x -- x-coordinates for drawing starting point
                in screen format in px
            screen_y -- y-coordinates for drawing starting point
                in screen format in px
            size -- a size of the edge of the square
            pen_color -- the color of the edge of the square
            fill_color -- the filler color or None if no fill is needed
    '''
    RIGHT_ANGLE = 90
    a_turtle.setheading(0)
    a_turtle.setposition(screen_x, screen_y)
    a_turtle.pencolor(pen_color)
    if fill_color is not None:
        a_turtle.fillcolor(fill_color)
        a_turtle.begin_fill()
    a_turtle.pendown()
    for i in range(4):
        a_turtle.forward(size)
        a_turtle.left(RIGHT_ANGLE)
    if fill_color is not None:
        a_turtle.end_fill()
    a_turtle.penup()


def draw_circle(a_turtle, screen_x, screen_y, radius, pen_color, fill_color):
    '''
        Function -- draw_circle
            Draws a circle
        Parameters:
            a_turtle -- a turtle used to draw
            screen_x -- x-coordinates for circle center in screen format in px
            screen_y -- y-coordinates for circle center in screen format in px
            radius -- a desired radius of the circle
            pen_color -- the color of the edge of the circle
            fill_color -- the filler color or None if no fill is needed
    '''
    a_turtle.setheading(180)
    a_turtle.pencolor(pen_color)
    if fill_color is not None:
        a_turtle.fillcolor(fill_color)
    a_turtle.setposition(screen_x, screen_y + radius)
    a_turtle.pendown()
    if fill_color is not None:
        a_turtle.begin_fill()
    a_turtle.circle(radius)
    if fill_color is not None:
        a_turtle.end_fill()
    a_turtle.penup()


def draw_line(
    a_turtle,
    screen_x_from,
    screen_y_from,
    screen_x_to,
    screen_y_to,
    color,
    pen_size,
):
    '''
        Function -- draw_line
            Draws line
        Parameters:
            a_turtle -- a turtle used to draw
            screen_x_from -- x-coordinates for drawing starting point
                in screen format in px
            screen_y_from -- y-coordinates for drawing starting point
                in screen format in px
            screen_x_to -- x-coordinates for drawing ending point
                in screen format in px
            screen_y_to -- y-coordinates for drawing ending point
                in screen format in px
            color -- the color of the line
            pen_size -- width of the line
    '''
    a_turtle.setposition(screen_x_from, screen_y_from)
    a_turtle.pensize(pen_size)
    a_turtle.pencolor(color)
    a_turtle.pendown()
    a_turtle.setposition(screen_x_to, screen_y_to)
    a_turtle.penup()
    a_turtle.pensize(1)


def draw_text(
    a_turtle,
    text,
    screen_x,
    screen_y,
    color,
    size,
):
    '''
        Function -- draw_text
            Draws text message
        Parameters:
            a_turtle -- a turtle used to draw
            screen_x -- x-coordinates for text starting point in screen format
                in px
            screen_y -- y-coordinates for text starting point in screen format
                in px
            color -- the color of the text
            size -- size of letters
    '''
    a_turtle.setposition(screen_x, screen_y)
    a_turtle.pencolor(color)
    a_turtle.write(text, align="center", font=(TEXT_FONT, size, "bold"))


def draw_cell(a_turtle, board_x, board_y):
    '''
        Function -- draw_cell
            Draws a board cell
        Parameters:
            a_turtle -- a turtle used to draw
            board_x -- coordinate of the cell in board format
            board_y -- coordinate of the cell in board format
    '''
    screen_x = board_coord_to_screen_coord_corner(board_x)
    screen_y = board_coord_to_screen_coord_corner(board_y)
    is_gray = check_cell_is_gray(board_x, board_y)
    color = DARK_CELL_COLOR if is_gray else LIGHT_CELL_COLOR
    draw_square(
        a_turtle=a_turtle,
        screen_x=screen_x,
        screen_y=screen_y,
        size=SQUARE_SIZE_PX,
        pen_color=color,
        fill_color=color,
    )


def draw_board_border(a_turtle):
    '''
        Function -- draw_board_border
            Draws board border
        Parameters:
            a_turtle -- a turtle used to draw
    '''
    screen_x = board_coord_to_screen_coord_corner(0) - 1
    screen_y = board_coord_to_screen_coord_corner(0) - 1
    size = NUM_SQUARES * SQUARE_SIZE_PX + 2
    draw_square(
        a_turtle=a_turtle,
        screen_x=screen_x,
        screen_y=screen_y,
        size=size,
        pen_color=BOARD_BORDER_COLOR,
        fill_color=None,
    )


def draw_piece(a_turtle, board_x, board_y, is_black, is_king):
    '''
        Function -- draw_piece
            Draws a piece
        Parameters:
            a_turtle -- a turtle used to draw
            board_x -- coordinate of the cell in board format
            board_y -- coordinate of the cell in board format
            is_black -- if is_black is True, then the black piece
                will be drawn. Otherwise, red piece.
            is_king -- if is_king is True, then the king piece will be drawn.
                Otherwise, regular piece.
    '''
    screen_x = board_coord_to_screen_coord_center(board_x)
    screen_y = board_coord_to_screen_coord_center(board_y)
    color = BLACKS_COLOR if is_black else REDS_COLOR
    draw_circle(
        a_turtle=a_turtle,
        screen_x=screen_x,
        screen_y=screen_y,
        radius=PIECE_RADIUS_PX,
        pen_color=color,
        fill_color=color,
    )
    if is_king:
        draw_circle(
            a_turtle=a_turtle,
            screen_x=screen_x,
            screen_y=screen_y,
            radius=KING_CROWN_RADIUS_PX,
            pen_color=KING_CROWN_COLOR,
            fill_color=None,
        )


def draw_move(
    a_turtle,
    board_x_from,
    board_y_from,
    board_x_to,
    board_y_to,
    is_black,
):
    '''
        Function -- draw_move
            Draws a trace of the move
        Parameters:
            a_turtle -- a turtle used to draw
            board_x_from -- x-coordinates for drawing starting point
                in board format
            board_y_from -- y-coordinates for drawing starting point
                in board format
            board_x_to -- x-coordinates for drawing ending point
                in board format
            board_y_to -- y-coordinates for drawing ending point
                in board format
            is_black -- if is_black is True, then the black line will be drawn.
                Otherwise, red line.
    '''
    screen_x_from = board_coord_to_screen_coord_center(board_x_from)
    screen_y_from = board_coord_to_screen_coord_center(board_y_from)
    screen_x_to = board_coord_to_screen_coord_center(board_x_to)
    screen_y_to = board_coord_to_screen_coord_center(board_y_to)
    color = BLACKS_COLOR if is_black else REDS_COLOR
    pen_size = BLACK_TRACE_WIDTH if is_black else RED_TRACE_WIDTH
    draw_line(
        a_turtle=a_turtle,
        screen_x_from=screen_x_from,
        screen_y_from=screen_y_from,
        screen_x_to=screen_x_to,
        screen_y_to=screen_y_to,
        color=color,
        pen_size=pen_size,
    )


def draw_bottom_text(a_turtle, text):
    '''
        Function -- draw_bottom_text
            Draws bottom text message
        Parameters:
            a_turtle -- a turtle used to draw
            text -- the text to be written
    '''
    draw_text(
        a_turtle=a_turtle,
        text=text,
        screen_x=0,
        screen_y=(
            -(NUM_SQUARES * SQUARE_SIZE_PX) / 2 - (
                BOARD_PADDING_PX + TEXT_SIZE_PX
            )
        ),
        color=TEXT_COLOR,
        size=TEXT_SIZE_PX,
    )


def draw_top_text(a_turtle, text):
    '''
        Function -- draw_top_text
            Draws top text message
        Parameters:
            a_turtle -- a turtle used to draw
            text -- the text to be written
    '''
    draw_text(
        a_turtle=a_turtle,
        text=text,
        screen_x=0,
        screen_y=(NUM_SQUARES * SQUARE_SIZE_PX) / 2 + BOARD_PADDING_PX,
        color=TEXT_COLOR,
        size=TEXT_SIZE_PX,
    )


def clear(a_turtle):
    '''
        Function -- clear
            Clears the window
        Parameters:
            a_turtle -- a turtle used to draw
    '''
    full_size = (
        NUM_SQUARES * SQUARE_SIZE_PX + 4 * BOARD_PADDING_PX + 2 * TEXT_SIZE_PX
    )
    draw_square(
        a_turtle=a_turtle,
        screen_x=-full_size / 2,
        screen_y=-full_size / 2,
        size=full_size,
        pen_color=BACKGROUND_COLOR,
        fill_color=BACKGROUND_COLOR,
    )


def draw_empty_board(a_turtle):
    '''
        Function -- draw_empty_board
            Draws empty board
        Parameters:
            a_turtle -- a turtle used to draw
    '''
    draw_board_border(a_turtle)
    for board_x in range(NUM_SQUARES):
        for board_y in range(NUM_SQUARES):
            draw_cell(a_turtle, board_x, board_y)
