import pygame
import random
import json
import os
from db import save_result, get_personal_best, get_leaderboard


WIDTH = 800
HEIGHT = 600
CELL = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (70, 70, 70)
DARK_GRAY = (35, 35, 35)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_RED = (120, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 140, 255)
PURPLE = (180, 0, 255)
ORANGE = (255, 140, 0)

SETTINGS_FILE = "settings.json"


class SnakeGame:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSIS4 Snake Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 26)
        self.small_font = pygame.font.SysFont("arial", 20)
        self.big_font = pygame.font.SysFont("arial", 48)

        self.settings = self.load_settings()

        self.username = ""
        self.state = "menu"

        self.running = True

        self.reset_game()

    def load_settings(self):
        if not os.path.exists(SETTINGS_FILE):
            default = {
                "snake_color": [0, 255, 0],
                "grid": True,
                "sound": True
            }
            with open(SETTINGS_FILE, "w") as file:
                json.dump(default, file, indent=4)
            return default

        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)

    def reset_game(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (CELL, 0)
        self.next_direction = (CELL, 0)

        self.score = 0
        self.level = 1
        self.food_eaten = 0

        self.base_speed = 8
        self.current_speed = self.base_speed

        self.food = None
        self.food_value = 1
        self.food_spawn_time = 0
        self.food_lifetime = 7000

        self.poison = None

        self.powerup = None
        self.powerup_type = None
        self.powerup_spawn_time = 0
        self.powerup_lifetime = 8000

        self.speed_effect_end = 0
        self.slow_effect_end = 0

        self.shield = False
        self.obstacles = []

        self.game_saved = False
        self.personal_best = 0

        self.spawn_food()
        self.spawn_poison()

    def draw_text(self, text, font, color, x, y, center=False):
        surface = font.render(text, True, color)
        rect = surface.get_rect()

        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)

        self.screen.blit(surface, rect)

    def draw_button(self, text, x, y, w, h):
        mouse = pygame.mouse.get_pos()
        rect = pygame.Rect(x, y, w, h)

        color = GRAY
        if rect.collidepoint(mouse):
            color = (100, 100, 100)

        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        self.draw_text(text, self.font, WHITE, x + w // 2, y + h // 2, center=True)

        return rect

    def random_empty_cell(self):
        while True:
            x = random.randrange(CELL, WIDTH - CELL, CELL)
            y = random.randrange(CELL + 40, HEIGHT - CELL, CELL)

            pos = (x, y)

            if (
                pos not in self.snake
                and pos not in self.obstacles
                and pos != self.food
                and pos != self.poison
                and pos != self.powerup
            ):
                return pos

    def spawn_food(self):
        self.food = self.random_empty_cell()
        self.food_value = random.choice([1, 2, 3])
        self.food_spawn_time = pygame.time.get_ticks()

    def spawn_poison(self):
        self.poison = self.random_empty_cell()

    def spawn_powerup(self):
        if self.powerup is None:
            if random.randint(1, 100) <= 25:
                self.powerup = self.random_empty_cell()
                self.powerup_type = random.choice(["speed", "slow", "shield"])
                self.powerup_spawn_time = pygame.time.get_ticks()

    def generate_obstacles(self):
        self.obstacles = []

        if self.level < 3:
            return

        count = 5 + self.level * 2

        for _ in range(count):
            pos = self.random_empty_cell()

            head = self.snake[0]
            distance = abs(pos[0] - head[0]) + abs(pos[1] - head[1])

            if distance > CELL * 3:
                self.obstacles.append(pos)

    def update_level(self):
        new_level = self.food_eaten // 5 + 1

        if new_level > self.level:
            self.level = new_level
            self.base_speed += 1
            self.generate_obstacles()

    def handle_collision_with_shield(self):
        if self.shield:
            self.shield = False
            return False
        return True

    def update_powerup_effects(self):
        now = pygame.time.get_ticks()

        self.current_speed = self.base_speed

        if now < self.speed_effect_end:
            self.current_speed = self.base_speed + 5

        if now < self.slow_effect_end:
            self.current_speed = max(4, self.base_speed - 4)

        if self.powerup is not None:
            if now - self.powerup_spawn_time > self.powerup_lifetime:
                self.powerup = None
                self.powerup_type = None

    def move_snake(self):
        self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction

        new_head = (head_x + dx, head_y + dy)

        hit_wall = (
            new_head[0] < CELL
            or new_head[0] >= WIDTH - CELL
            or new_head[1] < CELL + 40
            or new_head[1] >= HEIGHT - CELL
        )

        hit_self = new_head in self.snake
        hit_obstacle = new_head in self.obstacles

        if hit_wall or hit_self or hit_obstacle:
            if self.handle_collision_with_shield():
                self.state = "game_over"
                return

        self.snake.insert(0, new_head)

        ate_food = new_head == self.food
        ate_poison = new_head == self.poison
        ate_powerup = new_head == self.powerup

        if ate_food:
            self.score += self.food_value
            self.food_eaten += 1
            self.spawn_food()
            self.update_level()
        else:
            self.snake.pop()

        if ate_poison:
            for _ in range(2):
                if len(self.snake) > 0:
                    self.snake.pop()

            if len(self.snake) <= 1:
                self.state = "game_over"
                return

            self.spawn_poison()

        if ate_powerup:
            now = pygame.time.get_ticks()

            if self.powerup_type == "speed":
                self.speed_effect_end = now + 5000

            elif self.powerup_type == "slow":
                self.slow_effect_end = now + 5000

            elif self.powerup_type == "shield":
                self.shield = True

            self.powerup = None
            self.powerup_type = None

    def update_food_timer(self):
        now = pygame.time.get_ticks()

        if now - self.food_spawn_time > self.food_lifetime:
            self.spawn_food()

    def draw_grid(self):
        if not self.settings["grid"]:
            return

        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, DARK_GRAY, (x, 40), (x, HEIGHT))

        for y in range(40, HEIGHT, CELL):
            pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WIDTH, y))

    def draw_game(self):
        self.screen.fill(BLACK)

        self.draw_grid()

        pygame.draw.rect(self.screen, WHITE, (CELL, CELL + 40, WIDTH - CELL * 2, HEIGHT - CELL * 3), 2)

        for block in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, (*block, CELL, CELL))

        for part in self.snake:
            pygame.draw.rect(
                self.screen,
                self.settings["snake_color"],
                (*part, CELL, CELL)
            )

        food_color = YELLOW
        if self.food_value == 2:
            food_color = ORANGE
        elif self.food_value == 3:
            food_color = PURPLE

        pygame.draw.rect(self.screen, food_color, (*self.food, CELL, CELL))

        if self.poison:
            pygame.draw.rect(self.screen, DARK_RED, (*self.poison, CELL, CELL))

        if self.powerup:
            color = BLUE
            if self.powerup_type == "speed":
                color = RED
            elif self.powerup_type == "slow":
                color = BLUE
            elif self.powerup_type == "shield":
                color = GREEN

            pygame.draw.rect(self.screen, color, (*self.powerup, CELL, CELL))

        shield_text = "ON" if self.shield else "OFF"

        self.draw_text(f"User: {self.username}", self.small_font, WHITE, 10, 8)
        self.draw_text(f"Score: {self.score}", self.small_font, WHITE, 170, 8)
        self.draw_text(f"Level: {self.level}", self.small_font, WHITE, 290, 8)
        self.draw_text(f"Best: {self.personal_best}", self.small_font, WHITE, 400, 8)
        self.draw_text(f"Shield: {shield_text}", self.small_font, WHITE, 520, 8)

    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != (0, CELL):
                self.next_direction = (0, -CELL)
            elif event.key == pygame.K_DOWN and self.direction != (0, -CELL):
                self.next_direction = (0, CELL)
            elif event.key == pygame.K_LEFT and self.direction != (CELL, 0):
                self.next_direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-CELL, 0):
                self.next_direction = (CELL, 0)

    def main_menu(self):
        self.screen.fill(BLACK)

        self.draw_text("SNAKE GAME", self.big_font, GREEN, WIDTH // 2, 80, center=True)
        self.draw_text("Enter username:", self.font, WHITE, WIDTH // 2, 150, center=True)

        pygame.draw.rect(self.screen, WHITE, (250, 185, 300, 45), 2)
        self.draw_text(self.username, self.font, WHITE, 265, 193)

        play_btn = self.draw_button("Play", 300, 260, 200, 45)
        leader_btn = self.draw_button("Leaderboard", 300, 320, 200, 45)
        settings_btn = self.draw_button("Settings", 300, 380, 200, 45)
        quit_btn = self.draw_button("Quit", 300, 440, 200, 45)

        return play_btn, leader_btn, settings_btn, quit_btn

    def handle_menu_event(self, event, buttons):
        play_btn, leader_btn, settings_btn, quit_btn = buttons

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            elif event.key == pygame.K_RETURN:
                if self.username.strip():
                    self.start_game()
            else:
                if len(self.username) < 15 and event.unicode.isprintable():
                    self.username += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_btn.collidepoint(event.pos):
                if self.username.strip():
                    self.start_game()

            elif leader_btn.collidepoint(event.pos):
                self.state = "leaderboard"

            elif settings_btn.collidepoint(event.pos):
                self.state = "settings"

            elif quit_btn.collidepoint(event.pos):
                self.running = False

    def start_game(self):
        self.username = self.username.strip()
        self.personal_best = get_personal_best(self.username)
        self.reset_game()
        self.personal_best = get_personal_best(self.username)
        self.state = "playing"

    def game_over_screen(self):
        if not self.game_saved:
            save_result(self.username, self.score, self.level)
            self.personal_best = max(self.personal_best, self.score)
            self.game_saved = True

        self.screen.fill(BLACK)

        self.draw_text("GAME OVER", self.big_font, RED, WIDTH // 2, 100, center=True)
        self.draw_text(f"Final Score: {self.score}", self.font, WHITE, WIDTH // 2, 180, center=True)
        self.draw_text(f"Level Reached: {self.level}", self.font, WHITE, WIDTH // 2, 220, center=True)
        self.draw_text(f"Personal Best: {self.personal_best}", self.font, WHITE, WIDTH // 2, 260, center=True)

        retry_btn = self.draw_button("Retry", 300, 330, 200, 45)
        menu_btn = self.draw_button("Main Menu", 300, 390, 200, 45)

        return retry_btn, menu_btn

    def handle_game_over_event(self, event, buttons):
        retry_btn, menu_btn = buttons

        if event.type == pygame.MOUSEBUTTONDOWN:
            if retry_btn.collidepoint(event.pos):
                self.start_game()

            elif menu_btn.collidepoint(event.pos):
                self.state = "menu"

    def leaderboard_screen(self):
        self.screen.fill(BLACK)

        self.draw_text("LEADERBOARD", self.big_font, YELLOW, WIDTH // 2, 60, center=True)

        rows = get_leaderboard()

        headers = "Rank   Username        Score   Level   Date"
        self.draw_text(headers, self.small_font, WHITE, 120, 130)

        y = 170

        for i, row in enumerate(rows, start=1):
            username, score, level, played_at = row
            date_text = played_at.strftime("%Y-%m-%d")

            line = f"{i:<6} {username:<14} {score:<7} {level:<7} {date_text}"
            self.draw_text(line, self.small_font, WHITE, 120, y)
            y += 35

        back_btn = self.draw_button("Back", 300, 520, 200, 45)

        return back_btn

    def handle_leaderboard_event(self, event, back_btn):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_btn.collidepoint(event.pos):
                self.state = "menu"

    def settings_screen(self):
        self.screen.fill(BLACK)

        self.draw_text("SETTINGS", self.big_font, BLUE, WIDTH // 2, 70, center=True)

        grid_text = "Grid: ON" if self.settings["grid"] else "Grid: OFF"
        sound_text = "Sound: ON" if self.settings["sound"] else "Sound: OFF"

        grid_btn = self.draw_button(grid_text, 280, 160, 240, 45)
        sound_btn = self.draw_button(sound_text, 280, 220, 240, 45)

        green_btn = self.draw_button("Green Snake", 280, 300, 240, 45)
        blue_btn = self.draw_button("Blue Snake", 280, 360, 240, 45)
        yellow_btn = self.draw_button("Yellow Snake", 280, 420, 240, 45)

        save_btn = self.draw_button("Save & Back", 280, 500, 240, 45)

        return grid_btn, sound_btn, green_btn, blue_btn, yellow_btn, save_btn

    def handle_settings_event(self, event, buttons):
        grid_btn, sound_btn, green_btn, blue_btn, yellow_btn, save_btn = buttons

        if event.type == pygame.MOUSEBUTTONDOWN:
            if grid_btn.collidepoint(event.pos):
                self.settings["grid"] = not self.settings["grid"]

            elif sound_btn.collidepoint(event.pos):
                self.settings["sound"] = not self.settings["sound"]

            elif green_btn.collidepoint(event.pos):
                self.settings["snake_color"] = [0, 255, 0]

            elif blue_btn.collidepoint(event.pos):
                self.settings["snake_color"] = [0, 140, 255]

            elif yellow_btn.collidepoint(event.pos):
                self.settings["snake_color"] = [255, 255, 0]

            elif save_btn.collidepoint(event.pos):
                self.save_settings()
                self.state = "menu"

    def run(self):
        while self.running:
            buttons = None

            if self.state == "menu":
                buttons = self.main_menu()

            elif self.state == "playing":
                self.update_powerup_effects()
                self.update_food_timer()
                self.spawn_powerup()
                self.move_snake()
                self.draw_game()

            elif self.state == "game_over":
                buttons = self.game_over_screen()

            elif self.state == "leaderboard":
                buttons = self.leaderboard_screen()

            elif self.state == "settings":
                buttons = self.settings_screen()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.state == "menu":
                    self.handle_menu_event(event, buttons)

                elif self.state == "playing":
                    self.handle_game_events(event)

                elif self.state == "game_over":
                    self.handle_game_over_event(event, buttons)

                elif self.state == "leaderboard":
                    self.handle_leaderboard_event(event, buttons)

                elif self.state == "settings":
                    self.handle_settings_event(event, buttons)

            if self.state == "playing":
                self.clock.tick(self.current_speed)
            else:
                self.clock.tick(30)

        pygame.quit()