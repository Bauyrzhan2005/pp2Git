import pygame, random, sys

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake with Levels")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

snake = [(300, 300)]
direction = (CELL, 0)

score = 0
level = 1
speed = 8

def generate_food():
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        # Food must not appear on snake
        if (x, y) not in snake:
            return (x, y)

food = generate_food()

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Change snake direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL):
                direction = (0, -CELL)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                direction = (0, CELL)
            elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                direction = (CELL, 0)

    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # Check wall collision
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        running = False

    # Check collision with itself
    if new_head in snake:
        running = False

    snake.insert(0, new_head)

    # If snake eats food
    if new_head == food:
        score += 1
        food = generate_food()

        # Level up every 3 foods
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    # Draw snake
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], CELL, CELL))

    # Draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

    # Show score and level
    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()
sys.exit()