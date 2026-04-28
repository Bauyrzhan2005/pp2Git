import pygame, sys

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen.fill(WHITE)

color = BLACK
tool = "brush"
drawing = False
start_pos = None
brush_size = 5

def draw_menu():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, 50))

    texts = [
        ("B Brush", 10),
        ("R Rect", 120),
        ("C Circle", 230),
        ("E Eraser", 350),
        ("1 Black", 480),
        ("2 Red", 590),
        ("3 Green", 680),
        ("4 Blue", 790)
    ]

    for text, x in texts:
        img = font.render(text, True, BLACK)
        screen.blit(img, (x, 12))

running = True
while running:
    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Select tool and color
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            elif event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_1:
                color = BLACK
            elif event.key == pygame.K_2:
                color = RED
            elif event.key == pygame.K_3:
                color = GREEN
            elif event.key == pygame.K_4:
                color = BLUE

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            # Draw rectangle
            if tool == "rect":
                x1, y1 = start_pos
                x2, y2 = end_pos
                rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(screen, color, rect, 3)

            # Draw circle
            elif tool == "circle":
                x1, y1 = start_pos
                x2, y2 = end_pos
                radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, radius, 3)

    # Brush and eraser work while mouse is moving
    if drawing:
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[1] > 50:
            if tool == "brush":
                pygame.draw.circle(screen, color, mouse_pos, brush_size)
            elif tool == "eraser":
                pygame.draw.circle(screen, WHITE, mouse_pos, 15)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()