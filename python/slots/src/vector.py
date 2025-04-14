import math
import random
from typing import Type


class Vector:
    """2D Vector Class."""

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



