from ChessProject.Move import *
# Represents pieces in the game


class Piece:
    def __init__(self, color):
        self.symbol = None
        self.color = color
        self.value = None

    def __repr__(self):
        return self.symbol

    def __str__(self):
        return self.symbol

    def __eq__(self, other):
        if not other or other == "*":
            return False
        return self.symbol == other.symbol

    def __ne__(self, other):
        return not self.__eq__(other)

    def moves_possible(self, i, board):
        raise NotImplementedError


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = piece_dictionary[color][Pawn]
        self.value = 10
        if color == WHITE:
            self.dir = north
        else:
            self.dir = south

    def moves_possible(self, i, board):
        moves_possible = []
        if not board.get_pos(i+self.dir) \
                and self.color == self.color:
            move = Move(i, i+self.dir, board)
            moves_possible.append(move)
        if no_end_conflict(i+east+self.dir, board, self.color) and \
                board.get_pos(i+east+self.dir):
            move = Move(i, i+east+self.dir, board)
            moves_possible.append(move)
        if no_end_conflict(i+west+self.dir, board, self.color) \
                and board.get_pos(i+west+self.dir):
            move = Move(i, i+west+self.dir, board)
            moves_possible.append(move)
        if (self.color == WHITE and int_to_tuple_ind(i)[1] == 1) \
                or (self.color == BLACK and int_to_tuple_ind(i)[1] == 6):
            if not board.get_pos(i+2*self.dir):
                move = Move(i, i+2*self.dir, board)
                moves_possible.append(move)
        return moves_possible


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = piece_dictionary[color][Knight]
        self.value = 32

    def moves_possible(self, i, board):
        return [Move(i, i1, board) for i1 in knight_dirs(i)
                if no_end_conflict(i1, board, self.color)]


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = piece_dictionary[color][Bishop]
        self.value = 33

    def moves_possible(self, i, board):
        return diag_to_edge(i, board, self.color)


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = piece_dictionary[color][Rook]
        self.value = 50

    def moves_possible(self, i, board):
        return line_to_edge(i, board, self.color)


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = piece_dictionary[color][Queen]
        self.value = 100

    def moves_possible(self, i, board):
        moves = []
        moves.extend(line_to_edge(i, board, self.color))
        moves.extend(diag_to_edge(i, board, self.color))
        return moves


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = piece_dictionary[color][King]
        self.value = 1000

    def king_castle_move(self, i, board):
        castle_moves = []
        if self.color == WHITE and i == 4:
            if not board.get_pos(i+east) \
                    and not board.get_pos(i+2*east) \
                    and board.get_pos(i+3*east) == Rook(WHITE):
                castle_moves.append(Move(i, i+2*east, board))
        elif self.color == BLACK and i == 60:
            if not board.get_pos(i+east) \
                    and not board.get_pos(i+2*east) \
                    and board.get_pos(i+3*east) == Rook(BLACK):
                castle_moves.append(Move(i, i+2*east, board))
        return castle_moves

    def queen_castle_move(self, i, board):
        castle_moves = []
        if self.color == WHITE and i == W_KING_START:
            if not board.get_pos(i+west) \
                    and not board.get_pos(i+2*west) and not board.get_pos(i+3*west) \
                    and board.get_pos(i+4*west) == Rook(WHITE):
                castle_moves.append(Move(i, i+2*west, board))
        elif self.color == BLACK and i == B_KING_START:
            if not board.get_pos(i+west) \
                    and not board.get_pos(i+2*west) and not board.get_pos(i+3*west) \
                    and board.get_pos(i+4*west) == Rook(BLACK):
                castle_moves.append(Move(i, i+2*west, board))
        return castle_moves

    def moves_possible(self, i, board):
        return [Move(i, i1, board) for i1 in king_dirs(i)
                if no_end_conflict(i1, board, self.color)]


def no_end_conflict(i, board, initial_color):
    if end_inbounds(i, board) \
            and (not board.get_pos(i) or board.get_pos(i).color != initial_color):
        return True
    return False


def line_to_edge(i, board, color):
    directions = [north, south, west, east]
    return moves_in_direction(i, board, color, directions)


def diag_to_edge(i, board, color):
    directions = [north+west, north+east, south+west, south+east]
    return moves_in_direction(i, board, color, directions)


def moves_in_direction(i, board, color, directions):
    squares_in_line = []
    for direction in directions:
        i_curr = i
        while end_inbounds(i_curr+direction, board):
            i_curr += direction
            square = board.get_pos(i_curr)
            if not square:
                squares_in_line.append(i_curr)
            elif square.color != color:
                squares_in_line.append(i_curr)
                break
            else:
                break
    return [Move(i, i1, board) for i1 in squares_in_line]


def knight_dirs(i):
    return [(i+2*north+west), (i+2*north+east), (i+2*south+west), (i+2*south+east),
            (i+north+2*west), (i+north+2*east), (i+south+2*west), (i+south+2*east)]


def king_dirs(i):
    return [(i+north), (i+north+east), (i+east), (i+south+east),
            (i+south), (i+south+west), (i+west), (i+north+west)]


WHITE = "white"
BLACK = "black"
W_KING_START = 114
B_KING_START = 30
W_ROOK_START_L = 26
W_ROOK_START_R = 33
B_ROOK_START_L = 110
B_ROOK_START_R = 117

piece_dictionary = {WHITE: {Pawn: "♙", Knight: "♘", Bishop: "♗", Rook: "♖", Queen: "♕", King: "♔"},
                    BLACK: {Pawn: "♟", Knight: "♞", Bishop: "♝", Rook: "♜", Queen: "♛", King: "♚"}}


rev_piece_dict = {"♙": Pawn(WHITE), "♘": Knight(WHITE), "♗": Bishop(WHITE),
                  "♖": Rook(WHITE), "♕": Queen(WHITE), "♔": King(WHITE),
                  "♟": Pawn(BLACK), "♞": Knight(BLACK), "♝": Bishop(BLACK),
                  "♜": Rook(BLACK), "♛": Queen(BLACK), "♚": King(BLACK)}
