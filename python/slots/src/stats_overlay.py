import psutil
import pygame
from pygame import Surface

import colors


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

    def update(self, frame_rate: int, walker_count: int) -> None:
        """Update the stats."""
        self.stats = [
            f"Frame Rate: {frame_rate}",
            f"Walker Count: {walker_count}",
            f"RAM Usage: {self.get_ram_usage()}",
        ]

    def get_estimate_size(self) -> tuple[float, float]:
        """Return the size of the overlay based on stats text."""
        padding = 10
        width = max(len(line) for line in self.stats) * 10 + padding
        height = len(self.stats) * 25 + padding
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


