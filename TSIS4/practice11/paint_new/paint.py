import pygame
import math
pygame.init()

width, height = 900,600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paint Game")

clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

colors = [black, red, green, blue]

current_color = black
tool = "brush"

drawing = False
start_pos = (0,0)

screen.fill(white)

def draw_ui():
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (10 + i*40, 10, 30, 30))

    for i in range(8):
        pygame.draw.rect(screen, black, (10 + i*110, 60, 105, 30), 2)
    
    font = pygame.font.Font(None, 20)
    labels = ["Brush", "Rect", "Circle", "Square", "Right Triangle", "Equi Triangle", "Rhombus", "Eraser"]
    for i, label in enumerate(labels):
        screen.blit(font.render(label, True, black), (15 + i*110, 68))
    
canvas = pygame.Surface((width, height))
canvas.fill(white)

running = True

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            
            for i, color in enumerate(colors):
                if pygame.Rect(10 + i*40, 10, 30, 30).collidepoint(x,y):
                    current_color = color
            if pygame.Rect(10,60,105,30).collidepoint(x,y): tool = "brush"
            if pygame.Rect(120,60,105,30).collidepoint(x,y): tool = "rect"
            if pygame.Rect(230,60,105,30).collidepoint(x,y): tool = "circle"
            if pygame.Rect(340,60,105,30).collidepoint(x,y): tool = "square"
            if pygame.Rect(450,60,105,30).collidepoint(x,y): tool = "right triangle"
            if pygame.Rect(560,60,105,30).collidepoint(x,y): tool = "equilateral triangle"
            if pygame.Rect(670,60,105,30).collidepoint(x,y): tool = "rhombus"
            if pygame.Rect(780,60,105,30).collidepoint(x,y): tool = "eraser"
                
            drawing = True
            start_pos = event.pos 
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos
            
            if tool == "rect":
                rect = pygame.Rect(start_pos,(end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                pygame.draw.rect(canvas, current_color, rect, 2)
                
            if tool == "circle":
                radius = int(((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)**0.5)
                pygame.draw.circle(canvas,current_color, start_pos, radius, 2)

            if tool == "square":
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]

                side = max(abs(dx), abs(dy))

                rect = pygame.Rect(start_pos[0], start_pos[1], side, side)
                pygame.draw.rect(canvas, current_color, rect, 2)

            if tool == "right triangle":
                points = [start_pos, end_pos, (start_pos[0], end_pos[1])]
                pygame.draw.polygon(canvas, current_color, points, 2)

            if tool == "equilateral triangle":
                side = math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)
                h = (side * math.sqrt(3)) / 2
                points = [start_pos, (start_pos[0] - side/2, start_pos[1] + h), (start_pos[0] + side/2, start_pos[1] + h)]
                pygame.draw.polygon(canvas, current_color, points, 2)

            if tool == "rhombus":
                x1, y1 = start_pos
                x2, y2 = end_pos

                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2

                points = [
                 (mid_x, y1),  
                 (x2, mid_y),  
                 (mid_x, y2),  
                 (x1, mid_y)   
    ]
                pygame.draw.polygon(canvas, current_color, points, 2)
                
                
        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == "brush":
                pygame.draw.circle(canvas, current_color, event.pos, 5)
            if tool == "eraser":
                pygame.draw.circle(canvas, white, event.pos, 10)
                
    screen.fill(white)
    screen.blit(canvas, (0,0))
    draw_ui()
    
    pygame.display.update()
    
pygame.quit()