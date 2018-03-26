from ChessProject.Board import *
from ChessProject.Move import *
from ChessProject.Game import Game
from ChessProject.Pieces import *
import sys


class Player:
    def __init__(self, color, game):
        self.color = color
        self.game = game

    def my_move(self):
        raise NotImplementedError


class Human(Player):
    def my_move(self):
        move_name = input()
        if move_name.lower() == "quit" or move_name.lower() == "resign":
            return Move(None, None, None, True)
        try:
            start_pos, end_pos = full_str_to_int_ind(move_name)
            move = Move(start_pos, end_pos, self.game.board)
            if move:
                return move
        except (ValueError, IndexError, KeyError):
            pass


class AI(Player):
    def __init__(self, color, game):
        super().__init__(color, game)
        self.next_best_move = None

    def my_move(self):
        game_copy = Game(self.game)
        self.find_move(True, 3, MIN_INT, MAX_INT, self.color, game_copy)
        return self.next_best_move

    # max player (white), min player (black)
    def find_move(self, save_move, depth, alpha, beta, player, game):
        move_value = 0
        best_move = None
        legal_moves = game.findLegalMoves()
        if depth == 0:
            return game.board.heuristic_score()
        if player == WHITE:
            curr_max = MIN_INT
            for move in legal_moves:
                game_version = Game(game)
                game_version.make_move(move)
                score = self.find_move(False, depth-1, alpha, beta, BLACK, game_version)
                if score > curr_max:
                    curr_max = score
                    best_move = move
                    alpha = max(score, alpha)
                    if alpha >= beta:
                        break
            move_value = curr_max
        elif player == BLACK:
            curr_min = MAX_INT
            for move in legal_moves:
                game_version = Game(game)
                game_version.make_move(move)
                score = self.find_move(False, depth-1, alpha, beta, WHITE, game_version)
                if score < curr_min:
                    curr_min = score
                    best_move = move
                    beta = min(score, beta)
                    if beta <= alpha:
                        break
            move_value = curr_min
        if save_move:
            self.next_best_move = best_move
        return move_value


MAX_INT = sys.maxsize
MIN_INT = -sys.maxsize - 1
WHITE = "white"
BLACK = "black"

WHITE_OPENING = ["d2-d4", "e2-e4", "b1-c3", "g1-f3", "c1-d2",
                 "c1-e3", "c1-f4", "c1-g5", "f1-e2", "f1-d3", "f1-c4"]
BLACK_OPENING = ["d7-d5", "e7-e5", "d7-d6", "e7-e6", "b8-c6", "g8-f6", "c8-d7",
                 "c8-e6", "c8-f5", "c8-g4", "f8-e7", "f8-d6", "f8-c5"]

