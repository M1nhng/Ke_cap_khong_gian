import pygame
import random
import math

# Load and scale item images
item_images = {
    'heal': pygame.image.load("D:/Python/Game/images/healing.png"),
    'speed_up': pygame.image.load("D:/Python/Game/images/speed.png"),
    'triple_shot': pygame.image.load("D:/Python/Game/images/threebullets.png"),
    'shield_up': pygame.image.load("D:/Python/Game/images/defence.png")
}

for key in item_images:
    item_images[key] = pygame.transform.scale(item_images[key], (40, 40))

ITEM_TYPES = list(item_images.keys())

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, player_x, player_y):
        super().__init__()
        self.type = item_type
        self.image = item_images[item_type]
        self.rect = self.image.get_rect(center=(x, y))
        # Calculate direction toward player with random deviation
        dx = player_x - x
        dy = player_y - y
        distance = max(1, math.hypot(dx, dy))  # Avoid division by zero
        angle = math.atan2(dy, dx)
        # Add random deviation up to ±30 degrees (converted to radians)
        deviation = random.uniform(-math.pi / 6, math.pi / 6)
        angle += deviation
        # Set velocity components for speed of 1 pixel per frame
        self.dx = math.cos(angle) * 1.0
        self.dy = math.sin(angle) * 1.0

    def update(self):
        self.rect.y += 0.7

    def is_off_screen(self):
        screen = pygame.display.get_surface()
        return (self.rect.right < 0 or 
                self.rect.left > screen.get_width() or 
                self.rect.bottom < 0 or 
                self.rect.top > screen.get_height())

def check_collision_and_apply(player, items, enemies, boss_bullets):
    for item in items[:]:
        if player.get_rect().colliderect(item.rect):
            if item.type == 'heal':
                player.hp = min(player.max_hp, player.hp + 20)
            elif item.type == 'speed_up':
                player.speed_boost_timer = 300
            elif item.type == 'triple_shot':
                player.triple_shot_timer = 300
            elif item.type == 'shield_up':
                player.shield = min(player.max_shield, player.shield + 10)
            items.remove(item)
        elif item.is_off_screen():
            items.remove(item)