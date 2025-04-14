import random
from typing import Type

import pygame
from pygame import Rect, Surface

import colors
from src.vector import Vector


class Walker:
    """The Fighter."""

    radius = 5
    border_width = 1
    outer_radius = radius + border_width
    color = colors.RYTHM
    border_color = "grey"

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

