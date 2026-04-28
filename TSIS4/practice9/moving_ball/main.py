import pygame
from ball import Ball

pygame.init()

W = 800
H = 600

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Moving Ball")
clock = pygame.time.Clock()

ball = Ball(W//2, H//2, 25, 800, 600)

running = True
while True:

    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move(0, -20)
            elif event.key == pygame.K_DOWN:
                ball.move(0, 20)
            elif event.key == pygame.K_LEFT:
                ball.move(20, 0)
            elif event.key == pygame.K_RIGHT:
                ball.move(-20, 0)

    
    ball.draw(screen)
    pygame.display.flip()

    clock.tick(60)