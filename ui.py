"""Simple Pygame UI helpers."""
from __future__ import annotations

import pygame
from typing import Tuple

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)
LIGHT_GRAY = (180, 180, 180)
DARK_GRAY = (35, 35, 35)
GREEN = (40, 180, 90)
RED = (210, 65, 65)
YELLOW = (245, 205, 70)
BLUE = (70, 150, 245)


class Button:
    def __init__(self, rect: Tuple[int, int, int, int], text: str, font: pygame.font.Font,
                 bg=GRAY, hover=LIGHT_GRAY, fg=WHITE):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg = bg
        self.hover = hover
        self.fg = fg

    def draw(self, screen: pygame.Surface) -> None:
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover if self.rect.collidepoint(mouse_pos) else self.bg
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        label = self.font.render(self.text, True, self.fg)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event: pygame.event.Event) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_text(screen: pygame.Surface, text: str, font: pygame.font.Font, color, x: int, y: int,
              center: bool = False) -> None:
    label = font.render(text, True, color)
    rect = label.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(label, rect)
