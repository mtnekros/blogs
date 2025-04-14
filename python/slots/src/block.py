import pygame
from pygame import Rect
from pygame.surface import Surface


class Block:
    """The blocks on the ground."""

    def __init__(self, left: int, top: int) -> None:
        """Initialize the block."""
        width = 80
        height = 80
        self.rect = Rect(left, top, width, height)
        _sprite = pygame.image.load("./assets/grass_block.png").convert_alpha()
        self.sprite = pygame.transform.scale(_sprite, (width, height))

    def draw(self, screen: Surface) -> None:
        """Draw the block."""
        screen.blit(self.sprite, self.rect.topleft)
