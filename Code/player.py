import pygame

class Player:
    def __init__(self, x, y):
        self.invulnerable_timer = 0
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        
        self.image = pygame.transform.scale(
            pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\arcade_space.png"),
            (self.width, self.height)
        )

        #Vẽ heart
        self.heart = pygame.transform.scale(
            pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\love.png"),
            (24, 24)
        )
        #vẽ giáp
        self.shield_icon=pygame.transform.scale(
            pygame.image.load(r"D:\OneDrive\Máy tính\cde\.vscode\game1\image_game\shield.png"),
            (24,24)
        )
        self.hp = 100
        self.max_hp = 100
        self.shield = 20
        self.max_shield = 20
        self.base_speed = 1.5
        self.speed = self.base_speed
        self.triple_shot_timer = 0
        self.speed_boost_timer = 0

    def move(self, direction, boundary_y):
        if direction['left']: self.x -= self.speed
        if direction['right']: self.x += self.speed
        if direction['up']: self.y -= self.speed
        if direction['down']: self.y += self.speed
        if self.x < -self.width: self.x = 1200  # đi xuyên trái -> xuất hiện phải
        #self.x = max(0, min(self.x, 1200 - self.width))
        #self.y = max(boundary_y, min(self.y, 850 - self.height))

    def draw(self, screen):
        if self.invulnerable_timer % 4 < 2:
            screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update_buffs(self):
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
        if self.triple_shot_timer > 0:
            self.triple_shot_timer -= 1
        if self.speed_boost_timer > 0:
            self.speed = self.base_speed * 2  # chỉnh hệ số ở đây để tăng tốc
            self.speed_boost_timer -= 1
        else:
            self.speed = self.base_speed

    def draw_status_bars(self, screen):
        bar_width = 160
        bar_height = 18
        padding = 10

        # Tính vị trí để căn phải
        bar_x = 1200 - bar_width - padding
        heart_x = bar_x - 38
        bar_y = 10

        
        # Thanh máu (xanh lá)
        hp_fill = (self.hp / self.max_hp) * bar_width
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))       # viền đỏ
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, hp_fill, bar_height))         # máu xanh
        screen.blit(self.heart, (heart_x, bar_y-2))#ICON TRÁI TIM
        # Thanh giáp (màu trắng)
        shield_bar_y = bar_y + bar_height + 8
        shield_fill = (self.shield / self.max_shield) * bar_width
        pygame.draw.rect(screen, (180, 180, 180), (bar_x, shield_bar_y, bar_width, bar_height))   # nền xám
        pygame.draw.rect(screen, (0, 191, 255), (bar_x, shield_bar_y, shield_fill, bar_height)) # fill trắng
        screen.blit(self.shield_icon,(heart_x,shield_bar_y-2))#ICON giáp
