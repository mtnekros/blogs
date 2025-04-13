from typing import Literal

import pygame
from pygame.constants import K_UP
from pygame.key import ScancodeWrapper


def get_frame(sheet, frame_width, frame_height, index, top_offset: int, flip: bool = False):
    """Return a specific frame from a horizontal sprite sheet."""
    frame_rect = pygame.Rect(index * frame_width, top_offset, frame_width, frame_height)
    frame_image = sheet.subsurface(frame_rect).copy()
    if flip:
        frame_image = pygame.transform.flip(frame_image, True, False)
    return frame_image

AnimationType = Literal["running", "resting", "jumping"]
Direction = Literal["left", "right"]
class Animation:
    """Animation: handles player animation."""

    def __init__(self) -> None:
        """Initialize animation."""
        frame_width = 85
        frame_height = 100
        self.state: AnimationType = "resting"
        self.direction: Direction = "right"
        running_frames = [get_frame(sprite_sheet, frame_width, frame_height, i, 0) for i in range(6)]
        self.frames: dict[AnimationType, list] = {
            "resting": [ get_frame(sprite_sheet, frame_width, frame_height, i, 155) for i in range(2) ],
            "running": running_frames,
            "jumping": [ get_frame(sprite_sheet, frame_width, frame_height, i, 155) for i in range(2) ],
        }
        self.animation_speed: dict[AnimationType, float] = {
            "resting": 4,
            "running": 15,
            "jumping": 2,
        }
        self.i_frame = 0
        self.x = 100

        self.y = 450
        self.x_speed = 450
        self.y_speed = 0
        self.y_gravity = 60
        self.ground = 450
        self.is_jumping = False
        self.jumping_y_speed = -950
        self.jump_count = 0
        self.max_jumps = 2

    @property
    def curr_frames(self) -> list:
        """Return current animation state frames."""
        return self.frames[self.state]


    def update(self, pressed_keys: ScancodeWrapper, dt: float) -> None:
        """Update animation."""
        if pressed_keys[pygame.K_UP] and self.jump_count <= self.max_jumps:
            self.i_frame = 0
            self.is_jumping = True
            self.y_speed = self.jumping_y_speed
            self.jump_count += 1
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
        self.i_frame = self.i_frame + dt * self.animation_speed[self.state]
        if self.is_jumping:
            self.y_speed = self.y_speed+self.y_gravity
            self.y += self.y_speed * dt
        if self.y > self.ground:
            self.y_speed = 0
            self.y = self.ground
            self.is_jumping = False
            self.jump_count = 0

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the frame."""
        frame = self.curr_frames[int(self.i_frame) % len(self.curr_frames)]
        if self.direction == "left":
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, (self.x, self.y))

FRAME_RATE = 60
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

pygame.init()

sprite_sheet = pygame.image.load("./assets/player.png").convert_alpha()
anim = Animation()

running = True
color = (20, 20, 20)
while running:
    dt = clock.tick(FRAME_RATE) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            color = (0, 50 ,50)
        if event.type == pygame.KEYDOWN:
            color = (20, 20, 20)

    screen.fill(color)
    anim.update(pygame.key.get_pressed(), dt)
    anim.draw(screen)
    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.quit()

