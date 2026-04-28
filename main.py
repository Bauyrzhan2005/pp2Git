from __future__ import annotations

import pygame

from persistence import load_settings, save_settings, load_leaderboard, add_score
from racer import RacerGame, WIDTH, HEIGHT
from ui import Button, draw_text, WHITE, BLACK, GRAY, DARK_GRAY, GREEN, RED, YELLOW, BLUE

pygame.init()
pygame.display.set_caption("TSIS 3 Racer Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 24)
SMALL = pygame.font.SysFont("arial", 18)
BIG = pygame.font.SysFont("arial", 44, bold=True)

settings = load_settings()
username = "Player"


def ask_username() -> str:
    name = ""
    while True:
        screen.fill((25, 25, 35))
        draw_text(screen, "Enter your name", BIG, WHITE, WIDTH // 2, 170, True)
        pygame.draw.rect(screen, WHITE, (110, 280, 280, 50), 2, border_radius=8)
        draw_text(screen, name or "Player", FONT, YELLOW, WIDTH // 2, 293, True)
        draw_text(screen, "Press ENTER to start", SMALL, WHITE, WIDTH // 2, 360, True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name.strip() or "Player"
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12 and event.unicode.isprintable():
                    name += event.unicode


def main_menu() -> str:
    buttons = [
        Button((150, 250, 200, 50), "Play", FONT),
        Button((150, 315, 200, 50), "Leaderboard", FONT),
        Button((150, 380, 200, 50), "Settings", FONT),
        Button((150, 445, 200, 50), "Quit", FONT, bg=RED),
    ]
    actions = ["play", "leaderboard", "settings", "quit"]
    while True:
        screen.fill((25, 25, 35))
        draw_text(screen, "RACER GAME", BIG, YELLOW, WIDTH // 2, 130, True)
        draw_text(screen, "TSIS 3 Advanced Driving", SMALL, WHITE, WIDTH // 2, 180, True)
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            for button, action in zip(buttons, actions):
                if button.clicked(event):
                    return action


def settings_screen() -> None:
    global settings
    colors = ["Blue", "Red", "Green", "Yellow"]
    difficulties = ["Easy", "Normal", "Hard"]
    back = Button((150, 590, 200, 45), "Back", FONT)
    while True:
        screen.fill((25, 25, 35))
        draw_text(screen, "SETTINGS", BIG, YELLOW, WIDTH // 2, 80, True)

        sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"
        sound_btn = Button((130, 160, 240, 45), sound_text, FONT, bg=GREEN if settings["sound"] else RED)
        sound_btn.draw(screen)

        draw_text(screen, "Car Color", FONT, WHITE, WIDTH // 2, 245, True)
        color_buttons = []
        for i, color in enumerate(colors):
            btn = Button((70 + i * 92, 285, 82, 42), color, SMALL, bg=BLUE if settings["car_color"] == color else GRAY)
            btn.draw(screen)
            color_buttons.append((btn, color))

        draw_text(screen, "Difficulty", FONT, WHITE, WIDTH // 2, 390, True)
        difficulty_buttons = []
        for i, diff in enumerate(difficulties):
            btn = Button((75 + i * 120, 430, 105, 42), diff, SMALL, bg=BLUE if settings["difficulty"] == diff else GRAY)
            btn.draw(screen)
            difficulty_buttons.append((btn, diff))

        back.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if sound_btn.clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)
            for btn, color in color_buttons:
                if btn.clicked(event):
                    settings["car_color"] = color
                    save_settings(settings)
            for btn, diff in difficulty_buttons:
                if btn.clicked(event):
                    settings["difficulty"] = diff
                    save_settings(settings)
            if back.clicked(event):
                return


def leaderboard_screen() -> None:
    back = Button((150, 620, 200, 45), "Back", FONT)
    while True:
        screen.fill((25, 25, 35))
        draw_text(screen, "LEADERBOARD", BIG, YELLOW, WIDTH // 2, 60, True)
        draw_text(screen, "Rank   Name        Score    Distance", SMALL, WHITE, 60, 120)
        y = 160
        leaderboard = load_leaderboard()
        if not leaderboard:
            draw_text(screen, "No scores yet", FONT, WHITE, WIDTH // 2, 260, True)
        for rank, entry in enumerate(leaderboard[:10], 1):
            row = f"{rank:<5} {entry['name']:<10} {entry['score']:<8} {entry['distance']}m"
            draw_text(screen, row, SMALL, WHITE, 60, y)
            y += 38
        back.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if back.clicked(event):
                return


def game_over_screen(game: RacerGame) -> str:
    add_score(game.username, game.score, int(game.distance), game.coin_score // 50)
    retry = Button((80, 500, 150, 50), "Retry", FONT, bg=GREEN)
    menu = Button((270, 500, 150, 50), "Main Menu", FONT)
    while True:
        screen.fill((25, 25, 35))
        title = "FINISH!" if game.finished else "GAME OVER"
        draw_text(screen, title, BIG, YELLOW if game.finished else RED, WIDTH // 2, 120, True)
        draw_text(screen, f"Name: {game.username}", FONT, WHITE, WIDTH // 2, 220, True)
        draw_text(screen, f"Score: {game.score}", FONT, WHITE, WIDTH // 2, 260, True)
        draw_text(screen, f"Distance: {int(game.distance)}m", FONT, WHITE, WIDTH // 2, 300, True)
        draw_text(screen, f"Coins: {game.coin_score // 50}", FONT, WHITE, WIDTH // 2, 340, True)
        retry.draw(screen)
        menu.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if retry.clicked(event):
                return "retry"
            if menu.clicked(event):
                return "menu"


def play_game() -> str:
    global username
    username = ask_username()
    while True:
        game = RacerGame(screen, clock, settings, username)
        result = game.run()
        if result == "quit":
            return "quit"
        if result == "menu":
            return "menu"
        after = game_over_screen(game)
        if after == "retry":
            continue
        return after


def main() -> None:
    while True:
        action = main_menu()
        if action == "quit":
            break
        if action == "play":
            result = play_game()
            if result == "quit":
                break
        elif action == "leaderboard":
            leaderboard_screen()
        elif action == "settings":
            settings_screen()

    pygame.quit()


if __name__ == "__main__":
    main()
