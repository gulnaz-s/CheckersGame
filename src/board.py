'''
This file handles everything related to board in the game.
Only methods that do not have a Turtle as a parameter and methods
that do not use random module can be tested.
'''

import random
from copy import copy

from constants import PLAYER_COLOR_BLACK, PLAYER_COLOR_RED
from drawing import draw_empty_board


class Board:
    '''
        Class -- Board
            Represents a board in the game with all pieces
        Attributes:
            pieces -- pieces state on the board in dictionary format,
                    where the key is the coordinate of the piece on the board
                    and the value is the Piece object
        Methods:
            get_all_moves -- checks for possible moves for this piece color
            get_normal_moves -- checks for moves for this piece color that
                are not capturing
            get_capture_moves -- checks for moves for this piece color that
                are capturing
            get_stats -- gets the statistics of how many blacks, reds,
                blacks kings and red kings are on the board now
            get_score -- computes the internal score of the game for this
                board state. The score represents the probable winner and is
                used for estimating the best computer move. A score less than
                one represents that black is more likely to win. A score more
                than one represents that red is more likely to win. A score of
                one represents equal chances for winning.
            get_text_score -- gets the score text for the UI.
            apply_move -- applies the provided move
            optimal_move_black -- finds an optimal move for black pieces
            optimal_move_red -- finds an optimal move for red pieces
            draw -- draws Board
            get_piece_at -- gets the piece at specified board location
    '''
    def __init__(self, pieces):
        '''
            Constructor -- creates a new instance of Board
            Parameters:
                self -- the current Board object
                pieces -- pieces state on the board in dictionary format,
                    where the key is the coordinate of the piece on the board
                    and the value is the Piece object
        '''
        self.pieces = pieces

    def get_all_moves(self, color):
        '''
        Method -- get_all_moves
            Checks for possible moves for this piece color
        Parameter:
            self -- the current Board object
            color -- color of pieces
        Returns:
            All possible moves this piece color can make in this turn
        '''
        capture_moves = self.get_capture_moves(color)
        if len(capture_moves) > 0:
            return capture_moves
        else:
            return self.get_normal_moves(color)

    def get_normal_moves(self, color):
        '''
        Method -- get_normal_moves
            Checks for moves for this piece color that are not capturing
        Parameter:
            self -- the current Board object
            color -- color of pieces
        Returns:
            All possible moves this piece color can make in this turn
            that are not capturing
        '''
        result = []
        for piece in self.pieces.values():
            if piece.color == color:
                result += piece.get_normal_moves(self)
        return result

    def get_capture_moves(self, color):
        '''
        Method -- get_capture_moves
            Checks for moves for this piece color that are capturing
        Parameter:
            self -- the current Board object
            color -- color of pieces
        Returns:
            All possible moves this piece color can make in this turn
            that are capturing
        '''
        result = []
        for piece in self.pieces.values():
            if piece.color == color:
                result += piece.get_capture_moves(self)
        return result

    def get_piece_at(self, board_x, board_y):
        '''
        Method -- get_piece_at
            Gets the piece at specified board location
        Parameter:
            self -- the current Board object
            board_x -- coordinate of the cell in board format
            board_y -- coordinate of the cell in board format
        Returns:
            Piece at specified board location or None if there is no piece
        '''
        return self.pieces.get((board_x, board_y))

    def get_stats(self):
        '''
        Method -- get_stats
            Gets the statistics of how many blacks, reds, blacks kings and
            red kings are on the board now
        Parameter:
            self -- the current Board object
        Returns:
            The Tuple with blacks, reds, blacks kings and reds king number
        '''
        blacks = 0
        reds = 0
        blacks_kings = 0
        reds_kings = 0
        for piece in self.pieces.values():
            if piece.color == PLAYER_COLOR_RED:
                reds += 1
                if piece.is_king:
                    reds_kings += 1
            else:
                blacks += 1
                if piece.is_king:
                    blacks_kings += 1
        return blacks, reds, blacks_kings, reds_kings

    def get_score(self):
        '''
        Method -- get_score
            Computes the internal score of the game for this board state.
            The score represents the probable winner and is used for estimating
            the best computer move. A score less than one represents that black
            is more likely to win. A score more than one represents that red is
            more likely to win. A score of one represents equal chances for
            winning.
        Parameter:
            self -- the current Board object
        Returns:
            The internal score of the game represented as a float number.
        '''
        blacks, reds, blacks_kings, reds_kings = self.get_stats()
        if reds == 0:
            return -10000000000
        if blacks == 0:
            return 10000000000
        return (reds + 2 * reds_kings) / (blacks + 2 * blacks_kings)

    def get_text_score(self):
        '''
        Method -- get_text_score
            Get the score text for the UI.
        Parameter:
            self -- the current Board object
        Returns:
            The text representation of the score of the game
        '''
        blacks, reds, blacks_kings, reds_kings = self.get_stats()
        return "     You   {:>2} ({}) : ({}) {:<2}   Computer".format(
            blacks, blacks_kings, reds_kings, reds
        )

    def apply_move(self, move):
        '''
        Method -- apply_move
            Applies the provided move
        Parameter:
            self -- the current Board object
            move -- the Move object
        Returns:
            The new Board object with the move applied
        '''
        next_pieces = copy(self.pieces)
        from_location = (move.from_piece.board_x, move.from_piece.board_y)
        next_pieces.pop(from_location)
        if move.remove is not None:
            remove_location = (move.remove.board_x, move.remove.board_y)
            next_pieces.pop(remove_location)
        to_location = (move.to_piece.board_x, move.to_piece.board_y)
        next_pieces[to_location] = move.to_piece
        return Board(next_pieces)

    def optimal_move_black(self, depth):
        '''
        Method -- optimal_move_black
            Finds an optimal move for black pieces
        Parameter:
            self -- the current Board object
            depth -- the search depth for the optimal moves
        Returns:
            Best move for black pieces
        '''
        min_score = 1000000000000
        best_moves = []
        options = self.get_all_moves(PLAYER_COLOR_BLACK)
        for move in options:
            next_board = self.apply_move(move)
            if depth > 0:
                if (
                    move.is_capture() and
                    move.to_piece.get_capture_moves(next_board)
                ):
                    next_opt_move = next_board.optimal_move_black(depth - 1)
                else:
                    next_opt_move = (
                        next_board.optimal_move_red(None, depth - 1)
                    )
                if next_opt_move is not None:
                    next_board = next_board.apply_move(next_opt_move)
            move_score = next_board.get_score()
            if move_score < min_score:
                min_score = move_score
                best_moves = [move]
            elif move_score == min_score:
                best_moves.append(move)
        if len(best_moves) == 0:
            return None
        return random.choice(best_moves)

    def optimal_move_red(self, options, depth):
        '''
        Method -- optimal_move_red
            Finds an optimal move for red pieces
        Parameter:
            self -- the current Board object
            options -- possible moves for red pieces
            depth -- the search depth for the optimal moves
        Returns:
            Best move for red pieces
        '''
        max_score = -1000000000000
        best_moves = []
        if options is None:
            options = self.get_all_moves(PLAYER_COLOR_RED)
        for move in options:
            next_board = self.apply_move(move)
            if depth > 0:
                if (
                    move.is_capture() and
                    move.to_piece.get_capture_moves(next_board)
                ):
                    next_opt_move = (
                        next_board.optimal_move_red(None, depth - 1)
                    )
                else:
                    next_opt_move = next_board.optimal_move_black(depth - 1)
                if next_opt_move is not None:
                    next_board = next_board.apply_move(next_opt_move)
            move_score = next_board.get_score()
            if move_score > max_score:
                max_score = move_score
                best_moves = [move]
            elif move_score == max_score:
                best_moves.append(move)
        if len(best_moves) == 0:
            return None
        return random.choice(best_moves)

    def draw(self, a_turtle):
        '''
        Method -- draw
            Draws Board
        Parameter:
            self -- the current Board object
            a_turtle -- the Turtle object
        '''
        draw_empty_board(a_turtle)
        for piece in self.pieces.values():
            piece.draw(a_turtle)

    def __eq__(self, other):
        '''
            Method -- __eq__
                Checks if two objects are equal
            Parameters:
                self -- The current Board object
                other -- An object to compare self to.
            Returns:
                True if the two objects are equal, False otherwise.
        '''
        if type(self) != type(other):
            return False
        return self.pieces == other.pieces
