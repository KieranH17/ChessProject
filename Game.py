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
            self.legalMoves = []
            self.board = None
            self.inCheck = False
            self.isEnPassant = False
            self.enPassantMoves = []
            self.kingside_castles_white = True
            self.queenside_castles_white = True
            self.kingside_castles_black = True
            self.queenside_castles_black = True
        else:
            self.turn_num = game.turn_num
            self.curr_player = game.curr_player
            self.legalMoves = game.legalMoves
            self.board = game.board.deep_copy()
            self.inCheck = game.inCheck
            self.isEnPassant = game.isEnPassant
            self.enPassantMoves = copy.deepcopy(game.enPassantMoves)
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

            self.legalMoves = self.findLegalMoves()
            if not self.legalMoves:
                if self.inCheck:
                    print("Checkmate!")
                else:
                    print("Stalemate.")
                break

            if self.inCheck:
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
            if not self.make_move(move):
                print("Invalid move.")

            self.do_promotion(white, black)

    def is_king_taken(self, checkee_color, checker_moves, board=None):
        if board is None:
            board = self.board
        for move in checker_moves:
            targetPiece = board.get_pos(move.end_pos)
            if targetPiece:
                kingPiece = King(checkee_color)
                if targetPiece == kingPiece:
                    return True
        return False

    def isLegalMove(self, move):
        return move in self.legalMoves

    def findLegalMoves(self, board=None, curr_player=None, can_be_checked=True, count_castles=True):
        if board is None:
            board = self.board
        if curr_player is None:
            curr_player = self.curr_player
        legalMoves = []
        movesToAdd = []
        for i in range(0, 144):
            if board.get_pos(i) == "*":
                continue
            potential_piece = board.get_pos(i)
            if potential_piece and potential_piece.color == curr_player:
                movesToAdd.extend(potential_piece.moves_possible(i, board))
                if potential_piece == King(curr_player) and count_castles:
                    castle_moves = potential_piece.king_castle_move(i, board)
                    if self.get_kingside_castles(curr_player) and not self.inCheck\
                            and castle_moves:
                        inter_move_1 = Move(i, i+east, board)
                        if not self.will_be_check(inter_move_1, curr_player, board):
                            movesToAdd.extend(castle_moves)
                    castle_moves = potential_piece.queen_castle_move(i, board)
                    if self.get_queenside_castles(curr_player) and not self.inCheck\
                            and castle_moves:
                        inter_move_1 = Move(i, i+west, board)
                        inter_move_2 = Move(i, i+2*west, board)
                        if not self.will_be_check(inter_move_1, curr_player, board) \
                                and not self.will_be_check(inter_move_2, curr_player, board):
                            movesToAdd.extend(castle_moves)

        if self.isEnPassant:
            movesToAdd.extend(self.enPassantMoves)
        if not can_be_checked:
            legalMoves.extend(movesToAdd)
        else:
            for move in movesToAdd:
                if not self.will_be_check(move, curr_player, board):
                    legalMoves.append(move)
        return legalMoves

    def will_be_check(self, move, curr_player, board):
        board_copy = board.deep_copy()
        board_copy.move_piece(move)

        nextPlayerTurn = WHITE
        if curr_player == WHITE:
            nextPlayerTurn = BLACK
        nextLegalMoves = self.findLegalMoves(board_copy, nextPlayerTurn, False, False)
        return self.is_king_taken(curr_player, nextLegalMoves, board_copy)

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

    def make_move(self, move):
        if move.is_valid and self.isLegalMove(move):
            # get rid of en passant'ed pawn
            if move in self.enPassantMoves:
                self.board.del_pos(move.start_pos-move.get_piece().dir)
            self.isEnPassant = False
            self.enPassantMoves = []

            self.check_castles(move)
            self.check_enpassant(move)

            self.board.move_piece(move)

            possible_next_moves = self.findLegalMoves(self.board, self.curr_player, False, False)
            if self.curr_player == BLACK:
                self.curr_player = WHITE
            else:
                self.curr_player = BLACK
            self.inCheck = self.is_king_taken(self.curr_player, possible_next_moves)
            self.turn_num += 1
            return True
        return False

    def check_enpassant(self, move):
        start_pos = move.start_pos
        end_pos = move.end_pos
        # set en passant for next turn
        if move.get_piece() == Pawn(self.curr_player):
            if abs(start_pos - end_pos) == 2*north:
                otherPlayer = WHITE
                if WHITE == self.curr_player:
                    otherPlayer = BLACK
                left_square = self.board.get_pos(start_pos+west)
                if left_square == Pawn(otherPlayer):
                    self.isEnPassant = True
                    passMove = Move(start_pos+west,
                                    start_pos+left_square.dir, self.board)
                    self.enPassantMoves.append(passMove)
                right_square = self.board.get_pos(start_pos+east)
                if right_square == Pawn(otherPlayer):
                    self.isEnPassant = True
                    passMove = Move(start_pos+east,
                                    start_pos+right_square.dir, self.board)
                    self.enPassantMoves.append(passMove)

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

    def do_promotion(self, white, black):
        for i in range(0, 8):
            if self.curr_player == WHITE:
                if self.board.get_pos_tuple((i, 7)) == Pawn(WHITE):
                    print("Which piece would you like to promote to: '♘', '♗', '♖', or '♕'?")
                    print("(Copy paste the exact symbol as input).")
                    choice = white.select_promotion()
                    while choice not in ['♘', '♗', '♖', '♕']:
                        print("Invalid selection. Try again.")
                        choice = white.select_promotion()
                    self.board.set_pos_tuple((i, 7), rev_piece_dict[choice])
            if self.curr_player == BLACK:
                if self.board.get_pos_tuple((i, 0)) == Pawn(BLACK):
                    print("Which piece would you like to promote to: '♞', '♝', '♜', or '♛'?")
                    print("(Copy paste the exact symbol as input).")
                    while choice not in ['♞', '♝', '♜', '♛']:
                        print("Invalid selection. Try again.")
                        choice = black.select_promotion()
                    self.board.set_pos_tuple((i, 0), rev_piece_dict[choice])


WHITE = "white"
BLACK = "black"
