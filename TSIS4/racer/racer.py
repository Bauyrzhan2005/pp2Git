import pygame, random, sys

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer with Coins")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
RED = (255, 0, 0)
YELLOW = (255, 215, 0)
BLUE = (0, 0, 255)

car = pygame.Rect(175, 500, 50, 80)
coins = []
score = 0
speed = 5

def create_coin():
    x = random.randint(40, WIDTH - 40)
    y = random.randint(-600, -50)
    return pygame.Rect(x, y, 25, 25)

for i in range(5):
    coins.append(create_coin())

running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Move car left and right
    if keys[pygame.K_LEFT] and car.left > 0:
        car.x -= 7
    if keys[pygame.K_RIGHT] and car.right < WIDTH:
        car.x += 7

    # Draw road lines
    for y in range(0, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (195, y, 10, 40))

    # Move and draw coins
    for coin in coins:
        coin.y += speed
        pygame.draw.ellipse(screen, YELLOW, coin)

        # If coin goes down, create new position
        if coin.top > HEIGHT:
            coin.x = random.randint(40, WIDTH - 40)
            coin.y = random.randint(-600, -50)

        # Check collision with car
        if car.colliderect(coin):
            score += 1
            coin.x = random.randint(40, WIDTH - 40)
            coin.y = random.randint(-600, -50)

    # Draw player car
    pygame.draw.rect(screen, BLUE, car)

    # Show collected coins
    text = font.render("Coins: " + str(score), True, WHITE)
    screen.blit(text, (WIDTH - 140, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()