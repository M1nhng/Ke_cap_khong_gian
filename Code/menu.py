import pygame
import button

def show_menu():
    pygame.init()

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pause Menu")

    font = pygame.font.SysFont("arialblack", 85)
    TEXT_COL = (255, 255, 255)

    # Load button images
    resume_img = pygame.image.load("D:/Python/Game/images/button_resume.png").convert_alpha()
    options_img = pygame.image.load("D:/Python/Game/images/button_options.png").convert_alpha()
    quit_img = pygame.image.load("D:/Python/Game/images/button_quit.png").convert_alpha()
    audio_img = pygame.image.load("D:/Python/Game/images/button_audio.png").convert_alpha()
    video_img = pygame.image.load("D:/Python/Game/images/button_video.png").convert_alpha()
    back_img = pygame.image.load("D:/Python/Game/images/button_back.png").convert_alpha()

    # Create buttons
    resume_button = button.Button(535, 210, resume_img, 1)
    options_button = button.Button(528, 350, options_img, 1)
    quit_button = button.Button(562, 485, quit_img, 1)
    audio_button = button.Button(438, 110, audio_img, 1)
    video_button = button.Button(438, 230, video_img, 1)
    back_button = button.Button(538, 610, back_img, 1)

    menu_state = "main"

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
            if quit_button.draw(screen):
                return "quit"

        elif menu_state == "options":
            if audio_button.draw(screen):
                print("Audio setting clicked")
            if video_button.draw(screen):
                print("Video setting clicked")
            if back_button.draw(screen):
                menu_state = "main"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        pygame.display.update()

    pygame.quit()
