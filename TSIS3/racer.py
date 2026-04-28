"""Racer game logic: traffic, obstacles, power-ups, scoring and race progress."""
from __future__ import annotations

import random
import pygame

from ui import WHITE, BLACK, GRAY, DARK_GRAY, GREEN, RED, YELLOW, BLUE, draw_text

WIDTH, HEIGHT = 500, 700
FPS = 60
ROAD_LEFT = 90
ROAD_WIDTH = 320
LANES = 4
LANE_WIDTH = ROAD_WIDTH // LANES
LANE_CENTERS = [ROAD_LEFT + LANE_WIDTH // 2 + i * LANE_WIDTH for i in range(LANES)]
FINISH_DISTANCE = 5000

CAR_COLORS = {
    "Blue": (40, 130, 255),
    "Red": (230, 65, 65),
    "Green": (45, 190, 100),
    "Yellow": (245, 210, 70),
}

DIFFICULTY = {
    "Easy": {"traffic": 1400, "obstacle": 1700, "speed": 4.0},
    "Normal": {"traffic": 1000, "obstacle": 1300, "speed": 5.0},
    "Hard": {"traffic": 750, "obstacle": 950, "speed": 6.0},
}


class GameObject:
    def __init__(self, lane: int, y: int, w: int, h: int, kind: str):
        self.lane = lane
        self.rect = pygame.Rect(0, y, w, h)
        self.rect.centerx = LANE_CENTERS[lane]
        self.kind = kind
        self.value = 0
        self.spawn_time = pygame.time.get_ticks()
        self.vx = 0

    def update(self, speed: float) -> None:
        self.rect.y += int(speed)
        if self.kind == "moving_barrier":
            self.rect.x += self.vx
            if self.rect.left < ROAD_LEFT or self.rect.right > ROAD_LEFT + ROAD_WIDTH:
                self.vx *= -1

    def off_screen(self) -> bool:
        return self.rect.top > HEIGHT + 50


def safe_lane(player_rect: pygame.Rect) -> int:
    distances = [(abs(player_rect.centerx - center), i) for i, center in enumerate(LANE_CENTERS)]
    distances.sort()
    player_lane = distances[0][1]
    choices = [i for i in range(LANES) if i != player_lane]
    return random.choice(choices)


def spawn_y_clear(objects, lane: int) -> bool:
    for obj in objects:
        if obj.lane == lane and obj.rect.y < 120:
            return False
    return True


class RacerGame:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, settings: dict, username: str):
        self.screen = screen
        self.clock = clock
        self.settings = settings
        self.username = username
        self.font = pygame.font.SysFont("arial", 24)
        self.small = pygame.font.SysFont("arial", 18)
        self.big = pygame.font.SysFont("arial", 44, bold=True)
        self.reset()

    def reset(self) -> None:
        self.player = pygame.Rect(0, HEIGHT - 120, 42, 70)
        self.player.centerx = LANE_CENTERS[1]
        self.objects = []
        self.coins = []
        self.powerups = []
        self.road_marks_y = 0
        base = DIFFICULTY.get(self.settings.get("difficulty", "Normal"), DIFFICULTY["Normal"])
        self.speed = base["speed"]
        self.base_speed = base["speed"]
        self.traffic_interval = base["traffic"]
        self.obstacle_interval = base["obstacle"]
        self.coin_interval = 850
        self.powerup_interval = 5000
        self.last_traffic = 0
        self.last_obstacle = 0
        self.last_coin = 0
        self.last_powerup = 0
        self.distance = 0
        self.coin_score = 0
        self.score = 0
        self.shield = False
        self.active_power = None
        self.active_until = 0
        self.game_over = False
        self.finished = False
        self.crashes_saved = 0

    def run(self) -> str:
        while True:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        self.move_player(-1)
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.move_player(1)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.x -= 5
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.x += 5
            self.player.left = max(self.player.left, ROAD_LEFT + 5)
            self.player.right = min(self.player.right, ROAD_LEFT + ROAD_WIDTH - 5)

            self.update(dt)
            self.draw()
            pygame.display.flip()

            if self.game_over or self.finished:
                return "finished"

    def move_player(self, direction: int) -> None:
        nearest_lane = min(range(LANES), key=lambda i: abs(self.player.centerx - LANE_CENTERS[i]))
        new_lane = max(0, min(LANES - 1, nearest_lane + direction))
        self.player.centerx = LANE_CENTERS[new_lane]

    def current_level(self) -> int:
        return int(self.distance // 700)

    def update(self, dt: int) -> None:
        now = pygame.time.get_ticks()
        level = self.current_level()
        speed_bonus = min(level * 0.35, 3.5)
        self.speed = self.base_speed + speed_bonus

        if self.active_power == "Nitro":
            if now < self.active_until:
                self.speed += 3.0
            else:
                self.active_power = None

        self.distance += self.speed * dt / 25
        if self.distance >= FINISH_DISTANCE:
            self.finished = True

        traffic_rate = max(380, self.traffic_interval - level * 80)
        obstacle_rate = max(450, self.obstacle_interval - level * 70)

        if now - self.last_traffic > traffic_rate:
            self.spawn_traffic()
            self.last_traffic = now
        if now - self.last_obstacle > obstacle_rate:
            self.spawn_obstacle()
            self.last_obstacle = now
        if now - self.last_coin > self.coin_interval:
            self.spawn_coin()
            self.last_coin = now
        if now - self.last_powerup > self.powerup_interval:
            self.spawn_powerup()
            self.last_powerup = now

        for collection in (self.objects, self.coins, self.powerups):
            for obj in collection:
                obj.update(self.speed)
            collection[:] = [obj for obj in collection if not obj.off_screen()]

        # power-ups timeout if not collected
        self.powerups[:] = [p for p in self.powerups if now - p.spawn_time < 6000]

        self.handle_collisions()
        self.score = int(self.distance * 0.5 + self.coin_score + self.crashes_saved * 150)

    def spawn_traffic(self) -> None:
        lane = safe_lane(self.player)
        if not spawn_y_clear(self.objects, lane):
            return
        car = GameObject(lane, -90, 44, 72, "traffic")
        self.objects.append(car)

    def spawn_obstacle(self) -> None:
        lane = safe_lane(self.player)
        if not spawn_y_clear(self.objects, lane):
            return
        kind = random.choice(["barrier", "oil", "pothole", "speed_bump", "moving_barrier", "boost_strip"])
        if kind == "moving_barrier":
            obj = GameObject(lane, -40, 70, 26, kind)
            obj.vx = random.choice([-2, 2])
        elif kind == "boost_strip":
            obj = GameObject(lane, -45, 55, 55, kind)
        else:
            obj = GameObject(lane, -45, 52, 34, kind)
        self.objects.append(obj)

    def spawn_coin(self) -> None:
        lane = random.randrange(LANES)
        coin = GameObject(lane, -30, 28, 28, "coin")
        coin.value = random.choice([1, 2, 5])
        self.coins.append(coin)

    def spawn_powerup(self) -> None:
        lane = random.randrange(LANES)
        power = GameObject(lane, -40, 34, 34, random.choice(["Nitro", "Shield", "Repair"]))
        self.powerups.append(power)

    def handle_collisions(self) -> None:
        now = pygame.time.get_ticks()

        for coin in self.coins[:]:
            if self.player.colliderect(coin.rect):
                self.coin_score += coin.value * 50
                self.coins.remove(coin)

        for power in self.powerups[:]:
            if self.player.colliderect(power.rect):
                self.powerups.remove(power)
                if self.active_power is not None:
                    continue
                if power.kind == "Nitro":
                    self.active_power = "Nitro"
                    self.active_until = now + 4000
                elif power.kind == "Shield":
                    self.active_power = "Shield"
                    self.shield = True
                    self.active_until = 0
                elif power.kind == "Repair":
                    self.active_power = "Repair"
                    self.crashes_saved += 1
                    if self.objects:
                        self.objects.pop(0)
                    self.active_power = None

        for obj in self.objects[:]:
            if not self.player.colliderect(obj.rect):
                continue

            if obj.kind == "boost_strip" and self.active_power is None:
                self.active_power = "Nitro"
                self.active_until = now + 3000
                self.objects.remove(obj)
                continue

            if obj.kind in ("oil", "pothole", "speed_bump"):
                self.speed = max(2.5, self.speed - 1.8)
                self.objects.remove(obj)
                continue

            if obj.kind in ("traffic", "barrier", "moving_barrier"):
                if self.shield:
                    self.shield = False
                    self.active_power = None
                    self.crashes_saved += 1
                    self.objects.remove(obj)
                else:
                    self.game_over = True

    def draw_road(self) -> None:
        self.screen.fill((25, 120, 60))
        road = pygame.Rect(ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT)
        pygame.draw.rect(self.screen, DARK_GRAY, road)
        pygame.draw.rect(self.screen, WHITE, (ROAD_LEFT - 4, 0, 4, HEIGHT))
        pygame.draw.rect(self.screen, WHITE, (ROAD_LEFT + ROAD_WIDTH, 0, 4, HEIGHT))

        self.road_marks_y = (self.road_marks_y + int(self.speed)) % 50
        for i in range(1, LANES):
            x = ROAD_LEFT + i * LANE_WIDTH
            for y in range(-50 + self.road_marks_y, HEIGHT, 50):
                pygame.draw.rect(self.screen, WHITE, (x - 2, y, 4, 26))

    def draw_object(self, obj: GameObject) -> None:
        if obj.kind == "traffic":
            pygame.draw.rect(self.screen, RED, obj.rect, border_radius=8)
            pygame.draw.rect(self.screen, BLACK, obj.rect, 2, border_radius=8)
        elif obj.kind == "barrier":
            pygame.draw.rect(self.screen, (230, 120, 40), obj.rect, border_radius=4)
        elif obj.kind == "moving_barrier":
            pygame.draw.rect(self.screen, (170, 70, 230), obj.rect, border_radius=4)
        elif obj.kind == "oil":
            pygame.draw.ellipse(self.screen, BLACK, obj.rect)
        elif obj.kind == "pothole":
            pygame.draw.ellipse(self.screen, (70, 45, 35), obj.rect)
        elif obj.kind == "speed_bump":
            pygame.draw.rect(self.screen, YELLOW, obj.rect, border_radius=10)
        elif obj.kind == "boost_strip":
            pygame.draw.rect(self.screen, (50, 220, 255), obj.rect, border_radius=8)
            draw_text(self.screen, "N", self.small, BLACK, obj.rect.centerx, obj.rect.centery - 10, True)

    def draw(self) -> None:
        self.draw_road()

        for obj in self.objects:
            self.draw_object(obj)

        for coin in self.coins:
            color = YELLOW if coin.value == 1 else (255, 160, 30) if coin.value == 2 else (150, 255, 120)
            pygame.draw.circle(self.screen, color, coin.rect.center, coin.rect.width // 2)
            draw_text(self.screen, str(coin.value), self.small, BLACK, coin.rect.centerx, coin.rect.centery - 9, True)

        for power in self.powerups:
            color = BLUE if power.kind == "Nitro" else GREEN if power.kind == "Shield" else RED
            pygame.draw.rect(self.screen, color, power.rect, border_radius=8)
            draw_text(self.screen, power.kind[0], self.small, WHITE, power.rect.centerx, power.rect.centery - 9, True)

        car_color = CAR_COLORS.get(self.settings.get("car_color", "Blue"), BLUE)
        pygame.draw.rect(self.screen, car_color, self.player, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, self.player, 2, border_radius=10)
        if self.shield:
            pygame.draw.circle(self.screen, (110, 220, 255), self.player.center, 45, 3)

        remaining = max(0, FINISH_DISTANCE - int(self.distance))
        draw_text(self.screen, f"Name: {self.username}", self.small, WHITE, 10, 10)
        draw_text(self.screen, f"Score: {self.score}", self.small, WHITE, 10, 35)
        draw_text(self.screen, f"Coins: {self.coin_score // 50}", self.small, WHITE, 10, 60)
        draw_text(self.screen, f"Distance: {int(self.distance)}m", self.small, WHITE, 10, 85)
        draw_text(self.screen, f"Remain: {remaining}m", self.small, WHITE, 10, 110)

        if self.active_power == "Nitro":
            left = max(0, (self.active_until - pygame.time.get_ticks()) // 1000)
            draw_text(self.screen, f"Power: Nitro {left}s", self.small, YELLOW, 320, 10)
        elif self.active_power == "Shield":
            draw_text(self.screen, "Power: Shield", self.small, GREEN, 320, 10)
        else:
            draw_text(self.screen, "Power: None", self.small, WHITE, 320, 10)

        progress_w = 300
        pygame.draw.rect(self.screen, WHITE, (100, HEIGHT - 25, progress_w, 10), 1)
        fill_w = int(progress_w * min(self.distance, FINISH_DISTANCE) / FINISH_DISTANCE)
        pygame.draw.rect(self.screen, GREEN, (100, HEIGHT - 25, fill_w, 10))
