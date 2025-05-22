import random
import time

from src.game import Game

random.seed(time.time())

def main() -> None:
    """Entry point for the game."""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
