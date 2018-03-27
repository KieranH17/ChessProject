from ChessProject.Pieces import *


class Board:
    def __init__(self, board=None):
        if not board:
            self.contents = "************" \
                            "************" \
                            "**--------**" \
                            "**--------**" \
                            "**--------**" \
                            "**--------**" \
                            "**--------**" \
                            "**--------**" \
                            "**--------**" \
                            "**--------**" \
                            "************" \
                            "************"
        else:
            self.contents = board.contents

    def set_standard(self):
        piece_list = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for i in range(0, 8):
            j = START_INDEX + i
            self.set_pos(j+north, Pawn(WHITE))
            self.set_pos(j+6*north, Pawn(BLACK))
            self.set_pos(j, piece_list[i](WHITE))
            self.set_pos(j+7*north, piece_list[i](BLACK))

    def move_piece(self, move):
        self.set_pos(move.end_pos, self.get_pos(move.start_pos))
        self.del_pos(move.start_pos)

    def get_pos_tuple(self, tuple_coord):
        return self.get_pos(tuple_to_int_ind(tuple_coord))

    def get_pos(self, index):
        str_piece = self.contents[index]
        if str_piece == "-":
            return None
        if str_piece == "*":
            return str_piece
        return rev_piece_dict[str_piece]

    def set_pos_tuple(self, tuple_coord, piece=None):
        index = tuple_to_int_ind(tuple_coord)
        self.set_pos(index, piece)

    def set_pos(self, index, piece=None):
        if not piece:
            piece_symbol = "-"
        else:
            piece_symbol = piece.symbol
        self.contents = self.contents[:index] + piece_symbol + self.contents[index+1:144]

    def del_pos_tuple(self, tuple_coord):
        self.set_pos_tuple(tuple_coord)

    def del_pos(self, index):
        self.set_pos(index)

    def deep_copy(self):
        return Board(self)

    def print_board(self):
        for row in range(0, 8):
            print("  " + "-"*33)
            print(8 - row, end=" | ")
            for col in range(0, 8):
                item = self.get_pos_tuple((col, 7 - row))
                if not item:
                    item = " "
                print(str(item)+' |', end=" ")
            print()
        print("  " + "-"*33)
        print("    a | b | c | d | e | f | g | h |")
        # white tries to maximize, black tries to minimize score

    def heuristic_score(self):
        h_score = 0
        for piece_symbol in self.contents:
            if piece_symbol == "-" or piece_symbol == "*":
                piece = None
            else:
                piece = rev_piece_dict[piece_symbol]
            if piece:
                if piece.color == WHITE:
                    h_score += piece.value
                else:
                    h_score -= piece.value
        return h_score


START_INDEX = 26
