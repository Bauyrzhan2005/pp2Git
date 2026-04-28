import pygame
import os

class MusicPlayer:
    def __init__(self):
        current_dir = os.path.dirname(__file__)

        self.music_dir = os.path.join(current_dir, "music")

        if os.path.exists(self.music_dir):
            self.playlist = [f for f in os.listdir(self.music_dir) if f.endswith((".mp3", ".wav" ))]
        else:
            self.playlist = []
            print(f"Error: Music folder not found at {self.music_dir}")
    
        self.current_index = 0

    def play(self):
        if self.playlist:
            track_path = os.path.join(self.music_dir, self.playlist[self.current_index])
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.music_dir)
            self.play()

    def previous(self):
        self.current_index = (self.current_index - 1) % len(self.music_dir)


    def get_current_track(self):
        if self.playlist:
            return self.playlist[self.current_index]
        return "No tracks found"
    
    def is_playing(self):
        return pygame.mixer.music.get_busy()