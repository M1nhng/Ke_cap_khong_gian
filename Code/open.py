import pygame
import button
from Game import run_game

def show_main_menu():
    pygame.init()
    
    # Cài đặt màn hình
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 850
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Robber - Main Menu")
    
    # Load background (dùng chung với game)
    background = pygame.image.load('D:/Python/Game/images/background.png')
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Load nút Play
    play_img = pygame.image.load("D:/Python/Game/images/button_play.png").convert_alpha()
    play_button = button.Button(500, 300,play_img,0.5)
    
    # Font tiêu đề
    title_font = pygame.font.SysFont("arialblack", 80)
    title_text = title_font.render("SPACE SHOOTER", True, (255, 255, 255))
    
    running = True
    while running:
        # Vẽ background
        screen.blit(background, (0, 0))
        
        # Vẽ tiêu đề
        screen.blit(title_text, (250, 100))
        
        # Vẽ nút Play và kiểm tra click
        if play_button.draw(screen):
            run_game()  # Bắt đầu game khi click Play
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        pygame.display.update()
    
    pygame.quit()
