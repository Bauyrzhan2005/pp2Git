import pygame
from clock import get_current_time_data, get_hand_position

pygame.init()

bg = pygame.image.load(r"C:\Users\Lenovo\Desktop\pp2\practice9\mickeys_clock\images\mickey_hand.png")
WIDTH = bg.get_width()
HEIGHT = bg.get_height()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")

CENTER = (WIDTH // 2, HEIGHT // 2)
SEC_LENGTH = int(WIDTH * 0.25)
MIN_LENGTH = int(HEIGHT * 0.15)

clock = pygame.time.Clock()
running = True

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    sec_angle, min_angle = get_current_time_data()
    screen.blit(bg, (0, 0))

    pygame.draw.line(screen, (0, 0, 0), CENTER, get_hand_position(CENTER, MIN_LENGTH, min_angle), 15)

    pygame.draw.line(screen, (255, 0, 0), CENTER, get_hand_position(CENTER, SEC_LENGTH, sec_angle), 10)

    pygame.draw.circle(screen, (0, 0, 0), CENTER, 15)

    pygame.display.flip()

    clock.tick(60)