import pygame
from audio_settings import set_sfx_volume

pygame.mixer.init()

# Load âm click một lần thôi
click_sound = pygame.mixer.Sound("D:/Python/Game/sounds/button-click-289742.mp3")
set_sfx_volume(click_sound)

class Button:
    def __init__(self, x, y, image, scale=1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                # Khi click button: Phát âm thanh click
                set_sfx_volume(click_sound)  # Cập nhật volume SFX hiện tại
                click_sound.play()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
