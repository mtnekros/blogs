import math
import random
import sys
import time
from typing import Tuple, Type

import psutil
import pygame
from pygame import (
    Rect,
    Surface,
)
from pympler.asizeof import asizeof

import colors
from src.player import Player

random.seed(time.time())

USE_SLOTS = False

class Game:
    """The game class used to run the game."""

    FRAME_RATE = 60
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700
    CENTER_X = SCREEN_WIDTH // 2
    CENTER_Y = SCREEN_HEIGHT // 2
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
        self.stats_overlay.update(self.walkers)

    def draw(self) -> None:
        """Render the objects in the game."""
        self.screen.fill(Game.BACKGROUND)
        # self.road.draw(self.screen)
        for walker in self.walkers:
            walker.draw(self.screen)
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

class Vector:
    """2D Vector Class."""

    if USE_SLOTS:
        __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        """Initialize vector with x & y value."""
        self.x = x
        self.y = y

    def __iadd__(self, other: 'Vector') -> 'Vector':
        """Add vector with another vector."""
        self = self + other
        return self

    def __add__(self, other: 'Vector') -> 'Vector':
        """Add vector with another vector."""
        return Vector(
            self.x + other.x,
            self.y + other.y,
        )

    def __mul__(self, scalar: float) -> 'Vector':
        """Multiply vector with a scalar."""
        return Vector(
            self.x * scalar,
            self.y * scalar,
        )

    def length_squared(self) -> float:
        """Magnitude of vector squared."""
        return self.x ** 2 + self.y ** 2

    def length(self) -> float:
        """Magnitude of vector."""
        return math.sqrt(self.length_squared())

    def normalized(self) -> 'Vector':
        """Return a normalized unit vector."""
        length = self.length()
        if length == 0:
            return Vector(self.x, self.y)
        return Vector(
            self.x / length,
            self.y / length,
        )

    @classmethod
    def random_within_length(cls: Type['Vector'], min_length: float, max_length: float) -> 'Vector':
        """Get a random vector of a random magnitude."""
        length = random.random() * (max_length - min_length) + min_length  # noqa: S311
        random_vector = cls(
            random.choice([1, -1]) * random.random(), # noqa: S311
            random.choice([1, -1]) * random.random(), # noqa: S311
        )
        return random_vector.normalized() * length

class Walker:
    """The Fighter."""

    radius = 5
    border_width = 1
    outer_radius = radius + border_width
    color = colors.RYTHM
    border_color = "grey"

    if USE_SLOTS:
        __slots__ = ("pos", "vector")

    def __init__(self, x: float, y: float) -> None:
        """Create walker instance."""
        self.pos = Vector(x, y)
        self.vector = Vector.random_within_length(50, 100)

    @classmethod
    def create_at_random_pos(cls: Type['Walker'], screen_width: int, screen_height: int) -> 'Walker':
        """Create walker instance."""
        return cls(
            x=random.randint(Walker.outer_radius, screen_width-Walker.outer_radius),  # noqa: S311
            y=random.randint(Walker.outer_radius, screen_height-Walker.outer_radius),  # noqa: S311
        )

    @property
    def left(self) ->  float:
        """Left bound of the walker."""
        return self.pos.x - self.outer_radius

    @property
    def right(self) -> float:
        """Right bound of the walker."""
        return self.pos.x + self.outer_radius

    @property
    def top(self) -> float:
        """Top bound of the walker."""
        return self.pos.y - self.outer_radius

    @property
    def bottom(self) -> float:
        """Bottom bound of the walker."""
        return self.pos.y + self.outer_radius

    def update(self, dt: float, bbox: Rect) -> None:
        """Update the position of walker."""
        self.pos += self.vector * dt
        if self.left < bbox.left or self.right > bbox.right:
            self.vector.x *= -1
        if self.top < bbox.top or self.bottom > bbox.bottom:
            self.vector.y *= -1

        self.clamp(bbox)

    def clamp(self, bbox: Rect) -> None:
        """Clamp the walker inside the bounding box."""
        if self.left < bbox.left:
            self.pos.x = bbox.left + self.outer_radius
        if self.right > bbox.right:
            self.pos.x = bbox.right - self.outer_radius
        if self.top < bbox.top:
            self.pos.y = bbox.top + self.outer_radius
        if self.bottom > bbox.bottom:
            self.pos.y = bbox.bottom - self.outer_radius

    def draw(self, screen: Surface) -> None:
        """Draw the walker."""
        pygame.draw.circle(screen, self.border_color, (self.pos.x, self.pos.y), self.radius+self.border_width)
        pygame.draw.circle(screen, self.color, (self.pos.x, self.pos.y), self.radius)

class StatsOverlay:
    """Class to draw & update stats from the game."""

    pygame.font.init()
    background = colors.LIGHT
    font_color = "black"
    text_offset = 10
    y_offset = 20

    __slots__ = ("left", "top", "font", "stats")

    def __init__(self, left: float, top: float) -> None:
        """Initialize stats overlay position & fonts."""
        self.left = left
        self.top = top
        self.font =  pygame.font.SysFont(None, 24)
        self.stats = []

    def get_ram_usage(self) -> str:
        """Get ram usage."""
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_usage = memory_info.rss / (1024 * 1024) # Convert bytes to MB
        return f"{memory_usage:.2f} MB"

    def update(self, walkers: list[Walker]) -> None:
        """Update the stats."""
        self.stats = [
            f"Slots usage: {'Yes' if USE_SLOTS else 'No'}",
            f"Frame Rate: {Game.FRAME_RATE}",
            f"Walker Count: {len(walkers)}",
            f"RAM Usage: {self.get_ram_usage()}",
            f"Walker Memory (sys.getsizeof): {sys.getsizeof(walkers) / 1024:.2f} KB",
            f"Walker Memory (pympler): {asizeof(walkers) / 1024:.2f} KB",
        ]

    def get_estimate_size(self) -> Tuple[float, float]:
        """Return the size of the overlay based on stats text."""
        width = max(len(line) for line in self.stats) * 9
        height = len(self.stats) * 25
        return width, height

    def draw(self, screen: Surface) -> None:
        """Draw the stats on the screen."""
        overlay = Surface(self.get_estimate_size())
        overlay.set_alpha(180) # transparency
        overlay.fill("gray")
        y_offset = self.text_offset
        for line in self.stats:
            text = self.font.render(line, True, "black")
            overlay.blit(text, (self.left + self.text_offset, self.top + y_offset))
            y_offset += self.y_offset
        screen.blit(overlay, (self.left, self.top))



def main() -> None:
    """Entry point for the game."""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
