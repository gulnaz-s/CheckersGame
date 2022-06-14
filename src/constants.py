'''
This file contains constants used by other classes for Checkers game.
'''

NUM_SQUARES = 8  # Number of squares in one row (column)
SQUARE_SIZE_PX = 50  # The size of the square in px

PIECE_RADIUS_PX = 20  # Radius of a piece in px
# Radius of an inner circle (distinction mark) for king piece
KING_CROWN_RADIUS_PX = 10
BOARD_PADDING_PX = 20
TEXT_SIZE_PX = 10
# Amount of rows (in a sequence starting from the top or bottom depending on
# the color) occupied by one piece color at the beginning of the game.
INITIAL_ROWS = 3
WINDOW_PADDING_PX = 20
# The search depth for the optimal moves.
# The bigger the number the harder the game.
MAX_RECURSION_DEPTH = 5
RED_TRACE_WIDTH = 1  # The width of trace after the reds move
BLACK_TRACE_WIDTH = 3  # The width of trace after the blacks move

TEXT_COLOR = "black"
BOARD_BORDER_COLOR = "black"
KING_CROWN_COLOR = "white"
BACKGROUND_COLOR = "white"
BLACKS_COLOR = "black"
REDS_COLOR = "dark red"
LIGHT_CELL_COLOR = "white"  # The color for light cells on the board
DARK_CELL_COLOR = "light gray"  # The color for dark cells on the board

PLAYER_COLOR_RED = "R"
PLAYER_COLOR_BLACK = "B"

TEXT_FONT = "Courier New"  # A font used to display text messages in the game
