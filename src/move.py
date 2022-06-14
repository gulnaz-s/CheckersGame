'''
This file handles everything related to piece moves in the game.
Only methods that do not have a Turtle as a parameter can be tested.
'''

from constants import PLAYER_COLOR_BLACK
from drawing import draw_move


class Move:
    '''
        Class -- Move
            Represents moves in the game
        Attributes:
            from_piece -- the piece to be moved
            to_piece -- the piece after the move
            remove -- If a capturing move, then a piece object to be removed.
                    None otherwise.
        Methods:
            is_capture -- checks if the move is capture move
            draw -- draws the move trace
    '''
    def __init__(self, from_piece, to_piece, remove=None):
        '''
            Constructor -- creates a new instance of Move
            Parameters:
                self -- the current Move object
                from_piece -- the piece to be moved
                to_piece -- the piece after the move
                remove -- If a capturing move, then a piece object to be
                    removed. None otherwise.
        '''
        self.from_piece = from_piece
        self.to_piece = to_piece
        self.remove = remove

    def is_capture(self):
        '''
        Method -- is_capture
            Checks if the move is capture move
        Parameter:
            self -- the current Move object
        Returns:
            True if the move is capture move. Otherwise, False.
        '''
        return self.remove is not None

    def draw(self, turtle):
        '''
        Method -- draw
            Draws the move trace
        Parameter:
            self -- the current Move object
            turtle -- the Turtle object
        '''
        draw_move(
            a_turtle=turtle,
            board_x_from=self.from_piece.board_x,
            board_y_from=self.from_piece.board_y,
            board_x_to=self.to_piece.board_x,
            board_y_to=self.to_piece.board_y,
            is_black=self.from_piece.color == PLAYER_COLOR_BLACK,
        )

    def __eq__(self, other):
        '''
            Method -- __eq__
                Checks if two objects are equal
            Parameters:
                self -- The current Move object
                other -- An object to compare self to.
            Returns:
                True if the two objects are equal, False otherwise.
        '''
        if type(self) != type(other):
            return False
        return (
            self.from_piece == other.from_piece and
            self.to_piece == other.to_piece and
            self.remove == other.remove
        )
