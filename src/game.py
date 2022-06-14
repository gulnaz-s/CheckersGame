'''
This file handles everything related to conducting the game.
This class cannot be tested because it has Turtle object in the constructor.
'''

from drawing import (
    clear,
    check_cell_is_gray,
    draw_bottom_text,
    draw_top_text,
    screen_coord_to_board_coord,
)
from board import Board
from constants import (
    INITIAL_ROWS,
    NUM_SQUARES,
    MAX_RECURSION_DEPTH,
    PLAYER_COLOR_BLACK,
    PLAYER_COLOR_RED,
)
from piece import Piece


class Game:
    '''
        Class -- Game
            Represents game
        Attributes:
            board -- the board state at the beginning of the game
            a_turtle -- the Turtle object
            is_game_over -- True when the game is over. Otherwise, False.
            computer_last_moves -- tracks the moves of the computer
            active_piece -- a piece that was chosen by the user
            active_piece_locked -- True if the active piece can not be changed.
                Otherwise, False. Used to constrain player piece in subsequent
                turns of multiturn capturing moves.
            message -- a message to be shown in the UI (at the bottom)
            score -- the message with score of the game shown in the UI
                (at the top)
            player_allowed_moves -- all allowed moved for player
                (black pieces).
            draw -- draws the state of the game
        Methods:
            make_initial_position -- makes initial position of the game
            draw -- draws the state of the game with all text messages
            make_computer_move -- makes the computer move
            get_player_moves_for_position -- collects all possible moves
                for the piece
            handle_click -- Handles clicks in the UI, applies user and
                computer moves if needed
    '''
    def __init__(self, a_turtle):
        '''
            Constructor -- creates a new instance of Game
            Parameters:
                self -- the current Game object
                a_turtle -- the Turtle object
        '''
        self.board = Board(self.make_initial_position())
        self.a_turtle = a_turtle
        self.is_game_over = False
        self.computer_last_moves = []
        self.active_piece = None
        self.active_piece_moves = []
        self.active_piece_locked = False
        self.message = ""
        self.score = ""
        self.player_allowed_moves = (
            self.board.get_all_moves(PLAYER_COLOR_BLACK)
        )
        self.draw()

    def make_initial_position(self):
        '''
        Method -- make_initial_position
            Makes initial position of the game
        Parameter:
            self -- the current Game object
        Returns:
            The position of all pieces in dictionary, where the key is
            the coordinate of the piece on the board and the value is
            the Piece object
        '''
        result = {}
        for board_x in range(NUM_SQUARES):
            for board_y in range(INITIAL_ROWS):
                if check_cell_is_gray(board_x, board_y):
                    result[(board_x, board_y)] = (
                        Piece(board_x, board_y, PLAYER_COLOR_BLACK)
                    )
        for board_x in range(NUM_SQUARES):
            for board_y in range(NUM_SQUARES - INITIAL_ROWS, NUM_SQUARES):
                if check_cell_is_gray(board_x, board_y):
                    result[(board_x, board_y)] = (
                        Piece(board_x, board_y, PLAYER_COLOR_RED)
                    )
        return result

    def draw(self):
        '''
        Method -- draw
            Draws the state of the game with all text messages
        Parameter:
            self -- the current Game object
        '''
        clear(self.a_turtle)
        self.board.draw(self.a_turtle)
        for move in self.active_piece_moves:
            move.draw(self.a_turtle)
        for move in self.computer_last_moves:
            move.draw(self.a_turtle)
        draw_bottom_text(self.a_turtle, self.message)
        draw_top_text(self.a_turtle, self.board.get_text_score())

    def make_computer_move(self, options=None):
        '''
        Method -- make_computer_move
            Makes the computer move
        Parameter:
            self -- the current Game object
            options -- options for possible moves by the computer.
                Used to constrain move options for subsequent parts of
                multistep capturing move.
        '''
        best_move = self.board.optimal_move_red(options, MAX_RECURSION_DEPTH)
        if best_move is None:
            self.message = "You win"
            self.is_game_over = True
            self.draw()
            return
        self.board = self.board.apply_move(best_move)
        self.computer_last_moves.append(best_move)
        if best_move.is_capture():
            next_options = best_move.to_piece.get_capture_moves(self.board)
            if len(next_options) > 0:
                self.make_computer_move(next_options)

    def get_player_moves_for_position(self, board_x, board_y):
        '''
        Method -- get_player_moves_for_position
            Collects all possible moves for the piece
        Parameter:
            self -- the current Game object
            board_x -- x-coordinate in board format
            board_y -- y-coordinate in board format
        Returns:
            Allowed moves for piece in a particular position
        '''
        result = []
        for move in self.player_allowed_moves:
            if (
                move.from_piece.board_x == board_x and
                move.from_piece.board_y == board_y
            ):
                result.append(move)
        return result

    def handle_click(self, screen_x, screen_y):
        '''
        Method -- handle_click
            Handles clicks in the UI, applies user and computer moves if needed
        Parameter:
            self -- the current Game object
            screen_x -- x-coordinates of the click in screen format in px
            screen_y -- y-coordinates of the click in screen format in px
        '''
        if self.is_game_over:
            return
        board_x = screen_coord_to_board_coord(screen_x)
        board_y = screen_coord_to_board_coord(screen_y)
        if board_x is None or board_y is None:
            return
        clicked_piece = self.board.get_piece_at(board_x, board_y)
        if clicked_piece is not None:
            if clicked_piece.color != PLAYER_COLOR_BLACK:
                self.message = "You can't select opponent's pieces"
                self.draw()
                return
            if self.active_piece_locked:
                self.message = "You can't change piece now"
                self.draw()
                return
            if self.active_piece == clicked_piece:
                self.active_piece = None
                self.active_piece_moves = []
                return
            moves = self.get_player_moves_for_position(board_x, board_y)
            if len(moves) == 0:
                self.message = "There are no possible moves from this cell"
                self.draw()
                return
            self.computer_last_moves = []
            self.active_piece = clicked_piece
            self.active_piece_moves = moves
            self.active_piece_locked = False
            self.message = ""
        else:
            moved = False
            for move in self.active_piece_moves:
                if (
                    move.to_piece.board_x == board_x and
                    move.to_piece.board_y == board_y
                ):
                    self.board = self.board.apply_move(move)
                    next_capture_moves = (
                        move.to_piece.get_capture_moves(self.board)
                    )
                    if move.is_capture() and len(next_capture_moves) > 0:
                        self.active_piece = move.to_piece
                        self.active_piece_moves = next_capture_moves
                        self.active_piece_locked = True
                    else:
                        self.active_piece = None
                        self.active_piece_moves = []
                        self.active_piece_locked = False
                        self.computer_last_moves = []
                        self.make_computer_move()
                        self.player_allowed_moves = (
                            self.board.get_all_moves(PLAYER_COLOR_BLACK)
                        )
                        if len(self.player_allowed_moves) == 0:
                            self.message = "You lost"
                            self.is_game_over = True
                            self.draw()
                            return
                    moved = True
                    break
            if not moved:
                self.message = "This isn't a valid move"
        self.draw()
