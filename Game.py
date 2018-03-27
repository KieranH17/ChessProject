from ChessProject.Pieces import *
from ChessProject.Move import *
from ChessProject.Board import *
import copy


class Game:
    # if game, basically fully copy the game state
    def __init__(self, game=None):
        if not game:
            self.turn_num = 1
            self.curr_player = WHITE
            self.legalmoves = []
            self.board = None
            self.in_check = False
            self.is_enpassant = False
            self.enpassant_moves = []
            self.kingside_castles_white = True
            self.queenside_castles_white = True
            self.kingside_castles_black = True
            self.queenside_castles_black = True
        else:
            self.turn_num = game.turn_num
            self.curr_player = game.curr_player
            self.legalmoves = game.legalmoves
            self.board = game.board.deep_copy()
            self.in_check = game.in_check
            self.is_enpassant = game.is_enpassant
            self.enpassant_moves = copy.deepcopy(game.enpassant_moves)
            self.kingside_castles_white = game.kingside_castles_white
            self.queenside_castles_white = game.queenside_castles_white
            self.kingside_castles_black = game.kingside_castles_black
            self.queenside_castles_black = game.queenside_castles_black

    def place_pieces(self):
        if self.board is None:
            self.board = Board()
            self.board.set_standard()

    def play(self, white, black):
        while True:
            self.board.print_board()

            self.legalmoves = self.findlegalmoves()
            if not self.legalmoves:
                if self.in_check:
                    print("Checkmate!")
                else:
                    print("Stalemate.")
                break

            if self.in_check:
                print(self.curr_player + " is in check")

            if self.curr_player == WHITE:
                move = white.my_move()
            else:
                move = black.my_move()

            if not move:
                print("Invalid input.")
                continue
            elif move.is_resign_move():
                print(self.curr_player + " resigned")
                break
            if not self.make_move(move, white, black):
                print("Invalid move.")

    def is_king_taken(self, checkee_color, checker_moves, board=None):
        if board is None:
            board = self.board
        for move in checker_moves:
            target_piece = board.get_pos(move.end_pos)
            if target_piece:
                king_piece = King(checkee_color)
                if target_piece == king_piece:
                    return True
        return False

    def islegalmove(self, move):
        return move in self.legalmoves

    def findlegalmoves(self, board=None, curr_player=None, can_be_checked=True, count_castles=True):
        if board is None:
            board = self.board
        if curr_player is None:
            curr_player = self.curr_player
        legalmoves = []
        moves_to_add = []
        for i in range(0, 144):
            if board.get_pos(i) == "*":
                continue
            potential_piece = board.get_pos(i)
            if potential_piece and potential_piece.color == curr_player:
                moves_to_add.extend(potential_piece.moves_possible(i, board))
                if potential_piece == King(curr_player) and count_castles:
                    castle_moves = potential_piece.king_castle_move(i, board)
                    if self.get_kingside_castles(curr_player) and not self.in_check\
                            and castle_moves:
                        inter_move_1 = Move(i, i+east, board)
                        if not self.will_be_check(inter_move_1, curr_player, board):
                            moves_to_add.extend(castle_moves)
                    castle_moves = potential_piece.queen_castle_move(i, board)
                    if self.get_queenside_castles(curr_player) and not self.in_check\
                            and castle_moves:
                        inter_move_1 = Move(i, i+west, board)
                        inter_move_2 = Move(i, i+2*west, board)
                        if not self.will_be_check(inter_move_1, curr_player, board) \
                                and not self.will_be_check(inter_move_2, curr_player, board):
                            moves_to_add.extend(castle_moves)

        if self.is_enpassant:
            moves_to_add.extend(self.enpassant_moves)
        if not can_be_checked:
            legalmoves.extend(moves_to_add)
        else:
            for move in moves_to_add:
                if not self.will_be_check(move, curr_player, board):
                    legalmoves.append(move)
        return legalmoves

    def will_be_check(self, move, curr_player, board):
        board_copy = board.deep_copy()
        board_copy.move_piece(move)

        next_player_turn = WHITE
        if curr_player == WHITE:
            next_player_turn = BLACK
        nextlegalmoves = self.findlegalmoves(board_copy, next_player_turn, False, False)
        return self.is_king_taken(curr_player, nextlegalmoves, board_copy)

    def get_kingside_castles(self, color):
        if color == WHITE:
            return self.kingside_castles_white
        else:
            return self.kingside_castles_black

    def get_queenside_castles(self, color):
        if color == WHITE:
            return self.queenside_castles_white
        else:
            return self.queenside_castles_black

    def set_kingside_castles(self, color, is_allowed):
        if color == WHITE:
            if is_allowed:
                self.kingside_castles_white = True
            else:
                self.kingside_castles_white = False
        else:
            if is_allowed:
                self.kingside_castles_black = True
            else:
                self.kingside_castles_black = False

    def set_queenside_castles(self, color, is_allowed):
        if color == WHITE:
            if is_allowed:
                self.queenside_castles_white = True
            else:
                self.queenside_castles_white = False
        else:
            if is_allowed:
                self.queenside_castles_black = True
            else:
                self.queenside_castles_black = False

    def make_move(self, move, white=None, black=None):
        if move.is_valid and self.islegalmove(move):
            # get rid of en passant'ed pawn
            if move in self.enpassant_moves:
                self.board.del_pos(move.start_pos-move.get_piece().dir)
            self.is_enpassant = False
            self.enpassant_moves = []

            self.check_castles(move)
            self.check_enpassant(move)

            self.board.move_piece(move)
            self.do_promotion(white, black)

            possible_next_moves = self.findlegalmoves(self.board, self.curr_player, False, False)
            if self.curr_player == BLACK:
                self.curr_player = WHITE
            else:
                self.curr_player = BLACK
            self.in_check = self.is_king_taken(self.curr_player, possible_next_moves)
            self.turn_num += 1
            return True
        return False

    def check_enpassant(self, move):
        start_pos = move.start_pos
        end_pos = move.end_pos
        # set en passant for next turn
        if move.get_piece() == Pawn(self.curr_player):
            if abs(start_pos - end_pos) == 2*north:
                other_player = WHITE
                if WHITE == self.curr_player:
                    other_player = BLACK
                left_square = self.board.get_pos(start_pos+west)
                if left_square == Pawn(other_player):
                    self.is_enpassant = True
                    pass_move = Move(start_pos+west, start_pos+left_square.dir, self.board)
                    self.enpassant_moves.append(pass_move)
                right_square = self.board.get_pos(start_pos+east)
                if right_square == Pawn(other_player):
                    self.is_enpassant = True
                    pass_move = Move(start_pos+east, start_pos+right_square.dir, self.board)
                    self.enpassant_moves.append(pass_move)

    # Accounts for rook and king movement on each move, updating caslte variables
    def check_castles(self, move):
        start_pos = move.start_pos
        end_pos = move.end_pos
        # account for rook/king castle movement
        if move.get_piece() == King(self.curr_player):
            self.set_kingside_castles(self.curr_player, False)
            self.set_queenside_castles(self.curr_player, False)
            if abs(start_pos - end_pos) == 2*west:
                if end_pos == W_KING_START+2*east:
                    self.board.set_pos(end_pos+west, Rook(self.curr_player))
                    self.board.del_pos(end_pos+east)
                else:
                    self.board.set_pos(end_pos+east, Rook(self.curr_player))
                    self.board.del_pos(end_pos+west)
        elif move.get_piece() == Rook(self.curr_player):
            if self.curr_player == WHITE:
                if start_pos == W_ROOK_START_L:
                    self.set_queenside_castles(self.curr_player, False)
                elif start_pos == W_ROOK_START_R:
                    self.set_kingside_castles(self.curr_player, False)
            if self.curr_player == BLACK:
                if start_pos == B_ROOK_START_L:
                    self.set_queenside_castles(self.curr_player, False)
                elif start_pos == B_ROOK_START_R:
                    self.set_kingside_castles(self.curr_player, False)

    def do_promotion(self, white=None, black=None):
        for i in range(0, 8):
            if self.curr_player == WHITE:
                if self.board.get_pos_tuple((i, 7)) == Pawn(WHITE):
                    if white:
                        choice = white.select_promotion()
                    else:
                        choice = '♕'
                    self.board.set_pos_tuple((i, 7), rev_piece_dict[choice])
            if self.curr_player == BLACK:
                if self.board.get_pos_tuple((i, 0)) == Pawn(BLACK):
                    if black:
                        choice = black.select_promotion()
                    else:
                        choice = '♛'
                    self.board.set_pos_tuple((i, 0), rev_piece_dict[choice])


WHITE = "white"
BLACK = "black"
