import pygame
from pygame import (
    Rect,
    Surface,
)


def get_frame(
    sheet: Surface,
    frame_width: float,
    frame_height: float,
    index: int,
    top_offset: int,
    flip: bool = False,
) -> Surface:
    """Return a specific frame from a sprite sheet."""
    frame_rect = Rect(index * frame_width, top_offset, frame_width, frame_height)
    frame_image = sheet.subsurface(frame_rect).copy()
    if flip:
        frame_image = pygame.transform.flip(frame_image, True, False)
    return frame_image



class Animation:
    """Animation class that will hold the logic for cycling through the given frames."""

    def __init__(self, frames: list[Surface], duration_secs: float, cycle: bool=True) -> None:
        """Initialize animation."""
        self.frames = frames
        self.passed_duration = 0
        self.total_duration_secs = duration_secs
        self.cycle = cycle

    @property
    def is_running(self) -> bool:
        """Return if the animiation is running."""
        return self.passed_duration <= self.total_duration_secs

    def reset(self) -> None:
        """Reset animation."""
        self.passed_duration = 0

    def update(self, dt: float) -> None:
        """Update animation."""
        if self.is_running:
            self.passed_duration += dt

        if self.cycle and self.passed_duration >= self.total_duration_secs:
            self.passed_duration = 0

    def get_frame(self) -> Surface:
        """Return the current frame."""
        if self.is_running:
            i_frame = self.passed_duration / self.total_duration_secs * len(self.frames)
            return self.frames[int(i_frame)]
        return self.frames[-1]



