'''
This file handles everything related to pieces in the game.
Only methods that do not have a Turtle as a parameter can be tested.
'''

from constants import PLAYER_COLOR_BLACK, PLAYER_COLOR_RED
from drawing import draw_piece
from move import Move

RED_STEPS = [(1, -1), (-1, -1)]
BLACK_STEPS = [(1, 1), (-1, 1)]
KING_STEPS = [(1, -1), (-1, -1), (1, 1), (-1, 1)]


class Piece:
    '''
        Class -- Piece
            Represents a piece in the game
        Attributes:
            board_x -- x-coordinate of the piece on the board
            board_y -- y-coordinate of the piece on the board
            color -- the color of the piece
            is_king -- if the piece is king type or not. False by default.
        Methods:
            check_is_inside -- checks if the coordinates of the piece are
                in the bound of the board
            maybe_promote_to_king -- promoted to king if it is required by
                the game rules
            move_by -- creates a new Piece by moving the current one by
                a provided offset
            draw -- draws piece
            get_allowed_steps -- looks for all available steps (move offsets)
                for this Piece object
            get_normal_moves -- looks for all available non-capture moves for
                this Piece object
            get_capture_moves -- looks for all available capture moves for
                this Piece object
    '''
    def __init__(self, board_x, board_y, color, is_king=False):
        '''
            Constructor -- creates a new instance of Piece
            Parameters:
                self -- the current Piece object
                board_x -- x-coordinate of the piece on the board
                board_y -- y-coordinate of the piece on the board
                color -- the color of the piece
                is_king -- if the piece is king type or not. False by default.
        '''
        self.board_x = board_x
        self.board_y = board_y
        self.color = color
        self.is_king = is_king

    def check_is_inside(self):
        '''
        Method -- check_is_inside
            Checks if the coordinates of the piece are in bound of the board
        Parameter:
            self -- the current Piece object
        Returns:
            True if the piece is in board bounds. Otherwise, False.
        '''
        return (
            0 <= self.board_x < 8
            and 0 <= self.board_y < 8
        )

    def maybe_promote_to_king(self):
        '''
        Method -- maybe_promote_to_king
            Promoted to king if it is required by the game rules
        Parameter:
            self -- the current Piece object
        Returns:
            True if the piece can be promoted to king. Otherwise, False.
        '''
        if self.color == PLAYER_COLOR_RED and self.board_y == 0:
            self.is_king = True
        if self.color == PLAYER_COLOR_BLACK and self.board_y == 7:
            self.is_king = True

    def move_by(self, board_dx, board_dy):
        '''
        Method -- move_by
            Creates a new Piece by moving the current one by a provided offset
        Parameter:
            self -- the current Piece object
            board_dx -- desired x-coordinate offset
            board_dy -- desired y-coordinate offset
        Returns:
            A new piece moved by a given offset, if it is inside the board (the
            move is allowed). Also promotes the piece to the king if it has
            reached the end of the board.
        '''
        next_piece = Piece(
            board_x=self.board_x + board_dx,
            board_y=self.board_y + board_dy,
            color=self.color,
            is_king=self.is_king,
        )
        if not next_piece.check_is_inside():
            return None
        next_piece.maybe_promote_to_king()
        return next_piece

    def draw(self, a_turtle):
        '''
        Method -- draw
            Draws the piece
        Parameter:
            self -- the current Piece object
            a_turtle -- the Turtle object
        '''
        draw_piece(
            a_turtle=a_turtle,
            board_x=self.board_x,
            board_y=self.board_y,
            is_black=(self.color == PLAYER_COLOR_BLACK),
            is_king=self.is_king,
        )

    def get_allowed_steps(self):
        '''
        Method -- get_allowed_steps
            Looks for all available steps (move offsets) for this Piece object
        Parameter:
            self -- the current Piece object
        Returns:
            All available steps for this Piece object
        '''
        if self.is_king:
            return KING_STEPS
        if self.color == PLAYER_COLOR_RED:
            return RED_STEPS
        return BLACK_STEPS

    def get_normal_moves(self, board):
        '''
        Method -- get_normal_moves
            Looks for all available non-capture moves for this Piece object
        Parameter:
            self -- the current Piece object
            board -- current Board object state
        Returns:
            All available moves for this Piece object that are not capturing
        '''
        result = []
        for dx, dy in self.get_allowed_steps():
            next_piece = self.move_by(dx, dy)
            if (
                next_piece is not None
                and board.get_piece_at(next_piece.board_x, next_piece.board_y)
                is None
            ):
                result.append(Move(
                    from_piece=self,
                    to_piece=next_piece,
                ))
        return result

    def get_capture_moves(self, board):
        '''
        Method -- get_capture_moves
            Looks for all available capture moves for this Piece object
        Parameter:
            self -- the current Piece object
            board -- current Board object state
        Returns:
            All available moves for this Piece object that are capturing
        '''
        result = []
        for dx, dy in self.get_allowed_steps():
            next_piece = self.move_by(dx * 2, dy * 2)
            jump_over_piece = board.get_piece_at(
                self.board_x + dx, self.board_y + dy
            )
            if (
                next_piece is not None
                and board.get_piece_at(next_piece.board_x, next_piece.board_y)
                is None
                and jump_over_piece is not None
                and jump_over_piece.color != self.color
            ):
                result.append(Move(
                    from_piece=self,
                    to_piece=next_piece,
                    remove=jump_over_piece,
                ))
        return result

    def __eq__(self, other):
        '''
            Method -- __eq__
                Checks if two objects are equal
            Parameters:
                self -- The current Piece object
                other -- An object to compare self to.
            Returns:
                True if the two objects are equal, False otherwise.
        '''
        if type(self) != type(other):
            return False
        return (
            self.board_x == other.board_x and
            self.board_y == other.board_y and
            self.color == other.color and
            self.is_king == other.is_king
        )
