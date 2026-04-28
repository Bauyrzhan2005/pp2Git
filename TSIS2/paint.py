import pygame
import datetime
from collections import deque

pygame.init()

WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 26)
text_font = pygame.font.SysFont(None, 36)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)

current_color = BLACK
brush_size = 5
tool = "pencil"

drawing = False
start_pos = None
last_pos = None
preview_canvas = None

text_mode = False
text_pos = None
typed_text = ""

colors = [
    (BLACK, "Black"),
    (RED, "Red"),
    (GREEN, "Green"),
    (BLUE, "Blue"),
    (WHITE, "White"),
]

tools = [
    ("pencil", "Pencil"),
    ("line", "Line"),
    ("rect", "Rect"),
    ("circle", "Circle"),
    ("eraser", "Eraser"),
    ("fill", "Fill"),
    ("text", "Text"),
]

def to_canvas_pos(pos):
    x, y = pos
    return x, y - TOOLBAR_HEIGHT

def inside_canvas(pos):
    x, y = pos
    return 0 <= x < WIDTH and TOOLBAR_HEIGHT <= y < HEIGHT

def draw_toolbar():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, TOOLBAR_HEIGHT))

    x = 10
    for tool_name, label in tools:
        rect = pygame.Rect(x, 10, 75, 30)
        color = (180, 220, 255) if tool == tool_name else (245, 245, 245)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

        txt = font.render(label, True, BLACK)
        screen.blit(txt, (x + 8, 17))
        x += 85

    x = 10
    y = 50
    for color, name in colors:
        rect = pygame.Rect(x, y, 30, 30)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        if current_color == color:
            pygame.draw.rect(screen, (255, 200, 0), rect, 4)
        x += 40

    info = f"Brush: {brush_size} | Keys: 1=2px, 2=5px, 3=10px | Ctrl+S=save"
    txt = font.render(info, True, BLACK)
    screen.blit(txt, (250, 55))

def handle_toolbar_click(pos):
    global tool, current_color

    x, y = pos

    tx = 10
    for tool_name, label in tools:
        rect = pygame.Rect(tx, 10, 75, 30)
        if rect.collidepoint(pos):
            tool = tool_name
            return True
        tx += 85

    cx = 10
    cy = 50
    for color, name in colors:
        rect = pygame.Rect(cx, cy, 30, 30)
        if rect.collidepoint(pos):
            current_color = color
            return True
        cx += 40

    return False

def flood_fill(surface, start_pos, new_color):
    width, height = surface.get_size()
    x, y = start_pos

    if not (0 <= x < width and 0 <= y < height):
        return

    target_color = surface.get_at((x, y))

    if target_color == new_color:
        return

    q = deque()
    q.append((x, y))

    while q:
        x, y = q.popleft()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), new_color)

        q.append((x + 1, y))
        q.append((x - 1, y))
        q.append((x, y + 1))
        q.append((x, y - 1))

def save_canvas():
    filename = "paint_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
    pygame.image.save(canvas, filename)
    print("Saved:", filename)

running = True

while running:
    screen.fill((230, 230, 230))
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    if drawing and tool in ["line", "rect", "circle"] and start_pos is not None:
        temp = canvas.copy()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        end_pos = (mouse_x, mouse_y - TOOLBAR_HEIGHT)

        if tool == "line":
            pygame.draw.line(temp, current_color, start_pos, end_pos, brush_size)

        elif tool == "rect":
            x1, y1 = start_pos
            x2, y2 = end_pos
            rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
            pygame.draw.rect(temp, current_color, rect, brush_size)

        elif tool == "circle":
            x1, y1 = start_pos
            x2, y2 = end_pos
            radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
            pygame.draw.circle(temp, current_color, start_pos, radius, brush_size)

        screen.blit(temp, (0, TOOLBAR_HEIGHT))

    if text_mode:
        show_text = text_font.render(typed_text + "|", True, current_color)
        screen.blit(show_text, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    draw_toolbar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            elif text_mode:
                if event.key == pygame.K_RETURN:
                    final_text = text_font.render(typed_text, True, current_color)
                    canvas.blit(final_text, text_pos)
                    text_mode = False
                    typed_text = ""

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    typed_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]

                else:
                    typed_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < TOOLBAR_HEIGHT:
                handle_toolbar_click(event.pos)

            elif inside_canvas(event.pos):
                pos = to_canvas_pos(event.pos)

                if tool == "fill":
                    flood_fill(canvas, pos, current_color)

                elif tool == "text":
                    text_mode = True
                    text_pos = pos
                    typed_text = ""

                else:
                    drawing = True
                    start_pos = pos
                    last_pos = pos

        if event.type == pygame.MOUSEMOTION:
            if drawing and inside_canvas(event.pos):
                pos = to_canvas_pos(event.pos)

                if tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, pos, brush_size)
                    last_pos = pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and inside_canvas(event.pos):
                end_pos = to_canvas_pos(event.pos)

                if tool == "line":
                    pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)

                elif tool == "rect":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(canvas, current_color, rect, brush_size)

                elif tool == "circle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)

            drawing = False
            start_pos = None
            last_pos = None

    pygame.display.flip()
    clock.tick(60)

pygame.quit()