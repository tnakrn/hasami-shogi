# Author: Tina Kuran
# Date: 12/03/2021
# Description: CS162 Fall 2021 Portfolio Project - Hasami Shogi Game


class Board:
    """A class to represent the game board. Used by the HasamiShogiGame class."""

    def __init__(self):
        """Initializes the data members for the Board class. Takes no parameters.
        All data members are private.
        """
        self._board = {}
        self._rows = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

        # Populate the board with the initial starting position of all pieces.
        for letter in self._rows:
            if letter == "a":
                for i in range(1, 10):
                    self._board[letter + str(i)] = "RED"
            elif letter == "i":
                for i in range(1, 10):
                    self._board[letter + str(i)] = "BLACK"
            else:
                for i in range(1, 10):
                    self._board[letter + str(i)] = "NONE"

    def get_board(self):
        """Takes no parameters. Returns the game board. Used by the HasamiShogiGame
        class to get the game board.
        """
        return self._board

    def get_rows(self):
        """Takes no parameters. Returns the rows of board. Used by the HasamiShogiGame
        class to get the alphabet values of the rows.
        """
        return self._rows

    def update_board(self, start_square, end_square, piece_color):
        """Takes three parameters - strings that represent the square moved
        from and the square moved to, and a piece color. Updates the game
        board so that the piece that moves is removed from the start square,
        and the end square is updated with the piece. Used by HasamiShogiGame
        class to update the board.
        """
        self._board[start_square] = "NONE"
        self._board[end_square] = piece_color

    def empty_square(self, a_square):
        """Takes a string parameter that represents a square. Empties out that square on
        the board. Does not return a value.
        """
        self._board[a_square] = 'NONE'

    def print_board(self):
        """Takes no parameters. Prints out a visual representation of the board.
        Does not return a value. For personal use.
        """
        # Hard code column headers.
        print("   1  2  3  4  5  6  7  8  9")
        # Initialize an empty row for the board.
        a_row = ""

        for letter in self._rows:
            for i in range(1, 10):
                # For the first column in a row, add the letter so that we
                # have row labels a-h.
                if i == 1:
                    a_row += letter
                # Check if each square is "RED", "BLACK", or "NONE", and
                # populate squares accordingly.
                if self._board[letter + str(i)] == "RED":
                    a_row += "  R"
                elif self._board[letter + str(i)] == "BLACK":
                    a_row += "  B"
                else:
                    a_row += "  ."
            print(a_row)
            a_row = ""


class Piece:
    """A class to represent a piece in the game. Used by the HasamiShogiGame
    class.
    """

    def __init__(self, color):
        """Initializes the data members for the Piece class. Takes one parameter -
        color of the piece. All data members are private.
        """
        self._color = color

    def get_color(self):
        """Takes no parameters. Returns the color of a piece."""
        return self._color

    def set_color(self, piece_color):
        """Takes a parameter a color 'RED', 'BLACK', or 'NONE'. Updates the color
        of the piece.
        """
        self._color = piece_color


class HasamiShogiGame:
    """A class to represent the game Hasami Shogi. Uses the Board and Piece
    classes to access the game board and piece attributes.
    """

    def __init__(self):
        """Initializes the data members for the HasamiShogiGame class. Takes
        no parameters. All data members are private. The game should be "UNFINISHED"
        (in progress) when it starts. The first piece to go is "BLACK". Since neither
        player has had pieces captured when the game starts, captured pieces for both
        "RED" and "BLACK" should be 0. _players_switch is used when switching turns.
        """
        self._board = Board()
        self._game_state = "UNFINISHED"
        self._active_player = Piece("BLACK")
        self._num_captured_pieces = {"BLACK": 0,
                                     "RED": 0}
        self._players_switch = {"BLACK": Piece("RED"),
                                "RED": Piece("BLACK")}

    def get_game_state(self):
        """Takes no parameters and returns 'UNFINISHED', 'RED_WON' or
        'BLACK_WON'.
        """
        return self._game_state

    def set_game_state(self, winning_piece):
        """Takes one parameter 'BLACK_WON' or 'RED_WON' and updates the game_state."""
        self._game_state = winning_piece

    def get_active_player(self):
        """Takes no parameters and returns whose turn it is - either 'RED'
        or 'BLACK'.
        """
        return self._active_player.get_color()

    def set_active_player(self, piece_obj):
        """Takes one parameter, a Piece object with color either 'RED' or 'BLACK',
        and updates the active player. Does not return a value.
        """
        self._active_player = piece_obj

    def get_num_captured_pieces(self, piece_color):
        """Takes one parameter, 'RED' or 'BLACK', and returns the number
        of pieces of that color that have been captured. Returns None
        if the piece_color is not 'RED' or 'BLACK'.
        """
        if piece_color in self._num_captured_pieces:
            return self._num_captured_pieces[piece_color]

    def get_square_occupant(self, square_to_check):
        """Takes one parameter, a string representing a square (such as 'i7'),
        and returns 'RED', 'BLACK', or 'NONE', depending on whether the
        specified square is occupied by a red piece, a black piece, or
        neither. Returns None if the square does not exist on the board.
        """
        if square_to_check in self._board.get_board():
            return self._board.get_board()[square_to_check]

    def make_capture(self, active_piece_color, num_pieces_captured):
        """Takes two parameters - color of active piece 'RED' or 'BLACK', and the number of
        pieces captured of the opponent. Makes a capture and updates the num_captured_pieces
        for the pieces. Does not return a value.
        """
        if active_piece_color == "BLACK":
            self._num_captured_pieces["RED"] += num_pieces_captured
        else:
            self._num_captured_pieces["BLACK"] += num_pieces_captured

    def check_capture(self, end_square):
        """Takes one parameter - the end square. Checks whether or not there is a capture. If yes,
        calls the make_capture method. Does not return a value.
        """
        sides_captured = 0

        # If the next square to the right is the opponent, check for capture to the right.
        if int(end_square[1]) < 9 and \
                self._board.get_board()[end_square[0] + str(int(end_square[1]) + 1)] != 'NONE' and \
                self._board.get_board()[
                    end_square[0] + str(int(end_square[1]) + 1)] != self._active_player.get_color():
            next_column = int(end_square[1]) + 1
            next_square = end_square[0] + str(next_column)

            # While the square to the right is the opponent, continue to advance and check the
            # occupant of the square. Stop once you reach the edge of the board or another piece
            # of the same color (as the active player).
            while self._board.get_board()[next_square] != 'NONE' and \
                    self._board.get_board()[next_square] != self._active_player.get_color() and \
                    next_column <= 8:
                next_column += 1
                next_square = end_square[0] + str(next_column)

            # If you hit another piece of the same color as active player, count how many of opponents
            # pieces are in between end square and the square with the active player's color, and
            # make capture.
            if self._board.get_board()[next_square] == self._active_player.get_color():
                captured_pieces = 0
                for i in range(int(end_square[1]) + 1, next_column):
                    captured_pieces += 1
                    self._board.empty_square(end_square[0] + str(i))
                sides_captured += 1
                self.make_capture(self._active_player.get_color(), captured_pieces)

        # If the next square to the left is the opponent, check for capture to the left.
        if int(end_square[1]) > 1 and \
                self._board.get_board()[end_square[0] + str(int(end_square[1]) - 1)] != 'NONE' and \
                self._board.get_board()[
                    end_square[0] + str(int(end_square[1]) - 1)] != self._active_player.get_color():
            next_column = int(end_square[1]) - 1
            next_square = end_square[0] + str(next_column)

            # While the square to the left is the opponent, continue to advance and check the
            # occupant of the square. Stop once you reach the edge of the board or another piece
            # of the same color (as the active player).
            while self._board.get_board()[next_square] != 'NONE' and \
                    self._board.get_board()[next_square] != self._active_player.get_color() and \
                    next_column >= 2:
                next_column -= 1
                next_square = end_square[0] + str(next_column)

            # If you hit another piece of the same color as active player, count how many of opponents
            # pieces are in between end square and the square with the active player's color, and
            # make capture.
            if self._board.get_board()[next_square] == self._active_player.get_color():
                captured_pieces = 0
                for i in range(next_column + 1, int(end_square[1])):
                    captured_pieces += 1
                    self._board.empty_square(end_square[0] + str(i))
                sides_captured += 1
                self.make_capture(self._active_player.get_color(), captured_pieces)

        # Vertical captures.
        temp_1 = None
        temp_2 = None
        temp_3 = None
        for i in range(len(self._board.get_rows())):
            if self._board.get_rows()[i] == end_square[0]:
                temp_1 = i
                temp_2 = i + 1
                temp_3 = i - 1

        # If the next square down is the opponent, check for capture up.
        if temp_2 < 8 and \
                self._board.get_board()[self._board.get_rows()[temp_2] + end_square[1]] != 'NONE' and \
                self._board.get_board()[
                    self._board.get_rows()[temp_2] + end_square[1]] != self._active_player.get_color():
            next_row = self._board.get_rows()[temp_2]
            next_square = next_row + end_square[1]

            # While the square below is the opponent, continue to advance and check the
            # occupant of the square. Stop once you reach the edge of the board or another piece
            # of the same color (as the active player).
            while self._board.get_board()[next_square] != 'NONE' and \
                    self._board.get_board()[next_square] != self._active_player.get_color() and \
                    temp_2 <= 7:
                temp_2 += 1
                next_row = self._board.get_rows()[temp_2]
                next_square = next_row + end_square[1]

            # If you hit another piece of the same color as active player, count how many of opponents
            # pieces are in between end square and the square with the active player's color, and
            # make capture.
            if self._board.get_board()[next_square] == self._active_player.get_color():
                captured_pieces = 0
                for i in range(temp_1 + 1, temp_2):
                    captured_pieces += 1
                    self._board.empty_square(self._board.get_rows()[i] + end_square[1])
                sides_captured += 1
                self.make_capture(self._active_player.get_color(), captured_pieces)

        # If the next square up is the opponent, check for capture up.
        if sides_captured < 3 and \
                temp_3 > 0 and \
                self._board.get_board()[self._board.get_rows()[temp_3] + end_square[1]] != 'NONE' and \
                self._board.get_board()[
                    self._board.get_rows()[temp_3] + end_square[1]] != self._active_player.get_color():
            next_row = self._board.get_rows()[temp_3]
            next_square = next_row + end_square[1]

            # While the square above is the opponent, continue to advance and check the
            # occupant of the square. Stop once you reach the edge of the board or another piece
            # of the same color (as the active player).
            while self._board.get_board()[next_square] != 'NONE' and \
                    self._board.get_board()[next_square] != self._active_player.get_color() and \
                    temp_3 >= 1:
                temp_3 -= 1
                next_row = self._board.get_rows()[temp_3]
                next_square = next_row + end_square[1]

            # If you hit another piece of the same color as active player, count how many of opponents
            # pieces are in between end square and the square with the active player's color, and
            # make capture.
            if self._board.get_board()[next_square] == self._active_player.get_color():
                captured_pieces = 0
                for i in range(temp_3 + 1, temp_1):
                    captured_pieces += 1
                    self._board.empty_square(self._board.get_rows()[i] + end_square[1])
                sides_captured += 1
                self.make_capture(self._active_player.get_color(), captured_pieces)

        # There are only eight squares that would warrant checking for a corner capture.
        # If the end square is one of those eight squares, and the corner square contains
        # the opponent's piece, check for corner capture.
        corner_pairs = {"a2": ["b1", "a1"],
                        "a8": ["b9", "a9"],
                        "b1": ["a2", "a1"],
                        "b9": ["a8", "a9"],
                        "h1": ["i2", "i1"],
                        "h9": ["i8", "i9"],
                        "i2": ["h1", "i1"],
                        "i8": ["h9", "i9"]
                        }

        if sides_captured < 3 and end_square in corner_pairs:
            if self._board.get_board()[corner_pairs[end_square][0]] == self._active_player.get_color() and \
                    self._board.get_board()[corner_pairs[end_square][1]] != 'NONE' and \
                    self._board.get_board()[corner_pairs[end_square][1]] != self._active_player.get_color():
                sides_captured += 1
                self._board.empty_square(corner_pairs[end_square][1])
                self.make_capture(self._active_player.get_color(), 1)

    def check_win(self):
        """Takes no parameters. Checks the number of captured pieces for each
        piece to determine if a player has won or not. Updates the game_state
        if a win is determined. Does not return a value.
        """
        if self._num_captured_pieces["RED"] >= 8:
            self.set_game_state("BLACK_WON")
        elif self._num_captured_pieces["BLACK"] >= 8:
            self.set_game_state("RED_WON")

    def switch_active_player(self):
        """Takes no parameters. Switches the active player to the other color.
        Does not return a value.
        """
        self.set_active_player(self._players_switch[self._active_player.get_color()])

    def make_move(self, start_square, end_square):
        """Takes two parameters - strings that represent the square moved
        from and the square moved to. For example, make_move('b3', 'b9').
        If the square being moved from does not contain a piece belonging
        to the player whose turn it is, or if the indicated move is not
        legal, or if the game has already been won, then it should just
        return False. Otherwise it should make the indicated move, remove
        any captured pieces, update the game state if necessary, update
        whose turn it is, and return True.
        """
        # If the start square does not contain a piece belonging to the
        # active player.
        if self.get_square_occupant(start_square) != self._active_player.get_color():
            return False

        # If the piece tries to move in a way that is not horizontal or vertical.
        if start_square[0] != end_square[0] and \
                start_square[1] != end_square[1]:
            return False

        # If the game has already been won.
        if self.get_game_state() != "UNFINISHED":
            return False

        # If the start square or end square do not exist on the board.
        if start_square not in self._board.get_board() or \
                end_square not in self._board.get_board():
            return False

        # If the piece is trying to move horizontally but there is another
        # piece in between the start square and end square or end square is
        # occupied.
        if start_square[0] == end_square[0]:
            # Horizontally to the right.
            if int(start_square[1]) < int(end_square[1]):
                for i in range(int(start_square[1]) + 1, int(end_square[1]) + 1):
                    if self._board.get_board()[start_square[0] + str(i)] != "NONE":
                        return False
            # Horizontally to the left.
            else:
                for i in range(int(end_square[1]), int(start_square[1])):
                    if self._board.get_board()[end_square[0] + str(i)] != "NONE":
                        return False

        # If the piece is trying to move vertically but there is another
        # piece in between the start square and end square or end square is
        # occupied.
        if start_square[1] == end_square[1]:
            temp_1 = None
            temp_2 = None
            for i in range(len(self._board.get_rows())):
                if self._board.get_rows()[i] == start_square[0]:
                    temp_1 = i
                elif self._board.get_rows()[i] == end_square[0]:
                    temp_2 = i
            # Vertically down. Slice list from letter after the start row to the
            # end row letter.
            if start_square[0] < end_square[0]:
                temp_list = self._board.get_rows()[temp_1 + 1:temp_2 + 1]
            # Vertically up. Slice list from end row letter to one letter before
            # start row letter.
            else:
                temp_list = self._board.get_rows()[temp_2:temp_1]
            # Iterate through the sliced list to check for an occupied square.
            for j in range(len(temp_list)):
                if self._board.get_board()[temp_list[j] + start_square[1]] != "NONE":
                    return False

        # Otherwise make a legal move. Update board, check for captures, check for a win,
        # update the turn, and return True.
        self._board.update_board(start_square, end_square, self._active_player.get_color())
        self.check_capture(end_square)
        self.check_win()
        self.switch_active_player()
        return True
