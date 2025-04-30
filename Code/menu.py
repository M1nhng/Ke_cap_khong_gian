import pygame
import button
from audio_settings import VOLUME_SETTINGS


def show_menu():
    pygame.init()

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pause Menu")

    resume_img = pygame.image.load("D:/Python/Game/images/button_resume.png").convert_alpha()
    options_img = pygame.image.load("D:/Python/Game/images/button_options.png").convert_alpha()
    quit_img = pygame.image.load("D:/Python/Game/images/button_quit.png").convert_alpha()

    resume_button = button.Button(535, 210, resume_img, 1)
    options_button = button.Button(528, 350, options_img, 1)
    quit_button = button.Button(562, 485, quit_img, 1)

    running = True
    while running:
        screen.fill((0, 0, 0))

        if resume_button.draw(screen):
            return "resume"
        if options_button.draw(screen):
            show_options_menu()
        if quit_button.draw(screen):
            return "quit"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        pygame.display.update()

    pygame.quit()

def show_options_menu():
    pygame.init()

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    audio_img = pygame.image.load("D:/Python/Game/images/button_audio.png").convert_alpha()
    video_img = pygame.image.load("D:/Python/Game/images/button_video.png").convert_alpha()
    back_img = pygame.image.load("D:/Python/Game/images/button_back.png").convert_alpha()
    keys_img = pygame.image.load("D:/Python/Game/images/button_keys.png").convert_alpha()

    audio_button = button.Button(438, 110, audio_img, 1)
    video_button = button.Button(438, 250, video_img, 1)
    back_button = button.Button(538, 610, back_img, 1)
    keys_button = button.Button(458, 400, keys_img, 1)

    running = True
    while running:
        screen.fill((0, 0, 0))

        if audio_button.draw(screen):
            show_audio_settings()
        if video_button.draw(screen):
            print("Video settings clicked")
        if keys_button.draw(screen):
            print("Keys setting clicked")
        if back_button.draw(screen):
            return "back"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        pygame.display.update()

    pygame.quit()

def show_audio_settings():
    pygame.init()

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    label_font = pygame.font.SysFont("arial", 40)
    TEXT_COL = (255, 255, 255)

    back_img = pygame.image.load("D:/Python/Game/images/button_back.png").convert_alpha()
    back_button = button.Button(538, 610, back_img, 1)

    bar_width = 300
    bar_height = 10
    knob_radius = 12
    bar_x = (SCREEN_WIDTH - bar_width) // 2

    max_val = 1.0
    min_val = 0.0
    volume_bar_y = 150
    sfx_bar_y = 250
    music_bar_y = 350


    volume = VOLUME_SETTINGS["master"]
    sfx = VOLUME_SETTINGS["sfx"]
    music = VOLUME_SETTINGS["music"]

    dragging_volume = dragging_sfx = dragging_music = False

    def draw_text(text, font, color, x, y):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Master Volume
        draw_text("Master Volume", label_font, TEXT_COL, bar_x, volume_bar_y - 50)
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, volume_bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, volume_bar_y, volume * bar_width, bar_height))
        volume_knob_x = bar_x + volume * bar_width
        pygame.draw.circle(screen, (255, 255, 0), (int(volume_knob_x), volume_bar_y + bar_height // 2), knob_radius)

        # SFX
        draw_text("SFX", label_font, TEXT_COL, bar_x, sfx_bar_y - 50)
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, sfx_bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, sfx_bar_y, sfx * bar_width, bar_height))
        sfx_knob_x = bar_x + sfx * bar_width
        pygame.draw.circle(screen, (255, 255, 0), (int(sfx_knob_x), sfx_bar_y + bar_height // 2), knob_radius)

        # Music
        draw_text("Music", label_font, TEXT_COL, bar_x, music_bar_y - 50)
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, music_bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, music_bar_y, music * bar_width, bar_height))
        music_knob_x = bar_x + music * bar_width
        pygame.draw.circle(screen, (255, 255, 0), (int(music_knob_x), music_bar_y + bar_height // 2), knob_radius)

        if back_button.draw(screen):
            return "back"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if pygame.Rect(volume_knob_x - knob_radius, volume_bar_y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mx, my):
                    dragging_volume = True
                elif pygame.Rect(sfx_knob_x - knob_radius, sfx_bar_y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mx, my):
                    dragging_sfx = True
                elif pygame.Rect(music_knob_x - knob_radius, music_bar_y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mx, my):
                    dragging_music = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging_volume = dragging_sfx = dragging_music = False

            elif event.type == pygame.MOUSEMOTION:
                mx, _ = event.pos
                changed = False
                if dragging_volume:
                    volume = max(min_val, min(max_val, (mx - bar_x) / bar_width))
                    changed = True
                if dragging_sfx:
                    sfx = max(min_val, min(max_val, (mx - bar_x) / bar_width))
                    changed = True
                if dragging_music:
                    music = max(min_val, min(max_val, (mx - bar_x) / bar_width))
                    changed = True
                if changed:
                    VOLUME_SETTINGS["master"] = volume
                    VOLUME_SETTINGS["sfx"] = sfx
                    VOLUME_SETTINGS["music"] = music

        pygame.display.update()

    pygame.quit()
