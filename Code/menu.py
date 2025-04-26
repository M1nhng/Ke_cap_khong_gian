import pygame
import button

def show_menu():
    pygame.init()

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pause Menu")

    font = pygame.font.SysFont("arialblack", 85)
    label_font = pygame.font.SysFont("arial", 40)
    TEXT_COL = (255, 255, 255)

    # Load button images
    resume_img = pygame.image.load("D:/Python/Game/images/button_resume.png").convert_alpha()
    options_img = pygame.image.load("D:/Python/Game/images/button_options.png").convert_alpha()
    quit_img = pygame.image.load("D:/Python/Game/images/button_quit.png").convert_alpha()
    audio_img = pygame.image.load("D:/Python/Game/images/button_audio.png").convert_alpha()
    video_img = pygame.image.load("D:/Python/Game/images/button_video.png").convert_alpha()
    back_img = pygame.image.load("D:/Python/Game/images/button_back.png").convert_alpha()
    keys_img = pygame.image.load("D:/Python/Game/images/button_keys.png").convert_alpha()
    # Create buttons
    resume_button = button.Button(535, 210, resume_img, 1)
    options_button = button.Button(528, 350, options_img, 1)
    quit_button = button.Button(562, 485, quit_img, 1)
    audio_button = button.Button(438, 110, audio_img, 1)
    video_button = button.Button(438, 250, video_img, 1)
    back_button = button.Button(538, 610, back_img, 1)
    keys_button = button.Button(458, 400, keys_img, 1)
    menu_state = "main"
    audio_submenu = False

    # Volume/SFX/Music setup
    bar_width = 300
    bar_height = 10
    knob_radius = 12
    bar_x = (SCREEN_WIDTH - bar_width) // 2  # Center aligned

    volume = 5.0
    max_volume = 10.0
    min_volume = 0.0
    volume_bar_y = 150

    sfx = 5.0
    max_sfx = 10.0
    min_sfx = 0.0
    sfx_bar_y = 250

    music = 5.0
    max_music = 10.0
    min_music = 0.0
    music_bar_y = 350

    dragging_volume = False
    dragging_sfx = False
    dragging_music = False

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))


    running = True
    while running:
        screen.fill((0, 0, 0))

        if menu_state == "main":
            if resume_button.draw(screen):
                return "resume"
            if options_button.draw(screen):
                menu_state = "options"
                audio_submenu = False
            if quit_button.draw(screen):
                return "quit"

        elif menu_state == "options":
            if not audio_submenu:
                if audio_button.draw(screen):
                    audio_submenu = True
                if video_button.draw(screen):
                    print("Video setting clicked")
                if keys_button.draw(screen):
                    print("Keys setting clicked")    
                if back_button.draw(screen):
                    menu_state = "main"
            else:
                # Volume
                draw_text("Master Volume", label_font, TEXT_COL, bar_x, volume_bar_y - 50)
                pygame.draw.rect(screen, (255, 255, 255), (bar_x, volume_bar_y, bar_width, bar_height))
                pygame.draw.rect(screen, (0, 255, 0), (bar_x, volume_bar_y, (volume / max_volume) * bar_width, bar_height))
                volume_knob_x = bar_x + (volume / max_volume) * bar_width
                pygame.draw.circle(screen, (255, 255, 0), (int(volume_knob_x), volume_bar_y + bar_height // 2), knob_radius)

                # SFX
                draw_text("SFX", label_font, TEXT_COL, bar_x, sfx_bar_y - 50)
                pygame.draw.rect(screen, (255, 255, 255), (bar_x, sfx_bar_y, bar_width, bar_height))
                pygame.draw.rect(screen, (0, 255, 0), (bar_x, sfx_bar_y, (sfx / max_sfx) * bar_width, bar_height))
                sfx_knob_x = bar_x + (sfx / max_sfx) * bar_width
                pygame.draw.circle(screen, (255, 255, 0), (int(sfx_knob_x), sfx_bar_y + bar_height // 2), knob_radius)

                # Music
                draw_text("Music", label_font, TEXT_COL, bar_x, music_bar_y - 50)
                pygame.draw.rect(screen, (255, 255, 255), (bar_x, music_bar_y, bar_width, bar_height))
                pygame.draw.rect(screen, (0, 255, 0), (bar_x, music_bar_y, (music / max_music) * bar_width, bar_height))
                music_knob_x = bar_x + (music / max_music) * bar_width
                pygame.draw.circle(screen, (255, 255, 0), (int(music_knob_x), music_bar_y + bar_height // 2), knob_radius)

                # Back
                if back_button.draw(screen):
                    audio_submenu = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if audio_submenu:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Volume
                    if pygame.Rect(volume_knob_x - knob_radius, volume_bar_y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mouse_x, mouse_y) \
                       or (bar_x <= mouse_x <= bar_x + bar_width and volume_bar_y - 20 <= mouse_y <= volume_bar_y + bar_height + 20):
                        dragging_volume = True
                        volume = max(min_volume, min(max_volume, (mouse_x - bar_x) / bar_width * max_volume))

                    # SFX
                    if pygame.Rect(sfx_knob_x - knob_radius, sfx_bar_y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mouse_x, mouse_y) \
                       or (bar_x <= mouse_x <= bar_x + bar_width and sfx_bar_y - 20 <= mouse_y <= sfx_bar_y + bar_height + 20):
                        dragging_sfx = True
                        sfx = max(min_sfx, min(max_sfx, (mouse_x - bar_x) / bar_width * max_sfx))

                    # Music
                    if pygame.Rect(music_knob_x - knob_radius, music_bar_y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mouse_x, mouse_y) \
                       or (bar_x <= mouse_x <= bar_x + bar_width and music_bar_y - 20 <= mouse_y <= music_bar_y + bar_height + 20):
                        dragging_music = True
                        music = max(min_music, min(max_music, (mouse_x - bar_x) / bar_width * max_music))

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging_volume = dragging_sfx = dragging_music = False

                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, _ = event.pos
                    if dragging_volume:
                        volume = max(min_volume, min(max_volume, (mouse_x - bar_x) / bar_width * max_volume))
                    if dragging_sfx:
                        sfx = max(min_sfx, min(max_sfx, (mouse_x - bar_x) / bar_width * max_sfx))
                    if dragging_music:
                        music = max(min_music, min(max_music, (mouse_x - bar_x) / bar_width * max_music))

        pygame.display.update()

    pygame.quit()


# ✅ Hàm thêm mới để gọi từ open.py
def show_options_menu():
    pygame.init()

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  

    TEXT_COL = (255, 255, 255)
    font = pygame.font.SysFont("arialblack", 70)

    # Load button images
    audio_img = pygame.image.load("D:/Python/Game/images/button_audio.png").convert_alpha()
    video_img = pygame.image.load("D:/Python/Game/images/button_video.png").convert_alpha()
    back_img = pygame.image.load("D:/Python/Game/images/button_back.png").convert_alpha()
    keys_img = pygame.image.load("D:/Python/Game/images/button_keys.png").convert_alpha()
    # Create buttons
    audio_button = button.Button(438, 110, audio_img, 1)
    video_button = button.Button(438, 250, video_img, 1)
    back_button = button.Button(538, 610, back_img, 1)
    keys_button = button.Button(458, 400, keys_img, 1)
    running = True
    while running:
        screen.fill((0, 0, 0))

        if audio_button.draw(screen):
            result = show_audio_settings()
            if result == "quit":
                return "quit"

        if video_button.draw(screen):
            print("Video settings clicked")

        if back_button.draw(screen):
            return "back"
        if keys_button.draw(screen):
            print("Keys setting clicked")


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

    # Volume/SFX/Music setup
    bar_width = 300
    bar_height = 10
    knob_radius = 12
    bar_x = (SCREEN_WIDTH - bar_width) // 2

    volume, sfx, music = 5.0, 5.0, 5.0
    max_val = 10.0
    min_val = 0.0
    volume_bar_y = 150
    sfx_bar_y = 250
    music_bar_y = 350

    dragging_volume = dragging_sfx = dragging_music = False

    def draw_text(text, font, color, x, y):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Volume
        draw_text("Master Volume", label_font, TEXT_COL, bar_x, volume_bar_y - 50)
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, volume_bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, volume_bar_y, (volume / max_val) * bar_width, bar_height))
        volume_knob_x = bar_x + (volume / max_val) * bar_width
        pygame.draw.circle(screen, (255, 255, 0), (int(volume_knob_x), volume_bar_y + bar_height // 2), knob_radius)

        # SFX
        draw_text("SFX", label_font, TEXT_COL, bar_x, sfx_bar_y - 50)
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, sfx_bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, sfx_bar_y, (sfx / max_val) * bar_width, bar_height))
        sfx_knob_x = bar_x + (sfx / max_val) * bar_width
        pygame.draw.circle(screen, (255, 255, 0), (int(sfx_knob_x), sfx_bar_y + bar_height // 2), knob_radius)

        # Music
        draw_text("Music", label_font, TEXT_COL, bar_x, music_bar_y - 50)
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, music_bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, music_bar_y, (music / max_val) * bar_width, bar_height))
        music_knob_x = bar_x + (music / max_val) * bar_width
        pygame.draw.circle(screen, (255, 255, 0), (int(music_knob_x), music_bar_y + bar_height // 2), knob_radius)

        if back_button.draw(screen):
            return "back"


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                # Volume
                if pygame.Rect(volume_knob_x - knob_radius, volume_bar_y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mx, my):
                    dragging_volume = True
                elif pygame.Rect(sfx_knob_x - knob_radius, sfx_bar_y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mx, my):
                    dragging_sfx = True
                elif pygame.Rect(music_knob_x - knob_radius, music_bar_y - knob_radius, knob_radius * 2, knob_radius * 2).collidepoint(mx, my):
                    dragging_music = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging_volume = dragging_sfx = dragging_music = False

            elif event.type == pygame.MOUSEMOTION:
                mx, _ = pygame.mouse.get_pos()
                if dragging_volume:
                    volume = max(min_val, min(max_val, (mx - bar_x) / bar_width * max_val))
                if dragging_sfx:
                    sfx = max(min_val, min(max_val, (mx - bar_x) / bar_width * max_val))
                if dragging_music:
                    music = max(min_val, min(max_val, (mx - bar_x) / bar_width * max_val))

        pygame.display.update()

    pygame.quit()


