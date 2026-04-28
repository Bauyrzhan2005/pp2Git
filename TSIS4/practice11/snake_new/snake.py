import pygame
import sys
import random

pygame.init()

width = 600
height = 600
cell = 20

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

white = (255,0,0)
green = (0,255,0)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)

FOOD_TYPES = [
    {"name": "common", "color": red, "points": 1, "chance": 0.8, "timer": None},
    {"name": "gold", "color": (255, 215, 0), "points": 3, "chance": 0.5, "timer": None},
    {"name": "emerald", "color": (128, 0, 128), "points": 5, "chance": 0.2, "timer": 100} 
]

font = pygame.font.Font(None, 36)

snake = [(100,100), (80,100), (60,100)]
direction = (cell, 0)

score = 0
level = 1
speed = 5

foods_eaten = 0

walls = []
foods = []

def generate_food():
    while True:
        x = random.randrange(0, width, cell)
        y = random.randrange(0, height, cell)
        
        pos = (x, y)

        if pos not in snake and pos not in walls and pos not in [f["pos"] for f in foods]:
            if random.random() < 0.3:
                ftype = FOOD_TYPES[1]
            elif random.random() < 0.1:
                ftype = FOOD_TYPES[2]

            else:
                ftype = FOOD_TYPES[0]
            return {"pos": pos, "color": ftype["color"], "points": ftype["points"], "timer": ftype["timer"]}
        
        
        
for _ in range(3):
    foods.append(generate_food())

def draw_snake():
    for seg in snake:
        pygame.draw.rect(screen, green,(*seg, cell, cell))

def draw_food():
    for f in foods:
     if f["timer"] is not None and f["timer"] < 5 and f["timer"] % 2 == 0:
            continue
     pygame.draw.rect(screen, f["color"], (*f["pos"], cell, cell))

def draw_walls():
    for wall in walls:
        pygame.draw.rect(screen, blue, (*wall, cell, cell))

def upd_level():
    global level, speed, foods_eaten
    if foods_eaten >=3:
        level+=1
        speed+=1
        foods_eaten = 0
        add_walls()

def add_walls():
    for _ in range(5):
        x = random.randrange(0, width, cell)
        y = random.randrange(0, height, cell)
        
        if (x,y) not in snake:
            walls.append((x,y))
        
running = True

while running:
    clock.tick(10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP] and direction != (0, cell):
        direction = (0, -cell)
    if keys[pygame.K_DOWN] and direction != (0, -cell):
        direction = (0, cell)
    if keys[pygame.K_RIGHT] and direction != (-cell, 0):
        direction = (cell, 0)
    if keys[pygame.K_LEFT] and direction != (cell, 0):
        direction = (-cell, 0)
    
    head_x = snake[0][0] + direction[0]
    head_y = snake[0][1] + direction[1]
    new_head = (head_x, head_y)
    
    if (
        head_x < 0 or head_x >= width or 
        head_y < 0 or head_y >= height or 
        new_head in snake or
        new_head in walls
    ):
        running = False
        continue

    for f in foods[:]:
        if f["timer"] is not None: 
            f["timer"] -= 1
            if f["timer"] <= 0:
                foods.remove(f)
                foods.append(generate_food())
        
    snake.insert(0, new_head)

    eaten_food = None
    for f in foods:
        if new_head == f["pos"]:
            eaten_food = f
            break
    
    if eaten_food:
        score += eaten_food["points"]
        foods_eaten += 1
        foods.remove(eaten_food)
        foods.append(generate_food())
        upd_level()
    else:
        snake.pop()
        
    screen.fill(black)
    
    draw_snake()
    draw_food()
    draw_walls()
    
    score_text = font.render(f"Score : {score}", True, white)
    level_text = font.render(f"Level {level}", True, white)
    
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10,40))
    
    pygame.display.update()

pygame.quit()
sys.exit()