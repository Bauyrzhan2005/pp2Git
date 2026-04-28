import pygame, sys, random, os
from pygame.locals import *

pygame.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
SPEED, SCORE, COIN_SCORE = 5, 0, 0
FPS = 60

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer - Simple")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)


GRAY, RED, WHITE, YELLOW, GREEN, BLACK = (50,50,50), (200,0,0), (255,255,255), (255,215,0), (34,139,34), (0,0,0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(65, SCREEN_WIDTH-65), -100)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.spawn()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (15, 15), 14)
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(65, SCREEN_WIDTH-65), random.randint(-500, -50))

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT: self.spawn()

class Emerald(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (128, 0, 128), (15, 15), 14)
        self.points = 5
        self.rect = self.image.get_rect()
        self.rect.top = SCREEN_HEIGHT + 100 

    def spawn(self):
        if random.random() < 0.3:
            self.rect.center = (random.randint(65, SCREEN_WIDTH-65), -100)
        else:
            self.rect.center = (random.randint(65, SCREEN_WIDTH-65), -1000)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT: self.spawn()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        try:
            path = os.path.join(os.path.dirname(__file__), "sprites", "TopDownCar.png")
            img = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.rotate(pygame.transform.scale(img, (90, 50)), 90)
        except:
            self.image = pygame.Surface((45, 80)); self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(200, 520))
       
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 40: self.rect.move_ip(-5, 0)
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH-40: self.rect.move_ip(5, 0)


P1, E1, C1, EM1 = Player(), Enemy(), Coin(), Emerald()
enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)
emerald = pygame.sprite.Group(EM1)
all_sprites = pygame.sprite.Group(P1, E1, C1, EM1)

game_over = False
bg_y = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); sys.exit()
        if game_over and event.type == KEYDOWN and event.key == K_r:
            game_over, SCORE, COIN_SCORE, SPEED = False, 0, 0, 5
            P1.rect.center, E1.spawn(), C1.spawn(), EM1.spawn()

    if not game_over:
        
        bg_y = (bg_y + SPEED) % 80
        for s in all_sprites: s.move()
        
        if pygame.sprite.spritecollide(P1, coins, False):
            COIN_SCORE += 1
            C1.spawn()

        if pygame.sprite.spritecollide(P1, emerald, False):
            COIN_SCORE += 5
            EM1.spawn()

            if COIN_SCORE % 5 == 0:
              SPEED += 3
        
        if pygame.sprite.spritecollideany(P1, enemies):
            game_over = True

        
        DISPLAYSURF.fill(GREEN)
        pygame.draw.rect(DISPLAYSURF, GRAY, (40, 0, SCREEN_WIDTH-80, SCREEN_HEIGHT))
        for y in range(-80, SCREEN_HEIGHT + 80, 80):
            pygame.draw.rect(DISPLAYSURF, WHITE, (SCREEN_WIDTH//2-5, y + bg_y, 10, 40))

        for s in all_sprites: DISPLAYSURF.blit(s.image, s.rect)
        
        
        DISPLAYSURF.blit(font.render(f"Score: {SCORE}", True, WHITE), (10, 10))
        DISPLAYSURF.blit(font.render(f"Coins: {COIN_SCORE}", True, YELLOW), (SCREEN_WIDTH-110, 10))
    else:
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(font_big.render("CRASH", True, WHITE), (90, 200))
        DISPLAYSURF.blit(font.render("Press R to Restart", True, WHITE), (110, 300))

    pygame.display.update()
    clock.tick(FPS)