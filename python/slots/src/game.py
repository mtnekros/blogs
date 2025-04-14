import pygame
from pygame import Rect, Vector2

from src.block import Block
from src.player import Player
from src.stats_overlay import StatsOverlay
from src.walker import Walker


class Game:
    """The game class used to run the game."""

    FRAME_RATE = 60
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 750
    CENTER_X = SCREEN_WIDTH // 2
    CENTER_Y = SCREEN_HEIGHT // 2
    GROUND_HEIGHT = 550
    BACKGROUND = "black"
    RECT = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    INITIAL_WALKER_COUNT = 10
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def __init__(self) -> None:
        """Initialize the game."""
        self.is_running = True
        # self.road = Road(width=350)
        self.walkers = []
        self.player = Player()
        self.add_walkers(count=Game.INITIAL_WALKER_COUNT)
        self.block = Block(100, Game.GROUND_HEIGHT)
        self.clock = pygame.time.Clock()
        self.stats_overlay = StatsOverlay(5, 5)

    def add_walkers(self, count: int=1) -> None:
        """Add walkers into the game."""
        for _ in range(count):
            self.walkers.append(
                Walker(Game.SCREEN_WIDTH/2, Game.SCREEN_HEIGHT/2)
            )

    def remove_walkers(self, count: int=1) -> None:
        """Remove walkers from the game."""
        for _ in range(count):
            if not self.walkers:
                print("No walkers to remove")
                return
            self.walkers.pop()

    def update(self, dt: float) -> None:
        """Update objects in the game.

        params dt(float): delta time passed since last time it was called.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.add_walkers(count=1)
                elif event.key == pygame.K_SPACE:
                    self.add_walkers(count=10)
                elif event.key == pygame.K_DOWN:
                    self.remove_walkers(count=1)
                elif event.key == pygame.K_DELETE:
                    self.remove_walkers(count=10)
        self.player.update(pygame.key.get_pressed(), dt)
        for walker in self.walkers:
            walker.update(dt, Game.RECT)
        self.stats_overlay.update(Game.FRAME_RATE, len(self.walkers))

    def draw(self) -> None:
        """Render the objects in the game."""
        self.screen.fill(Game.BACKGROUND)
        # self.road.draw(self.screen)
        for walker in self.walkers:
            walker.draw(self.screen)
        self.block.draw(self.screen)
        self.player.draw(self.screen)
        self.stats_overlay.draw(self.screen)

    def run(self) -> None:
        """Run the game loop."""
        pygame.init()
        while self.is_running:
            dt = self.clock.tick(Game.FRAME_RATE) / 1000.0
            self.update(dt)
            self.draw()
            pygame.display.flip()
        pygame.quit()



