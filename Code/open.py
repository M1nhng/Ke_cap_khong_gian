import pygame
import button
from Game import run_game

def show_main_menu():
    pygame.init()
    
    # Cài đặt màn hình
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 850
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Robber")

    
    # Load nút
    play_img = pygame.image.load("D:/Python/Game/images/button_play.png").convert_alpha()
    quit_img = pygame.image.load("D:/Python/Game/images/button_quit.png").convert_alpha()

    play_button = button.Button(500, 300,play_img,0.5)
    quit_button = button.Button(550, 600,quit_img,1)
    # Font tiêu đề
    title_font = pygame.font.SysFont("arialblack", 80)
    title_text = title_font.render("SPACE SHOOTER", True, (255, 255, 255))
    
    running = True
    while running:

        # Vẽ tiêu đề
        screen.blit(title_text, (250, 100))
        
        # Vẽ nút Play và kiểm tra click
        if play_button.draw(screen):
            run_game()  # Bắt đầu game khi click Play
        if quit_button.draw(screen):
                return "quit"    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        pygame.display.update()
    
    pygame.quit()
