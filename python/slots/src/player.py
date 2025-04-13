from typing import Literal

import pygame
from pygame.key import ScancodeWrapper

from src.animation import Animation, get_frame

Direction = Literal["right", "left"]
AnimationType = Literal["resting", "running", "jumping", "shooting"]
class Player:
    """Animation: handles player animation."""

    def __init__(self) -> None:
        """Initialize animation."""
        frame_width = 85
        frame_height = 100
        self.state: AnimationType = "resting"
        self.direction: Direction = "right"
        sprite_sheet = pygame.image.load("./assets/player.png").convert_alpha()
        running_frames = [get_frame(sprite_sheet, frame_width, frame_height, i, 0) for i in range(6)]
        resting_frames = [ get_frame(sprite_sheet, frame_width, frame_height, i, 155) for i in range(2) ]
        self.animations: dict[AnimationType, Animation] = {
            "resting": Animation(resting_frames, 1),
            "jumping": Animation(resting_frames, .7),
            "running": Animation(running_frames, 1)
        }
        self.x = 100
        self.y = 450
        self.x_speed = 450
        self.y_speed = 0
        self.y_gravity = 60
        self.ground = 450
        self.is_jumping = False
        self.jumping_y_speed = -950

    @property
    def current_animation(self) -> Animation:
        """Return current animation based on state."""
        return self.animations[self.state]

    def update(self, pressed_keys: ScancodeWrapper, dt: float) -> None:
        """Update animation."""
        if pressed_keys[pygame.K_UP] and not self.is_jumping:
            self.i_frame = 0
            self.is_jumping = True
            self.y_speed = self.jumping_y_speed
            self.animations["jumping"].reset()
        if pressed_keys[pygame.K_RIGHT]:
            self.state = "running"
            self.direction = "right"
            self.x += self.x_speed * dt
        elif pressed_keys[pygame.K_LEFT]:
            self.state = "running"
            self.direction = "left"
            self.x -= self.x_speed * dt
        else:
            self.state = "resting"
        if self.is_jumping:
            self.state = "jumping"
            self.y_speed = self.y_speed+self.y_gravity
            self.y += self.y_speed * dt
        if self.y > self.ground:
            self.y_speed = 0
            self.y = self.ground
            self.is_jumping = False
        self.current_animation.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the frame."""
        frame = self.current_animation.get_frame()
        if self.direction == "left":
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, (self.x, self.y))
