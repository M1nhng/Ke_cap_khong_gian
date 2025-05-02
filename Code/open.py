import pygame
import button
from menu import show_options_menu
from Game import run_game
from audio_settings import set_music_volume  # Để đồng bộ volume nhạc

def show_main_menu():
    pygame.init()

    # PHÁT NHẠC NỀN
    pygame.mixer.init()
    pygame.mixer.music.load("D:/Python/Game/sounds/nen.ogg")
    set_music_volume()  # Lấy volume từ thanh Music
    pygame.mixer.music.play(-1)  # Lặp vô hạn

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 850
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Shooter")

    play_img = pygame.image.load("D:/Python/Game/images/button_play.png").convert_alpha()
    quit_img = pygame.image.load("D:/Python/Game/images/button_quit.png").convert_alpha()
    settings_img = pygame.image.load("D:/Python/Game/images/settings.png").convert_alpha()

    play_button = button.Button(500, 300, play_img, 0.5)
    quit_button = button.Button(550, 600, quit_img, 1)

    title_font = pygame.font.SysFont("arialblack", 60)
    high_score_font = pygame.font.SysFont("arial", 30)
    title_text = title_font.render("SPACE SHOOTER", True, (255, 255, 255))

    try:
        with open("highscore.txt", "r") as f:
            high_score = int(f.read())
    except:
        high_score = 0

    high_score_text = high_score_font.render(f"High Score: {high_score}", True, (255, 255, 0))

    running = True
    while running:
        try:
            screen.fill((0, 0, 0))
            screen.blit(title_text, (350, 150))
            screen.blit(high_score_text, (530, 250))

            if play_button.draw(screen):
                set_music_volume()  # Đảm bảo khi vào game volume nhạc vẫn đồng bộ
                run_game()
                if pygame.get_init():
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.set_caption("Space Shooter")

            if quit_button.draw(screen):
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()
        except pygame.error:
            running = False

    pygame.quit()
