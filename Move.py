

# a move object
class Move:
    # name in format a1-a2
    def __init__(self, start_pos, end_pos, board, resign_move=False):
        if not resign_move:
            self.start_pos = start_pos
            self.end_pos = end_pos
            self.board = board
            self.curr_player = board.get_pos(start_pos).color
            self.piece_moved = board.get_pos(start_pos)
            self.resign_move = False
        else:
            self.resign_move = True

    def get_piece(self):
        return self.piece_moved

    def get_color(self):
        return self.curr_player

    def is_resign_move(self):
        return self.resign_move

    def is_valid(self, board):
        i0 = self.start_pos
        i1 = self.end_pos
        if end_inbounds(i0, board) and end_inbounds(i1, board):
            return True
        return False

    def __eq__(self, other):
        return (self.start_pos == other.start_pos) and (self.end_pos == other.end_pos)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "[" + str(self.start_pos) + "-" + str(self.end_pos) + "]"

    def __str__(self):
        return "[" + str(self.start_pos) + "-" + str(self.end_pos) + "]"


north, south, east, west = 12, -12, 1, -1


def tuple_to_int_ind(tuple_coord):
    return int(tuple_coord[0]+12*tuple_coord[1]+26)


def int_to_tuple_ind(index_coord):
    x = (index_coord % 12)-2
    y = (index_coord-26)//12
    return x, y


def str_to_coord(two_char):
    return ord(two_char[0])-97, int(two_char[1])-1


def full_str_to_int_ind(four_char):
    start_pos = tuple_to_int_ind(str_to_coord(four_char[:2]))
    end_pos = tuple_to_int_ind(str_to_coord(four_char[3:5]))
    return start_pos, end_pos


def end_inbounds(i, board):
    return board.get_pos(i) != "*"




