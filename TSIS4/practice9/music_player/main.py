import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

pygame.display.set_mode((600, 400))
pygame.display.set_caption("Pygame Music Player")

player = MusicPlayer()

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

running = True
while True:
    pygame.display.get_surface().fill((255, 255, 255))

    track_name = player.get_current_track()
    status = "Playing" if player.is_playing() else "Stopped"

    txt_title = font.render(f"Now playing: {track_name}", True, (0, 120, 255))
    txt_status = font.render(f"Status: {status}", True, (0, 0, 0))
    txt_help = small_font.render(f"P: Play | S: Stop | N: Next | B: Back | Q: Quit", True, (100,100,100))

    pygame.display.get_surface().blit(txt_title, (50,100))
    pygame.display.get_surface().blit(txt_status, (50,150))
    pygame.display.get_surface().blit(txt_help, (50,300))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.previous()
            elif event.key == pygame.K_q:
                running = False
                pygame.quit()

    pygame.display.flip()