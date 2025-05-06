import pygame

class Player:
    def __init__(self, x, y):
        self.invulnerable_timer = 0
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        
        self.image = pygame.transform.scale(
            pygame.image.load('D:/Python/Game/images/arcade_space.png'),
            (self.width, self.height)
        )

        # Heart icon
        self.heart = pygame.transform.scale(
            pygame.image.load('D:/Python/Game/images/love.png'),
            (24, 24)
        )
        # Shield icon
        self.shield_icon = pygame.transform.scale(
            pygame.image.load('D:/Python/Game/images/shield.png'),
            (24, 24)
        )
        # Shield effect
        self.shield_effect = pygame.transform.scale(
            pygame.image.load('D:/Python/Game/images/blueshield.png'),
            (120, 120)  # Slightly larger than player sprite
        )
        self.hp = 100
        self.max_hp = 100
        self.shield = 0  # Initial shield set to 0
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
        if self.x < -self.width: self.x = 1200  # Wrap around left to right

    def draw(self, screen):
        # Draw shield effect if shield is active
        if self.shield > 0:
            # Center the shield effect around the player
            shield_x = self.x - (self.shield_effect.get_width() - self.width) // 2
            shield_y = self.y - (self.shield_effect.get_height() - self.height) // 2
            screen.blit(self.shield_effect, (shield_x, shield_y))
        # Draw player sprite (with invulnerability flicker)
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
            self.speed = self.base_speed * 2
            self.speed_boost_timer -= 1
        else:
            self.speed = self.base_speed

    def draw_status_bars(self, screen):
        bar_width = 160
        bar_height = 18
        padding = 10

        # Position bars aligned to the right
        bar_x = 1200 - bar_width - padding
        heart_x = bar_x - 38
        bar_y = 10

        # HP bar (green)
        hp_fill = (self.hp / self.max_hp) * bar_width
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Red border
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, hp_fill, bar_height))    # Green fill
        screen.blit(self.heart, (heart_x, bar_y - 2))  # Heart icon

        # Shield bar (white)
        shield_bar_y = bar_y + bar_height + 8
        shield_fill = (self.shield / self.max_shield) * bar_width
        pygame.draw.rect(screen, (180, 180, 180), (bar_x, shield_bar_y, bar_width, bar_height))  # Gray background
        pygame.draw.rect(screen, (0, 191, 255), (bar_x, shield_bar_y, shield_fill, bar_height))  # White fill
        screen.blit(self.shield_icon, (heart_x, shield_bar_y - 2))  # Shield icon