from ChessProject.Game import *
from ChessProject.Player import *

# Python
import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))

class Main:
    def __init__(self):
        print("Welcome to Kieran's Chess Game")
        self.game = None
        self.run_game()

    def run_game(self):
        print("Press 'play' to select sides. Type 'quit' to exit.")
        while input().lower() != "quit":
            self.game = Game()
            print("Would you like white to be an 'AI' or 'human'?")
            if input().lower() == "human":
                white = Human(WHITE, self.game)
            else:
                white = AI(WHITE, self.game)
            print("Would you like black to be an 'AI' or 'human'?")
            if input().lower() == "human":
                black = Human(BLACK, self.game)
            else:
                black = AI(BLACK, self.game)
            print("Type moves in the format k#-k#. Type 'resign' to quit.")
            self.game.place_pieces()
            self.game.play(white, black)
            print("Game is over ...")
            print("Type 'continue' to play again, or 'quit' to exit.")


Main()
